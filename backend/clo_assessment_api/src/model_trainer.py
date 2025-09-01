"""
Model Trainer for CLO Assessment
Huấn luyện tự động model EraX-VL-7B-V1.5 cho đánh giá CLO
"""

import os
import json
import torch
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import logging
from datetime import datetime
import yaml
from dataclasses import dataclass, asdict
import pickle

# ML/DL imports
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
import joblib

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TrainingConfig:
    """Configuration for training"""
    model_name: str = "erax-vl-7b-v1.5"
    batch_size: int = 16
    learning_rate: float = 2e-5
    num_epochs: int = 10
    max_length: int = 512
    warmup_steps: int = 100
    weight_decay: float = 0.01
    save_steps: int = 500
    eval_steps: int = 100
    output_dir: str = "/home/ubuntu/clo_plo_assessment_platform/models/checkpoints"
    data_dir: str = "/home/ubuntu/clo_plo_assessment_platform/training_data/model_training/datasets"
    log_dir: str = "/home/ubuntu/clo_plo_assessment_platform/logs"
    use_gpu: bool = True
    seed: int = 42

@dataclass
class TrainingMetrics:
    """Training metrics tracking"""
    epoch: int
    train_loss: float
    val_loss: float
    train_accuracy: float
    val_accuracy: float
    train_f1: float
    val_f1: float
    learning_rate: float
    timestamp: str

class CLOAssessmentTrainer:
    """
    Trainer cho model đánh giá CLO
    """
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() and config.use_gpu else "cpu")
        
        # Create directories
        Path(config.output_dir).mkdir(parents=True, exist_ok=True)
        Path(config.log_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.vectorizer = None
        self.models = {}
        self.metrics_history = []
        
        # Set random seeds
        torch.manual_seed(config.seed)
        np.random.seed(config.seed)
        
        logger.info(f"Trainer initialized with device: {self.device}")
    
    def load_training_data(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Load training data từ datasets
        """
        data_path = Path(self.config.data_dir)
        
        # Load datasets
        with open(data_path / 'train_dataset.json', 'r', encoding='utf-8') as f:
            train_data = json.load(f)
        
        with open(data_path / 'validation_dataset.json', 'r', encoding='utf-8') as f:
            val_data = json.load(f)
        
        with open(data_path / 'test_dataset.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        # Load keyword mappings
        with open(data_path / 'keyword_mappings.json', 'r', encoding='utf-8') as f:
            keyword_mappings = json.load(f)
        
        logger.info(f"Loaded {len(train_data)} train, {len(val_data)} val, {len(test_data)} test samples")
        
        return {
            'train': train_data,
            'validation': val_data,
            'test': test_data
        }, keyword_mappings
    
    def preprocess_data(self, datasets: Dict[str, List]) -> Tuple[Dict, Dict]:
        """
        Tiền xử lý dữ liệu cho training
        """
        processed_data = {}
        
        for split_name, data in datasets.items():
            texts = [sample['text'] for sample in data]
            scores = [sample['target_score'] for sample in data]
            bloom_levels = [sample['bloom_level'] for sample in data]
            clo_codes = [sample['clo_code'] for sample in data]
            labels = [sample['label'] for sample in data]
            
            processed_data[split_name] = {
                'texts': texts,
                'scores': np.array(scores),
                'bloom_levels': np.array(bloom_levels),
                'clo_codes': clo_codes,
                'labels': labels
            }
        
        # Create TF-IDF vectorizer
        if self.vectorizer is None:
            self.vectorizer = TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 3),
                stop_words=None,  # Keep Vietnamese words
                lowercase=True,
                min_df=2,
                max_df=0.95
            )
            
            # Fit on training data
            self.vectorizer.fit(processed_data['train']['texts'])
        
        # Transform texts to features
        features = {}
        for split_name, data in processed_data.items():
            text_features = self.vectorizer.transform(data['texts']).toarray()
            
            # Add additional features
            bloom_features = np.array(data['bloom_levels']).reshape(-1, 1)
            
            # Combine features
            combined_features = np.hstack([text_features, bloom_features])
            
            features[split_name] = {
                'X': combined_features,
                'y_scores': data['scores'],
                'y_bloom': data['bloom_levels'],
                'clo_codes': data['clo_codes'],
                'labels': data['labels']
            }
        
        logger.info(f"Feature extraction completed. Feature dimension: {combined_features.shape[1]}")
        
        return processed_data, features
    
    def train_score_prediction_model(self, features: Dict) -> Dict[str, Any]:
        """
        Huấn luyện model dự đoán điểm số CLO
        """
        logger.info("Training score prediction models...")
        
        X_train = features['train']['X']
        y_train = features['train']['y_scores']
        X_val = features['validation']['X']
        y_val = features['validation']['y_scores']
        
        # Train multiple models
        models = {
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=self.config.seed,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=self.config.seed
            ),
            'ridge_regression': Ridge(
                alpha=1.0,
                random_state=self.config.seed
            )
        }
        
        model_results = {}
        
        for model_name, model in models.items():
            logger.info(f"Training {model_name}...")
            
            # Train model
            model.fit(X_train, y_train)
            
            # Evaluate
            train_pred = model.predict(X_train)
            val_pred = model.predict(X_val)
            
            # Calculate metrics
            train_mse = np.mean((train_pred - y_train) ** 2)
            val_mse = np.mean((val_pred - y_val) ** 2)
            train_mae = np.mean(np.abs(train_pred - y_train))
            val_mae = np.mean(np.abs(val_pred - y_val))
            
            # R² score
            train_r2 = model.score(X_train, y_train)
            val_r2 = model.score(X_val, y_val)
            
            model_results[model_name] = {
                'model': model,
                'train_mse': train_mse,
                'val_mse': val_mse,
                'train_mae': train_mae,
                'val_mae': val_mae,
                'train_r2': train_r2,
                'val_r2': val_r2
            }
            
            logger.info(f"{model_name} - Val MSE: {val_mse:.4f}, Val MAE: {val_mae:.4f}, Val R²: {val_r2:.4f}")
        
        # Select best model based on validation R²
        best_model_name = max(model_results.keys(), key=lambda k: model_results[k]['val_r2'])
        best_model = model_results[best_model_name]['model']
        
        logger.info(f"Best model: {best_model_name} with Val R²: {model_results[best_model_name]['val_r2']:.4f}")
        
        # Save best model
        model_path = Path(self.config.output_dir) / f"score_prediction_model_{best_model_name}.joblib"
        joblib.dump(best_model, model_path)
        
        # Save vectorizer
        vectorizer_path = Path(self.config.output_dir) / "tfidf_vectorizer.joblib"
        joblib.dump(self.vectorizer, vectorizer_path)
        
        self.models['score_predictor'] = best_model
        
        return model_results
    
    def train_bloom_classification_model(self, features: Dict) -> Dict[str, Any]:
        """
        Huấn luyện model phân loại Bloom level
        """
        logger.info("Training Bloom level classification model...")
        
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import classification_report
        
        X_train = features['train']['X']
        y_train = features['train']['y_bloom']
        X_val = features['validation']['X']
        y_val = features['validation']['y_bloom']
        
        # Train classifier
        bloom_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=self.config.seed,
            n_jobs=-1
        )
        
        bloom_classifier.fit(X_train, y_train)
        
        # Evaluate
        train_pred = bloom_classifier.predict(X_train)
        val_pred = bloom_classifier.predict(X_val)
        
        train_accuracy = accuracy_score(y_train, train_pred)
        val_accuracy = accuracy_score(y_val, val_pred)
        
        # Classification report
        val_report = classification_report(y_val, val_pred, output_dict=True)
        
        logger.info(f"Bloom Classification - Train Acc: {train_accuracy:.4f}, Val Acc: {val_accuracy:.4f}")
        
        # Save model
        bloom_model_path = Path(self.config.output_dir) / "bloom_classification_model.joblib"
        joblib.dump(bloom_classifier, bloom_model_path)
        
        self.models['bloom_classifier'] = bloom_classifier
        
        return {
            'model': bloom_classifier,
            'train_accuracy': train_accuracy,
            'val_accuracy': val_accuracy,
            'classification_report': val_report
        }
    
    def train_clo_specific_models(self, features: Dict, keyword_mappings: Dict) -> Dict[str, Any]:
        """
        Huấn luyện models riêng cho từng CLO
        """
        logger.info("Training CLO-specific models...")
        
        clo_models = {}
        
        # Group data by CLO
        clo_groups = {}
        for split in ['train', 'validation']:
            for i, clo_code in enumerate(features[split]['clo_codes']):
                if clo_code not in clo_groups:
                    clo_groups[clo_code] = {'X': [], 'y': [], 'split': []}
                
                clo_groups[clo_code]['X'].append(features[split]['X'][i])
                clo_groups[clo_code]['y'].append(features[split]['y_scores'][i])
                clo_groups[clo_code]['split'].append(split)
        
        # Train model for each CLO with sufficient data
        min_samples = 10
        trained_clos = 0
        
        for clo_code, data in clo_groups.items():
            if len(data['X']) >= min_samples:
                X = np.array(data['X'])
                y = np.array(data['y'])
                
                # Split into train/val
                train_indices = [i for i, split in enumerate(data['split']) if split == 'train']
                val_indices = [i for i, split in enumerate(data['split']) if split == 'validation']
                
                if len(train_indices) >= 5 and len(val_indices) >= 2:
                    X_train = X[train_indices]
                    y_train = y[train_indices]
                    X_val = X[val_indices]
                    y_val = y[val_indices]
                    
                    # Train simple model for this CLO
                    clo_model = Ridge(alpha=0.1, random_state=self.config.seed)
                    clo_model.fit(X_train, y_train)
                    
                    # Evaluate
                    val_pred = clo_model.predict(X_val)
                    val_mse = np.mean((val_pred - y_val) ** 2)
                    
                    clo_models[clo_code] = {
                        'model': clo_model,
                        'val_mse': val_mse,
                        'samples': len(data['X'])
                    }
                    
                    trained_clos += 1
        
        logger.info(f"Trained CLO-specific models for {trained_clos} CLOs")
        
        # Save CLO models
        clo_models_path = Path(self.config.output_dir) / "clo_specific_models.pkl"
        with open(clo_models_path, 'wb') as f:
            pickle.dump(clo_models, f)
        
        return clo_models
    
    def evaluate_models(self, features: Dict) -> Dict[str, Any]:
        """
        Đánh giá models trên test set
        """
        logger.info("Evaluating models on test set...")
        
        X_test = features['test']['X']
        y_test_scores = features['test']['y_scores']
        y_test_bloom = features['test']['y_bloom']
        
        evaluation_results = {}
        
        # Evaluate score prediction model
        if 'score_predictor' in self.models:
            score_pred = self.models['score_predictor'].predict(X_test)
            
            test_mse = np.mean((score_pred - y_test_scores) ** 2)
            test_mae = np.mean(np.abs(score_pred - y_test_scores))
            test_r2 = self.models['score_predictor'].score(X_test, y_test_scores)
            
            evaluation_results['score_prediction'] = {
                'test_mse': test_mse,
                'test_mae': test_mae,
                'test_r2': test_r2,
                'predictions': score_pred.tolist()
            }
        
        # Evaluate Bloom classification model
        if 'bloom_classifier' in self.models:
            bloom_pred = self.models['bloom_classifier'].predict(X_test)
            
            test_accuracy = accuracy_score(y_test_bloom, bloom_pred)
            precision, recall, f1, _ = precision_recall_fscore_support(y_test_bloom, bloom_pred, average='weighted')
            
            evaluation_results['bloom_classification'] = {
                'test_accuracy': test_accuracy,
                'test_precision': precision,
                'test_recall': recall,
                'test_f1': f1,
                'predictions': bloom_pred.tolist()
            }
        
        logger.info(f"Test Results - Score R²: {evaluation_results.get('score_prediction', {}).get('test_r2', 'N/A'):.4f}, "
                   f"Bloom Acc: {evaluation_results.get('bloom_classification', {}).get('test_accuracy', 'N/A'):.4f}")
        
        return evaluation_results
    
    def save_training_artifacts(self, model_results: Dict, evaluation_results: Dict, keyword_mappings: Dict):
        """
        Lưu các artifacts từ training
        """
        logger.info("Saving training artifacts...")
        
        # Save training config
        config_path = Path(self.config.output_dir) / "training_config.yaml"
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(asdict(self.config), f, default_flow_style=False)
        
        # Save model results
        results_path = Path(self.config.output_dir) / "training_results.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            # Convert numpy types to Python types for JSON serialization
            serializable_results = self._make_json_serializable({
                'model_results': model_results,
                'evaluation_results': evaluation_results,
                'training_config': asdict(self.config),
                'timestamp': datetime.now().isoformat()
            })
            json.dump(serializable_results, f, ensure_ascii=False, indent=2)
        
        # Save keyword mappings
        mappings_path = Path(self.config.output_dir) / "keyword_mappings.json"
        with open(mappings_path, 'w', encoding='utf-8') as f:
            json.dump(keyword_mappings, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Training artifacts saved to {self.config.output_dir}")
    
    def _make_json_serializable(self, obj):
        """
        Convert numpy types to Python types for JSON serialization
        """
        if isinstance(obj, dict):
            return {key: self._make_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        else:
            return obj
    
    def run_full_training_pipeline(self) -> Dict[str, Any]:
        """
        Chạy toàn bộ pipeline training
        """
        logger.info("🚀 Starting full training pipeline...")
        
        # Load data
        datasets, keyword_mappings = self.load_training_data()
        
        # Preprocess data
        processed_data, features = self.preprocess_data(datasets)
        
        # Train models
        score_model_results = self.train_score_prediction_model(features)
        bloom_model_results = self.train_bloom_classification_model(features)
        clo_models = self.train_clo_specific_models(features, keyword_mappings)
        
        # Evaluate models
        evaluation_results = self.evaluate_models(features)
        
        # Save artifacts
        all_model_results = {
            'score_prediction': score_model_results,
            'bloom_classification': bloom_model_results,
            'clo_specific': {
                'num_models': len(clo_models),
                'avg_mse': np.mean([model['val_mse'] for model in clo_models.values()]) if clo_models else 0
            }
        }
        
        self.save_training_artifacts(all_model_results, evaluation_results, keyword_mappings)
        
        logger.info("✅ Training pipeline completed successfully!")
        
        return {
            'model_results': all_model_results,
            'evaluation_results': evaluation_results,
            'num_clo_models': len(clo_models),
            'training_config': asdict(self.config)
        }

class ModelInference:
    """
    Class for model inference
    """
    
    def __init__(self, model_dir: str):
        self.model_dir = Path(model_dir)
        self.models = {}
        self.vectorizer = None
        self.keyword_mappings = {}
        
        self._load_models()
    
    def _load_models(self):
        """
        Load trained models
        """
        try:
            # Load vectorizer
            vectorizer_path = self.model_dir / "tfidf_vectorizer.joblib"
            if vectorizer_path.exists():
                self.vectorizer = joblib.load(vectorizer_path)
            
            # Load score prediction model
            score_models = list(self.model_dir.glob("score_prediction_model_*.joblib"))
            if score_models:
                self.models['score_predictor'] = joblib.load(score_models[0])
            
            # Load Bloom classification model
            bloom_model_path = self.model_dir / "bloom_classification_model.joblib"
            if bloom_model_path.exists():
                self.models['bloom_classifier'] = joblib.load(bloom_model_path)
            
            # Load CLO-specific models
            clo_models_path = self.model_dir / "clo_specific_models.pkl"
            if clo_models_path.exists():
                with open(clo_models_path, 'rb') as f:
                    self.models['clo_specific'] = pickle.load(f)
            
            # Load keyword mappings
            mappings_path = self.model_dir / "keyword_mappings.json"
            if mappings_path.exists():
                with open(mappings_path, 'r', encoding='utf-8') as f:
                    self.keyword_mappings = json.load(f)
            
            logger.info(f"Models loaded from {self.model_dir}")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
    
    def predict_clo_score(self, text: str, clo_code: str = None, bloom_level: int = None) -> Dict[str, Any]:
        """
        Predict CLO score for given text
        """
        if not self.vectorizer or 'score_predictor' not in self.models:
            raise ValueError("Models not loaded properly")
        
        # Preprocess text
        text_features = self.vectorizer.transform([text]).toarray()
        
        # Add bloom level feature
        if bloom_level is None and clo_code in self.keyword_mappings:
            bloom_level = self.keyword_mappings[clo_code].get('bloom_level', 2)
        elif bloom_level is None:
            bloom_level = 2  # Default
        
        bloom_features = np.array([[bloom_level]])
        combined_features = np.hstack([text_features, bloom_features])
        
        # Predict score
        predicted_score = self.models['score_predictor'].predict(combined_features)[0]
        
        # Predict Bloom level if classifier available
        predicted_bloom = None
        if 'bloom_classifier' in self.models:
            predicted_bloom = self.models['bloom_classifier'].predict(combined_features)[0]
        
        # Use CLO-specific model if available
        clo_specific_score = None
        if clo_code and 'clo_specific' in self.models and clo_code in self.models['clo_specific']:
            clo_model = self.models['clo_specific'][clo_code]['model']
            clo_specific_score = clo_model.predict(combined_features)[0]
        
        # Final score (prefer CLO-specific if available)
        final_score = clo_specific_score if clo_specific_score is not None else predicted_score
        
        return {
            'predicted_score': float(final_score),
            'general_model_score': float(predicted_score),
            'clo_specific_score': float(clo_specific_score) if clo_specific_score is not None else None,
            'predicted_bloom_level': int(predicted_bloom) if predicted_bloom is not None else None,
            'input_bloom_level': bloom_level,
            'confidence': min(1.0, max(0.0, (4.0 - abs(final_score - 2.5)) / 4.0))  # Simple confidence
        }

def main():
    """
    Main training function
    """
    # Training configuration
    config = TrainingConfig(
        model_name="clo_assessment_model",
        batch_size=32,
        num_epochs=15,
        learning_rate=1e-4,
        output_dir="/home/ubuntu/clo_plo_assessment_platform/models/checkpoints",
        data_dir="/home/ubuntu/clo_plo_assessment_platform/training_data/model_training/datasets"
    )
    
    # Initialize trainer
    trainer = CLOAssessmentTrainer(config)
    
    # Run training
    results = trainer.run_full_training_pipeline()
    
    print("🎉 Training completed successfully!")
    print(f"📊 Results summary:")
    print(f"   - Score prediction R²: {results['evaluation_results'].get('score_prediction', {}).get('test_r2', 'N/A'):.4f}")
    print(f"   - Bloom classification accuracy: {results['evaluation_results'].get('bloom_classification', {}).get('test_accuracy', 'N/A'):.4f}")
    print(f"   - CLO-specific models: {results['num_clo_models']}")
    
    # Test inference
    print("\n🧪 Testing inference...")
    inference = ModelInference(config.output_dir)
    
    test_text = "Sinh viên hiểu rõ các khái niệm cơ bản về cơ học kỹ thuật và áp dụng vào tính toán thiết kế."
    result = inference.predict_clo_score(test_text, bloom_level=3)
    
    print(f"Test prediction: {result}")
    
    return results

if __name__ == "__main__":
    main()


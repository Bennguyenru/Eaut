"""
Simple Model Trainer for CLO Assessment
Huấn luyện model đơn giản không cần GPU/torch
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import logging
from datetime import datetime
import pickle

# ML imports
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, mean_squared_error, r2_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, Ridge
import joblib

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleCLOTrainer:
    """
    Simple trainer cho CLO assessment models
    """
    
    def __init__(self, output_dir: str, data_dir: str):
        self.output_dir = Path(output_dir)
        self.data_dir = Path(data_dir)
        
        # Create directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.vectorizer = None
        self.models = {}
        
        logger.info(f"Simple trainer initialized")
    
    def load_data(self) -> Tuple[Dict, Dict]:
        """Load training data"""
        logger.info("Loading training data...")
        
        # Load datasets
        with open(self.data_dir / 'train_dataset.json', 'r', encoding='utf-8') as f:
            train_data = json.load(f)
        
        with open(self.data_dir / 'validation_dataset.json', 'r', encoding='utf-8') as f:
            val_data = json.load(f)
        
        with open(self.data_dir / 'test_dataset.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        # Load keyword mappings
        with open(self.data_dir / 'keyword_mappings.json', 'r', encoding='utf-8') as f:
            keyword_mappings = json.load(f)
        
        datasets = {
            'train': train_data,
            'validation': val_data,
            'test': test_data
        }
        
        logger.info(f"Loaded {len(train_data)} train, {len(val_data)} val, {len(test_data)} test samples")
        return datasets, keyword_mappings
    
    def prepare_features(self, datasets: Dict) -> Dict:
        """Prepare features for training"""
        logger.info("Preparing features...")
        
        # Extract texts and labels
        all_texts = []
        for split_data in datasets.values():
            all_texts.extend([sample['text'] for sample in split_data])
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=3000,
            ngram_range=(1, 2),
            lowercase=True,
            min_df=2,
            max_df=0.9
        )
        
        # Fit vectorizer on all texts
        self.vectorizer.fit(all_texts)
        
        # Prepare features for each split
        features = {}
        for split_name, split_data in datasets.items():
            texts = [sample['text'] for sample in split_data]
            scores = np.array([sample['target_score'] for sample in split_data])
            bloom_levels = np.array([sample['bloom_level'] for sample in split_data])
            clo_codes = [sample['clo_code'] for sample in split_data]
            labels = [sample['label'] for sample in split_data]
            
            # Transform texts to TF-IDF features
            text_features = self.vectorizer.transform(texts).toarray()
            
            # Add bloom level as feature
            bloom_features = bloom_levels.reshape(-1, 1)
            
            # Combine features
            X = np.hstack([text_features, bloom_features])
            
            features[split_name] = {
                'X': X,
                'y_scores': scores,
                'y_bloom': bloom_levels,
                'clo_codes': clo_codes,
                'labels': labels
            }
        
        logger.info(f"Feature preparation completed. Feature dimension: {X.shape[1]}")
        return features
    
    def train_score_model(self, features: Dict) -> Dict:
        """Train score prediction model"""
        logger.info("Training score prediction model...")
        
        X_train = features['train']['X']
        y_train = features['train']['y_scores']
        X_val = features['validation']['X']
        y_val = features['validation']['y_scores']
        
        # Train Random Forest model
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        train_pred = model.predict(X_train)
        val_pred = model.predict(X_val)
        
        train_mse = mean_squared_error(y_train, train_pred)
        val_mse = mean_squared_error(y_val, val_pred)
        train_r2 = r2_score(y_train, train_pred)
        val_r2 = r2_score(y_val, val_pred)
        
        logger.info(f"Score Model - Train R²: {train_r2:.4f}, Val R²: {val_r2:.4f}")
        
        # Save model
        model_path = self.output_dir / "score_prediction_model.joblib"
        joblib.dump(model, model_path)
        
        self.models['score_predictor'] = model
        
        return {
            'model': model,
            'train_mse': train_mse,
            'val_mse': val_mse,
            'train_r2': train_r2,
            'val_r2': val_r2
        }
    
    def train_bloom_model(self, features: Dict) -> Dict:
        """Train Bloom level classification model"""
        logger.info("Training Bloom classification model...")
        
        X_train = features['train']['X']
        y_train = features['train']['y_bloom']
        X_val = features['validation']['X']
        y_val = features['validation']['y_bloom']
        
        # Train Random Forest classifier
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        train_pred = model.predict(X_train)
        val_pred = model.predict(X_val)
        
        train_acc = accuracy_score(y_train, train_pred)
        val_acc = accuracy_score(y_val, val_pred)
        
        logger.info(f"Bloom Model - Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}")
        
        # Save model
        model_path = self.output_dir / "bloom_classification_model.joblib"
        joblib.dump(model, model_path)
        
        self.models['bloom_classifier'] = model
        
        return {
            'model': model,
            'train_accuracy': train_acc,
            'val_accuracy': val_acc
        }
    
    def train_keyword_models(self, features: Dict, keyword_mappings: Dict) -> Dict:
        """Train keyword-based assessment models"""
        logger.info("Training keyword-based models...")
        
        keyword_models = {}
        
        # Create keyword scoring functions
        for clo_code, mapping in keyword_mappings.items():
            primary_keywords = mapping.get('primary_keywords', [])
            scoring_method = mapping.get('scoring_method', 'termfreq')
            
            if primary_keywords:
                keyword_models[clo_code] = {
                    'keywords': primary_keywords,
                    'scoring_method': scoring_method,
                    'bloom_level': mapping.get('bloom_level', 2),
                    'full_score_threshold': mapping.get('full_score_threshold', 3),
                    'partial_score_floor': mapping.get('partial_score_floor', 0.3)
                }
        
        # Save keyword models
        keyword_path = self.output_dir / "keyword_models.json"
        with open(keyword_path, 'w', encoding='utf-8') as f:
            json.dump(keyword_models, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Created keyword models for {len(keyword_models)} CLOs")
        
        return keyword_models
    
    def evaluate_models(self, features: Dict) -> Dict:
        """Evaluate models on test set"""
        logger.info("Evaluating models on test set...")
        
        X_test = features['test']['X']
        y_test_scores = features['test']['y_scores']
        y_test_bloom = features['test']['y_bloom']
        
        results = {}
        
        # Evaluate score model
        if 'score_predictor' in self.models:
            score_pred = self.models['score_predictor'].predict(X_test)
            test_mse = mean_squared_error(y_test_scores, score_pred)
            test_r2 = r2_score(y_test_scores, score_pred)
            
            results['score_prediction'] = {
                'test_mse': test_mse,
                'test_r2': test_r2
            }
        
        # Evaluate bloom model
        if 'bloom_classifier' in self.models:
            bloom_pred = self.models['bloom_classifier'].predict(X_test)
            test_acc = accuracy_score(y_test_bloom, bloom_pred)
            
            results['bloom_classification'] = {
                'test_accuracy': test_acc
            }
        
        logger.info(f"Test Results - Score R²: {results.get('score_prediction', {}).get('test_r2', 'N/A'):.4f}, "
                   f"Bloom Acc: {results.get('bloom_classification', {}).get('test_accuracy', 'N/A'):.4f}")
        
        return results
    
    def save_artifacts(self, results: Dict):
        """Save training artifacts"""
        logger.info("Saving training artifacts...")
        
        # Save vectorizer
        vectorizer_path = self.output_dir / "tfidf_vectorizer.joblib"
        joblib.dump(self.vectorizer, vectorizer_path)
        
        # Prepare JSON-serializable results
        json_results = {}
        for key, value in results.items():
            if isinstance(value, dict):
                json_results[key] = {}
                for k, v in value.items():
                    if k != 'model':  # Skip model objects
                        json_results[key][k] = float(v) if isinstance(v, (np.float64, np.float32)) else v
            else:
                json_results[key] = value
        
        # Save results
        results_path = self.output_dir / "training_results.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(json_results, f, ensure_ascii=False, indent=2)
        
        # Save training info
        info = {
            'timestamp': datetime.now().isoformat(),
            'model_type': 'simple_sklearn',
            'vectorizer_features': self.vectorizer.get_feature_names_out().shape[0] if hasattr(self.vectorizer, 'get_feature_names_out') else 'unknown',
            'models_trained': list(self.models.keys())
        }
        
        info_path = self.output_dir / "training_info.json"
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Artifacts saved to {self.output_dir}")
    
    def run_training(self) -> Dict:
        """Run complete training pipeline"""
        logger.info("🚀 Starting simple training pipeline...")
        
        # Load data
        datasets, keyword_mappings = self.load_data()
        
        # Prepare features
        features = self.prepare_features(datasets)
        
        # Train models
        score_results = self.train_score_model(features)
        bloom_results = self.train_bloom_model(features)
        keyword_models = self.train_keyword_models(features, keyword_mappings)
        
        # Evaluate
        eval_results = self.evaluate_models(features)
        
        # Compile results
        all_results = {
            'score_model': score_results,
            'bloom_model': bloom_results,
            'keyword_models': len(keyword_models),
            'evaluation': eval_results,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save artifacts
        self.save_artifacts(all_results)
        
        logger.info("✅ Training completed successfully!")
        
        return all_results

class SimpleInference:
    """Simple inference class"""
    
    def __init__(self, model_dir: str):
        self.model_dir = Path(model_dir)
        self.models = {}
        self.vectorizer = None
        self.keyword_models = {}
        
        self._load_models()
    
    def _load_models(self):
        """Load trained models"""
        try:
            # Load vectorizer
            vectorizer_path = self.model_dir / "tfidf_vectorizer.joblib"
            if vectorizer_path.exists():
                self.vectorizer = joblib.load(vectorizer_path)
            
            # Load score model
            score_path = self.model_dir / "score_prediction_model.joblib"
            if score_path.exists():
                self.models['score_predictor'] = joblib.load(score_path)
            
            # Load bloom model
            bloom_path = self.model_dir / "bloom_classification_model.joblib"
            if bloom_path.exists():
                self.models['bloom_classifier'] = joblib.load(bloom_path)
            
            # Load keyword models
            keyword_path = self.model_dir / "keyword_models.json"
            if keyword_path.exists():
                with open(keyword_path, 'r', encoding='utf-8') as f:
                    self.keyword_models = json.load(f)
            
            logger.info(f"Models loaded from {self.model_dir}")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
    
    def predict_score(self, text: str, clo_code: str = None, bloom_level: int = None) -> Dict:
        """Predict CLO score"""
        if not self.vectorizer or 'score_predictor' not in self.models:
            return {'error': 'Models not loaded'}
        
        try:
            # Prepare features
            text_features = self.vectorizer.transform([text]).toarray()
            
            # Add bloom level
            if bloom_level is None:
                bloom_level = 2  # Default
            
            bloom_features = np.array([[bloom_level]])
            X = np.hstack([text_features, bloom_features])
            
            # Predict score
            predicted_score = self.models['score_predictor'].predict(X)[0]
            
            # Predict bloom if available
            predicted_bloom = None
            if 'bloom_classifier' in self.models:
                predicted_bloom = self.models['bloom_classifier'].predict(X)[0]
            
            # Keyword-based score
            keyword_score = None
            if clo_code and clo_code in self.keyword_models:
                keyword_score = self._calculate_keyword_score(text, clo_code)
            
            # Final score
            final_score = keyword_score if keyword_score is not None else predicted_score
            
            return {
                'predicted_score': float(final_score),
                'ml_model_score': float(predicted_score),
                'keyword_score': float(keyword_score) if keyword_score is not None else None,
                'predicted_bloom_level': int(predicted_bloom) if predicted_bloom is not None else None,
                'confidence': min(1.0, max(0.1, 1.0 - abs(final_score - 2.5) / 2.5))
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {'error': str(e)}
    
    def _calculate_keyword_score(self, text: str, clo_code: str) -> float:
        """Calculate score based on keywords"""
        if clo_code not in self.keyword_models:
            return None
        
        model_info = self.keyword_models[clo_code]
        keywords = model_info['keywords']
        method = model_info['scoring_method']
        threshold = model_info['full_score_threshold']
        floor = model_info['partial_score_floor']
        
        text_lower = text.lower()
        
        if method == 'distinct':
            # Count distinct keywords found
            found_count = sum(1 for keyword in keywords if keyword.lower() in text_lower)
            score = min(4.0, (found_count / threshold) * 4.0)
            
        elif method == 'termfreq':
            # Count total keyword occurrences
            total_count = sum(text_lower.count(keyword.lower()) for keyword in keywords)
            score = min(4.0, (total_count / threshold) * 4.0)
            
        elif method == 'presence':
            # Binary presence check
            has_keywords = any(keyword.lower() in text_lower for keyword in keywords)
            score = 3.5 if has_keywords else 1.0
            
        else:
            score = 2.0  # Default
        
        # Apply floor
        return max(score, floor * 4.0)

def main():
    """Main training function"""
    output_dir = "/home/ubuntu/clo_plo_assessment_platform/models/checkpoints"
    data_dir = "/home/ubuntu/clo_plo_assessment_platform/training_data/model_training/datasets"
    
    # Train models
    trainer = SimpleCLOTrainer(output_dir, data_dir)
    results = trainer.run_training()
    
    print("🎉 Training completed!")
    print(f"📊 Results:")
    print(f"   - Score R²: {results['evaluation'].get('score_prediction', {}).get('test_r2', 'N/A'):.4f}")
    print(f"   - Bloom Acc: {results['evaluation'].get('bloom_classification', {}).get('test_accuracy', 'N/A'):.4f}")
    print(f"   - Keyword models: {results['keyword_models']}")
    
    # Test inference
    print("\n🧪 Testing inference...")
    inference = SimpleInference(output_dir)
    
    test_text = "Sinh viên hiểu rõ các khái niệm cơ bản về cơ học kỹ thuật và áp dụng vào tính toán thiết kế chi tiết máy."
    result = inference.predict_score(test_text, bloom_level=3)
    
    print(f"Test prediction: {result}")
    
    return results

if __name__ == "__main__":
    main()


"""
Enhanced API with trained models integration
API nâng cao với tích hợp models đã huấn luyện
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import logging
from pathlib import Path
from datetime import datetime
import tempfile
import uuid
from typing import Dict, List, Any, Optional

# Import our trained models
import sys
# Add current directory to path for importing local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from simple_model_trainer import SimpleInference

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables
model_inference = None
clo_database = {}
plo_database = {}
assessment_history = []

def initialize_models():
    """Initialize trained models"""
    global model_inference, clo_database, plo_database
    
    try:
        # Load trained models
        model_dir = "/home/ubuntu/clo_plo_assessment_platform/models/checkpoints"
        model_inference = SimpleInference(model_dir)
        
        # Load CLO database
        clo_path = "/home/ubuntu/clo_plo_assessment_platform/training_data/processed_documents/extracted_clo/extracted_clos.json"
        if os.path.exists(clo_path):
            with open(clo_path, 'r', encoding='utf-8') as f:
                clo_list = json.load(f)
                clo_database = {clo['clo_code']: clo for clo in clo_list}
        
        # Load PLO database
        plo_path = "/home/ubuntu/clo_plo_assessment_platform/data/complete_plo_database.json"
        if os.path.exists(plo_path):
            with open(plo_path, 'r', encoding='utf-8') as f:
                plo_data = json.load(f)
                plo_database = {plo['code']: plo for plo in plo_data.get('plos', [])}
        
        logger.info(f"Models initialized successfully. CLOs: {len(clo_database)}, PLOs: {len(plo_database)}")
        
    except Exception as e:
        logger.error(f"Error initializing models: {e}")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': model_inference is not None,
        'clo_count': len(clo_database),
        'plo_count': len(plo_database)
    })

@app.route('/api/clos', methods=['GET'])
def get_clos():
    """Get all CLOs"""
    try:
        # Add search and filter functionality
        search = request.args.get('search', '')
        course_code = request.args.get('course_code', '')
        bloom_level = request.args.get('bloom_level', '')
        
        filtered_clos = []
        for clo in clo_database.values():
            # Apply filters
            if search and search.lower() not in clo.get('description', '').lower():
                continue
            if course_code and course_code not in clo.get('course_code', ''):
                continue
            if bloom_level and str(clo.get('bloom_level', '')) != bloom_level:
                continue
            
            filtered_clos.append(clo)
        
        return jsonify({
            'clos': filtered_clos,
            'total': len(filtered_clos),
            'filters_applied': {
                'search': search,
                'course_code': course_code,
                'bloom_level': bloom_level
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting CLOs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/clos/<clo_code>', methods=['GET'])
def get_clo(clo_code):
    """Get specific CLO"""
    try:
        if clo_code not in clo_database:
            return jsonify({'error': 'CLO not found'}), 404
        
        clo = clo_database[clo_code]
        
        # Add related information
        related_plo = None
        if clo.get('plo_code') and clo['plo_code'] in plo_database:
            related_plo = plo_database[clo['plo_code']]
        
        return jsonify({
            'clo': clo,
            'related_plo': related_plo,
            'assessment_methods': clo.get('assessment_methods', []),
            'keywords': clo.get('keywords', [])
        })
        
    except Exception as e:
        logger.error(f"Error getting CLO {clo_code}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/plos', methods=['GET'])
def get_plos():
    """Get all PLOs"""
    try:
        return jsonify({
            'plos': list(plo_database.values()),
            'total': len(plo_database)
        })
        
    except Exception as e:
        logger.error(f"Error getting PLOs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/assess/document', methods=['POST'])
def assess_document():
    """Assess document against CLOs"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text content required'}), 400
        
        text = data['text']
        clo_codes = data.get('clo_codes', [])
        auto_detect_clos = data.get('auto_detect_clos', True)
        
        # If no CLO codes provided and auto-detect is enabled
        if not clo_codes and auto_detect_clos:
            # Use keyword matching to suggest relevant CLOs
            clo_codes = suggest_relevant_clos(text)
        
        # Assess against each CLO
        assessment_results = []
        
        for clo_code in clo_codes:
            if clo_code in clo_database:
                clo_info = clo_database[clo_code]
                
                # Use trained model for prediction
                prediction = model_inference.predict_score(
                    text=text,
                    clo_code=clo_code,
                    bloom_level=clo_info.get('bloom_level')
                )
                
                # Add CLO context to result
                result = {
                    'clo_code': clo_code,
                    'clo_description': clo_info.get('description', ''),
                    'bloom_level': clo_info.get('bloom_level', 2),
                    'course_code': clo_info.get('course_code', ''),
                    'predicted_score': prediction.get('predicted_score', 0),
                    'confidence': prediction.get('confidence', 0),
                    'ml_model_score': prediction.get('ml_model_score', 0),
                    'keyword_score': prediction.get('keyword_score'),
                    'predicted_bloom_level': prediction.get('predicted_bloom_level'),
                    'assessment_method': 'ai_model',
                    'keywords_found': find_keywords_in_text(text, clo_info.get('keywords', [])),
                    'feedback': generate_feedback(prediction, clo_info)
                }
                
                assessment_results.append(result)
        
        # Calculate overall statistics
        if assessment_results:
            scores = [r['predicted_score'] for r in assessment_results]
            overall_stats = {
                'average_score': sum(scores) / len(scores),
                'max_score': max(scores),
                'min_score': min(scores),
                'total_clos_assessed': len(assessment_results),
                'passing_clos': len([s for s in scores if s >= 2.0]),
                'excellent_clos': len([s for s in scores if s >= 3.5])
            }
        else:
            overall_stats = {
                'average_score': 0,
                'max_score': 0,
                'min_score': 0,
                'total_clos_assessed': 0,
                'passing_clos': 0,
                'excellent_clos': 0
            }
        
        # Save assessment to history
        assessment_record = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'text_length': len(text),
            'clo_codes': clo_codes,
            'results': assessment_results,
            'overall_stats': overall_stats
        }
        
        assessment_history.append(assessment_record)
        
        return jsonify({
            'assessment_id': assessment_record['id'],
            'results': assessment_results,
            'overall_stats': overall_stats,
            'suggested_clos': clo_codes if auto_detect_clos else [],
            'timestamp': assessment_record['timestamp']
        })
        
    except Exception as e:
        logger.error(f"Error assessing document: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/assess/batch', methods=['POST'])
def assess_batch():
    """Assess multiple documents in batch"""
    try:
        data = request.get_json()
        
        if not data or 'documents' not in data:
            return jsonify({'error': 'Documents array required'}), 400
        
        documents = data['documents']
        clo_codes = data.get('clo_codes', [])
        
        batch_results = []
        
        for i, doc in enumerate(documents):
            if isinstance(doc, str):
                text = doc
                doc_id = f"doc_{i+1}"
            elif isinstance(doc, dict):
                text = doc.get('text', '')
                doc_id = doc.get('id', f"doc_{i+1}")
            else:
                continue
            
            # Assess each document
            if text:
                # Use the same assessment logic as single document
                doc_results = []
                
                for clo_code in clo_codes:
                    if clo_code in clo_database:
                        clo_info = clo_database[clo_code]
                        
                        prediction = model_inference.predict_score(
                            text=text,
                            clo_code=clo_code,
                            bloom_level=clo_info.get('bloom_level')
                        )
                        
                        result = {
                            'clo_code': clo_code,
                            'predicted_score': prediction.get('predicted_score', 0),
                            'confidence': prediction.get('confidence', 0)
                        }
                        
                        doc_results.append(result)
                
                # Calculate document stats
                if doc_results:
                    scores = [r['predicted_score'] for r in doc_results]
                    doc_stats = {
                        'average_score': sum(scores) / len(scores),
                        'max_score': max(scores),
                        'min_score': min(scores)
                    }
                else:
                    doc_stats = {'average_score': 0, 'max_score': 0, 'min_score': 0}
                
                batch_results.append({
                    'document_id': doc_id,
                    'text_length': len(text),
                    'results': doc_results,
                    'stats': doc_stats
                })
        
        # Calculate batch statistics
        if batch_results:
            all_scores = []
            for doc in batch_results:
                all_scores.extend([r['predicted_score'] for r in doc['results']])
            
            batch_stats = {
                'total_documents': len(batch_results),
                'total_assessments': len(all_scores),
                'average_score': sum(all_scores) / len(all_scores) if all_scores else 0,
                'passing_rate': len([s for s in all_scores if s >= 2.0]) / len(all_scores) if all_scores else 0
            }
        else:
            batch_stats = {
                'total_documents': 0,
                'total_assessments': 0,
                'average_score': 0,
                'passing_rate': 0
            }
        
        return jsonify({
            'batch_id': str(uuid.uuid4()),
            'results': batch_results,
            'batch_stats': batch_stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in batch assessment: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/suggest/clos', methods=['POST'])
def suggest_clos():
    """Suggest relevant CLOs for given text"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text content required'}), 400
        
        text = data['text']
        max_suggestions = data.get('max_suggestions', 5)
        
        suggestions = suggest_relevant_clos(text, max_suggestions)
        
        # Add CLO details to suggestions
        detailed_suggestions = []
        for clo_code in suggestions:
            if clo_code in clo_database:
                clo_info = clo_database[clo_code]
                detailed_suggestions.append({
                    'clo_code': clo_code,
                    'description': clo_info.get('description', ''),
                    'course_code': clo_info.get('course_code', ''),
                    'bloom_level': clo_info.get('bloom_level', 2),
                    'relevance_score': calculate_relevance_score(text, clo_info)
                })
        
        # Sort by relevance score
        detailed_suggestions.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return jsonify({
            'suggestions': detailed_suggestions,
            'text_length': len(text),
            'total_suggestions': len(detailed_suggestions)
        })
        
    except Exception as e:
        logger.error(f"Error suggesting CLOs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/dashboard', methods=['GET'])
def get_dashboard_analytics():
    """Get dashboard analytics data"""
    try:
        # Calculate various analytics
        analytics = {
            'overview': {
                'total_clos': len(clo_database),
                'total_plos': len(plo_database),
                'total_assessments': len(assessment_history),
                'unique_courses': len(set(clo.get('course_code', '') for clo in clo_database.values() if clo.get('course_code')))
            },
            'bloom_distribution': calculate_bloom_distribution(),
            'course_distribution': calculate_course_distribution(),
            'recent_assessments': get_recent_assessments(10),
            'performance_trends': calculate_performance_trends(),
            'top_performing_clos': get_top_performing_clos(5),
            'improvement_needed_clos': get_improvement_needed_clos(5)
        }
        
        return jsonify(analytics)
        
    except Exception as e:
        logger.error(f"Error getting dashboard analytics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/results', methods=['POST'])
def export_results():
    """Export assessment results"""
    try:
        data = request.get_json()
        
        export_format = data.get('format', 'json')  # json, csv, excel
        assessment_ids = data.get('assessment_ids', [])
        
        # Get assessment data
        if assessment_ids:
            assessments = [a for a in assessment_history if a['id'] in assessment_ids]
        else:
            assessments = assessment_history[-10:]  # Last 10 assessments
        
        if export_format == 'json':
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(assessments, f, ensure_ascii=False, indent=2)
                temp_path = f.name
            
            return send_file(temp_path, as_attachment=True, download_name='assessment_results.json')
        
        elif export_format == 'csv':
            # Convert to CSV format
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(['Assessment ID', 'Timestamp', 'CLO Code', 'Course Code', 'Predicted Score', 'Confidence', 'Bloom Level'])
            
            # Write data
            for assessment in assessments:
                for result in assessment.get('results', []):
                    writer.writerow([
                        assessment['id'],
                        assessment['timestamp'],
                        result['clo_code'],
                        result['course_code'],
                        result['predicted_score'],
                        result['confidence'],
                        result['bloom_level']
                    ])
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                f.write(output.getvalue())
                temp_path = f.name
            
            return send_file(temp_path, as_attachment=True, download_name='assessment_results.csv')
        
        else:
            return jsonify({'error': 'Unsupported export format'}), 400
        
    except Exception as e:
        logger.error(f"Error exporting results: {e}")
        return jsonify({'error': str(e)}), 500

# Helper functions

def suggest_relevant_clos(text: str, max_suggestions: int = 5) -> List[str]:
    """Suggest relevant CLOs based on text content"""
    text_lower = text.lower()
    clo_scores = []
    
    for clo_code, clo_info in clo_database.items():
        score = calculate_relevance_score(text, clo_info)
        clo_scores.append((clo_code, score))
    
    # Sort by score and return top suggestions
    clo_scores.sort(key=lambda x: x[1], reverse=True)
    return [clo_code for clo_code, score in clo_scores[:max_suggestions]]

def calculate_relevance_score(text: str, clo_info: Dict) -> float:
    """Calculate relevance score between text and CLO"""
    text_lower = text.lower()
    score = 0.0
    
    # Check keywords
    keywords = clo_info.get('keywords', [])
    for keyword in keywords:
        if keyword.lower() in text_lower:
            score += 1.0
    
    # Check description similarity (simple word overlap)
    description = clo_info.get('description', '').lower()
    desc_words = set(description.split())
    text_words = set(text_lower.split())
    
    if desc_words and text_words:
        overlap = len(desc_words.intersection(text_words))
        score += overlap / len(desc_words) * 2.0
    
    return score

def find_keywords_in_text(text: str, keywords: List[str]) -> List[str]:
    """Find which keywords appear in text"""
    text_lower = text.lower()
    found_keywords = []
    
    for keyword in keywords:
        if keyword.lower() in text_lower:
            found_keywords.append(keyword)
    
    return found_keywords

def generate_feedback(prediction: Dict, clo_info: Dict) -> str:
    """Generate feedback based on prediction"""
    score = prediction.get('predicted_score', 0)
    confidence = prediction.get('confidence', 0)
    
    if score >= 3.5:
        level = "Xuất sắc"
        feedback = f"Bài làm thể hiện sự hiểu biết sâu sắc về {clo_info.get('description', 'CLO này')}."
    elif score >= 2.5:
        level = "Tốt"
        feedback = f"Bài làm đạt yêu cầu về {clo_info.get('description', 'CLO này')}."
    elif score >= 2.0:
        level = "Đạt"
        feedback = f"Bài làm đạt mức cơ bản về {clo_info.get('description', 'CLO này')}."
    else:
        level = "Chưa đạt"
        feedback = f"Bài làm cần cải thiện về {clo_info.get('description', 'CLO này')}."
    
    if confidence < 0.7:
        feedback += " (Độ tin cậy thấp - cần xem xét thêm)"
    
    return f"{level}: {feedback}"

def calculate_bloom_distribution() -> Dict:
    """Calculate Bloom level distribution"""
    distribution = {}
    for clo in clo_database.values():
        level = clo.get('bloom_level', 2)
        distribution[level] = distribution.get(level, 0) + 1
    
    return distribution

def calculate_course_distribution() -> Dict:
    """Calculate course distribution"""
    distribution = {}
    for clo in clo_database.values():
        course = clo.get('course_code', 'Unknown')
        distribution[course] = distribution.get(course, 0) + 1
    
    return distribution

def get_recent_assessments(limit: int = 10) -> List[Dict]:
    """Get recent assessments"""
    return assessment_history[-limit:] if assessment_history else []

def calculate_performance_trends() -> Dict:
    """Calculate performance trends"""
    if not assessment_history:
        return {'trend': 'no_data', 'average_scores': []}
    
    # Simple trend calculation
    recent_scores = []
    for assessment in assessment_history[-20:]:  # Last 20 assessments
        if assessment.get('overall_stats', {}).get('average_score'):
            recent_scores.append(assessment['overall_stats']['average_score'])
    
    if len(recent_scores) >= 2:
        trend = 'improving' if recent_scores[-1] > recent_scores[0] else 'declining'
    else:
        trend = 'stable'
    
    return {
        'trend': trend,
        'average_scores': recent_scores,
        'current_average': recent_scores[-1] if recent_scores else 0
    }

def get_top_performing_clos(limit: int = 5) -> List[Dict]:
    """Get top performing CLOs"""
    clo_scores = {}
    clo_counts = {}
    
    for assessment in assessment_history:
        for result in assessment.get('results', []):
            clo_code = result['clo_code']
            score = result['predicted_score']
            
            if clo_code not in clo_scores:
                clo_scores[clo_code] = 0
                clo_counts[clo_code] = 0
            
            clo_scores[clo_code] += score
            clo_counts[clo_code] += 1
    
    # Calculate averages
    clo_averages = []
    for clo_code in clo_scores:
        if clo_counts[clo_code] > 0:
            avg_score = clo_scores[clo_code] / clo_counts[clo_code]
            clo_averages.append({
                'clo_code': clo_code,
                'average_score': avg_score,
                'assessment_count': clo_counts[clo_code],
                'description': clo_database.get(clo_code, {}).get('description', '')
            })
    
    # Sort by average score
    clo_averages.sort(key=lambda x: x['average_score'], reverse=True)
    
    return clo_averages[:limit]

def get_improvement_needed_clos(limit: int = 5) -> List[Dict]:
    """Get CLOs that need improvement"""
    top_clos = get_top_performing_clos(len(clo_database))
    
    # Return bottom performers
    return top_clos[-limit:] if len(top_clos) >= limit else top_clos

if __name__ == '__main__':
    # Initialize models on startup
    initialize_models()
    
    # Run the app
    app.run(host='0.0.0.0', port=5001, debug=True)


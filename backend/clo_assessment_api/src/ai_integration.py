"""
AI Integration Module for CLO Assessment using EraX-VL-7B-V1.5
This module handles text analysis and CLO scoring using the offline AI model.
"""

import os
import re
import json
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import numpy as np

# Note: In a real implementation, you would import the actual EraX-VL-7B-V1.5 model
# For now, we'll create a simulation that demonstrates the expected functionality

@dataclass
class CLOAssessmentConfig:
    """Configuration for CLO assessment"""
    clo_id: int
    keywords: List[str]
    method: str
    full_score_threshold: float
    partial_score_floor: float
    max_score: float = 4.0

class EraXVLModel:
    """
    Wrapper for EraX-VL-7B-V1.5 model
    In production, this would load and interface with the actual model
    """
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self.model_loaded = False
        self.logger = logging.getLogger(__name__)
        
    def load_model(self):
        """Load the EraX-VL-7B-V1.5 model"""
        try:
            # In production, load the actual model here
            # self.model = load_erax_vl_model(self.model_path)
            self.model_loaded = True
            self.logger.info("EraX-VL-7B-V1.5 model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise
    
    def extract_features(self, text: str) -> np.ndarray:
        """Extract semantic features from text using the model"""
        if not self.model_loaded:
            self.load_model()
        
        # Simulate feature extraction
        # In production, this would use the actual model
        text_length = len(text.split())
        feature_vector = np.random.random(768)  # Typical embedding size
        
        return feature_vector
    
    def analyze_text_content(self, text: str) -> Dict:
        """Analyze text content and extract relevant information"""
        if not self.model_loaded:
            self.load_model()
        
        # Simulate content analysis
        analysis = {
            'word_count': len(text.split()),
            'sentence_count': len(text.split('.')),
            'technical_terms': self._extract_technical_terms(text),
            'complexity_score': self._calculate_complexity(text),
            'semantic_features': self.extract_features(text).tolist()
        }
        
        return analysis
    
    def _extract_technical_terms(self, text: str) -> List[str]:
        """Extract technical terms from text"""
        # Simple implementation - in production, use the model's capabilities
        technical_patterns = [
            r'\b[A-Z]{2,}\b',  # Acronyms
            r'\b\w*(?:tion|sion|ment|ness|ity)\b',  # Technical suffixes
            r'\b(?:phân tích|tính toán|thiết kế|mô hình|hệ thống)\b'  # Vietnamese technical terms
        ]
        
        terms = []
        for pattern in technical_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            terms.extend(matches)
        
        return list(set(terms))
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate text complexity score"""
        words = text.split()
        sentences = text.split('.')
        
        if len(sentences) == 0:
            return 0.0
        
        avg_words_per_sentence = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        complexity = (avg_words_per_sentence * 0.6 + avg_word_length * 0.4) / 10
        return min(complexity, 1.0)

class CLOAssessmentEngine:
    """Main engine for assessing CLO achievement from text content"""
    
    def __init__(self, model_path: str = None):
        self.ai_model = EraXVLModel(model_path)
        self.logger = logging.getLogger(__name__)
    
    def assess_clo_achievement(self, text: str, clo_config: CLOAssessmentConfig) -> Dict:
        """
        Assess CLO achievement based on text content
        
        Args:
            text: The text content to analyze
            clo_config: Configuration for the specific CLO
            
        Returns:
            Dictionary with assessment results
        """
        try:
            # Analyze text content
            content_analysis = self.ai_model.analyze_text_content(text)
            
            # Calculate CLO score based on method
            if clo_config.method == 'keyword_frequency':
                score, details = self._assess_by_keyword_frequency(text, clo_config, content_analysis)
            elif clo_config.method == 'content_analysis':
                score, details = self._assess_by_content_analysis(text, clo_config, content_analysis)
            elif clo_config.method == 'spatial_reasoning':
                score, details = self._assess_spatial_reasoning(text, clo_config, content_analysis)
            elif clo_config.method == 'attitude_assessment':
                score, details = self._assess_attitude(text, clo_config, content_analysis)
            elif clo_config.method == 'concept_understanding':
                score, details = self._assess_concept_understanding(text, clo_config, content_analysis)
            elif clo_config.method == 'problem_solving':
                score, details = self._assess_problem_solving(text, clo_config, content_analysis)
            elif clo_config.method == 'technical_calculation':
                score, details = self._assess_technical_calculation(text, clo_config, content_analysis)
            elif clo_config.method == 'learning_engagement':
                score, details = self._assess_learning_engagement(text, clo_config, content_analysis)
            else:
                score, details = self._assess_generic(text, clo_config, content_analysis)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(details, content_analysis)
            
            return {
                'clo_id': clo_config.clo_id,
                'score': score,
                'confidence': confidence,
                'method': clo_config.method,
                'details': details,
                'content_analysis': content_analysis
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing CLO {clo_config.clo_id}: {e}")
            return {
                'clo_id': clo_config.clo_id,
                'score': 0.0,
                'confidence': 0.0,
                'method': clo_config.method,
                'details': {'error': str(e)},
                'content_analysis': {}
            }
    
    def _assess_by_keyword_frequency(self, text: str, config: CLOAssessmentConfig, analysis: Dict) -> Tuple[float, Dict]:
        """Assess based on keyword frequency"""
        text_lower = text.lower()
        keyword_matches = {}
        total_matches = 0
        
        for keyword in config.keywords:
            matches = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower))
            keyword_matches[keyword] = matches
            total_matches += matches
        
        # Calculate score based on frequency
        if total_matches >= config.full_score_threshold:
            score = config.max_score
        elif total_matches >= config.partial_score_floor * config.full_score_threshold:
            ratio = total_matches / config.full_score_threshold
            score = config.max_score * ratio
        else:
            score = 0.0
        
        details = {
            'keyword_matches': keyword_matches,
            'total_matches': total_matches,
            'threshold_met': total_matches >= config.full_score_threshold
        }
        
        return score, details
    
    def _assess_by_content_analysis(self, text: str, config: CLOAssessmentConfig, analysis: Dict) -> Tuple[float, Dict]:
        """Assess based on content analysis"""
        # Use AI model's semantic understanding
        complexity = analysis.get('complexity_score', 0)
        technical_terms = analysis.get('technical_terms', [])
        
        # Check for relevant keywords
        keyword_score = 0
        for keyword in config.keywords:
            if keyword.lower() in text.lower():
                keyword_score += 1
        
        # Combine factors
        content_score = (complexity * 0.3 + 
                        len(technical_terms) * 0.1 + 
                        keyword_score * 0.6) / config.full_score_threshold
        
        score = min(content_score * config.max_score, config.max_score)
        
        details = {
            'complexity_score': complexity,
            'technical_terms_count': len(technical_terms),
            'keyword_score': keyword_score,
            'content_score': content_score
        }
        
        return score, details
    
    def _assess_spatial_reasoning(self, text: str, config: CLOAssessmentConfig, analysis: Dict) -> Tuple[float, Dict]:
        """Assess spatial reasoning abilities"""
        spatial_keywords = ['không gian', 'hình chiếu', 'biểu diễn', 'ba chiều', 'hai chiều', 'vuông góc']
        spatial_matches = sum(1 for keyword in spatial_keywords if keyword in text.lower())
        
        score = min(spatial_matches / config.full_score_threshold * config.max_score, config.max_score)
        
        details = {
            'spatial_keywords_found': spatial_matches,
            'spatial_reasoning_indicators': spatial_keywords
        }
        
        return score, details
    
    def _assess_attitude(self, text: str, config: CLOAssessmentConfig, analysis: Dict) -> Tuple[float, Dict]:
        """Assess learning attitude and engagement"""
        attitude_indicators = ['nghiêm túc', 'tích cực', 'chuyên cần', 'cẩn thận', 'tỷ mỷ']
        attitude_matches = sum(1 for indicator in attitude_indicators if indicator in text.lower())
        
        # Attitude assessment is often binary - either demonstrated or not
        score = config.max_score if attitude_matches >= config.full_score_threshold else 0.0
        
        details = {
            'attitude_indicators_found': attitude_matches,
            'demonstrates_good_attitude': attitude_matches >= config.full_score_threshold
        }
        
        return score, details
    
    def _assess_concept_understanding(self, text: str, config: CLOAssessmentConfig, analysis: Dict) -> Tuple[float, Dict]:
        """Assess conceptual understanding"""
        concept_keywords = config.keywords
        understanding_indicators = ['hiểu', 'nắm được', 'áp dụng', 'phân tích', 'giải thích']
        
        concept_matches = sum(1 for keyword in concept_keywords if keyword.lower() in text.lower())
        understanding_matches = sum(1 for indicator in understanding_indicators if indicator in text.lower())
        
        combined_score = (concept_matches + understanding_matches) / config.full_score_threshold
        score = min(combined_score * config.max_score, config.max_score)
        
        details = {
            'concept_matches': concept_matches,
            'understanding_indicators': understanding_matches,
            'combined_score': combined_score
        }
        
        return score, details
    
    def _assess_problem_solving(self, text: str, config: CLOAssessmentConfig, analysis: Dict) -> Tuple[float, Dict]:
        """Assess problem-solving abilities"""
        problem_solving_keywords = ['giải quyết', 'phương pháp', 'bước', 'thuật toán', 'kết quả']
        matches = sum(1 for keyword in problem_solving_keywords if keyword in text.lower())
        
        score = min(matches / config.full_score_threshold * config.max_score, config.max_score)
        
        details = {
            'problem_solving_indicators': matches,
            'shows_systematic_approach': matches >= config.full_score_threshold
        }
        
        return score, details
    
    def _assess_technical_calculation(self, text: str, config: CLOAssessmentConfig, analysis: Dict) -> Tuple[float, Dict]:
        """Assess technical calculation abilities"""
        calculation_patterns = [
            r'\d+\s*[+\-*/]\s*\d+',  # Basic math operations
            r'=\s*\d+',  # Equals signs with numbers
            r'\b\d+\.\d+\b',  # Decimal numbers
            r'\b\d+\s*%\b'  # Percentages
        ]
        
        calculation_matches = 0
        for pattern in calculation_patterns:
            calculation_matches += len(re.findall(pattern, text))
        
        technical_terms = len(analysis.get('technical_terms', []))
        combined_score = (calculation_matches + technical_terms) / config.full_score_threshold
        score = min(combined_score * config.max_score, config.max_score)
        
        details = {
            'calculation_matches': calculation_matches,
            'technical_terms': technical_terms,
            'shows_technical_competency': combined_score >= 1.0
        }
        
        return score, details
    
    def _assess_learning_engagement(self, text: str, config: CLOAssessmentConfig, analysis: Dict) -> Tuple[float, Dict]:
        """Assess learning engagement and participation"""
        engagement_indicators = ['tham gia', 'thảo luận', 'đóng góp', 'ý kiến', 'phản hồi']
        matches = sum(1 for indicator in engagement_indicators if indicator in text.lower())
        
        # Engagement is often demonstrated through presence of indicators
        score = config.max_score if matches >= config.full_score_threshold else 0.0
        
        details = {
            'engagement_indicators': matches,
            'shows_active_participation': matches >= config.full_score_threshold
        }
        
        return score, details
    
    def _assess_generic(self, text: str, config: CLOAssessmentConfig, analysis: Dict) -> Tuple[float, Dict]:
        """Generic assessment method"""
        keyword_matches = sum(1 for keyword in config.keywords if keyword.lower() in text.lower())
        score = min(keyword_matches / config.full_score_threshold * config.max_score, config.max_score)
        
        details = {
            'keyword_matches': keyword_matches,
            'assessment_method': 'generic'
        }
        
        return score, details
    
    def _calculate_confidence(self, assessment_details: Dict, content_analysis: Dict) -> float:
        """Calculate confidence score for the assessment"""
        factors = []
        
        # Text length factor
        word_count = content_analysis.get('word_count', 0)
        if word_count > 100:
            factors.append(0.9)
        elif word_count > 50:
            factors.append(0.7)
        else:
            factors.append(0.5)
        
        # Technical content factor
        technical_terms = len(content_analysis.get('technical_terms', []))
        if technical_terms > 5:
            factors.append(0.9)
        elif technical_terms > 2:
            factors.append(0.7)
        else:
            factors.append(0.5)
        
        # Assessment method reliability
        if 'keyword_matches' in assessment_details:
            matches = assessment_details['keyword_matches']
            if isinstance(matches, dict):
                total_matches = sum(matches.values())
            else:
                total_matches = matches
            
            if total_matches > 3:
                factors.append(0.8)
            elif total_matches > 1:
                factors.append(0.6)
            else:
                factors.append(0.4)
        
        return sum(factors) / len(factors) if factors else 0.5

# Utility functions for batch processing
def assess_document_for_all_clos(text: str, clo_configs: List[CLOAssessmentConfig], 
                                model_path: str = None) -> List[Dict]:
    """Assess a document against all relevant CLOs"""
    engine = CLOAssessmentEngine(model_path)
    results = []
    
    for config in clo_configs:
        result = engine.assess_clo_achievement(text, config)
        results.append(result)
    
    return results

def calculate_plo_scores(clo_results: List[Dict], clo_plo_mappings: Dict[int, List[Tuple[int, float]]]) -> Dict[int, Dict]:
    """
    Calculate PLO scores based on CLO results and mappings
    
    Args:
        clo_results: List of CLO assessment results
        clo_plo_mappings: Dict mapping CLO IDs to list of (PLO ID, weight) tuples
    
    Returns:
        Dict mapping PLO IDs to their scores and details
    """
    plo_scores = {}
    
    for clo_result in clo_results:
        clo_id = clo_result['clo_id']
        clo_score = clo_result['score']
        
        if clo_id in clo_plo_mappings:
            for plo_id, weight in clo_plo_mappings[clo_id]:
                if plo_id not in plo_scores:
                    plo_scores[plo_id] = {
                        'total_weighted_score': 0.0,
                        'total_weight': 0.0,
                        'contributing_clos': []
                    }
                
                weighted_score = clo_score * weight
                plo_scores[plo_id]['total_weighted_score'] += weighted_score
                plo_scores[plo_id]['total_weight'] += weight
                plo_scores[plo_id]['contributing_clos'].append({
                    'clo_id': clo_id,
                    'score': clo_score,
                    'weight': weight,
                    'weighted_score': weighted_score
                })
    
    # Calculate final PLO scores
    final_plo_scores = {}
    for plo_id, data in plo_scores.items():
        if data['total_weight'] > 0:
            final_score = data['total_weighted_score'] / data['total_weight']
        else:
            final_score = 0.0
        
        final_plo_scores[plo_id] = {
            'score': final_score,
            'confidence': min([clo['score'] for clo in data['contributing_clos']] + [1.0]),
            'contributing_clos': data['contributing_clos'],
            'total_weight': data['total_weight']
        }
    
    return final_plo_scores


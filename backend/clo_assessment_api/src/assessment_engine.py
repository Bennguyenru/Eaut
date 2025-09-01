"""
Advanced CLO Assessment Engine
Tích hợp Bloom Taxonomy và Multi-criteria Evaluation
"""

import json
import re
import math
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import Counter, defaultdict

class BloomLevel(Enum):
    REMEMBER = 1
    UNDERSTAND = 2
    APPLY = 3
    ANALYZE = 4
    EVALUATE = 5
    CREATE = 6

@dataclass
class AssessmentResult:
    clo_code: str
    score: float
    confidence: float
    bloom_level: int
    evidence: List[str]
    detailed_scores: Dict[str, float]
    recommendations: List[str]

@dataclass
class DocumentAnalysis:
    content: str
    word_count: int
    sentence_count: int
    paragraph_count: int
    complexity_score: float
    keywords_found: Dict[str, int]
    bloom_indicators: Dict[int, int]

class BloomAssessmentEngine:
    """
    Engine đánh giá CLO dựa trên Bloom Taxonomy và Multi-criteria
    """
    
    def __init__(self, plo_database_path: str, clo_database_path: str, keywords_database_path: str):
        self.plo_data = self._load_json(plo_database_path)
        self.clo_data = self._load_json(clo_database_path)
        self.keywords_data = self._load_json(keywords_database_path)
        
        # Bloom taxonomy keywords
        self.bloom_keywords = {
            1: ["nhớ", "ghi nhớ", "liệt kê", "xác định", "định nghĩa", "mô tả", "kể", "nêu"],
            2: ["hiểu", "giải thích", "tóm tắt", "phân loại", "so sánh", "minh họa", "diễn đạt", "phân biệt"],
            3: ["áp dụng", "sử dụng", "thực hiện", "giải quyết", "vận dụng", "thực hành", "tính toán", "thực thi"],
            4: ["phân tích", "so sánh", "phân biệt", "tổ chức", "cấu trúc", "phân loại", "kiểm tra", "khảo sát"],
            5: ["đánh giá", "phê bình", "kiểm tra", "thử nghiệm", "giám sát", "phán đoán", "chấm điểm", "xếp hạng"],
            6: ["tạo ra", "thiết kế", "xây dựng", "phát triển", "sáng tạo", "tổng hợp", "kết hợp", "sản xuất"]
        }
        
        # Complexity indicators
        self.complexity_indicators = {
            "simple": ["cơ bản", "đơn giản", "dễ", "thông thường"],
            "moderate": ["trung bình", "vừa phải", "khá", "tương đối"],
            "complex": ["phức tạp", "khó", "nâng cao", "chuyên sâu", "chi tiết"]
        }
        
    def _load_json(self, file_path: str) -> Dict:
        """Load JSON data from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return {}
    
    def analyze_document(self, content: str) -> DocumentAnalysis:
        """
        Phân tích tài liệu để trích xuất thông tin cơ bản
        """
        # Basic text statistics
        words = re.findall(r'\b\w+\b', content.lower())
        sentences = re.split(r'[.!?]+', content)
        paragraphs = content.split('\n\n')
        
        word_count = len(words)
        sentence_count = len([s for s in sentences if s.strip()])
        paragraph_count = len([p for p in paragraphs if p.strip()])
        
        # Calculate complexity score
        avg_words_per_sentence = word_count / max(sentence_count, 1)
        avg_sentences_per_paragraph = sentence_count / max(paragraph_count, 1)
        complexity_score = (avg_words_per_sentence * 0.6 + avg_sentences_per_paragraph * 0.4) / 20
        complexity_score = min(complexity_score, 1.0)
        
        # Find keywords
        keywords_found = self._find_keywords(content)
        
        # Detect Bloom level indicators
        bloom_indicators = self._detect_bloom_indicators(content)
        
        return DocumentAnalysis(
            content=content,
            word_count=word_count,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            complexity_score=complexity_score,
            keywords_found=keywords_found,
            bloom_indicators=bloom_indicators
        )
    
    def _find_keywords(self, content: str) -> Dict[str, int]:
        """
        Tìm keywords trong nội dung
        """
        content_lower = content.lower()
        keywords_found = {}
        
        # Search through all keyword categories
        for category_name, category_data in self.keywords_data.get("keyword_categories", {}).items():
            for keyword in category_data.get("keywords", []):
                count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', content_lower))
                if count > 0:
                    keywords_found[keyword] = count
        
        return keywords_found
    
    def _detect_bloom_indicators(self, content: str) -> Dict[int, int]:
        """
        Phát hiện các chỉ báo Bloom level trong nội dung
        """
        content_lower = content.lower()
        bloom_indicators = {level: 0 for level in range(1, 7)}
        
        for level, keywords in self.bloom_keywords.items():
            for keyword in keywords:
                count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', content_lower))
                bloom_indicators[level] += count
        
        return bloom_indicators
    
    def assess_clo(self, content: str, clo_code: str) -> AssessmentResult:
        """
        Đánh giá CLO cho một tài liệu
        """
        # Analyze document
        doc_analysis = self.analyze_document(content)
        
        # Find CLO configuration
        clo_config = self._find_clo_config(clo_code)
        if not clo_config:
            return self._create_error_result(clo_code, "CLO not found")
        
        # Get keyword mapping for this CLO
        keyword_mapping = self._find_keyword_mapping(clo_code)
        if not keyword_mapping:
            return self._create_error_result(clo_code, "Keyword mapping not found")
        
        # Calculate scores using different methods
        scores = self._calculate_multi_criteria_scores(doc_analysis, clo_config, keyword_mapping)
        
        # Calculate final score
        final_score = self._calculate_weighted_score(scores, clo_config)
        
        # Calculate confidence
        confidence = self._calculate_confidence(doc_analysis, keyword_mapping, scores)
        
        # Determine Bloom level
        bloom_level = self._determine_bloom_level(doc_analysis, clo_config)
        
        # Generate evidence
        evidence = self._generate_evidence(doc_analysis, keyword_mapping)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(scores, clo_config, doc_analysis)
        
        return AssessmentResult(
            clo_code=clo_code,
            score=final_score,
            confidence=confidence,
            bloom_level=bloom_level,
            evidence=evidence,
            detailed_scores=scores,
            recommendations=recommendations
        )
    
    def _find_clo_config(self, clo_code: str) -> Optional[Dict]:
        """
        Tìm cấu hình CLO
        """
        for course in self.clo_data.get("course_learning_outcomes", []):
            for clo in course.get("clos", []):
                if clo.get("code") == clo_code:
                    return clo
        return None
    
    def _find_keyword_mapping(self, clo_code: str) -> Optional[Dict]:
        """
        Tìm keyword mapping cho CLO
        """
        for mapping in self.keywords_data.get("clo_keyword_mapping", []):
            if mapping.get("clo_code") == clo_code:
                return mapping
        return None
    
    def _calculate_multi_criteria_scores(self, doc_analysis: DocumentAnalysis, 
                                       clo_config: Dict, keyword_mapping: Dict) -> Dict[str, float]:
        """
        Tính điểm theo nhiều tiêu chí
        """
        scores = {}
        
        # 1. Keyword-based scoring
        scores["keyword_score"] = self._calculate_keyword_score(doc_analysis, keyword_mapping)
        
        # 2. Bloom taxonomy scoring
        scores["bloom_score"] = self._calculate_bloom_score(doc_analysis, clo_config)
        
        # 3. Content depth scoring
        scores["depth_score"] = self._calculate_depth_score(doc_analysis)
        
        # 4. Structure scoring
        scores["structure_score"] = self._calculate_structure_score(doc_analysis)
        
        # 5. Complexity scoring
        scores["complexity_score"] = doc_analysis.complexity_score
        
        return scores
    
    def _calculate_keyword_score(self, doc_analysis: DocumentAnalysis, keyword_mapping: Dict) -> float:
        """
        Tính điểm dựa trên keywords
        """
        primary_keywords = keyword_mapping.get("primary_keywords", [])
        secondary_keywords = keyword_mapping.get("secondary_keywords", [])
        scoring_method = keyword_mapping.get("scoring_method", "distinct")
        full_threshold = keyword_mapping.get("full_score_threshold", 3)
        partial_floor = keyword_mapping.get("partial_score_floor", 0.3)
        
        primary_found = sum(1 for kw in primary_keywords if kw in doc_analysis.keywords_found)
        secondary_found = sum(1 for kw in secondary_keywords if kw in doc_analysis.keywords_found)
        
        if scoring_method == "distinct":
            score = (primary_found * 1.0 + secondary_found * 0.5) / full_threshold
        elif scoring_method == "termfreq":
            primary_freq = sum(doc_analysis.keywords_found.get(kw, 0) for kw in primary_keywords)
            secondary_freq = sum(doc_analysis.keywords_found.get(kw, 0) for kw in secondary_keywords)
            score = (primary_freq * 1.0 + secondary_freq * 0.5) / full_threshold
        elif scoring_method == "presence":
            score = 1.0 if (primary_found > 0 or secondary_found > 0) else 0.0
        else:
            score = 0.0
        
        return max(min(score, 1.0), partial_floor if score > 0 else 0.0)
    
    def _calculate_bloom_score(self, doc_analysis: DocumentAnalysis, clo_config: Dict) -> float:
        """
        Tính điểm dựa trên Bloom taxonomy
        """
        target_bloom = clo_config.get("bloom_level", 3)
        bloom_indicators = doc_analysis.bloom_indicators
        
        # Calculate weighted score based on Bloom level alignment
        total_indicators = sum(bloom_indicators.values())
        if total_indicators == 0:
            return 0.3  # Minimum score if no indicators found
        
        # Weight higher for target level and adjacent levels
        weighted_score = 0.0
        for level, count in bloom_indicators.items():
            if level == target_bloom:
                weight = 1.0
            elif abs(level - target_bloom) == 1:
                weight = 0.7
            elif abs(level - target_bloom) == 2:
                weight = 0.4
            else:
                weight = 0.1
            
            weighted_score += (count / total_indicators) * weight
        
        return min(weighted_score, 1.0)
    
    def _calculate_depth_score(self, doc_analysis: DocumentAnalysis) -> float:
        """
        Tính điểm độ sâu nội dung
        """
        # Based on word count, sentence structure, and keyword diversity
        word_score = min(doc_analysis.word_count / 500, 1.0)  # Normalize to 500 words
        keyword_diversity = len(doc_analysis.keywords_found) / max(len(doc_analysis.keywords_found), 1)
        keyword_diversity_score = min(keyword_diversity / 10, 1.0)  # Normalize to 10 unique keywords
        
        return (word_score * 0.6 + keyword_diversity_score * 0.4)
    
    def _calculate_structure_score(self, doc_analysis: DocumentAnalysis) -> float:
        """
        Tính điểm cấu trúc tài liệu
        """
        # Good structure: reasonable paragraphs and sentences
        if doc_analysis.paragraph_count == 0:
            return 0.2
        
        avg_sentences_per_para = doc_analysis.sentence_count / doc_analysis.paragraph_count
        
        # Optimal: 3-7 sentences per paragraph
        if 3 <= avg_sentences_per_para <= 7:
            structure_score = 1.0
        elif 2 <= avg_sentences_per_para < 3 or 7 < avg_sentences_per_para <= 10:
            structure_score = 0.8
        elif 1 <= avg_sentences_per_para < 2 or 10 < avg_sentences_per_para <= 15:
            structure_score = 0.6
        else:
            structure_score = 0.4
        
        return structure_score
    
    def _calculate_weighted_score(self, scores: Dict[str, float], clo_config: Dict) -> float:
        """
        Tính điểm tổng có trọng số
        """
        # Default weights
        weights = {
            "keyword_score": 0.35,
            "bloom_score": 0.25,
            "depth_score": 0.20,
            "structure_score": 0.10,
            "complexity_score": 0.10
        }
        
        # Adjust weights based on CLO type
        bloom_level = clo_config.get("bloom_level", 3)
        if bloom_level <= 2:  # Remember, Understand
            weights["keyword_score"] = 0.45
            weights["bloom_score"] = 0.30
        elif bloom_level >= 5:  # Evaluate, Create
            weights["bloom_score"] = 0.35
            weights["depth_score"] = 0.25
            weights["keyword_score"] = 0.25
        
        final_score = sum(scores.get(key, 0) * weight for key, weight in weights.items())
        return min(max(final_score, 0.0), 4.0)  # Scale to 0-4
    
    def _calculate_confidence(self, doc_analysis: DocumentAnalysis, 
                            keyword_mapping: Dict, scores: Dict[str, float]) -> float:
        """
        Tính độ tin cậy của kết quả đánh giá
        """
        factors = []
        
        # Factor 1: Keyword coverage
        primary_keywords = keyword_mapping.get("primary_keywords", [])
        primary_found = sum(1 for kw in primary_keywords if kw in doc_analysis.keywords_found)
        keyword_coverage = primary_found / max(len(primary_keywords), 1)
        factors.append(keyword_coverage)
        
        # Factor 2: Content length adequacy
        length_adequacy = min(doc_analysis.word_count / 200, 1.0)  # 200 words minimum
        factors.append(length_adequacy)
        
        # Factor 3: Score consistency
        score_values = list(scores.values())
        if len(score_values) > 1:
            score_std = np.std(score_values)
            consistency = max(0, 1 - score_std)  # Lower std = higher consistency
        else:
            consistency = 0.5
        factors.append(consistency)
        
        # Factor 4: Bloom indicator presence
        bloom_presence = min(sum(doc_analysis.bloom_indicators.values()) / 5, 1.0)
        factors.append(bloom_presence)
        
        return sum(factors) / len(factors)
    
    def _determine_bloom_level(self, doc_analysis: DocumentAnalysis, clo_config: Dict) -> int:
        """
        Xác định Bloom level của tài liệu
        """
        bloom_indicators = doc_analysis.bloom_indicators
        
        # Find the level with highest indicators
        if sum(bloom_indicators.values()) == 0:
            return clo_config.get("bloom_level", 2)  # Default to CLO target
        
        max_level = max(bloom_indicators.items(), key=lambda x: x[1])[0]
        return max_level
    
    def _generate_evidence(self, doc_analysis: DocumentAnalysis, keyword_mapping: Dict) -> List[str]:
        """
        Tạo bằng chứng cho kết quả đánh giá
        """
        evidence = []
        
        # Keywords found
        if doc_analysis.keywords_found:
            top_keywords = sorted(doc_analysis.keywords_found.items(), 
                                key=lambda x: x[1], reverse=True)[:5]
            evidence.append(f"Keywords tìm thấy: {', '.join([f'{kw}({count})' for kw, count in top_keywords])}")
        
        # Document statistics
        evidence.append(f"Thống kê: {doc_analysis.word_count} từ, {doc_analysis.sentence_count} câu, {doc_analysis.paragraph_count} đoạn")
        
        # Bloom indicators
        bloom_found = [(level, count) for level, count in doc_analysis.bloom_indicators.items() if count > 0]
        if bloom_found:
            bloom_str = ", ".join([f"Level {level}({count})" for level, count in bloom_found])
            evidence.append(f"Bloom indicators: {bloom_str}")
        
        # Complexity
        complexity_level = "Thấp" if doc_analysis.complexity_score < 0.3 else "Trung bình" if doc_analysis.complexity_score < 0.7 else "Cao"
        evidence.append(f"Độ phức tạp: {complexity_level} ({doc_analysis.complexity_score:.2f})")
        
        return evidence
    
    def _generate_recommendations(self, scores: Dict[str, float], 
                                clo_config: Dict, doc_analysis: DocumentAnalysis) -> List[str]:
        """
        Tạo khuyến nghị cải thiện
        """
        recommendations = []
        
        # Low keyword score
        if scores.get("keyword_score", 0) < 0.5:
            recommendations.append("Cần bổ sung thêm các từ khóa chuyên môn liên quan đến CLO")
        
        # Low Bloom score
        if scores.get("bloom_score", 0) < 0.5:
            target_bloom = clo_config.get("bloom_level", 3)
            bloom_names = ["", "Nhớ", "Hiểu", "Áp dụng", "Phân tích", "Đánh giá", "Sáng tạo"]
            if target_bloom < len(bloom_names):
                recommendations.append(f"Cần thể hiện rõ hơn kỹ năng '{bloom_names[target_bloom]}' (Bloom level {target_bloom})")
        
        # Low depth score
        if scores.get("depth_score", 0) < 0.5:
            recommendations.append("Nội dung cần được mở rộng và đi sâu hơn")
        
        # Low structure score
        if scores.get("structure_score", 0) < 0.5:
            recommendations.append("Cần cải thiện cấu trúc và tổ chức nội dung")
        
        # Content length
        if doc_analysis.word_count < 100:
            recommendations.append("Nội dung quá ngắn, cần mở rộng thêm")
        elif doc_analysis.word_count > 2000:
            recommendations.append("Nội dung có thể quá dài, cần tóm gọn lại")
        
        return recommendations
    
    def _create_error_result(self, clo_code: str, error_message: str) -> AssessmentResult:
        """
        Tạo kết quả lỗi
        """
        return AssessmentResult(
            clo_code=clo_code,
            score=0.0,
            confidence=0.0,
            bloom_level=1,
            evidence=[f"Lỗi: {error_message}"],
            detailed_scores={},
            recommendations=[f"Kiểm tra lại cấu hình CLO: {error_message}"]
        )
    
    def assess_multiple_clos(self, content: str, clo_codes: List[str]) -> List[AssessmentResult]:
        """
        Đánh giá nhiều CLO cùng lúc
        """
        results = []
        for clo_code in clo_codes:
            result = self.assess_clo(content, clo_code)
            results.append(result)
        return results
    
    def generate_summary_report(self, results: List[AssessmentResult]) -> Dict[str, Any]:
        """
        Tạo báo cáo tổng hợp
        """
        if not results:
            return {"error": "No assessment results"}
        
        total_score = sum(r.score for r in results)
        avg_score = total_score / len(results)
        avg_confidence = sum(r.confidence for r in results) / len(results)
        
        # Grade mapping
        if avg_score >= 3.5:
            grade = "Xuất sắc"
        elif avg_score >= 2.5:
            grade = "Tốt"
        elif avg_score >= 2.0:
            grade = "Khá"
        elif avg_score >= 1.0:
            grade = "Trung bình"
        else:
            grade = "Yếu"
        
        # Bloom level distribution
        bloom_distribution = Counter(r.bloom_level for r in results)
        
        # Common recommendations
        all_recommendations = []
        for r in results:
            all_recommendations.extend(r.recommendations)
        common_recommendations = [rec for rec, count in Counter(all_recommendations).most_common(5)]
        
        return {
            "summary": {
                "total_clos": len(results),
                "average_score": round(avg_score, 2),
                "average_confidence": round(avg_confidence, 2),
                "grade": grade,
                "total_score": round(total_score, 2)
            },
            "bloom_distribution": dict(bloom_distribution),
            "individual_results": [
                {
                    "clo_code": r.clo_code,
                    "score": round(r.score, 2),
                    "confidence": round(r.confidence, 2),
                    "bloom_level": r.bloom_level
                } for r in results
            ],
            "recommendations": common_recommendations,
            "detailed_results": results
        }

# Utility functions for integration
def create_assessment_engine() -> BloomAssessmentEngine:
    """
    Factory function to create assessment engine
    """
    return BloomAssessmentEngine(
        plo_database_path="/home/ubuntu/clo_plo_assessment_platform/data/complete_plo_database.json",
        clo_database_path="/home/ubuntu/clo_plo_assessment_platform/data/complete_clo_database.json",
        keywords_database_path="/home/ubuntu/clo_plo_assessment_platform/data/assessment_keywords_database.json"
    )

def assess_document_for_clos(content: str, clo_codes: List[str]) -> Dict[str, Any]:
    """
    Main function for document assessment
    """
    engine = create_assessment_engine()
    results = engine.assess_multiple_clos(content, clo_codes)
    return engine.generate_summary_report(results)


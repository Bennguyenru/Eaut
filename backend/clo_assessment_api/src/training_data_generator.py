"""
Training Data Generator
Tạo dữ liệu huấn luyện cho model từ CLO đã trích xuất
"""

import json
import random
import re
from typing import Dict, List, Tuple, Any
from pathlib import Path
import pandas as pd
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class TrainingSample:
    text: str
    clo_code: str
    target_score: float
    bloom_level: int
    keywords_found: List[str]
    confidence: float
    label: str  # 'positive', 'negative', 'neutral'
    metadata: Dict[str, Any]

class TrainingDataGenerator:
    """
    Tạo dữ liệu huấn luyện từ CLO đã trích xuất
    """
    
    def __init__(self, extracted_data_path: str, output_dir: str):
        self.extracted_data_path = Path(extracted_data_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load extracted data
        with open(self.extracted_data_path, 'r', encoding='utf-8') as f:
            self.extracted_data = json.load(f)
        
        # Templates for generating synthetic data
        self.positive_templates = [
            "Sinh viên {action} {concept} một cách {quality}. {detail}",
            "Báo cáo thể hiện {concept} {quality}. {action} {detail}",
            "Bài làm {action} {concept} và {detail} {quality}",
            "Nội dung {action} rõ ràng về {concept}. {detail}",
            "Sinh viên đã {action} {concept} {quality} và {detail}"
        ]
        
        self.negative_templates = [
            "Bài làm thiếu {concept}. Không {action} {detail}",
            "Nội dung không {action} {concept}. {detail} chưa rõ ràng",
            "Sinh viên chưa {action} {concept}. {detail} không đầy đủ",
            "Báo cáo không thể hiện {concept}. {action} {detail} chưa tốt",
            "Thiếu {concept} trong bài làm. {action} {detail} không chính xác"
        ]
        
        # Bloom level actions
        self.bloom_actions = {
            1: ["nhớ", "liệt kê", "xác định", "nêu", "kể"],
            2: ["hiểu", "giải thích", "mô tả", "so sánh", "phân loại"],
            3: ["áp dụng", "sử dụng", "thực hiện", "vận dụng", "tính toán"],
            4: ["phân tích", "so sánh", "phân biệt", "kiểm tra", "đánh giá"],
            5: ["đánh giá", "phê bình", "thử nghiệm", "giám sát", "chấm điểm"],
            6: ["tạo ra", "thiết kế", "xây dựng", "phát triển", "sáng tạo"]
        }
        
        # Quality descriptors
        self.quality_descriptors = {
            'positive': ["chính xác", "chi tiết", "đầy đủ", "rõ ràng", "tốt", "xuất sắc", "hoàn chỉnh"],
            'negative': ["không chính xác", "thiếu sót", "không đầy đủ", "mơ hồ", "kém", "yếu", "không hoàn chỉnh"]
        }
    
    def generate_training_dataset(self, num_samples_per_clo: int = 10) -> Dict[str, Any]:
        """
        Tạo dataset huấn luyện hoàn chỉnh
        """
        all_samples = []
        
        # Generate samples for each CLO
        for clo in self.extracted_data['all_clos']:
            clo_samples = self._generate_samples_for_clo(clo, num_samples_per_clo)
            all_samples.extend(clo_samples)
        
        # Split into train/val/test
        random.shuffle(all_samples)
        
        train_size = int(0.7 * len(all_samples))
        val_size = int(0.15 * len(all_samples))
        
        train_samples = all_samples[:train_size]
        val_samples = all_samples[train_size:train_size + val_size]
        test_samples = all_samples[train_size + val_size:]
        
        dataset = {
            'train': [self._sample_to_dict(s) for s in train_samples],
            'validation': [self._sample_to_dict(s) for s in val_samples],
            'test': [self._sample_to_dict(s) for s in test_samples],
            'metadata': {
                'total_samples': len(all_samples),
                'train_samples': len(train_samples),
                'val_samples': len(val_samples),
                'test_samples': len(test_samples),
                'clos_covered': len(self.extracted_data['all_clos']),
                'generation_method': 'template_based_synthetic'
            }
        }
        
        # Save dataset
        self._save_dataset(dataset)
        
        return dataset
    
    def _generate_samples_for_clo(self, clo: Dict, num_samples: int) -> List[TrainingSample]:
        """
        Tạo samples cho một CLO cụ thể
        """
        samples = []
        
        # Generate positive samples (60%)
        positive_count = int(num_samples * 0.6)
        for i in range(positive_count):
            sample = self._generate_positive_sample(clo)
            samples.append(sample)
        
        # Generate negative samples (25%)
        negative_count = int(num_samples * 0.25)
        for i in range(negative_count):
            sample = self._generate_negative_sample(clo)
            samples.append(sample)
        
        # Generate neutral samples (15%)
        neutral_count = num_samples - positive_count - negative_count
        for i in range(neutral_count):
            sample = self._generate_neutral_sample(clo)
            samples.append(sample)
        
        return samples
    
    def _generate_positive_sample(self, clo: Dict) -> TrainingSample:
        """
        Tạo sample tích cực (đạt CLO tốt)
        """
        template = random.choice(self.positive_templates)
        bloom_level = clo.get('bloom_level', 2)
        keywords = clo.get('keywords', [])
        
        # Select appropriate action based on Bloom level
        actions = self.bloom_actions.get(bloom_level, self.bloom_actions[2])
        action = random.choice(actions)
        
        # Select concept from keywords
        concept = random.choice(keywords) if keywords else "khái niệm cơ bản"
        
        # Select quality descriptor
        quality = random.choice(self.quality_descriptors['positive'])
        
        # Generate detail
        detail = self._generate_detail(clo, 'positive')
        
        # Fill template
        text = template.format(
            action=action,
            concept=concept,
            quality=quality,
            detail=detail
        )
        
        # Calculate score (3.0-4.0 for positive)
        score = random.uniform(3.0, 4.0)
        
        # Keywords found (high coverage for positive)
        keywords_found = random.sample(keywords, min(len(keywords), random.randint(3, 5))) if keywords else []
        
        return TrainingSample(
            text=text,
            clo_code=clo['clo_code'],
            target_score=score,
            bloom_level=bloom_level,
            keywords_found=keywords_found,
            confidence=random.uniform(0.8, 0.95),
            label='positive',
            metadata={
                'template_used': template,
                'generation_method': 'synthetic_positive',
                'course_code': clo.get('course_code', ''),
                'original_clo_description': clo.get('description', '')
            }
        )
    
    def _generate_negative_sample(self, clo: Dict) -> TrainingSample:
        """
        Tạo sample tiêu cực (không đạt CLO)
        """
        template = random.choice(self.negative_templates)
        bloom_level = clo.get('bloom_level', 2)
        keywords = clo.get('keywords', [])
        
        # Select inappropriate action (lower Bloom level)
        wrong_level = max(1, bloom_level - random.randint(1, 2))
        actions = self.bloom_actions.get(wrong_level, self.bloom_actions[1])
        action = random.choice(actions)
        
        # Select concept from keywords
        concept = random.choice(keywords) if keywords else "khái niệm cơ bản"
        
        # Generate detail
        detail = self._generate_detail(clo, 'negative')
        
        # Fill template
        text = template.format(
            action=action,
            concept=concept,
            detail=detail
        )
        
        # Calculate score (0.0-1.9 for negative)
        score = random.uniform(0.0, 1.9)
        
        # Keywords found (low coverage for negative)
        keywords_found = random.sample(keywords, min(len(keywords), random.randint(0, 2))) if keywords else []
        
        return TrainingSample(
            text=text,
            clo_code=clo['clo_code'],
            target_score=score,
            bloom_level=wrong_level,
            keywords_found=keywords_found,
            confidence=random.uniform(0.6, 0.8),
            label='negative',
            metadata={
                'template_used': template,
                'generation_method': 'synthetic_negative',
                'course_code': clo.get('course_code', ''),
                'original_clo_description': clo.get('description', '')
            }
        )
    
    def _generate_neutral_sample(self, clo: Dict) -> TrainingSample:
        """
        Tạo sample trung tính (đạt CLO ở mức trung bình)
        """
        # Mix positive and negative elements
        if random.choice([True, False]):
            template = random.choice(self.positive_templates)
            quality = random.choice(self.quality_descriptors['positive'][:3])  # Use moderate positive
        else:
            template = random.choice(self.negative_templates)
            quality = "tương đối"
        
        bloom_level = clo.get('bloom_level', 2)
        keywords = clo.get('keywords', [])
        
        # Select action
        actions = self.bloom_actions.get(bloom_level, self.bloom_actions[2])
        action = random.choice(actions)
        
        # Select concept
        concept = random.choice(keywords) if keywords else "khái niệm cơ bản"
        
        # Generate detail
        detail = self._generate_detail(clo, 'neutral')
        
        # Fill template
        text = template.format(
            action=action,
            concept=concept,
            quality=quality,
            detail=detail
        )
        
        # Calculate score (2.0-2.9 for neutral)
        score = random.uniform(2.0, 2.9)
        
        # Keywords found (medium coverage for neutral)
        keywords_found = random.sample(keywords, min(len(keywords), random.randint(1, 3))) if keywords else []
        
        return TrainingSample(
            text=text,
            clo_code=clo['clo_code'],
            target_score=score,
            bloom_level=bloom_level,
            keywords_found=keywords_found,
            confidence=random.uniform(0.7, 0.85),
            label='neutral',
            metadata={
                'template_used': template,
                'generation_method': 'synthetic_neutral',
                'course_code': clo.get('course_code', ''),
                'original_clo_description': clo.get('description', '')
            }
        )
    
    def _generate_detail(self, clo: Dict, sample_type: str) -> str:
        """
        Tạo chi tiết cho sample
        """
        keywords = clo.get('keywords', [])
        course_code = clo.get('course_code', '')
        
        if sample_type == 'positive':
            details = [
                f"Thể hiện hiểu biết sâu sắc về {random.choice(keywords) if keywords else 'chủ đề'}",
                f"Áp dụng kiến thức {course_code} một cách hiệu quả",
                f"Phân tích {random.choice(keywords) if keywords else 'vấn đề'} một cách logic",
                f"Kết luận chính xác và có căn cứ",
                f"Sử dụng thuật ngữ chuyên môn đúng đắn"
            ]
        elif sample_type == 'negative':
            details = [
                f"Không hiểu rõ về {random.choice(keywords) if keywords else 'chủ đề'}",
                f"Áp dụng kiến thức {course_code} chưa chính xác",
                f"Phân tích {random.choice(keywords) if keywords else 'vấn đề'} còn hạn chế",
                f"Kết luận thiếu căn cứ",
                f"Sử dụng thuật ngữ chưa đúng"
            ]
        else:  # neutral
            details = [
                f"Hiểu cơ bản về {random.choice(keywords) if keywords else 'chủ đề'}",
                f"Áp dụng kiến thức {course_code} ở mức độ cơ bản",
                f"Phân tích {random.choice(keywords) if keywords else 'vấn đề'} đơn giản",
                f"Kết luận cơ bản",
                f"Sử dụng thuật ngữ cơ bản"
            ]
        
        return random.choice(details)
    
    def _sample_to_dict(self, sample: TrainingSample) -> Dict[str, Any]:
        """
        Chuyển TrainingSample thành dictionary
        """
        return {
            'text': sample.text,
            'clo_code': sample.clo_code,
            'target_score': round(sample.target_score, 2),
            'bloom_level': sample.bloom_level,
            'keywords_found': sample.keywords_found,
            'confidence': round(sample.confidence, 3),
            'label': sample.label,
            'metadata': sample.metadata
        }
    
    def _save_dataset(self, dataset: Dict[str, Any]) -> None:
        """
        Lưu dataset vào files
        """
        # Save complete dataset
        with open(self.output_dir / 'complete_training_dataset.json', 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        
        # Save individual splits
        for split_name, split_data in dataset.items():
            if split_name != 'metadata':
                with open(self.output_dir / f'{split_name}_dataset.json', 'w', encoding='utf-8') as f:
                    json.dump(split_data, f, ensure_ascii=False, indent=2)
        
        # Save as CSV for easy viewing
        all_samples = []
        for split_name, split_data in dataset.items():
            if split_name != 'metadata':
                for sample in split_data:
                    sample['split'] = split_name
                    all_samples.append(sample)
        
        if all_samples:
            df = pd.DataFrame(all_samples)
            df.to_csv(self.output_dir / 'complete_training_dataset.csv', index=False, encoding='utf-8')
        
        logger.info(f"Training dataset saved to {self.output_dir}")
    
    def create_keyword_mappings(self) -> Dict[str, Any]:
        """
        Tạo keyword mappings cho assessment engine
        """
        keyword_mappings = {}
        
        for clo in self.extracted_data['all_clos']:
            clo_code = clo['clo_code']
            keywords = clo.get('keywords', [])
            bloom_level = clo.get('bloom_level', 2)
            
            # Split keywords into primary and secondary
            primary_keywords = keywords[:5] if len(keywords) > 5 else keywords
            secondary_keywords = keywords[5:] if len(keywords) > 5 else []
            
            # Determine scoring method based on Bloom level
            if bloom_level <= 2:
                scoring_method = 'distinct'
                full_threshold = 3
                partial_floor = 0.3
            elif bloom_level >= 5:
                scoring_method = 'presence'
                full_threshold = 1
                partial_floor = 0.5
            else:
                scoring_method = 'termfreq'
                full_threshold = 4
                partial_floor = 0.4
            
            keyword_mappings[clo_code] = {
                'primary_keywords': primary_keywords,
                'secondary_keywords': secondary_keywords,
                'scoring_method': scoring_method,
                'full_score_threshold': full_threshold,
                'partial_score_floor': partial_floor,
                'bloom_level': bloom_level,
                'course_code': clo.get('course_code', ''),
                'description': clo.get('description', '')
            }
        
        # Save keyword mappings
        with open(self.output_dir / 'keyword_mappings.json', 'w', encoding='utf-8') as f:
            json.dump(keyword_mappings, f, ensure_ascii=False, indent=2)
        
        return keyword_mappings
    
    def create_rubric_templates(self) -> Dict[str, Any]:
        """
        Tạo rubric templates từ CLO data
        """
        rubrics = {}
        
        # Group CLOs by Bloom level
        bloom_groups = {}
        for clo in self.extracted_data['all_clos']:
            bloom_level = clo.get('bloom_level', 2)
            if bloom_level not in bloom_groups:
                bloom_groups[bloom_level] = []
            bloom_groups[bloom_level].append(clo)
        
        # Create rubric for each Bloom level
        bloom_names = {
            1: "Nhớ (Remember)",
            2: "Hiểu (Understand)", 
            3: "Áp dụng (Apply)",
            4: "Phân tích (Analyze)",
            5: "Đánh giá (Evaluate)",
            6: "Sáng tạo (Create)"
        }
        
        for bloom_level, clos in bloom_groups.items():
            rubric_name = f"bloom_level_{bloom_level}"
            
            rubrics[rubric_name] = {
                'name': bloom_names.get(bloom_level, f"Level {bloom_level}"),
                'description': f"Rubric cho Bloom taxonomy level {bloom_level}",
                'criteria': {
                    'excellent': {
                        'score_range': [3.5, 4.0],
                        'description': self._get_rubric_description(bloom_level, 'excellent'),
                        'indicators': self._get_rubric_indicators(bloom_level, 'excellent')
                    },
                    'good': {
                        'score_range': [2.5, 3.4],
                        'description': self._get_rubric_description(bloom_level, 'good'),
                        'indicators': self._get_rubric_indicators(bloom_level, 'good')
                    },
                    'satisfactory': {
                        'score_range': [2.0, 2.4],
                        'description': self._get_rubric_description(bloom_level, 'satisfactory'),
                        'indicators': self._get_rubric_indicators(bloom_level, 'satisfactory')
                    },
                    'needs_improvement': {
                        'score_range': [1.0, 1.9],
                        'description': self._get_rubric_description(bloom_level, 'needs_improvement'),
                        'indicators': self._get_rubric_indicators(bloom_level, 'needs_improvement')
                    },
                    'unsatisfactory': {
                        'score_range': [0.0, 0.9],
                        'description': self._get_rubric_description(bloom_level, 'unsatisfactory'),
                        'indicators': self._get_rubric_indicators(bloom_level, 'unsatisfactory')
                    }
                },
                'sample_clos': [clo['clo_code'] for clo in clos[:3]]  # Sample CLOs
            }
        
        # Save rubrics
        with open(self.output_dir / 'rubric_templates.json', 'w', encoding='utf-8') as f:
            json.dump(rubrics, f, ensure_ascii=False, indent=2)
        
        return rubrics
    
    def _get_rubric_description(self, bloom_level: int, performance_level: str) -> str:
        """
        Tạo mô tả rubric cho Bloom level và performance level
        """
        descriptions = {
            1: {  # Remember
                'excellent': "Nhớ chính xác và đầy đủ tất cả thông tin, khái niệm cơ bản",
                'good': "Nhớ tốt hầu hết thông tin, khái niệm cơ bản",
                'satisfactory': "Nhớ cơ bản các thông tin, khái niệm chính",
                'needs_improvement': "Nhớ hạn chế, thiếu nhiều thông tin cơ bản",
                'unsatisfactory': "Không nhớ hoặc nhớ sai hầu hết thông tin"
            },
            2: {  # Understand
                'excellent': "Hiểu sâu sắc và giải thích rõ ràng các khái niệm",
                'good': "Hiểu tốt và giải thích được hầu hết khái niệm",
                'satisfactory': "Hiểu cơ bản các khái niệm chính",
                'needs_improvement': "Hiểu hạn chế, giải thích chưa rõ ràng",
                'unsatisfactory': "Không hiểu hoặc hiểu sai các khái niệm"
            },
            3: {  # Apply
                'excellent': "Áp dụng kiến thức chính xác và linh hoạt trong nhiều tình huống",
                'good': "Áp dụng kiến thức đúng trong hầu hết tình huống",
                'satisfactory': "Áp dụng kiến thức cơ bản trong tình huống quen thuộc",
                'needs_improvement': "Áp dụng kiến thức chưa chính xác",
                'unsatisfactory': "Không áp dụng được kiến thức"
            },
            4: {  # Analyze
                'excellent': "Phân tích sâu sắc, logic và có hệ thống",
                'good': "Phân tích tốt với logic rõ ràng",
                'satisfactory': "Phân tích cơ bản các yếu tố chính",
                'needs_improvement': "Phân tích hạn chế, thiếu logic",
                'unsatisfactory': "Không phân tích được hoặc phân tích sai"
            },
            5: {  # Evaluate
                'excellent': "Đánh giá toàn diện với tiêu chí rõ ràng và có căn cứ",
                'good': "Đánh giá tốt với tiêu chí hợp lý",
                'satisfactory': "Đánh giá cơ bản với tiêu chí đơn giản",
                'needs_improvement': "Đánh giá thiếu căn cứ",
                'unsatisfactory': "Không đánh giá được hoặc đánh giá sai"
            },
            6: {  # Create
                'excellent': "Sáng tạo độc đáo, khả thi và có giá trị cao",
                'good': "Sáng tạo tốt với ý tưởng mới",
                'satisfactory': "Sáng tạo cơ bản với ý tưởng đơn giản",
                'needs_improvement': "Sáng tạo hạn chế, thiếu tính mới",
                'unsatisfactory': "Không sáng tạo được hoặc sao chép"
            }
        }
        
        return descriptions.get(bloom_level, {}).get(performance_level, "Mô tả chưa có")
    
    def _get_rubric_indicators(self, bloom_level: int, performance_level: str) -> List[str]:
        """
        Tạo indicators cho rubric
        """
        indicators = {
            1: {  # Remember
                'excellent': ["Liệt kê đầy đủ", "Định nghĩa chính xác", "Nhận biết tất cả"],
                'good': ["Liệt kê hầu hết", "Định nghĩa đúng", "Nhận biết tốt"],
                'satisfactory': ["Liệt kê cơ bản", "Định nghĩa đơn giản", "Nhận biết được"],
                'needs_improvement': ["Liệt kê thiếu", "Định nghĩa chưa đúng", "Nhận biết hạn chế"],
                'unsatisfactory': ["Không liệt kê được", "Định nghĩa sai", "Không nhận biết"]
            },
            2: {  # Understand
                'excellent': ["Giải thích rõ ràng", "So sánh chính xác", "Phân loại đúng"],
                'good': ["Giải thích tốt", "So sánh hợp lý", "Phân loại cơ bản"],
                'satisfactory': ["Giải thích đơn giản", "So sánh cơ bản", "Phân loại được"],
                'needs_improvement': ["Giải thích chưa rõ", "So sánh thiếu chính xác", "Phân loại sai"],
                'unsatisfactory': ["Không giải thích được", "Không so sánh được", "Không phân loại được"]
            },
            3: {  # Apply
                'excellent': ["Vận dụng linh hoạt", "Thực hiện chính xác", "Giải quyết hiệu quả"],
                'good': ["Vận dụng tốt", "Thực hiện đúng", "Giải quyết được"],
                'satisfactory': ["Vận dụng cơ bản", "Thực hiện đơn giản", "Giải quyết một phần"],
                'needs_improvement': ["Vận dụng hạn chế", "Thực hiện chưa đúng", "Giải quyết thiếu"],
                'unsatisfactory': ["Không vận dụng được", "Không thực hiện được", "Không giải quyết được"]
            },
            4: {  # Analyze
                'excellent': ["Phân tích toàn diện", "Tìm mối liên hệ", "Xác định nguyên nhân"],
                'good': ["Phân tích tốt", "Thấy liên hệ", "Tìm nguyên nhân"],
                'satisfactory': ["Phân tích cơ bản", "Thấy liên hệ đơn giản", "Xác định một phần"],
                'needs_improvement': ["Phân tích hạn chế", "Thiếu liên hệ", "Không tìm nguyên nhân"],
                'unsatisfactory': ["Không phân tích được", "Không thấy liên hệ", "Không xác định được"]
            },
            5: {  # Evaluate
                'excellent': ["Đánh giá khách quan", "Tiêu chí rõ ràng", "Kết luận có căn cứ"],
                'good': ["Đánh giá hợp lý", "Tiêu chí phù hợp", "Kết luận đúng"],
                'satisfactory': ["Đánh giá cơ bản", "Tiêu chí đơn giản", "Kết luận được"],
                'needs_improvement': ["Đánh giá thiên lệch", "Tiêu chí không rõ", "Kết luận thiếu căn cứ"],
                'unsatisfactory': ["Không đánh giá được", "Không có tiêu chí", "Kết luận sai"]
            },
            6: {  # Create
                'excellent': ["Ý tưởng độc đáo", "Thiết kế sáng tạo", "Sản phẩm hoàn chỉnh"],
                'good': ["Ý tưởng mới", "Thiết kế tốt", "Sản phẩm khả thi"],
                'satisfactory': ["Ý tưởng cơ bản", "Thiết kế đơn giản", "Sản phẩm cơ bản"],
                'needs_improvement': ["Ý tưởng thiếu mới", "Thiết kế chưa tốt", "Sản phẩm chưa hoàn chỉnh"],
                'unsatisfactory': ["Không có ý tưởng", "Không thiết kế được", "Không tạo được sản phẩm"]
            }
        }
        
        return indicators.get(bloom_level, {}).get(performance_level, ["Chưa có indicators"])

def main():
    """
    Main function để tạo training data
    """
    extracted_data_path = "/home/ubuntu/clo_plo_assessment_platform/training_data/processed_documents/extracted_clo/complete_extraction_results.json"
    output_dir = "/home/ubuntu/clo_plo_assessment_platform/training_data/model_training/datasets"
    
    generator = TrainingDataGenerator(extracted_data_path, output_dir)
    
    # Generate training dataset
    print("🔄 Generating training dataset...")
    dataset = generator.generate_training_dataset(num_samples_per_clo=15)
    
    # Create keyword mappings
    print("🔄 Creating keyword mappings...")
    keyword_mappings = generator.create_keyword_mappings()
    
    # Create rubric templates
    print("🔄 Creating rubric templates...")
    rubrics = generator.create_rubric_templates()
    
    print("✅ Training data generation completed!")
    print(f"📊 Dataset statistics:")
    print(f"   - Total samples: {dataset['metadata']['total_samples']}")
    print(f"   - Train samples: {dataset['metadata']['train_samples']}")
    print(f"   - Validation samples: {dataset['metadata']['val_samples']}")
    print(f"   - Test samples: {dataset['metadata']['test_samples']}")
    print(f"   - CLOs covered: {dataset['metadata']['clos_covered']}")
    print(f"   - Keyword mappings: {len(keyword_mappings)}")
    print(f"   - Rubric templates: {len(rubrics)}")

if __name__ == "__main__":
    main()


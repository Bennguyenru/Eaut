"""
Data Extraction Engine
Tự động trích xuất CLO, nội dung, và metadata từ đề cương học phần
"""

import os
import re
import json
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import docx
from docx import Document
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CourseInfo:
    course_code: str
    course_name: str
    course_name_en: str
    credits: int
    theory_hours: int
    practice_hours: int
    prerequisite: str
    department: str
    program: str

@dataclass
class CLOInfo:
    clo_code: str
    course_code: str
    description: str
    pi_code: str
    plo_code: str
    assessment_level: str
    bloom_level: int
    weight: float
    keywords: List[str]
    assessment_methods: List[str]

@dataclass
class ChapterInfo:
    chapter_number: int
    chapter_title: str
    theory_hours: int
    practice_hours: int
    content_details: List[str]
    mapped_clos: List[str]

@dataclass
class AssessmentInfo:
    method: str
    weight: float
    mapped_clos: List[str]
    max_score: int
    description: str

class SyllabusExtractor:
    """
    Engine trích xuất thông tin từ đề cương học phần
    """
    
    def __init__(self):
        self.clo_patterns = [
            r'CLO\s*(\d+)',
            r'CĐR\s*(\d+)',
            r'Chuẩn đầu ra\s*(\d+)'
        ]
        
        self.pi_patterns = [
            r'PI\s*(\d+)\.(\d+)',
            r'Tiêu chí\s*(\d+)\.(\d+)'
        ]
        
        self.bloom_keywords = {
            1: ['nhớ', 'ghi nhớ', 'liệt kê', 'xác định', 'định nghĩa', 'kể'],
            2: ['hiểu', 'giải thích', 'tóm tắt', 'phân loại', 'so sánh', 'minh họa'],
            3: ['áp dụng', 'sử dụng', 'thực hiện', 'giải quyết', 'vận dụng', 'tính toán'],
            4: ['phân tích', 'so sánh', 'phân biệt', 'tổ chức', 'cấu trúc', 'kiểm tra'],
            5: ['đánh giá', 'phê bình', 'kiểm tra', 'thử nghiệm', 'giám sát', 'phán đoán'],
            6: ['tạo ra', 'thiết kế', 'xây dựng', 'phát triển', 'sáng tạo', 'tổng hợp']
        }
        
        self.assessment_level_mapping = {
            'I': 'Introduce',
            'T': 'Teach', 
            'U': 'Utilize'
        }
    
    def extract_from_docx(self, file_path: str) -> Dict[str, Any]:
        """
        Trích xuất thông tin từ file DOCX
        """
        try:
            doc = Document(file_path)
            text_content = self._extract_text_from_doc(doc)
            tables = self._extract_tables_from_doc(doc)
            
            # Extract different components
            course_info = self._extract_course_info(text_content, tables)
            clo_info = self._extract_clo_info(text_content, tables)
            chapter_info = self._extract_chapter_info(text_content, tables)
            assessment_info = self._extract_assessment_info(text_content, tables)
            
            return {
                'course_info': asdict(course_info) if course_info else None,
                'clos': [asdict(clo) for clo in clo_info],
                'chapters': [asdict(chapter) for chapter in chapter_info],
                'assessments': [asdict(assessment) for assessment in assessment_info],
                'raw_text': text_content,
                'extraction_metadata': {
                    'file_path': file_path,
                    'total_clos': len(clo_info),
                    'total_chapters': len(chapter_info),
                    'total_assessments': len(assessment_info)
                }
            }
            
        except Exception as e:
            logger.error(f"Error extracting from {file_path}: {e}")
            return {'error': str(e), 'file_path': file_path}
    
    def _extract_text_from_doc(self, doc: Document) -> str:
        """
        Trích xuất text từ document
        """
        text_parts = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text.strip())
        return '\n'.join(text_parts)
    
    def _extract_tables_from_doc(self, doc: Document) -> List[List[List[str]]]:
        """
        Trích xuất tables từ document
        """
        tables = []
        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_data = []
                for cell in row.cells:
                    row_data.append(cell.text.strip())
                table_data.append(row_data)
            tables.append(table_data)
        return tables
    
    def _extract_course_info(self, text: str, tables: List) -> Optional[CourseInfo]:
        """
        Trích xuất thông tin cơ bản của môn học
        """
        try:
            # Extract course code
            course_code_match = re.search(r'Mã học phần:\s*([A-Z]{2,3}\d{4})', text)
            course_code = course_code_match.group(1) if course_code_match else ""
            
            # Extract course name
            course_name_match = re.search(r'Tên học phần \(tiếng việt\):\s*(.+)', text)
            course_name = course_name_match.group(1).strip() if course_name_match else ""
            
            # Extract English name
            course_name_en_match = re.search(r'Tên học phần \(tiếng anh\):\s*(.+)', text)
            course_name_en = course_name_en_match.group(1).strip() if course_name_en_match else ""
            
            # Extract credits
            credits_match = re.search(r'Số tín chỉ:\s*(\d+)', text)
            credits = int(credits_match.group(1)) if credits_match else 0
            
            # Extract hours
            hours_match = re.search(r'Lý thuyết.*?(\d+)\s*TC.*?\((\d+)\s*giờ\)', text)
            theory_hours = int(hours_match.group(2)) if hours_match else 0
            
            practice_match = re.search(r'Thực hành.*?(\d+)\s*TC.*?\((\d+)\s*giờ\)', text)
            practice_hours = int(practice_match.group(2)) if practice_match else 0
            
            # Extract prerequisite
            prereq_match = re.search(r'Học phần tiên quyết:\s*(.+)', text)
            prerequisite = prereq_match.group(1).strip() if prereq_match else "Không"
            
            # Extract department
            dept_match = re.search(r'Bộ môn.*?\((.+?)\)', text)
            department = dept_match.group(1).strip() if dept_match else ""
            
            # Extract program
            program_match = re.search(r'Thuộc chương trình đào tạo:\s*(.+)', text)
            program = program_match.group(1).strip() if program_match else ""
            
            return CourseInfo(
                course_code=course_code,
                course_name=course_name,
                course_name_en=course_name_en,
                credits=credits,
                theory_hours=theory_hours,
                practice_hours=practice_hours,
                prerequisite=prerequisite,
                department=department,
                program=program
            )
            
        except Exception as e:
            logger.error(f"Error extracting course info: {e}")
            return None
    
    def _extract_clo_info(self, text: str, tables: List) -> List[CLOInfo]:
        """
        Trích xuất thông tin CLO
        """
        clos = []
        
        # Find CLO table in tables
        clo_table = self._find_clo_table(tables)
        if clo_table:
            clos.extend(self._extract_clos_from_table(clo_table))
        
        # Also try to extract from text
        clos.extend(self._extract_clos_from_text(text))
        
        # Remove duplicates
        unique_clos = []
        seen_codes = set()
        for clo in clos:
            if clo.clo_code not in seen_codes:
                unique_clos.append(clo)
                seen_codes.add(clo.clo_code)
        
        return unique_clos
    
    def _find_clo_table(self, tables: List) -> Optional[List[List[str]]]:
        """
        Tìm bảng chứa thông tin CLO
        """
        for table in tables:
            if len(table) > 1:
                header_row = ' '.join(table[0]).lower()
                if any(keyword in header_row for keyword in ['clo', 'cđr', 'chuẩn đầu ra', 'mã tiêu chí']):
                    return table
        return None
    
    def _extract_clos_from_table(self, table: List[List[str]]) -> List[CLOInfo]:
        """
        Trích xuất CLO từ bảng
        """
        clos = []
        
        # Find column indices
        header = table[0]
        clo_col = self._find_column_index(header, ['clo', 'cđr', 'mã cđr'])
        desc_col = self._find_column_index(header, ['nội dung', 'mô tả', 'description'])
        pi_col = self._find_column_index(header, ['pi', 'mã tiêu chí', 'tiêu chí'])
        level_col = self._find_column_index(header, ['mức độ', 'level', 'đánh giá'])
        
        for i, row in enumerate(table[1:], 1):
            if len(row) > max(clo_col or 0, desc_col or 0, pi_col or 0, level_col or 0):
                try:
                    clo_code = row[clo_col] if clo_col is not None else f"CLO{i}"
                    description = row[desc_col] if desc_col is not None else ""
                    pi_code = row[pi_col] if pi_col is not None else ""
                    assessment_level = row[level_col] if level_col is not None else ""
                    
                    # Clean up CLO code
                    if not clo_code.startswith('CLO'):
                        clo_code = f"CLO{clo_code}" if clo_code.isdigit() else f"CLO{i}"
                    
                    # Determine Bloom level
                    bloom_level = self._determine_bloom_level(description)
                    
                    # Extract keywords
                    keywords = self._extract_keywords_from_text(description)
                    
                    # Map PI to PLO
                    plo_code = self._map_pi_to_plo(pi_code)
                    
                    clo = CLOInfo(
                        clo_code=clo_code,
                        course_code="",  # Will be filled later
                        description=description,
                        pi_code=pi_code,
                        plo_code=plo_code,
                        assessment_level=assessment_level,
                        bloom_level=bloom_level,
                        weight=1.0,  # Default weight
                        keywords=keywords,
                        assessment_methods=[]
                    )
                    clos.append(clo)
                    
                except Exception as e:
                    logger.warning(f"Error processing CLO row {i}: {e}")
                    continue
        
        return clos
    
    def _extract_clos_from_text(self, text: str) -> List[CLOInfo]:
        """
        Trích xuất CLO từ text thuần
        """
        clos = []
        
        # Pattern to find CLO descriptions
        clo_pattern = r'CLO\s*(\d+)[:\s]*(.+?)(?=CLO\s*\d+|$)'
        matches = re.finditer(clo_pattern, text, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            clo_num = match.group(1)
            description = match.group(2).strip()
            
            # Clean description
            description = re.sub(r'\s+', ' ', description)
            description = description.split('\n')[0]  # Take first line
            
            if len(description) > 10:  # Valid description
                bloom_level = self._determine_bloom_level(description)
                keywords = self._extract_keywords_from_text(description)
                
                clo = CLOInfo(
                    clo_code=f"CLO{clo_num}",
                    course_code="",
                    description=description,
                    pi_code="",
                    plo_code="",
                    assessment_level="",
                    bloom_level=bloom_level,
                    weight=1.0,
                    keywords=keywords,
                    assessment_methods=[]
                )
                clos.append(clo)
        
        return clos
    
    def _find_column_index(self, header: List[str], keywords: List[str]) -> Optional[int]:
        """
        Tìm index của cột dựa trên keywords
        """
        for i, col in enumerate(header):
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in keywords):
                return i
        return None
    
    def _determine_bloom_level(self, description: str) -> int:
        """
        Xác định Bloom level từ mô tả
        """
        description_lower = description.lower()
        
        # Count keywords for each level
        level_scores = {}
        for level, keywords in self.bloom_keywords.items():
            score = sum(1 for keyword in keywords if keyword in description_lower)
            if score > 0:
                level_scores[level] = score
        
        if level_scores:
            return max(level_scores.items(), key=lambda x: x[1])[0]
        
        # Default based on common patterns
        if any(word in description_lower for word in ['hiểu', 'nắm', 'biết']):
            return 2
        elif any(word in description_lower for word in ['áp dụng', 'sử dụng', 'thực hiện']):
            return 3
        elif any(word in description_lower for word in ['phân tích', 'tính toán']):
            return 4
        else:
            return 2  # Default to Understand
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """
        Trích xuất keywords từ text
        """
        # Simple keyword extraction
        words = re.findall(r'\b\w{3,}\b', text.lower())
        
        # Filter out common words
        stop_words = {'của', 'và', 'trong', 'với', 'các', 'cho', 'từ', 'về', 'có', 'được', 'là', 'một'}
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Return top 10 most relevant keywords
        return list(set(keywords))[:10]
    
    def _map_pi_to_plo(self, pi_code: str) -> str:
        """
        Map PI code to PLO code
        """
        if not pi_code:
            return ""
        
        # Extract PLO number from PI code
        match = re.search(r'PI\s*(\d+)', pi_code)
        if match:
            plo_num = match.group(1)
            return f"PLO{plo_num}"
        
        return ""
    
    def _extract_chapter_info(self, text: str, tables: List) -> List[ChapterInfo]:
        """
        Trích xuất thông tin chương
        """
        chapters = []
        
        # Find content table
        content_table = self._find_content_table(tables)
        if content_table:
            chapters.extend(self._extract_chapters_from_table(content_table))
        
        return chapters
    
    def _find_content_table(self, tables: List) -> Optional[List[List[str]]]:
        """
        Tìm bảng nội dung học phần
        """
        for table in tables:
            if len(table) > 1:
                header_row = ' '.join(table[0]).lower()
                if any(keyword in header_row for keyword in ['nội dung', 'chương', 'bài', 'lt', 'bt']):
                    return table
        return None
    
    def _extract_chapters_from_table(self, table: List[List[str]]) -> List[ChapterInfo]:
        """
        Trích xuất thông tin chương từ bảng
        """
        chapters = []
        
        for i, row in enumerate(table[1:], 1):
            if len(row) >= 2:
                try:
                    content = row[1] if len(row) > 1 else ""
                    
                    # Extract chapter info
                    chapter_match = re.search(r'Chương\s*(\d+)[:\s]*(.+)', content)
                    if chapter_match:
                        chapter_num = int(chapter_match.group(1))
                        chapter_title = chapter_match.group(2).strip()
                        
                        # Extract hours
                        theory_hours = 0
                        practice_hours = 0
                        
                        if len(row) > 2:
                            try:
                                theory_hours = int(row[2]) if row[2].isdigit() else 0
                            except:
                                pass
                        
                        if len(row) > 3:
                            try:
                                practice_hours = int(row[3]) if row[3].isdigit() else 0
                            except:
                                pass
                        
                        # Extract mapped CLOs
                        mapped_clos = []
                        if len(row) > 6:
                            clo_text = row[6]
                            clo_matches = re.findall(r'CLO\d+', clo_text)
                            mapped_clos = clo_matches
                        
                        chapter = ChapterInfo(
                            chapter_number=chapter_num,
                            chapter_title=chapter_title,
                            theory_hours=theory_hours,
                            practice_hours=practice_hours,
                            content_details=[],
                            mapped_clos=mapped_clos
                        )
                        chapters.append(chapter)
                        
                except Exception as e:
                    logger.warning(f"Error processing chapter row {i}: {e}")
                    continue
        
        return chapters
    
    def _extract_assessment_info(self, text: str, tables: List) -> List[AssessmentInfo]:
        """
        Trích xuất thông tin đánh giá
        """
        assessments = []
        
        # Find assessment table
        assessment_table = self._find_assessment_table(tables)
        if assessment_table:
            assessments.extend(self._extract_assessments_from_table(assessment_table))
        
        return assessments
    
    def _find_assessment_table(self, tables: List) -> Optional[List[List[str]]]:
        """
        Tìm bảng đánh giá
        """
        for table in tables:
            if len(table) > 1:
                header_row = ' '.join(table[0]).lower()
                if any(keyword in header_row for keyword in ['đánh giá', 'hình thức', 'trọng số', 'điểm']):
                    return table
        return None
    
    def _extract_assessments_from_table(self, table: List[List[str]]) -> List[AssessmentInfo]:
        """
        Trích xuất thông tin đánh giá từ bảng
        """
        assessments = []
        
        for i, row in enumerate(table[1:], 1):
            if len(row) >= 3:
                try:
                    method = row[1] if len(row) > 1 else ""
                    weight_text = row[2] if len(row) > 2 else "0"
                    
                    # Extract weight
                    weight_match = re.search(r'(\d+(?:\.\d+)?)', weight_text)
                    weight = float(weight_match.group(1)) / 100 if weight_match else 0.0
                    
                    # Extract mapped CLOs
                    mapped_clos = []
                    if len(row) > 3:
                        clo_text = row[3]
                        clo_matches = re.findall(r'CLO\d+', clo_text)
                        mapped_clos = clo_matches
                    
                    # Extract max score
                    max_score = 10  # Default
                    if len(row) > 4:
                        score_match = re.search(r'(\d+)', row[4])
                        max_score = int(score_match.group(1)) if score_match else 10
                    
                    assessment = AssessmentInfo(
                        method=method,
                        weight=weight,
                        mapped_clos=mapped_clos,
                        max_score=max_score,
                        description=""
                    )
                    assessments.append(assessment)
                    
                except Exception as e:
                    logger.warning(f"Error processing assessment row {i}: {e}")
                    continue
        
        return assessments

class TrainingDataGenerator:
    """
    Tạo dữ liệu huấn luyện từ các đề cương đã trích xuất
    """
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.extractor = SyllabusExtractor()
    
    def process_all_syllabi(self, syllabi_dir: str) -> Dict[str, Any]:
        """
        Xử lý tất cả đề cương trong thư mục
        """
        syllabi_path = Path(syllabi_dir)
        results = {
            'courses': [],
            'all_clos': [],
            'all_chapters': [],
            'all_assessments': [],
            'statistics': {},
            'errors': []
        }
        
        docx_files = list(syllabi_path.glob('*.docx'))
        logger.info(f"Found {len(docx_files)} DOCX files to process")
        
        for file_path in docx_files:
            logger.info(f"Processing: {file_path.name}")
            
            try:
                extracted_data = self.extractor.extract_from_docx(str(file_path))
                
                if 'error' not in extracted_data:
                    # Add course code to CLOs
                    course_code = extracted_data.get('course_info', {}).get('course_code', '')
                    for clo in extracted_data.get('clos', []):
                        clo['course_code'] = course_code
                        clo['clo_code'] = f"{clo['clo_code']}_{course_code}"
                    
                    results['courses'].append(extracted_data)
                    results['all_clos'].extend(extracted_data.get('clos', []))
                    results['all_chapters'].extend(extracted_data.get('chapters', []))
                    results['all_assessments'].extend(extracted_data.get('assessments', []))
                else:
                    results['errors'].append(extracted_data)
                    
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                results['errors'].append({'file': str(file_path), 'error': str(e)})
        
        # Generate statistics
        results['statistics'] = self._generate_statistics(results)
        
        # Save results
        self._save_results(results)
        
        return results
    
    def _generate_statistics(self, results: Dict) -> Dict[str, Any]:
        """
        Tạo thống kê từ dữ liệu đã trích xuất
        """
        stats = {
            'total_courses': len(results['courses']),
            'total_clos': len(results['all_clos']),
            'total_chapters': len(results['all_chapters']),
            'total_assessments': len(results['all_assessments']),
            'errors': len(results['errors']),
            'bloom_distribution': {},
            'course_types': {},
            'assessment_methods': {}
        }
        
        # Bloom level distribution
        bloom_counts = {}
        for clo in results['all_clos']:
            level = clo.get('bloom_level', 0)
            bloom_counts[level] = bloom_counts.get(level, 0) + 1
        stats['bloom_distribution'] = bloom_counts
        
        # Course types
        course_types = {}
        for course in results['courses']:
            course_info = course.get('course_info', {})
            program = course_info.get('program', 'Unknown')
            course_types[program] = course_types.get(program, 0) + 1
        stats['course_types'] = course_types
        
        # Assessment methods
        assessment_methods = {}
        for assessment in results['all_assessments']:
            method = assessment.get('method', 'Unknown')
            assessment_methods[method] = assessment_methods.get(method, 0) + 1
        stats['assessment_methods'] = assessment_methods
        
        return stats
    
    def _save_results(self, results: Dict) -> None:
        """
        Lưu kết quả vào các file
        """
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save complete results
        with open(self.output_dir / 'complete_extraction_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # Save CLOs only
        with open(self.output_dir / 'extracted_clos.json', 'w', encoding='utf-8') as f:
            json.dump(results['all_clos'], f, ensure_ascii=False, indent=2)
        
        # Save as CSV for easy viewing
        if results['all_clos']:
            df_clos = pd.DataFrame(results['all_clos'])
            df_clos.to_csv(self.output_dir / 'extracted_clos.csv', index=False, encoding='utf-8')
        
        # Save statistics
        with open(self.output_dir / 'extraction_statistics.json', 'w', encoding='utf-8') as f:
            json.dump(results['statistics'], f, ensure_ascii=False, indent=2)
        
        logger.info(f"Results saved to {self.output_dir}")
    
    def create_training_dataset(self, results: Dict) -> Dict[str, Any]:
        """
        Tạo dataset huấn luyện từ dữ liệu đã trích xuất
        """
        training_data = {
            'positive_samples': [],
            'negative_samples': [],
            'keyword_mappings': {},
            'bloom_examples': {},
            'assessment_rubrics': {}
        }
        
        # Create positive samples from CLO descriptions
        for clo in results['all_clos']:
            sample = {
                'text': clo['description'],
                'clo_code': clo['clo_code'],
                'bloom_level': clo['bloom_level'],
                'keywords': clo['keywords'],
                'score': 3.0,  # Good score for CLO description
                'label': 'positive'
            }
            training_data['positive_samples'].append(sample)
        
        # Create keyword mappings
        for clo in results['all_clos']:
            training_data['keyword_mappings'][clo['clo_code']] = {
                'primary_keywords': clo['keywords'][:5],
                'secondary_keywords': clo['keywords'][5:],
                'bloom_level': clo['bloom_level'],
                'scoring_method': 'termfreq' if clo['bloom_level'] >= 3 else 'distinct'
            }
        
        # Create Bloom examples
        for level in range(1, 7):
            examples = [clo['description'] for clo in results['all_clos'] if clo['bloom_level'] == level]
            training_data['bloom_examples'][level] = examples[:10]  # Top 10 examples
        
        # Save training dataset
        output_path = self.output_dir / 'training_dataset.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Training dataset saved to {output_path}")
        return training_data

# Main execution functions
def extract_all_syllabi():
    """
    Main function to extract all syllabi
    """
    syllabi_dir = "/home/ubuntu/clo_plo_assessment_platform/training_data/raw_documents/course_syllabi"
    output_dir = "/home/ubuntu/clo_plo_assessment_platform/training_data/processed_documents/extracted_clo"
    
    generator = TrainingDataGenerator(output_dir)
    results = generator.process_all_syllabi(syllabi_dir)
    
    # Create training dataset
    training_data = generator.create_training_dataset(results)
    
    print(f"✅ Extraction completed!")
    print(f"📊 Statistics:")
    print(f"   - Total courses: {results['statistics']['total_courses']}")
    print(f"   - Total CLOs: {results['statistics']['total_clos']}")
    print(f"   - Total chapters: {results['statistics']['total_chapters']}")
    print(f"   - Errors: {results['statistics']['errors']}")
    
    return results, training_data

if __name__ == "__main__":
    extract_all_syllabi()


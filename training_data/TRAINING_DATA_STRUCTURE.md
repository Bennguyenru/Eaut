# Cấu trúc Thư mục Training Data cho CLO/PLO Assessment

## 📁 Tổng quan Cấu trúc

```
training_data/
├── raw_documents/              # Tài liệu gốc chưa xử lý
│   ├── course_syllabi/         # Đề cương học phần
│   ├── student_assignments/    # Bài tập sinh viên
│   ├── assessment_samples/     # Mẫu đánh giá
│   └── reference_materials/    # Tài liệu tham khảo
├── processed_documents/        # Tài liệu đã xử lý
│   ├── extracted_clo/          # CLO đã trích xuất
│   ├── extracted_content/      # Nội dung đã trích xuất
│   ├── annotated_text/         # Text đã gán nhãn
│   └── feature_vectors/        # Vector đặc trưng
├── labeled_data/               # Dữ liệu đã gán nhãn
│   ├── positive_samples/       # Mẫu tích cực (đạt CLO)
│   ├── negative_samples/       # Mẫu tiêu cực (không đạt CLO)
│   ├── graded_samples/         # Mẫu đã chấm điểm
│   └── rubric_examples/        # Ví dụ rubric
├── model_training/             # Dữ liệu huấn luyện model
│   ├── datasets/               # Dataset huấn luyện
│   ├── checkpoints/            # Model checkpoints
│   ├── configs/                # Cấu hình huấn luyện
│   └── logs/                   # Log huấn luyện
└── evaluation_criteria/        # Tiêu chí đánh giá
    ├── bloom_taxonomy/         # Bloom taxonomy
    ├── assessment_rubrics/     # Rubric đánh giá
    ├── scoring_guidelines/     # Hướng dẫn chấm điểm
    └── quality_metrics/        # Metrics chất lượng
```

## 📋 Mô tả Chi tiết

### 1. raw_documents/ - Tài liệu Gốc

#### course_syllabi/ - Đề cương Học phần
- **Mục đích**: Lưu trữ các đề cương học phần gốc
- **Định dạng**: .docx, .pdf, .doc
- **Nội dung**: CLO, nội dung môn học, phương pháp đánh giá
- **Ví dụ**: 
  - `24.Sứcbềnvậtliệu-ME2206.docx`
  - `21.Vẽkỹthuật-ME2252.docx`
  - `BảnmôtảCTĐTngànhCNKTOTO.docx`

#### student_assignments/ - Bài tập Sinh viên
- **Mục đích**: Lưu trữ bài tập, báo cáo của sinh viên
- **Định dạng**: .pdf, .docx, .txt
- **Phân loại**:
  - `excellent/` - Bài làm xuất sắc (3.5-4.0)
  - `good/` - Bài làm tốt (2.5-3.4)
  - `satisfactory/` - Bài làm khá (2.0-2.4)
  - `poor/` - Bài làm yếu (0-1.9)

#### assessment_samples/ - Mẫu Đánh giá
- **Mục đích**: Mẫu đánh giá CLO từ giảng viên
- **Nội dung**: Đánh giá thực tế, feedback, điểm số
- **Phân loại theo môn học và CLO**

#### reference_materials/ - Tài liệu Tham khảo
- **Mục đích**: Tài liệu chuẩn, guidelines, standards
- **Nội dung**: TCVN, ISO, sách giáo khoa, papers

### 2. processed_documents/ - Tài liệu Đã xử lý

#### extracted_clo/ - CLO Đã trích xuất
- **Định dạng**: JSON, CSV
- **Nội dung**: CLO đã chuẩn hóa từ đề cương
- **Schema**:
```json
{
  "course_code": "ME2206",
  "clo_code": "CLO1_ME2206",
  "description": "Hiểu rõ được các kiến thức...",
  "bloom_level": 2,
  "keywords": ["tác dụng cơ học", "thiết kế", "chế tạo"],
  "assessment_methods": ["Thi lý thuyết", "Bài tập"]
}
```

#### extracted_content/ - Nội dung Đã trích xuất
- **Định dạng**: .txt, .json
- **Nội dung**: Text đã làm sạch từ tài liệu gốc
- **Metadata**: Thông tin về nguồn, ngày tạo, xử lý

#### annotated_text/ - Text Đã gán nhãn
- **Định dạng**: .json, .xml
- **Nội dung**: Text với nhãn CLO, Bloom level, keywords
- **Annotation schema**:
```json
{
  "text": "Sinh viên hiểu rõ các khái niệm...",
  "annotations": [
    {
      "start": 0,
      "end": 15,
      "label": "BLOOM_UNDERSTAND",
      "clo": "CLO1_ME2206"
    }
  ]
}
```

#### feature_vectors/ - Vector Đặc trưng
- **Định dạng**: .npy, .pkl, .h5
- **Nội dung**: Vector embedding từ text
- **Models**: BERT, PhoBERT, EraX-VL embeddings

### 3. labeled_data/ - Dữ liệu Đã gán nhãn

#### positive_samples/ - Mẫu Tích cực
- **Nội dung**: Tài liệu đạt CLO tốt
- **Điểm số**: 2.5-4.0
- **Phân loại theo CLO và môn học**

#### negative_samples/ - Mẫu Tiêu cực
- **Nội dung**: Tài liệu không đạt CLO
- **Điểm số**: 0-1.9
- **Lý do**: Thiếu keywords, sai Bloom level, nội dung không phù hợp

#### graded_samples/ - Mẫu Đã chấm điểm
- **Nội dung**: Tài liệu với điểm số chi tiết
- **Metadata**: Rubric sử dụng, giảng viên chấm, ngày chấm
- **Format**:
```json
{
  "document_id": "sample_001",
  "clo_scores": {
    "CLO1": 3.2,
    "CLO2": 2.8,
    "CLO3": 3.5
  },
  "overall_score": 3.17,
  "feedback": "Nội dung tốt nhưng cần cải thiện...",
  "grader": "GV_001",
  "date": "2023-12-01"
}
```

#### rubric_examples/ - Ví dụ Rubric
- **Nội dung**: Rubric chuẩn cho từng CLO
- **Phân loại**: Theo môn học, Bloom level, loại bài tập

### 4. model_training/ - Dữ liệu Huấn luyện Model

#### datasets/ - Dataset Huấn luyện
- **train.json**: Dữ liệu huấn luyện (70%)
- **val.json**: Dữ liệu validation (15%)
- **test.json**: Dữ liệu test (15%)
- **Format**:
```json
{
  "input_text": "Nội dung bài làm sinh viên...",
  "clo_code": "CLO1_ME2206",
  "target_score": 3.2,
  "bloom_level": 3,
  "confidence": 0.85
}
```

#### checkpoints/ - Model Checkpoints
- **Nội dung**: Saved models, weights
- **Phân loại**: Theo epoch, performance metrics
- **Naming**: `model_epoch_{epoch}_acc_{accuracy}.pth`

#### configs/ - Cấu hình Huấn luyện
- **training_config.yaml**: Hyperparameters
- **model_config.yaml**: Kiến trúc model
- **data_config.yaml**: Cấu hình dataset

#### logs/ - Log Huấn luyện
- **training.log**: Log quá trình huấn luyện
- **tensorboard/**: TensorBoard logs
- **metrics.json**: Metrics theo epoch

### 5. evaluation_criteria/ - Tiêu chí Đánh giá

#### bloom_taxonomy/ - Bloom Taxonomy
- **bloom_keywords.json**: Keywords cho từng level
- **bloom_rubrics.json**: Rubric theo Bloom
- **bloom_examples.json**: Ví dụ cho từng level

#### assessment_rubrics/ - Rubric Đánh giá
- **general_rubric.json**: Rubric chung
- **course_specific_rubrics/**: Rubric theo môn học
- **clo_specific_rubrics/**: Rubric theo CLO

#### scoring_guidelines/ - Hướng dẫn Chấm điểm
- **scoring_manual.md**: Hướng dẫn chi tiết
- **common_errors.json**: Lỗi thường gặp
- **best_practices.md**: Best practices

#### quality_metrics/ - Metrics Chất lượng
- **accuracy_metrics.json**: Độ chính xác
- **consistency_metrics.json**: Tính nhất quán
- **reliability_metrics.json**: Độ tin cậy

## 🔄 Quy trình Xử lý Dữ liệu

### 1. Thu thập Dữ liệu
```bash
# Copy tài liệu mới vào raw_documents
cp new_syllabus.docx training_data/raw_documents/course_syllabi/
```

### 2. Trích xuất CLO
```python
# Chạy script trích xuất CLO
python scripts/extract_clo_from_syllabus.py
```

### 3. Xử lý Text
```python
# Làm sạch và chuẩn hóa text
python scripts/preprocess_documents.py
```

### 4. Gán nhãn
```python
# Gán nhãn tự động hoặc thủ công
python scripts/annotate_documents.py
```

### 5. Tạo Dataset
```python
# Tạo dataset huấn luyện
python scripts/create_training_dataset.py
```

### 6. Huấn luyện Model
```python
# Huấn luyện model
python scripts/train_model.py --config configs/training_config.yaml
```

## 📊 Thống kê Dữ liệu

### Hiện tại
- **Course Syllabi**: 15+ đề cương học phần
- **CLO Extracted**: 60+ CLO từ 4 môn học mẫu
- **Keywords**: 200+ keywords phân loại
- **Rubrics**: 20+ rubric templates

### Mục tiêu
- **Course Syllabi**: 100+ đề cương (toàn bộ chương trình)
- **Student Assignments**: 1000+ bài tập đã chấm điểm
- **Training Samples**: 5000+ samples cho huấn luyện
- **Model Accuracy**: >90% trên test set

## 🛠️ Tools và Scripts

### Extraction Tools
- `extract_clo_from_syllabus.py`: Trích xuất CLO từ đề cương
- `extract_content_from_pdf.py`: Trích xuất nội dung từ PDF
- `parse_student_assignments.py`: Parse bài tập sinh viên

### Processing Tools
- `preprocess_text.py`: Tiền xử lý text
- `annotate_bloom_level.py`: Gán nhãn Bloom level
- `generate_keywords.py`: Tạo keywords tự động

### Training Tools
- `create_dataset.py`: Tạo dataset huấn luyện
- `train_clo_classifier.py`: Huấn luyện classifier
- `evaluate_model.py`: Đánh giá model

### Validation Tools
- `validate_annotations.py`: Kiểm tra annotations
- `check_data_quality.py`: Kiểm tra chất lượng dữ liệu
- `inter_rater_reliability.py`: Tính độ tin cậy giữa người chấm

## 📝 Quy tắc Đặt tên

### Files
- **Course Syllabi**: `{course_code}_{course_name}.{ext}`
- **Student Assignments**: `{student_id}_{course_code}_{assignment_type}_{date}.{ext}`
- **Processed Data**: `{source}_{processing_type}_{date}.{ext}`

### Directories
- **By Course**: `{course_code}/`
- **By Date**: `{YYYY-MM-DD}/`
- **By Type**: `{data_type}/`

## 🔒 Bảo mật và Quyền riêng tư

### Student Data
- Anonymize student IDs
- Remove personal information
- Secure storage with encryption

### Grading Data
- Backup regularly
- Version control for changes
- Access control for sensitive data

## 📈 Monitoring và Maintenance

### Daily Tasks
- Check new documents
- Validate data quality
- Update statistics

### Weekly Tasks
- Review annotations
- Update rubrics
- Retrain models if needed

### Monthly Tasks
- Full data audit
- Performance evaluation
- Documentation updates

---

**Cấu trúc này đảm bảo tổ chức dữ liệu khoa học, có thể mở rộng và phù hợp cho việc huấn luyện model AI đánh giá CLO/PLO.**


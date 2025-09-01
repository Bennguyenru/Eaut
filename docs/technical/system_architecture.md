# Kiến trúc Hệ thống Đánh giá CLO/PLO - Khoa Cơ khí EAUT

## 1. Tổng quan Hệ thống

### 1.1 Mục tiêu
Xây dựng nền tảng đánh giá mức độ đạt chuẩn đầu ra môn học (CLO) và chương trình (PLO) tự động, sử dụng AI model EraX-VL-7B-V1.5 chạy offline.

### 1.2 Tính năng chính
- Upload và phân tích tài liệu học tập (bài thi, báo cáo, đồ án)
- Đánh giá tự động mức độ đạt CLO dựa trên nội dung
- Mapping CLO → PLO và tính toán mức độ đạt PLO
- Dashboard hiển thị kết quả và báo cáo
- Quản lý dữ liệu PLO, CLO, và mapping

## 2. Kiến trúc Tổng thể

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Model      │
│   (React)       │◄──►│   (Flask)       │◄──►│  EraX-VL-7B     │
│                 │    │                 │    │   (Offline)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (SQLite)      │
                       └─────────────────┘
```

## 3. Thành phần Hệ thống

### 3.1 Frontend (React)
- **Dashboard**: Tổng quan kết quả đánh giá
- **Upload Module**: Upload tài liệu cần đánh giá
- **Assessment Results**: Hiển thị kết quả chi tiết
- **Configuration**: Quản lý PLO, CLO, mapping
- **Reports**: Báo cáo và visualization

### 3.2 Backend (Flask)
- **API Gateway**: Xử lý requests từ frontend
- **Document Processor**: Xử lý tài liệu upload
- **AI Integration**: Tích hợp model EraX-VL-7B-V1.5
- **Assessment Engine**: Logic đánh giá CLO/PLO
- **Database Manager**: Quản lý dữ liệu

### 3.3 AI Model (EraX-VL-7B-V1.5)
- **Text Analysis**: Phân tích nội dung văn bản
- **Content Extraction**: Trích xuất thông tin quan trọng
- **Scoring**: Đánh giá mức độ đạt CLO

### 3.4 Database (SQLite)
- **PLO Table**: Lưu trữ Program Learning Outcomes
- **CLO Table**: Lưu trữ Course Learning Outcomes  
- **Mapping Table**: Quan hệ CLO → PLO
- **Assessment Results**: Kết quả đánh giá
- **Documents**: Metadata tài liệu

## 4. Luồng Xử lý Chính

### 4.1 Luồng Đánh giá Tài liệu
1. User upload tài liệu qua Frontend
2. Backend nhận và xử lý tài liệu
3. Gửi nội dung đến AI Model để phân tích
4. AI Model trả về điểm số cho từng CLO
5. Backend tính toán mức độ đạt PLO
6. Lưu kết quả vào Database
7. Frontend hiển thị kết quả

### 4.2 Luồng Quản lý Cấu hình
1. Admin cấu hình PLO, CLO qua Frontend
2. Backend validate và lưu vào Database
3. Cập nhật mapping CLO → PLO
4. Refresh scoring algorithms

## 5. Cơ sở Dữ liệu

### 5.1 Schema Tables

#### PLO Table
```sql
CREATE TABLE plo (
    id INTEGER PRIMARY KEY,
    code VARCHAR(10) NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### CLO Table  
```sql
CREATE TABLE clo (
    id INTEGER PRIMARY KEY,
    code VARCHAR(10) NOT NULL,
    course_code VARCHAR(10) NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    pi_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### CLO-PLO Mapping
```sql
CREATE TABLE clo_plo_mapping (
    id INTEGER PRIMARY KEY,
    clo_id INTEGER REFERENCES clo(id),
    plo_id INTEGER REFERENCES plo(id),
    weight FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Assessment Results
```sql
CREATE TABLE assessment_results (
    id INTEGER PRIMARY KEY,
    document_id INTEGER,
    clo_id INTEGER REFERENCES clo(id),
    score FLOAT,
    confidence FLOAT,
    details TEXT,
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 6. API Endpoints

### 6.1 Document Management
- `POST /api/documents/upload` - Upload tài liệu
- `GET /api/documents/{id}` - Lấy thông tin tài liệu
- `DELETE /api/documents/{id}` - Xóa tài liệu

### 6.2 Assessment
- `POST /api/assess/document/{id}` - Đánh giá tài liệu
- `GET /api/assess/results/{document_id}` - Lấy kết quả đánh giá
- `GET /api/assess/summary` - Tổng hợp kết quả

### 6.3 Configuration
- `GET /api/plo` - Danh sách PLO
- `POST /api/plo` - Tạo PLO mới
- `GET /api/clo` - Danh sách CLO
- `POST /api/clo` - Tạo CLO mới
- `GET /api/mapping` - Lấy mapping CLO-PLO
- `POST /api/mapping` - Cập nhật mapping

## 7. Tích hợp AI Model

### 7.1 Model Setup
- Download và setup EraX-VL-7B-V1.5 model
- Cấu hình để chạy offline
- Optimize cho performance

### 7.2 Text Processing Pipeline
1. **Preprocessing**: Làm sạch và chuẩn hóa text
2. **Feature Extraction**: Trích xuất features từ model
3. **CLO Matching**: So sánh với keywords của từng CLO
4. **Scoring**: Tính điểm dựa trên độ tương đồng
5. **Confidence**: Tính độ tin cậy của kết quả

## 8. Deployment

### 8.1 Requirements
- Python 3.8+
- Node.js 16+
- GPU (khuyến nghị cho AI model)
- 8GB+ RAM
- 50GB+ storage

### 8.2 Installation Steps
1. Clone repository
2. Setup Python environment
3. Install dependencies
4. Download AI model
5. Initialize database
6. Build frontend
7. Start services

## 9. Security & Performance

### 9.1 Security
- Input validation và sanitization
- File upload restrictions
- API rate limiting
- Data encryption

### 9.2 Performance
- Model caching
- Database indexing
- Async processing
- Result caching


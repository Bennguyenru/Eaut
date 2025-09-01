# Cấu trúc Dự án - Nền tảng Đánh giá CLO/PLO

## Khoa Cơ khí - Trường Đại học Công nghệ Đông Á (EAUT)

---

## 📁 Tổng quan Cấu trúc

```
clo_plo_assessment_platform/
├── 📁 src/                        # SOURCE CODE
│   ├── 📁 backend/                # Backend API Server
│   ├── 📁 frontend/               # Frontend Web Application  
│   ├── 📁 shared/                 # Shared utilities & types
│   └── 📁 utils/                  # Common utilities
├── 📁 models/                     # AI MODELS & CHECKPOINTS
│   ├── 📁 ai_models/              # EraX-VL-7B-V1.5 models
│   ├── 📁 pretrained/             # Pre-trained models
│   └── 📁 checkpoints/            # Model checkpoints
├── 📁 data/                       # DATA & CONFIGURATION
│   ├── 📄 plo.csv                 # PLO definitions
│   ├── 📄 clo.csv                 # CLO definitions
│   ├── 📄 clo_plo_mapping.csv     # CLO→PLO mappings
│   ├── 📄 clo_keywords.csv        # Keywords configuration
│   └── 📄 scoring_scale.csv       # Scoring parameters
├── 📁 uploads/                    # UPLOADED DOCUMENTS
│   ├── 📁 documents/              # Original uploaded files
│   ├── 📁 processed/              # AI processed files
│   └── 📁 temp/                   # Temporary files
├── 📁 exports/                    # EXPORTED RESULTS
│   ├── 📁 reports/                # PDF/Excel reports
│   ├── 📁 data/                   # CSV/JSON exports
│   └── 📁 charts/                 # Generated charts
├── 📁 docs/                       # DOCUMENTATION
│   ├── 📁 technical/              # Technical documentation
│   ├── 📁 user_guides/            # User manuals
│   ├── 📁 api/                    # API documentation
│   └── 📁 tutorials/              # Video tutorials
├── 📁 tests/                      # TESTING
│   ├── 📁 unit/                   # Unit tests
│   ├── 📁 integration/            # Integration tests
│   └── 📁 e2e/                    # End-to-end tests
├── 📁 scripts/                    # AUTOMATION SCRIPTS
│   ├── 📁 deployment/             # Deployment scripts
│   ├── 📁 maintenance/            # Maintenance scripts
│   └── 📁 data_migration/         # Data migration tools
├── 📁 logs/                       # LOG FILES
│   ├── 📁 backend/                # Backend logs
│   ├── 📁 frontend/               # Frontend logs
│   ├── 📁 ai/                     # AI processing logs
│   └── 📁 system/                 # System logs
├── 📁 backups/                    # BACKUP FILES
├── 📁 assets/                     # STATIC ASSETS
│   ├── 📁 images/                 # Images & screenshots
│   ├── 📁 icons/                  # Icons & logos
│   └── 📁 templates/              # Report templates
├── 📄 README.md                   # Main documentation
├── 📄 DEMO_SCRIPT.md              # Demo instructions
├── 📄 DELIVERABLES.md             # Project deliverables
├── 📄 PROJECT_STRUCTURE.md        # This file
└── 📄 todo.md                     # Project progress
```

---

## 🗂️ Chi tiết Từng Thư mục

### 📁 src/ - Source Code

#### 📁 src/backend/ - Backend API Server
```
src/backend/
├── 📁 clo_assessment_api/         # Main Flask application
│   ├── 📁 src/                    # Application source
│   │   ├── 📄 main.py             # Flask app entry point
│   │   ├── 📄 config.py           # Configuration settings
│   │   ├── 📄 ai_integration.py   # AI model wrapper
│   │   ├── 📁 models/             # Database models
│   │   │   ├── 📄 database.py     # Database setup
│   │   │   ├── 📄 plo.py          # PLO model
│   │   │   ├── 📄 clo.py          # CLO model
│   │   │   └── 📄 assessment.py   # Assessment model
│   │   ├── 📁 routes/             # API endpoints
│   │   │   ├── 📄 plo_routes.py   # PLO management
│   │   │   ├── 📄 clo_routes.py   # CLO management
│   │   │   └── 📄 assessment_routes.py # Assessment API
│   │   └── 📁 utils/              # Utility functions
│   ├── 📄 requirements.txt        # Python dependencies
│   ├── 📄 import_data.py          # Database initialization
│   └── 📄 clo_plo_assessment.db   # SQLite database
```

#### 📁 src/frontend/ - Frontend Web Application
```
src/frontend/
├── 📁 src/                        # React source code
│   ├── 📄 App.jsx                 # Main App component
│   ├── 📁 components/             # React components
│   │   ├── 📄 Dashboard.jsx       # Analytics dashboard
│   │   ├── 📄 PLOManagement.jsx   # PLO management
│   │   ├── 📄 CLOManagement.jsx   # CLO management
│   │   ├── 📄 DocumentUpload.jsx  # File upload
│   │   ├── 📄 AssessmentResults.jsx # Results display
│   │   └── 📄 Navigation.jsx      # Navigation bar
│   ├── 📁 lib/                    # Libraries & utilities
│   │   └── 📄 api.js              # API client
│   └── 📁 styles/                 # CSS styles
├── 📁 public/                     # Static assets
├── 📄 package.json                # Node.js dependencies
├── 📄 vite.config.js              # Vite configuration
└── 📄 index.html                  # HTML template
```

#### 📁 src/shared/ - Shared Code
```
src/shared/
├── 📄 types.js                    # Common type definitions
├── 📄 constants.js                # Application constants
├── 📄 validators.js               # Data validation
└── 📄 helpers.js                  # Helper functions
```

#### 📁 src/utils/ - Utilities
```
src/utils/
├── 📄 file_processor.py           # File processing utilities
├── 📄 text_analyzer.py            # Text analysis tools
├── 📄 score_calculator.py         # Scoring algorithms
└── 📄 report_generator.py         # Report generation
```

---

### 📁 models/ - AI Models & Checkpoints

#### 📁 models/ai_models/ - EraX-VL-7B-V1.5
```
models/ai_models/
├── 📁 erax-vl-7b-v1.5/           # Main AI model
│   ├── 📄 config.json            # Model configuration
│   ├── 📄 pytorch_model.bin      # Model weights
│   ├── 📄 tokenizer.json         # Tokenizer
│   ├── 📄 tokenizer_config.json  # Tokenizer config
│   └── 📄 vocab.txt              # Vocabulary
├── 📄 model_info.json            # Model metadata
└── 📄 README_MODELS.md           # Model documentation
```

#### 📁 models/pretrained/ - Pre-trained Models
```
models/pretrained/
├── 📁 vietnamese_nlp/            # Vietnamese NLP models
├── 📁 text_classification/       # Text classification models
└── 📁 embeddings/                # Word embeddings
```

#### 📁 models/checkpoints/ - Model Checkpoints
```
models/checkpoints/
├── 📁 training_runs/             # Training checkpoints
├── 📁 fine_tuned/                # Fine-tuned models
└── 📁 backups/                   # Model backups
```

---

### 📁 data/ - Data & Configuration

#### Cấu trúc Data Files
```
data/
├── 📄 plo.csv                    # Program Learning Outcomes
│   # Columns: code, title, description, category, performance_indicators
├── 📄 clo.csv                    # Course Learning Outcomes  
│   # Columns: code, course_code, course_name, title, description, assessment_level, plo_mappings
├── 📄 clo_plo_mapping.csv        # CLO→PLO Mappings
│   # Columns: clo_code, plo_code, pi_code, mapping_strength
├── 📄 clo_keywords.csv           # Keywords Configuration
│   # Columns: clo_code, keywords, weights, scoring_method
├── 📄 scoring_scale.csv          # Scoring Parameters
│   # Columns: clo_code, method, full_at, partial_floor, max_score
├── 📁 samples/                   # Sample data files
│   ├── 📄 sample_plo.csv         # Sample PLO data
│   ├── 📄 sample_clo.csv         # Sample CLO data
│   └── 📄 sample_assessments.csv # Sample assessment results
└── 📁 schemas/                   # Data schemas
    ├── 📄 plo_schema.json        # PLO data schema
    ├── 📄 clo_schema.json        # CLO data schema
    └── 📄 assessment_schema.json # Assessment schema
```

---

### 📁 uploads/ - Uploaded Documents

#### 📁 uploads/documents/ - Original Files
```
uploads/documents/
├── 📁 2024/                      # Year-based organization
│   ├── 📁 01/                    # Month folders
│   │   ├── 📁 ME2252/            # Course-based subfolders
│   │   │   ├── 📄 assignment_1_student_a.pdf
│   │   │   ├── 📄 exam_midterm_student_b.docx
│   │   │   └── 📄 project_report_student_c.pdf
│   │   └── 📁 AET3217/
│   └── 📁 02/
├── 📁 2025/
└── 📄 upload_log.csv             # Upload history log
```

#### 📁 uploads/processed/ - AI Processed Files
```
uploads/processed/
├── 📁 extracted_text/            # Extracted text content
├── 📁 analysis_results/          # AI analysis results
├── 📁 keywords_found/            # Keywords detection results
└── 📁 scores_calculated/         # Calculated scores
```

#### 📁 uploads/temp/ - Temporary Files
```
uploads/temp/
├── 📁 upload_staging/            # Files being uploaded
├── 📁 processing_queue/          # Files waiting for AI processing
└── 📁 cleanup/                   # Files marked for deletion
```

---

### 📁 exports/ - Exported Results

#### 📁 exports/reports/ - Generated Reports
```
exports/reports/
├── 📁 pdf/                       # PDF reports
│   ├── 📄 clo_assessment_report_2024_01.pdf
│   ├── 📄 plo_summary_report_2024_Q1.pdf
│   └── 📄 individual_assessment_student_a.pdf
├── 📁 excel/                     # Excel reports
│   ├── 📄 clo_scores_summary.xlsx
│   ├── 📄 plo_achievement_analysis.xlsx
│   └── 📄 detailed_assessment_results.xlsx
└── 📁 powerpoint/                # PowerPoint presentations
    ├── 📄 quarterly_review_Q1_2024.pptx
    └── 📄 annual_assessment_summary.pptx
```

#### 📁 exports/data/ - Data Exports
```
exports/data/
├── 📁 csv/                       # CSV data exports
│   ├── 📄 all_assessments.csv    # All assessment results
│   ├── 📄 clo_scores_by_course.csv
│   └── 📄 plo_achievement_trends.csv
├── 📁 json/                      # JSON data exports
│   ├── 📄 assessment_api_export.json
│   └── 📄 dashboard_data.json
└── 📁 xml/                       # XML exports (for integration)
    └── 📄 abet_compliance_report.xml
```

#### 📁 exports/charts/ - Generated Charts
```
exports/charts/
├── 📁 png/                       # PNG chart images
├── 📁 svg/                       # SVG vector charts
└── 📁 interactive/               # Interactive HTML charts
```

---

### 📁 docs/ - Documentation

#### 📁 docs/technical/ - Technical Documentation
```
docs/technical/
├── 📄 system_architecture.md     # System architecture
├── 📄 database_schema.md         # Database design
├── 📄 ai_model_integration.md    # AI integration guide
├── 📄 security_considerations.md # Security documentation
└── 📄 performance_optimization.md # Performance tuning
```

#### 📁 docs/user_guides/ - User Documentation
```
docs/user_guides/
├── 📄 README.md                  # Main user guide
├── 📄 installation_guide.md      # Installation instructions
├── 📄 user_manual.md             # Complete user manual
├── 📄 quick_start_guide.md       # Quick start tutorial
└── 📄 troubleshooting.md         # Common issues & solutions
```

#### 📁 docs/api/ - API Documentation
```
docs/api/
├── 📄 api_reference.md           # Complete API reference
├── 📄 authentication.md          # Authentication guide
├── 📄 endpoints_overview.md      # API endpoints overview
├── 📁 examples/                  # API usage examples
│   ├── 📄 curl_examples.sh       # cURL examples
│   ├── 📄 python_examples.py     # Python examples
│   └── 📄 javascript_examples.js # JavaScript examples
└── 📄 postman_collection.json    # Postman collection
```

#### 📁 docs/tutorials/ - Tutorials & Training
```
docs/tutorials/
├── 📁 video_scripts/             # Video tutorial scripts
├── 📁 screenshots/               # Tutorial screenshots
├── 📄 getting_started.md         # Getting started tutorial
├── 📄 advanced_features.md       # Advanced features guide
└── 📄 best_practices.md          # Best practices guide
```

---

### 📁 tests/ - Testing

#### 📁 tests/unit/ - Unit Tests
```
tests/unit/
├── 📁 backend/                   # Backend unit tests
│   ├── 📄 test_models.py         # Database model tests
│   ├── 📄 test_routes.py         # API route tests
│   └── 📄 test_ai_integration.py # AI integration tests
├── 📁 frontend/                  # Frontend unit tests
│   ├── 📄 Dashboard.test.jsx     # Dashboard component tests
│   ├── 📄 PLOManagement.test.jsx # PLO management tests
│   └── 📄 api.test.js            # API client tests
└── 📄 test_config.py             # Test configuration
```

#### 📁 tests/integration/ - Integration Tests
```
tests/integration/
├── 📄 test_api_integration.py    # API integration tests
├── 📄 test_database_operations.py # Database integration
├── 📄 test_file_upload.py        # File upload workflow
└── 📄 test_assessment_pipeline.py # End-to-end assessment
```

#### 📁 tests/e2e/ - End-to-End Tests
```
tests/e2e/
├── 📄 test_user_workflows.py     # Complete user workflows
├── 📄 test_dashboard_functionality.py # Dashboard E2E tests
├── 📁 fixtures/                  # Test fixtures & data
└── 📁 screenshots/               # Test screenshots
```

---

### 📁 scripts/ - Automation Scripts

#### 📁 scripts/deployment/ - Deployment Scripts
```
scripts/deployment/
├── 📄 deploy_production.sh       # Production deployment
├── 📄 deploy_staging.sh          # Staging deployment
├── 📄 setup_environment.sh       # Environment setup
├── 📄 install_dependencies.sh    # Dependencies installation
├── 📁 docker/                    # Docker deployment
│   ├── 📄 Dockerfile.backend     # Backend Docker image
│   ├── 📄 Dockerfile.frontend    # Frontend Docker image
│   └── 📄 docker-compose.yml     # Docker Compose config
└── 📁 kubernetes/                # Kubernetes deployment
    ├── 📄 backend-deployment.yaml
    ├── 📄 frontend-deployment.yaml
    └── 📄 service.yaml
```

#### 📁 scripts/maintenance/ - Maintenance Scripts
```
scripts/maintenance/
├── 📄 backup_database.sh         # Database backup
├── 📄 cleanup_temp_files.sh      # Temporary files cleanup
├── 📄 update_ai_models.py        # AI model updates
├── 📄 system_health_check.py     # System monitoring
└── 📄 log_rotation.sh            # Log file rotation
```

#### 📁 scripts/data_migration/ - Data Migration
```
scripts/data_migration/
├── 📄 migrate_from_v1.py         # Version migration
├── 📄 import_legacy_data.py      # Legacy data import
├── 📄 export_for_backup.py       # Data export utility
└── 📄 validate_data_integrity.py # Data validation
```

---

### 📁 logs/ - Log Files

#### Cấu trúc Log Files
```
logs/
├── 📁 backend/                   # Backend application logs
│   ├── 📄 app.log                # Main application log
│   ├── 📄 api.log                # API request/response log
│   ├── 📄 database.log           # Database operation log
│   └── 📄 error.log              # Error log
├── 📁 frontend/                  # Frontend logs
│   ├── 📄 console.log            # Browser console log
│   └── 📄 performance.log        # Performance metrics
├── 📁 ai/                        # AI processing logs
│   ├── 📄 model_inference.log    # AI model inference log
│   ├── 📄 document_processing.log # Document processing log
│   └── 📄 assessment_results.log # Assessment calculation log
├── 📁 system/                    # System logs
│   ├── 📄 access.log             # Access log
│   ├── 📄 security.log           # Security events
│   └── 📄 performance.log        # System performance
└── 📄 log_config.json            # Logging configuration
```

---

### 📁 backups/ - Backup Files

#### Cấu trúc Backup
```
backups/
├── 📁 database/                  # Database backups
│   ├── 📄 daily/                 # Daily backups
│   ├── 📄 weekly/                # Weekly backups
│   └── 📄 monthly/               # Monthly backups
├── 📁 uploads/                   # Uploaded files backup
├── 📁 configurations/            # Configuration backups
├── 📁 models/                    # AI model backups
└── 📄 backup_schedule.json       # Backup configuration
```

---

### 📁 assets/ - Static Assets

#### 📁 assets/images/ - Images & Screenshots
```
assets/images/
├── 📁 logos/                     # University & department logos
├── 📁 screenshots/               # Application screenshots
├── 📁 diagrams/                  # System diagrams
└── 📁 charts/                    # Chart templates
```

#### 📁 assets/icons/ - Icons & Graphics
```
assets/icons/
├── 📁 ui_icons/                  # User interface icons
├── 📁 file_type_icons/           # File type icons
└── 📁 status_icons/              # Status indicator icons
```

#### 📁 assets/templates/ - Report Templates
```
assets/templates/
├── 📁 pdf_templates/             # PDF report templates
├── 📁 excel_templates/           # Excel report templates
└── 📁 powerpoint_templates/      # PowerPoint templates
```

---

## 🔧 Cấu hình Thư mục

### Environment Variables
```bash
# Đường dẫn thư mục chính
export CLO_PLO_ROOT="/home/ubuntu/clo_plo_assessment_platform"
export CLO_PLO_MODELS="$CLO_PLO_ROOT/models"
export CLO_PLO_UPLOADS="$CLO_PLO_ROOT/uploads"
export CLO_PLO_EXPORTS="$CLO_PLO_ROOT/exports"
export CLO_PLO_LOGS="$CLO_PLO_ROOT/logs"
export CLO_PLO_BACKUPS="$CLO_PLO_ROOT/backups"
```

### Permissions Setup
```bash
# Thiết lập quyền truy cập
chmod -R 755 src/
chmod -R 777 uploads/
chmod -R 755 exports/
chmod -R 644 docs/
chmod -R 600 logs/
chmod -R 700 backups/
chmod -R 644 assets/
```

### Gitignore Configuration
```gitignore
# Thư mục không commit
uploads/documents/
uploads/processed/
uploads/temp/
logs/
backups/
models/ai_models/
exports/reports/
node_modules/
__pycache__/
*.pyc
*.log
*.db
.env
.venv/
```

---

## 📋 Hướng dẫn Sử dụng Cấu trúc

### 1. Khởi tạo Dự án Mới
```bash
# Clone hoặc tạo thư mục dự án
git clone <repository> clo_plo_assessment_platform
cd clo_plo_assessment_platform

# Tạo cấu trúc thư mục
bash scripts/deployment/setup_environment.sh
```

### 2. Development Workflow
```bash
# Backend development
cd src/backend/clo_assessment_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend development  
cd src/frontend
npm install
npm run dev
```

### 3. Deployment Process
```bash
# Production deployment
bash scripts/deployment/deploy_production.sh

# Staging deployment
bash scripts/deployment/deploy_staging.sh
```

### 4. Maintenance Tasks
```bash
# Backup database
bash scripts/maintenance/backup_database.sh

# Cleanup temporary files
bash scripts/maintenance/cleanup_temp_files.sh

# System health check
python scripts/maintenance/system_health_check.py
```

---

## 🎯 Lợi ích Cấu trúc

### 1. Tổ chức Rõ ràng
- **Phân tách rõ ràng**: Code, data, docs, logs tách biệt
- **Dễ tìm kiếm**: Mỗi loại file có thư mục riêng
- **Scalable**: Dễ mở rộng khi dự án phát triển

### 2. Bảo mật Tốt hơn
- **Phân quyền**: Mỗi thư mục có permission phù hợp
- **Backup**: Dữ liệu quan trọng được backup riêng
- **Logs**: Theo dõi hoạt động hệ thống

### 3. Maintenance Dễ dàng
- **Scripts**: Tự động hóa các tác vụ thường xuyên
- **Monitoring**: Logs tập trung và có tổ chức
- **Updates**: Dễ dàng cập nhật từng component

### 4. Development Hiệu quả
- **Separation of Concerns**: Frontend/Backend tách biệt
- **Testing**: Test cases có tổ chức rõ ràng
- **Documentation**: Tài liệu đầy đủ và dễ tìm

---

*Cấu trúc này được thiết kế để hỗ trợ phát triển, triển khai và bảo trì hệ thống CLO/PLO Assessment Platform một cách hiệu quả và chuyên nghiệp.*


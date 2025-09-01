# Hướng dẫn Cài đặt Chi tiết

## Nền tảng Đánh giá CLO/PLO - Khoa Cơ khí EAUT

---

## 📋 Mục lục

1. [Yêu cầu Hệ thống](#yêu-cầu-hệ-thống)
2. [Chuẩn bị Môi trường](#chuẩn-bị-môi-trường)
3. [Cài đặt Backend](#cài-đặt-backend)
4. [Cài đặt Frontend](#cài-đặt-frontend)
5. [Cấu hình AI Model](#cấu-hình-ai-model)
6. [Khởi động Hệ thống](#khởi-động-hệ-thống)
7. [Kiểm tra và Xác thực](#kiểm-tra-và-xác-thực)
8. [Troubleshooting](#troubleshooting)

---

## 🖥️ Yêu cầu Hệ thống

### Phần cứng Tối thiểu

| Thành phần | Tối thiểu | Khuyến nghị | Ghi chú |
|------------|-----------|-------------|---------|
| **CPU** | Intel Core i5-8400 / AMD Ryzen 5 2600 | Intel Core i7-10700K / AMD Ryzen 7 3700X | 8+ cores cho AI processing |
| **RAM** | 16GB DDR4 | 32GB DDR4 | Model AI cần 8-12GB RAM |
| **Storage** | 50GB SSD | 100GB NVMe SSD | Tốc độ đọc/ghi cao |
| **GPU** | Tùy chọn | NVIDIA RTX 3060 / RTX 4060 | Tăng tốc AI inference |
| **Network** | Không cần | Ethernet 1Gbps | Chỉ cho setup ban đầu |

### Hệ điều hành Hỗ trợ

#### Ubuntu Linux (Khuyến nghị)
- **Ubuntu 20.04 LTS** (Focal Fossa)
- **Ubuntu 22.04 LTS** (Jammy Jellyfish)
- **Ubuntu 24.04 LTS** (Noble Numbat)

#### Windows
- **Windows 10** (Build 19041+)
- **Windows 11** (All versions)
- **Windows Server 2019/2022**

#### macOS
- **macOS Big Sur** (11.0+)
- **macOS Monterey** (12.0+)
- **macOS Ventura** (13.0+)

---

## 🛠️ Chuẩn bị Môi trường

### Bước 1: Cập nhật Hệ thống

#### Ubuntu/Debian
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git build-essential
```

#### CentOS/RHEL/Fedora
```bash
sudo dnf update -y
sudo dnf install -y curl wget git gcc gcc-c++ make
```

#### Windows
```powershell
# Cài đặt Chocolatey package manager
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Cài đặt Git và các tools cần thiết
choco install git nodejs python -y
```

#### macOS
```bash
# Cài đặt Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cài đặt dependencies
brew install git node python@3.11
```

### Bước 2: Cài đặt Python 3.8+

#### Ubuntu/Debian
```bash
sudo apt install -y python3.11 python3.11-pip python3.11-venv python3.11-dev
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

#### Windows
```powershell
# Download và cài đặt Python từ python.org
# Hoặc sử dụng Microsoft Store
winget install Python.Python.3.11
```

#### macOS
```bash
brew install python@3.11
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Bước 3: Cài đặt Node.js 18+

#### Ubuntu/Debian
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### Windows
```powershell
choco install nodejs -y
# Hoặc download từ nodejs.org
```

#### macOS
```bash
brew install node@20
```

### Bước 4: Xác thực Cài đặt

```bash
# Kiểm tra Python version
python3 --version  # Should be 3.8+

# Kiểm tra pip
pip3 --version

# Kiểm tra Node.js
node --version     # Should be 18+
npm --version

# Kiểm tra Git
git --version
```

---

## 🔧 Cài đặt Backend

### Bước 1: Clone Repository

```bash
# Tạo thư mục dự án
mkdir -p ~/clo_plo_platform
cd ~/clo_plo_platform

# Clone source code (hoặc copy từ USB/local)
git clone https://github.com/eaut/clo-plo-platform.git .
# Hoặc nếu có source code local:
# cp -r /path/to/source/* .
```

### Bước 2: Tạo Python Virtual Environment

```bash
cd backend/clo_assessment_api

# Tạo virtual environment
python3 -m venv venv

# Kích hoạt virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### Bước 3: Cài đặt Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Cài đặt requirements
pip install -r requirements.txt

# Nếu gặp lỗi, cài đặt từng package:
pip install flask==2.3.3
pip install flask-sqlalchemy==3.0.5
pip install flask-cors==4.0.0
pip install pandas==2.0.3
pip install numpy==1.24.3
pip install scikit-learn==1.3.0
pip install transformers==4.33.2
pip install torch==2.0.1
pip install torchvision==0.15.2
pip install Pillow==10.0.0
pip install python-docx==0.8.11
pip install PyPDF2==3.0.1
pip install openpyxl==3.1.2
```

### Bước 4: Cấu hình Database

```bash
# Tạo thư mục logs
mkdir -p logs

# Khởi tạo database với dữ liệu mẫu
python import_data.py

# Kiểm tra database đã tạo
ls -la *.db
```

### Bước 5: Test Backend

```bash
# Khởi động backend server
python -m src.main

# Trong terminal khác, test API
curl http://localhost:5001/api/health
# Expected response: {"status": "healthy", "timestamp": "..."}
```

---

## 🎨 Cài đặt Frontend

### Bước 1: Cài đặt Dependencies

```bash
cd ../../frontend

# Cài đặt npm packages
npm install

# Nếu gặp lỗi, thử:
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Bước 2: Cấu hình Environment

```bash
# Tạo file .env.local
cat > .env.local << EOF
VITE_API_BASE_URL=http://localhost:5001/api
VITE_APP_TITLE=Nền tảng đánh giá CLO/PLO - EAUT
VITE_APP_VERSION=1.0.0
EOF
```

### Bước 3: Build và Test Frontend

```bash
# Development mode
npm run dev

# Production build (tùy chọn)
npm run build
npm run preview
```

### Bước 4: Xác thực Frontend

Mở trình duyệt và truy cập:
- **Development**: http://localhost:5174
- **Production**: http://localhost:4173

---

## 🧠 Cấu hình AI Model

### Bước 1: Tạo thư mục Model

```bash
cd backend/clo_assessment_api
mkdir -p models/erax-vl-7b-v1.5
```

### Bước 2: Tải Model Files

#### Phương pháp 1: Hugging Face Hub (Cần Internet)
```bash
pip install huggingface_hub

python << EOF
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="EraX-VL-7B-V1.5",
    local_dir="./models/erax-vl-7b-v1.5",
    local_dir_use_symlinks=False
)
EOF
```

#### Phương pháp 2: Manual Download (Offline)
```bash
# Nếu có model files từ USB/local storage
cp -r /path/to/erax-vl-7b-v1.5/* ./models/erax-vl-7b-v1.5/

# Cấu trúc thư mục cần có:
# models/erax-vl-7b-v1.5/
# ├── config.json
# ├── pytorch_model.bin (hoặc model.safetensors)
# ├── tokenizer.json
# ├── tokenizer_config.json
# └── vocab.txt
```

### Bước 3: Test AI Model

```bash
python << EOF
import sys
sys.path.append('src')
from ai_integration import AIProcessor

try:
    ai = AIProcessor()
    print("✅ AI Model loaded successfully!")
    
    # Test inference
    result = ai.assess_document_content(
        "Sinh viên hiểu rõ các nguyên lý cơ học và có thể áp dụng vào thực tế.",
        ["cơ học", "nguyên lý", "áp dụng"],
        "presence"
    )
    print(f"✅ Test assessment score: {result}")
    
except Exception as e:
    print(f"❌ AI Model error: {e}")
EOF
```

### Bước 4: Cấu hình GPU (Tùy chọn)

#### Kiểm tra CUDA
```bash
nvidia-smi
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

#### Cấu hình GPU trong config
```python
# Sửa file src/config.py
AI_MODEL_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
AI_BATCH_SIZE = 8 if torch.cuda.is_available() else 2
```

---

## 🚀 Khởi động Hệ thống

### Phương pháp 1: Manual Start

#### Terminal 1 - Backend
```bash
cd backend/clo_assessment_api
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
python -m src.main
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

### Phương pháp 2: Script Automation

#### Linux/macOS
```bash
# Tạo script khởi động
cat > start_platform.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting CLO/PLO Assessment Platform..."

# Start backend
cd backend/clo_assessment_api
source venv/bin/activate
python -m src.main &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
cd ../../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Platform started!"
echo "📊 Dashboard: http://localhost:5174"
echo "🔧 API: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF

chmod +x start_platform.sh
./start_platform.sh
```

#### Windows PowerShell
```powershell
# Tạo script start_platform.ps1
@"
Write-Host "🚀 Starting CLO/PLO Assessment Platform..." -ForegroundColor Green

# Start backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend\clo_assessment_api; .\venv\Scripts\activate; python -m src.main"

# Wait for backend
Start-Sleep -Seconds 5

# Start frontend  
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "✅ Platform started!" -ForegroundColor Green
Write-Host "📊 Dashboard: http://localhost:5174" -ForegroundColor Cyan
Write-Host "🔧 API: http://localhost:5001" -ForegroundColor Cyan
"@ | Out-File -FilePath start_platform.ps1

.\start_platform.ps1
```

### Phương pháp 3: Docker Compose (Advanced)

```bash
# Tạo docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5001:5001"
    volumes:
      - ./backend/clo_assessment_api:/app
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
      - AI_MODEL_DEVICE=cpu
    
  frontend:
    build: ./frontend
    ports:
      - "5174:5174"
    depends_on:
      - backend
    environment:
      - VITE_API_BASE_URL=http://localhost:5001/api

volumes:
  data:
EOF

# Khởi động với Docker
docker-compose up -d
```

---

## ✅ Kiểm tra và Xác thực

### Bước 1: Health Check

```bash
# Kiểm tra backend API
curl -s http://localhost:5001/api/health | jq .

# Expected output:
# {
#   "status": "healthy",
#   "timestamp": "2025-08-31T16:00:00Z",
#   "version": "1.0.0"
# }
```

### Bước 2: Database Verification

```bash
cd backend/clo_assessment_api

# Kiểm tra database
python << EOF
from src.models.database import db
from src.models.plo import PLO
from src.models.clo import CLO

# Count records
plo_count = PLO.query.count()
clo_count = CLO.query.count()

print(f"✅ PLOs in database: {plo_count}")
print(f"✅ CLOs in database: {clo_count}")

if plo_count >= 5 and clo_count >= 4:
    print("✅ Database verification passed!")
else:
    print("❌ Database verification failed!")
EOF
```

### Bước 3: Frontend Verification

Mở trình duyệt và kiểm tra:

1. **Dashboard Load**: http://localhost:5174
   - ✅ Trang chính hiển thị
   - ✅ Stats cards hiển thị số liệu
   - ✅ Biểu đồ render thành công

2. **API Connection**: 
   - ✅ Badge "API kết nối" màu xanh
   - ✅ Không có alert lỗi kết nối

3. **Navigation**:
   - ✅ Tab PLO hiển thị danh sách
   - ✅ Tab CLO hiển thị danh sách
   - ✅ Tab Upload hoạt động
   - ✅ Tab Results hiển thị

### Bước 4: End-to-End Test

```bash
# Test upload và assessment
curl -X POST http://localhost:5001/api/assessments/upload \
  -F "file=@test_document.pdf" \
  -F "course_code=ME2252" \
  -F "document_type=assignment"

# Kiểm tra response
# Expected: {"status": "success", "assessment_id": "..."}
```

---

## 🔧 Troubleshooting

### Lỗi Backend

#### 1. Port 5001 đã được sử dụng
```bash
# Tìm process đang sử dụng port
sudo netstat -tulpn | grep 5001
# hoặc
sudo lsof -i :5001

# Kill process
sudo kill -9 <PID>

# Hoặc đổi port trong config
# Sửa src/config.py: API_PORT = 5002
```

#### 2. Import Error - Module not found
```bash
# Kiểm tra virtual environment
which python
pip list

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Kiểm tra PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

#### 3. Database Error
```bash
# Xóa và tạo lại database
rm *.db
python import_data.py

# Kiểm tra permissions
chmod 664 *.db
```

#### 4. AI Model Loading Error
```bash
# Kiểm tra model files
ls -la models/erax-vl-7b-v1.5/

# Test model loading
python -c "
import torch
from transformers import AutoModel
model = AutoModel.from_pretrained('./models/erax-vl-7b-v1.5')
print('Model loaded successfully!')
"

# Nếu thiếu VRAM, sử dụng CPU
# Sửa config: AI_MODEL_DEVICE = "cpu"
```

### Lỗi Frontend

#### 1. npm install fails
```bash
# Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json

# Update npm
npm install -g npm@latest

# Reinstall
npm install
```

#### 2. Vite build error
```bash
# Kiểm tra Node.js version
node --version  # Should be 18+

# Update Node.js nếu cần
# Ubuntu: sudo apt install nodejs
# Windows: choco upgrade nodejs
# macOS: brew upgrade node
```

#### 3. API Connection Error
```bash
# Kiểm tra backend đang chạy
curl http://localhost:5001/api/health

# Kiểm tra CORS settings
# Sửa backend/src/main.py:
# CORS(app, origins=["http://localhost:5174"])
```

### Lỗi System

#### 1. Insufficient Memory
```bash
# Kiểm tra RAM usage
free -h
htop

# Giảm AI batch size
# Sửa config: AI_BATCH_SIZE = 1

# Enable swap nếu cần
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 2. Disk Space
```bash
# Kiểm tra disk usage
df -h

# Clean up
sudo apt autoremove
docker system prune -a  # Nếu dùng Docker
```

#### 3. Permission Issues
```bash
# Fix ownership
sudo chown -R $USER:$USER ~/clo_plo_platform

# Fix permissions
chmod -R 755 ~/clo_plo_platform
chmod -R 644 ~/clo_plo_platform/**/*.py
```

---

## 📋 Checklist Cài đặt

### Pre-installation
- [ ] Kiểm tra yêu cầu phần cứng
- [ ] Cài đặt Python 3.8+
- [ ] Cài đặt Node.js 18+
- [ ] Cài đặt Git
- [ ] Tạo thư mục dự án

### Backend Setup
- [ ] Clone/copy source code
- [ ] Tạo Python virtual environment
- [ ] Cài đặt dependencies
- [ ] Khởi tạo database
- [ ] Test backend API

### Frontend Setup
- [ ] Cài đặt npm dependencies
- [ ] Cấu hình environment variables
- [ ] Test development server
- [ ] Verify API connection

### AI Model Setup
- [ ] Tạo thư mục models
- [ ] Tải model files
- [ ] Test model loading
- [ ] Cấu hình GPU (nếu có)

### Final Verification
- [ ] Health check API
- [ ] Database verification
- [ ] Frontend functionality
- [ ] End-to-end test
- [ ] Performance check

### Documentation
- [ ] Đọc README.md
- [ ] Lưu thông tin cấu hình
- [ ] Backup database
- [ ] Tạo script khởi động

---

## 📞 Hỗ trợ Cài đặt

Nếu gặp vấn đề trong quá trình cài đặt:

1. **Kiểm tra log files**: `logs/backend.log`, browser console
2. **Tham khảo troubleshooting**: Phần trên
3. **Liên hệ support**: support@eaut.edu.vn
4. **GitHub Issues**: https://github.com/eaut/clo-plo-platform/issues

---

*Hướng dẫn này được cập nhật thường xuyên. Phiên bản mới nhất có tại repository chính thức.*


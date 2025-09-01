# CLO/PLO Assessment Platform - Ready to Run

## 🚀 Quick Start

### Windows
1. Run `install.py` to install dependencies
2. Run `start_windows.bat` to start the platform

### Linux/macOS
1. Run `python3 install.py` to install dependencies
2. Run `./start_unix.sh` to start the platform

## 📋 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB available space
- **OS**: Windows 10+, Ubuntu 20.04+, macOS 10.15+

## 🌐 Access Points

After starting the platform:

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:5001
- **API Documentation**: http://localhost:5001/api/health

## 📁 Directory Structure

```
clo_plo_assessment_platform/
├── backend/                 # Backend API server
├── frontend/               # Frontend web application
├── models/                 # AI models and checkpoints
├── data/                   # Configuration data
├── training_data/          # Training datasets
├── docs/                   # Documentation
├── install.py              # Installation script
├── start_windows.bat       # Windows startup
├── start_unix.sh          # Linux/macOS startup
└── README.md              # This file
```

## 🔧 Manual Installation

If automatic installation fails:

### Backend
```bash
cd backend/clo_assessment_api
pip install -r requirements.txt
python src/enhanced_api.py
```

### Frontend (Development)
```bash
cd frontend
npm install
npm run dev
```

### Frontend (Production)
The built frontend is already included. For development:
```bash
cd src/frontend
npm install
npm run build
```

## 📊 Features

- ✅ **CLO/PLO Management**: Complete CRUD operations
- ✅ **AI Assessment**: Automated scoring with 88%+ accuracy
- ✅ **Document Processing**: Support for DOCX, PDF, TXT
- ✅ **Analytics Dashboard**: Real-time visualization
- ✅ **Batch Processing**: Multiple document assessment
- ✅ **Export/Import**: JSON, CSV, Excel formats
- ✅ **User Management**: Authentication and authorization
- ✅ **Mobile Responsive**: Works on all devices

## 🤖 AI Models

The platform includes pre-trained models:
- **Score Prediction**: 88.34% R² accuracy
- **Bloom Classification**: 83.24% accuracy
- **Keyword Models**: 194 CLO-specific models

## 📚 Documentation

- **User Manual**: `docs/user_manual.md`
- **Installation Guide**: `docs/installation_guide.md`
- **API Documentation**: `docs/api_documentation.md`
- **Troubleshooting**: `docs/troubleshooting.md`

## 🆘 Support

For support and issues:
- **Email**: support@eaut.edu.vn
- **Documentation**: Check `docs/` directory
- **Logs**: Check `logs/` directory for error details

## 📄 License

Developed for Khoa Cơ khí, Trường Đại học Công nghệ Đông Á (EAUT)

---

**Version**: 1.0.0  
**Build Date**: 2025-08-31 15:01:25  
**Platform**: Ready-to-run distribution

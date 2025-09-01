#!/usr/bin/env python3
"""
CLO/PLO Assessment Platform Installer
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_requirements():
    """Check system requirements"""
    print("Checking system requirements...")
    
    # Check Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    else:
        print(f"✅ Python {sys.version.split()[0]} found")
    
    # Check pip
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip found")
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        return False
    
    # Check Node.js (optional)
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        print("✅ Node.js found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Node.js not found (optional for development)")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    
    requirements_file = Path("backend/clo_assessment_api/requirements.txt")
    if requirements_file.exists():
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    else:
        print("❌ Requirements file not found")
        return False

def setup_database():
    """Setup database"""
    print("Setting up database...")
    
    # Create necessary directories
    dirs_to_create = [
        "logs",
        "uploads",
        "exports",
        "backups"
    ]
    
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Created directory: {dir_name}")
    
    return True

def main():
    """Main installer function"""
    print("=" * 50)
    print("CLO/PLO Assessment Platform Installer")
    print("=" * 50)
    
    if not check_requirements():
        print("❌ System requirements not met")
        sys.exit(1)
    
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    if not setup_database():
        print("❌ Failed to setup database")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Installation completed successfully!")
    print("=" * 50)
    print("\nTo start the platform:")
    
    if platform.system() == "Windows":
        print("  Run: start_windows.bat")
    else:
        print("  Run: ./start_unix.sh")
    
    print("\nThen open your browser to:")
    print("  Frontend: http://localhost:3000")
    print("  Backend API: http://localhost:5001")

if __name__ == "__main__":
    main()

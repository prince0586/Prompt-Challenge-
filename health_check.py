#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Health check script for Mandi-Setu application.
Verifies all components are working correctly.
"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows compatibility
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def check_imports():
    """Check if all required imports work."""
    print("🔍 Checking imports...")
    
    try:
        from config.settings import get_config, AppConfig
        print("  ✓ Config module")
        
        from mandi_setu.theme.theme_manager import apply_viksit_bharat_theme
        print("  ✓ Theme module")
        
        import streamlit as st
        print("  ✓ Streamlit")
        
        from dotenv import load_dotenv
        print("  ✓ Python-dotenv")
        
        from pydantic import BaseModel
        print("  ✓ Pydantic")
        
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def check_configuration():
    """Check if configuration loads correctly."""
    print("\n⚙️  Checking configuration...")
    
    try:
        from config.settings import get_config
        config = get_config()
        
        print(f"  ✓ App name: {config.app_name}")
        print(f"  ✓ Version: {config.version}")
        print(f"  ✓ Environment: {config.environment}")
        print(f"  ✓ Debug mode: {config.debug_mode}")
        
        # Check if .env file exists
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            print("  ✓ .env file found")
        else:
            print("  ⚠️  .env file not found (using defaults)")
        
        return True
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False

def check_theme():
    """Check if theme components work."""
    print("\n🎨 Checking theme...")
    
    try:
        from mandi_setu.theme.theme_manager import get_viksit_bharat_css, get_theme_colors
        
        css = get_viksit_bharat_css()
        colors = get_theme_colors()
        
        print(f"  ✓ CSS generated ({len(css)} characters)")
        print(f"  ✓ Theme colors loaded ({len(colors)} colors)")
        
        return True
    except Exception as e:
        print(f"  ❌ Theme error: {e}")
        return False

def check_file_structure():
    """Check if required files and directories exist."""
    print("\n📁 Checking file structure...")
    
    base_path = Path(__file__).parent
    required_paths = [
        "app.py",
        "config/settings.py",
        "src/mandi_setu/theme/theme_manager.py",
        "requirements.txt",
        ".env"
    ]
    
    all_exist = True
    for path in required_paths:
        full_path = base_path / path
        if full_path.exists():
            print(f"  ✓ {path}")
        else:
            print(f"  ❌ {path} (missing)")
            all_exist = False
    
    return all_exist

def main():
    """Run all health checks."""
    print("🏥 Mandi-Setu Health Check")
    print("=" * 40)
    
    checks = [
        ("Imports", check_imports),
        ("Configuration", check_configuration),
        ("Theme", check_theme),
        ("File Structure", check_file_structure)
    ]
    
    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))
    
    print("\n📊 Summary:")
    print("-" * 20)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All checks passed! Application is ready to run.")
        print("\nTo start the application:")
        print("  python -m streamlit run app.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
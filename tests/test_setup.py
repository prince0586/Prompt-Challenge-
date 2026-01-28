"""
Basic setup tests for Mandi-Setu application.
Verifies that the core infrastructure is properly configured.
"""

import pytest
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from config.settings import AppConfig, get_config, get_database_config, get_ai_config


class TestProjectSetup:
    """Test basic project setup and configuration."""
    
    def test_config_loading(self):
        """Test that configuration loads without errors."""
        config = AppConfig()
        assert config is not None
        assert config.app_name == "Mandi-Setu"
        assert config.version == "1.0.0"
    
    def test_database_config(self):
        """Test database configuration."""
        db_config = get_database_config()
        assert db_config is not None
        assert db_config.sqlite_path == "data/mandi_setu.db"
        assert db_config.dynamodb_table_name == "mandi-setu-parchis"
    
    def test_ai_config(self):
        """Test AI configuration."""
        ai_config = get_ai_config()
        assert ai_config is not None
        assert ai_config.gemini_model == "gemini-1.5-flash"
        assert "hi" in ai_config.supported_languages
        assert "en" in ai_config.supported_languages
    
    def test_supported_languages(self):
        """Test that all required languages are supported."""
        ai_config = get_ai_config()
        required_languages = ["hi", "ta", "te", "bn", "mr", "gu", "en"]
        
        for lang in required_languages:
            assert lang in ai_config.supported_languages
    
    def test_environment_detection(self):
        """Test environment detection methods."""
        config = AppConfig()
        
        # Default should be development
        assert config.environment == "development"
        assert config.is_development()
        assert not config.is_production()
    
    def test_config_to_dict(self):
        """Test configuration serialization."""
        config = AppConfig()
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert "app_name" in config_dict
        assert "database" in config_dict
        assert "ai" in config_dict
        assert "ui" in config_dict
        assert "performance" in config_dict


class TestThemeManager:
    """Test theme manager functionality."""
    
    def test_theme_colors(self):
        """Test that theme colors are properly defined."""
        from src.mandi_setu.theme.theme_manager import get_theme_colors
        
        colors = get_theme_colors()
        assert colors['saffron'] == '#FF9933'
        assert colors['green'] == '#138808'
        assert colors['white'] == '#FFFFFF'
    
    def test_css_generation(self):
        """Test CSS generation."""
        from src.mandi_setu.theme.theme_manager import get_viksit_bharat_css
        
        css = get_viksit_bharat_css()
        assert isinstance(css, str)
        assert '--saffron-color: #FF9933' in css
        assert '--green-color: #138808' in css
        assert 'Noto Sans Devanagari' in css


class TestDirectoryStructure:
    """Test that the project directory structure is correct."""
    
    def test_required_directories_exist(self):
        """Test that all required directories exist."""
        base_path = Path(__file__).parent.parent
        
        required_dirs = [
            "src/mandi_setu/components",
            "src/mandi_setu/models", 
            "src/mandi_setu/database",
            "src/mandi_setu/voice",
            "src/mandi_setu/ai",
            "src/mandi_setu/theme",
            "config",
            "tests",
            "data"
        ]
        
        for dir_path in required_dirs:
            full_path = base_path / dir_path
            assert full_path.exists(), f"Directory {dir_path} does not exist"
            assert full_path.is_dir(), f"{dir_path} is not a directory"
    
    def test_init_files_exist(self):
        """Test that __init__.py files exist in Python packages."""
        base_path = Path(__file__).parent.parent
        
        init_files = [
            "src/__init__.py",
            "src/mandi_setu/__init__.py",
            "src/mandi_setu/components/__init__.py",
            "src/mandi_setu/models/__init__.py",
            "src/mandi_setu/database/__init__.py",
            "src/mandi_setu/voice/__init__.py",
            "src/mandi_setu/ai/__init__.py",
            "src/mandi_setu/theme/__init__.py",
            "config/__init__.py",
            "tests/__init__.py"
        ]
        
        for init_file in init_files:
            full_path = base_path / init_file
            assert full_path.exists(), f"Init file {init_file} does not exist"
    
    def test_main_files_exist(self):
        """Test that main application files exist."""
        base_path = Path(__file__).parent.parent
        
        main_files = [
            "app.py",
            "requirements.txt",
            "README.md",
            ".env.template",
            "config/settings.py",
            "src/mandi_setu/theme/theme_manager.py"
        ]
        
        for file_path in main_files:
            full_path = base_path / file_path
            assert full_path.exists(), f"File {file_path} does not exist"
            assert full_path.is_file(), f"{file_path} is not a file"


if __name__ == "__main__":
    pytest.main([__file__])
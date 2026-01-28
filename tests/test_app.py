"""
Test suite for AgriTrade Pro main application.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path for testing
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import streamlit as st
from config.settings import get_config
from mandi_setu.ui.language_manager import language_manager


class TestAppConfiguration:
    """Test application configuration and setup."""
    
    def test_config_loading(self):
        """Test that configuration loads correctly."""
        config = get_config()
        assert config is not None
        assert config.app_name == "AgriTrade Pro"
        assert config.version == "1.0.0"
    
    def test_supported_languages(self):
        """Test that all supported languages are available."""
        config = get_config()
        expected_languages = ["hi", "ta", "te", "bn", "mr", "gu", "en"]
        assert set(config.ai.supported_languages) == set(expected_languages)


class TestLanguageManager:
    """Test language management functionality."""
    
    def test_language_options(self):
        """Test that language options are properly configured."""
        options = language_manager.get_language_options()
        assert len(options) == 7  # 7 supported languages
        assert "English" in options
        assert "हिंदी (Hindi)" in options
    
    def test_text_translation(self):
        """Test text translation functionality."""
        # Test English translation
        text = language_manager.get_text("app_title", "en")
        assert "AgriTrade Pro" in text
        
        # Test Hindi translation
        text = language_manager.get_text("app_title", "hi")
        assert "एग्रीट्रेड प्रो" in text
    
    def test_fallback_translation(self):
        """Test fallback behavior for missing translations."""
        # Test with non-existent key
        text = language_manager.get_text("non_existent_key", "en")
        assert text == "non_existent_key"
        
        # Test with non-existent language
        text = language_manager.get_text("app_title", "xx")
        assert "AgriTrade Pro" in text  # Should fallback to English


class TestSessionState:
    """Test session state management."""
    
    def test_session_state_initialization(self):
        """Test that session state is properly initialized."""
        from app import initialize_session_state
        
        # Create a mock session state that behaves like Streamlit's
        class MockSessionState:
            def __init__(self):
                self._data = {}
            
            def __contains__(self, key):
                return key in self._data
            
            def __getitem__(self, key):
                return self._data[key]
            
            def __setitem__(self, key, value):
                self._data[key] = value
            
            def __getattr__(self, key):
                if key.startswith('_'):
                    return object.__getattribute__(self, key)
                return self._data.get(key)
            
            def __setattr__(self, key, value):
                if key.startswith('_'):
                    object.__setattr__(self, key, value)
                else:
                    self._data[key] = value
            
            def get(self, key, default=None):
                return self._data.get(key, default)
        
        # Mock streamlit session state
        mock_session = MockSessionState()
        
        with patch('streamlit.session_state', mock_session):
            with patch('app.st.session_state', mock_session):
                initialize_session_state()
                
                # Check required session state variables
                assert 'config' in mock_session
                assert 'negotiation_active' in mock_session
                assert 'conversation_history' in mock_session
                assert 'trade_ledger' in mock_session
                assert 'current_language' in mock_session
                assert 'recording_status' in mock_session
                assert 'current_trade_data' in mock_session
                
                # Check default values
                assert mock_session.negotiation_active is False
                assert mock_session.conversation_history == []
                assert mock_session.trade_ledger == []
                assert mock_session.recording_status == "idle"


class TestTradeDataGeneration:
    """Test trade data generation functionality."""
    
    @patch('streamlit.session_state')
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    def test_add_sample_trade_data(self, mock_rerun, mock_success, mock_session):
        """Test sample trade data generation."""
        from app import add_sample_trade_data
        
        # Setup mock session state
        mock_session.trade_ledger = []
        mock_session.current_language = "en"
        
        # Call function
        add_sample_trade_data()
        
        # Verify trade was added
        assert len(mock_session.trade_ledger) == 1
        trade = mock_session.trade_ledger[0]
        
        # Check trade structure
        assert 'product_name' in trade
        assert 'quantity' in trade
        assert 'unit' in trade
        assert 'unit_price' in trade
        assert 'total_amount' in trade
        assert 'mandi_cess' in trade
        assert 'timestamp' in trade
        assert 'language' in trade
        
        # Check calculations
        expected_total = trade['quantity'] * trade['unit_price']
        assert trade['total_amount'] == expected_total
        assert trade['mandi_cess'] == int(expected_total * 0.05)


class TestVoiceSimulation:
    """Test voice simulation functionality."""
    
    @patch('streamlit.session_state')
    def test_voice_command_processing(self, mock_session):
        """Test voice command processing simulation."""
        from app import simulate_voice_processing
        
        # Setup mock session state
        mock_session.voice_response = None
        
        # Test potato command
        simulate_voice_processing("Potato 50 kg at 25 rupees per kg")
        
        assert mock_session.voice_response is not None
        assert "Potato" in mock_session.voice_response
        assert "50 kg" in mock_session.voice_response
        assert "₹25/kg" in mock_session.voice_response
    
    @patch('streamlit.session_state')
    def test_price_query_processing(self, mock_session):
        """Test price query processing."""
        from app import simulate_voice_processing
        
        # Setup mock session state
        mock_session.voice_response = None
        
        # Test price query
        simulate_voice_processing("What is the current rice price?")
        
        assert mock_session.voice_response is not None
        assert "Market Prices" in mock_session.voice_response
        assert "₹" in mock_session.voice_response


class TestAnalytics:
    """Test analytics functionality."""
    
    @patch('streamlit.session_state')
    def test_analytics_calculation(self, mock_session):
        """Test analytics calculations."""
        # Setup mock trade data
        mock_session.trade_ledger = [
            {
                'product_name': 'Potato',
                'quantity': 50,
                'unit_price': 25,
                'total_amount': 1250,
                'mandi_cess': 62
            },
            {
                'product_name': 'Tomato',
                'quantity': 30,
                'unit_price': 35,
                'total_amount': 1050,
                'mandi_cess': 52
            }
        ]
        
        # Calculate expected values
        total_trades = len(mock_session.trade_ledger)
        total_value = sum(trade['total_amount'] for trade in mock_session.trade_ledger)
        total_cess = sum(trade['mandi_cess'] for trade in mock_session.trade_ledger)
        avg_trade_value = total_value / total_trades
        
        assert total_trades == 2
        assert total_value == 2300
        assert total_cess == 114
        assert avg_trade_value == 1150


class TestUIComponents:
    """Test UI component rendering."""
    
    @patch('streamlit.markdown')
    def test_header_rendering(self, mock_markdown):
        """Test header component rendering."""
        from app import render_header
        
        # Mock session state
        with patch('streamlit.session_state') as mock_session:
            mock_session.trade_ledger = []
            mock_session.conversation_history = []
            
            render_header()
            
            # Verify markdown was called (header was rendered)
            assert mock_markdown.called
    
    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    def test_market_insights_rendering(self, mock_columns, mock_markdown):
        """Test market insights panel rendering."""
        from app import render_market_insights
        
        render_market_insights()
        
        # Verify components were rendered
        assert mock_markdown.called


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_empty_trade_ledger(self):
        """Test behavior with empty trade ledger."""
        with patch('streamlit.session_state') as mock_session:
            mock_session.trade_ledger = []
            
            # Should not raise any errors
            from app import render_trade_ledger_main
            render_trade_ledger_main()
    
    def test_invalid_language_code(self):
        """Test handling of invalid language codes."""
        text = language_manager.get_text("app_title", "invalid_lang")
        # Should fallback to English
        assert "AgriTrade Pro" in text


class TestPerformance:
    """Test performance-related functionality."""
    
    def test_large_trade_ledger_performance(self):
        """Test performance with large number of trades."""
        import time
        
        # Create large trade ledger
        large_ledger = []
        for i in range(1000):
            large_ledger.append({
                'product_name': f'Product_{i}',
                'quantity': 50,
                'unit_price': 25,
                'total_amount': 1250,
                'mandi_cess': 62,
                'timestamp': '2024-01-26 14:30:00'
            })
        
        with patch('streamlit.session_state') as mock_session:
            mock_session.trade_ledger = large_ledger
            
            start_time = time.time()
            
            # Test analytics calculation
            total_value = sum(trade['total_amount'] for trade in mock_session.trade_ledger)
            
            end_time = time.time()
            
            # Should complete quickly (less than 1 second)
            assert end_time - start_time < 1.0
            assert total_value == 1250000  # 1000 * 1250


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
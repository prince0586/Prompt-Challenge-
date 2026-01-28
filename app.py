"""
AgriTrade Pro: Main Streamlit Application

A multilingual AI assistant for agricultural market vendors in India.
Supports voice-based negotiations, automatic data extraction, and digital documentation.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from config.settings import get_config, AppConfig
from mandi_setu.theme.theme_manager import apply_viksit_bharat_theme
from mandi_setu.ui.language_manager import language_manager


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    
    # Configuration
    if 'config' not in st.session_state:
        st.session_state.config = get_config()
    
    # Application state
    if 'negotiation_active' not in st.session_state:
        st.session_state.negotiation_active = False
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'trade_ledger' not in st.session_state:
        st.session_state.trade_ledger = []
    
    if 'current_language' not in st.session_state:
        st.session_state.current_language = st.session_state.config.ai.default_language
    
    # Voice interface state
    if 'recording_status' not in st.session_state:
        st.session_state.recording_status = "idle"  # idle, recording, processing
    
    # Current negotiation data
    if 'current_trade_data' not in st.session_state:
        st.session_state.current_trade_data = None


def render_header():
    """Render the application header with branding."""
    
    st.markdown(f"""
    <div class="header-container">
        <div class="hero-stats">
            <div class="stat-item">
                <div class="stat-number">₹{sum(trade.get('total_amount', 0) for trade in st.session_state.trade_ledger):,}</div>
                <div class="stat-label">Total Trade Value</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{len(st.session_state.trade_ledger)}</div>
                <div class="stat-label">Active Trades</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{len(st.session_state.conversation_history)}</div>
                <div class="stat-label">Conversations</div>
            </div>
        </div>
        <h1 class="app-title" data-text="{language_manager.get_text('app_title')}">{language_manager.get_text('app_title')}</h1>
        <p class="app-subtitle">{language_manager.get_text('app_subtitle')}</p>
        <div class="feature-badges">
            <span class="badge">🎤 Voice AI</span>
            <span class="badge">🌐 7 Languages</span>
            <span class="badge">📊 Real-time Analytics</span>
            <span class="badge">🔒 Secure Trading</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_main_interface():
    """Render the main user interface with advanced top-down layout and animations."""
    
    # Trade Negotiation Section (Top) with advanced container
    st.markdown("""
    <div class="main-section-container" data-section="negotiation">
        <div class="section-badge">🎯 Trade Negotiation Hub</div>
        <div class="section-glow"></div>
    </div>
    """, unsafe_allow_html=True)
    
    render_negotiation_interface()
    render_advanced_features()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Animated separator
    st.markdown("""
    <div class="section-separator">
        <div class="separator-line"></div>
        <div class="separator-icon">⚡</div>
        <div class="separator-line"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Trade Ledger Section (Bottom) with advanced container
    st.markdown("""
    <div class="main-section-container" data-section="ledger">
        <div class="section-badge">📊 Trade Analytics Dashboard</div>
        <div class="section-glow"></div>
    </div>
    """, unsafe_allow_html=True)
    
    render_trade_ledger_main()
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_advanced_features():
    """Render advanced AI features panel."""
    
    st.markdown("""
    <div class="advanced-features-panel">
        <h3>🚀 Advanced AI Features</h3>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-content">
                    <div class="feature-title">Price Prediction</div>
                    <div class="feature-desc">AI-powered market forecasting</div>
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-content">
                    <div class="feature-title">Market Analysis</div>
                    <div class="feature-desc">Real-time trend analysis</div>
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-content">
                    <div class="feature-title">Smart Negotiation</div>
                    <div class="feature-desc">AI-assisted deal optimization</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Advanced feature buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Price Prediction", type="secondary", use_container_width=True):
            show_price_prediction()
    
    with col2:
        if st.button("📈 Market Trends", type="secondary", use_container_width=True):
            show_market_trends()
    
    with col3:
        if st.button("🎤 Voice Simulation", type="secondary", use_container_width=True):
            simulate_voice_interaction()


def show_price_prediction():
    """Show AI-powered price prediction using full available space."""
    
    st.markdown("""
    <div class="feature-fullscreen">
        <div class="feature-header-full">
            <h2>🎯 AI Price Prediction Engine</h2>
            <p>Advanced market forecasting with machine learning algorithms</p>
            <div class="ai-status-badge-full">ACTIVE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate price predictions
    import random
    
    products = ['Potato', 'Tomato', 'Onion', 'Rice', 'Wheat', 'Carrot', 'Cabbage', 'Cauliflower']
    
    st.markdown("### 📊 Next 7 Days Price Forecast")
    
    # Create full-width prediction table
    st.markdown("""
    <div class="prediction-table">
        <div class="prediction-header-row">
            <div class="pred-product">Product</div>
            <div class="pred-current">Current Price</div>
            <div class="pred-predicted">Predicted Price</div>
            <div class="pred-change">Change</div>
            <div class="pred-confidence">Confidence</div>
            <div class="pred-recommendation">Recommendation</div>
        </div>
    """, unsafe_allow_html=True)
    
    for product in products:
        current_price = random.randint(18, 45)
        predicted_change = random.uniform(-15, 20)
        predicted_price = current_price + predicted_change
        confidence = random.uniform(75, 95)
        
        trend_class = "positive" if predicted_change > 0 else "negative" if predicted_change < 0 else "neutral"
        confidence_class = "high" if confidence > 85 else "medium" if confidence > 75 else "low"
        
        recommendation = "BUY" if predicted_change > 10 else "SELL" if predicted_change < -5 else "HOLD"
        rec_class = "buy" if recommendation == "BUY" else "sell" if recommendation == "SELL" else "hold"
        
        st.markdown(f"""
        <div class="prediction-row">
            <div class="pred-product">🥔 <strong>{product}</strong></div>
            <div class="pred-current">₹{current_price}/kg</div>
            <div class="pred-predicted">₹{predicted_price:.0f}/kg</div>
            <div class="pred-change {trend_class}">{predicted_change:+.1f}%</div>
            <div class="pred-confidence {confidence_class}">{confidence:.0f}%</div>
            <div class="pred-recommendation {rec_class}">{recommendation}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # AI Insights section
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="ai-insights-panel">
            <h4>🤖 AI Market Analysis</h4>
            <ul class="ai-insights-list">
                <li><strong>Bullish Trend:</strong> Potato and Rice showing strong upward momentum</li>
                <li><strong>Market Volatility:</strong> Tomato prices experiencing high fluctuation</li>
                <li><strong>Seasonal Impact:</strong> Winter vegetables showing price stability</li>
                <li><strong>Export Demand:</strong> Rice prices driven by international orders</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="trading-strategy-panel">
            <h4>💡 Recommended Trading Strategy</h4>
            <ul class="strategy-list">
                <li><strong>Focus Products:</strong> Potato and Rice for maximum profit</li>
                <li><strong>Timing:</strong> Buy early morning, sell by afternoon</li>
                <li><strong>Quantity:</strong> Bulk orders (50kg+) for better margins</li>
                <li><strong>Risk Management:</strong> Diversify across 3-4 products</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


def show_market_trends():
    """Show market trends analysis using full available space."""
    
    st.markdown("""
    <div class="feature-fullscreen">
        <div class="feature-header-full">
            <h2>📈 Real-time Market Trends</h2>
            <p>Live market analysis with trend indicators and alerts</p>
            <div class="update-badge-full">Updated: 2 minutes ago</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Market trend indicators in full width
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="trend-section trending-up-section">
            <h3>🔥 Trending Up</h3>
        """, unsafe_allow_html=True)
        
        trending_up = [
            {"product": "Potato", "change": "+12%", "reason": "High demand in Delhi", "volume": "2,500 tons"},
            {"product": "Rice", "change": "+8%", "reason": "Export orders increase", "volume": "1,800 tons"},
            {"product": "Wheat", "change": "+5%", "reason": "Seasonal shortage", "volume": "3,200 tons"},
            {"product": "Carrot", "change": "+3%", "reason": "Winter demand peak", "volume": "800 tons"}
        ]
        
        for item in trending_up:
            st.markdown(f"""
            <div class="trend-item-full trending-up">
                <div class="trend-product-name">🥔 {item['product']}</div>
                <div class="trend-change-value">{item['change']}</div>
                <div class="trend-reason-text">{item['reason']}</div>
                <div class="trend-volume">Volume: {item['volume']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="trend-section trending-down-section">
            <h3>📉 Trending Down</h3>
        """, unsafe_allow_html=True)
        
        trending_down = [
            {"product": "Tomato", "change": "-8%", "reason": "Oversupply in market", "volume": "1,200 tons"},
            {"product": "Onion", "change": "-3%", "reason": "Import competition", "volume": "2,100 tons"},
            {"product": "Cabbage", "change": "-2%", "reason": "Seasonal decline", "volume": "900 tons"},
            {"product": "Cauliflower", "change": "-1%", "reason": "Harvest season", "volume": "1,500 tons"}
        ]
        
        for item in trending_down:
            st.markdown(f"""
            <div class="trend-item-full trending-down">
                <div class="trend-product-name">🍅 {item['product']}</div>
                <div class="trend-change-value">{item['change']}</div>
                <div class="trend-reason-text">{item['reason']}</div>
                <div class="trend-volume">Volume: {item['volume']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="trend-section stable-section">
            <h3>➡️ Stable Prices</h3>
        """, unsafe_allow_html=True)
        
        stable_products = [
            {"product": "Garlic", "change": "0%", "reason": "Steady demand", "volume": "600 tons"},
            {"product": "Ginger", "change": "+0.5%", "reason": "Consistent supply", "volume": "400 tons"},
            {"product": "Coriander", "change": "-0.2%", "reason": "Balanced market", "volume": "300 tons"},
            {"product": "Mint", "change": "0%", "reason": "Regular trading", "volume": "200 tons"}
        ]
        
        for item in stable_products:
            st.markdown(f"""
            <div class="trend-item-full stable">
                <div class="trend-product-name">🌿 {item['product']}</div>
                <div class="trend-change-value">{item['change']}</div>
                <div class="trend-reason-text">{item['reason']}</div>
                <div class="trend-volume">Volume: {item['volume']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Market alerts in full width
    st.markdown("### ⚡ Live Market Alerts")
    
    alerts = [
        {"type": "opportunity", "message": "🎯 Bulk potato orders available - 500kg+ at premium rates (+15% above market)", "priority": "HIGH"},
        {"type": "warning", "message": "⚠️ Tomato prices expected to drop further - consider selling current stock", "priority": "MEDIUM"},
        {"type": "info", "message": "ℹ️ New government subsidy announced for wheat farmers - prices may stabilize", "priority": "LOW"},
        {"type": "opportunity", "message": "🚀 Export demand surge for rice - international buyers offering premium", "priority": "HIGH"}
    ]
    
    for alert in alerts:
        alert_type = alert["type"]
        priority_class = alert["priority"].lower()
        
        if alert_type == "opportunity":
            st.markdown(f"""
            <div class="market-alert-full opportunity {priority_class}">
                <div class="alert-icon">🎯</div>
                <div class="alert-content">
                    <div class="alert-message">{alert['message']}</div>
                    <div class="alert-priority">Priority: {alert['priority']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif alert_type == "warning":
            st.markdown(f"""
            <div class="market-alert-full warning {priority_class}">
                <div class="alert-icon">⚠️</div>
                <div class="alert-content">
                    <div class="alert-message">{alert['message']}</div>
                    <div class="alert-priority">Priority: {alert['priority']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="market-alert-full info {priority_class}">
                <div class="alert-icon">ℹ️</div>
                <div class="alert-content">
                    <div class="alert-message">{alert['message']}</div>
                    <div class="alert-priority">Priority: {alert['priority']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def simulate_voice_interaction():
    """Simulate realistic voice interaction using full available space."""
    
    st.markdown("""
    <div class="feature-fullscreen">
        <div class="feature-header-full">
            <h2>🎤 AI Voice Assistant</h2>
            <p>Advanced voice recognition and natural language processing</p>
            <div class="voice-status-badge-full">Ready to listen</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Voice simulation in full width layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="voice-commands-section">
            <h3>🗣️ Sample Voice Commands</h3>
            <p>Click any command to simulate voice processing</p>
        </div>
        """, unsafe_allow_html=True)
        
        voice_commands = [
            {"text": "आलू 50 किलो 25 रुपये प्रति किलो", "lang": "Hindi", "type": "trade"},
            {"text": "Tomato 30 kg at 35 rupees per kg", "lang": "English", "type": "trade"},
            {"text": "प्याज का भाव क्या है?", "lang": "Hindi", "type": "query"},
            {"text": "What is the current rice price?", "lang": "English", "type": "query"},
            {"text": "मुझे गेहूं बेचना है", "lang": "Hindi", "type": "sell"},
            {"text": "Show me today's market trends", "lang": "English", "type": "analysis"},
            {"text": "कल का मौसम कैसा रहेगा?", "lang": "Hindi", "type": "weather"},
            {"text": "Calculate profit for 100kg potato", "lang": "English", "type": "calculation"}
        ]
        
        for i, command in enumerate(voice_commands):
            type_class = command["type"]
            st.markdown(f"""
            <div class="voice-command-card {type_class}">
                <div class="command-header">
                    <span class="command-lang">{command['lang']}</span>
                    <span class="command-type">{command['type'].title()}</span>
                </div>
                <div class="command-text">{command['text']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🎤 Process Command", key=f"voice_cmd_{i}", use_container_width=True):
                simulate_voice_processing(command['text'])
    
    with col2:
        st.markdown("""
        <div class="ai-response-section">
            <h3>🤖 AI Response & Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Simulate AI processing
        if 'voice_response' in st.session_state:
            st.markdown(f"""
            <div class="ai-response-full">
                <div class="response-header">
                    <div class="response-status">✅ Processing Complete</div>
                    <div class="response-time">Response time: 1.2s</div>
                </div>
                <div class="response-content">
                    <div class="response-text">{st.session_state.voice_response}</div>
                </div>
                <div class="response-actions-full">
                    <button class="action-btn-full confirm">✅ Confirm Trade</button>
                    <button class="action-btn-full reject">❌ Reject Offer</button>
                    <button class="action-btn-full retry">🔄 Ask Again</button>
                    <button class="action-btn-full save">💾 Save to Ledger</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="ai-waiting-full">
                <div class="waiting-animation">
                    <div class="pulse-circle"></div>
                    <div class="waiting-icon">🎧</div>
                </div>
                <div class="waiting-text">Waiting for voice input...</div>
                <div class="waiting-subtitle">Click any command above to simulate voice processing</div>
            </div>
            """, unsafe_allow_html=True)


def simulate_voice_processing(command):
    """Process voice command and generate AI response."""
    
    # Simulate AI processing
    import time
    import random
    
    # Show processing animation
    with st.spinner("🤖 Processing voice command..."):
        time.sleep(1)  # Simulate processing time
    
    # Generate intelligent response based on command
    if "आलू" in command or "potato" in command.lower():
        response = "✅ Detected: Potato trade request\n📊 Quantity: 50 kg\n💰 Price: ₹25/kg\n📈 Market rate: ₹22/kg (Good deal!)\n🎯 Recommendation: Accept this offer"
    elif "टमाटर" in command or "tomato" in command.lower():
        response = "✅ Detected: Tomato trade request\n📊 Quantity: 30 kg\n💰 Price: ₹35/kg\n📉 Market rate: ₹32/kg (Slightly high)\n🎯 Recommendation: Negotiate for ₹32/kg"
    elif "भाव" in command or "price" in command.lower():
        response = "📊 Current Market Prices:\n🥔 Potato: ₹22/kg\n🍅 Tomato: ₹32/kg\n🧅 Onion: ₹28/kg\n🌾 Rice: ₹40/kg\n🌾 Wheat: ₹25/kg"
    elif "बेचना" in command or "sell" in command.lower():
        response = "🛒 Sell Request Detected\n📈 Current market conditions favorable\n💡 Best time to sell: Morning hours\n🎯 Recommended action: List your products now"
    else:
        response = "🤖 Voice command processed\n✅ Understanding your request\n📞 Connecting to trade network\n⏳ Please wait for market response"
    
    st.session_state.voice_response = response
    st.success("🎤 Voice command processed successfully!")
    st.rerun()


def render_negotiation_interface():
    """Render the main negotiation interface."""
    
    st.markdown(f'<div class="section-header">{language_manager.get_text("trade_negotiation")}</div>', 
                unsafe_allow_html=True)
    
    # AI Assistant Status Panel
    st.markdown("""
    <div class="ai-status-panel">
        <div class="ai-avatar">🤖</div>
        <div class="ai-info">
            <div class="ai-name">AgriTrade AI Assistant</div>
            <div class="ai-status">Ready to help with your trade negotiations</div>
        </div>
        <div class="ai-capabilities">
            <span class="capability">Voice Recognition</span>
            <span class="capability">Price Analysis</span>
            <span class="capability">Market Insights</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Start Negotiation Button
    if not st.session_state.negotiation_active:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button(language_manager.get_text("start_negotiation"), 
                        type="primary", 
                        use_container_width=True,
                        key="start_negotiation_btn"):
                start_negotiation()
        
        with col2:
            if st.button("🎯 Quick Demo", 
                        type="secondary", 
                        use_container_width=True,
                        key="quick_demo_btn"):
                run_quick_demo()
        
        with col3:
            if st.button(language_manager.get_text("add_sample_data"), 
                        type="tertiary", 
                        use_container_width=True,
                        key="add_sample_main_btn"):
                add_sample_trade_data()
        
        # Market Insights Panel
        render_market_insights()
        
    else:
        # Active negotiation interface
        render_active_negotiation()


def render_active_negotiation():
    """Render interface for active negotiation."""
    
    # Status indicator
    st.markdown(f"""
    <div class="status-indicator status-active">
        {language_manager.get_text("negotiation_active")}
    </div>
    """, unsafe_allow_html=True)
    
    # Voice recording interface with enhanced layout
    if st.session_state.recording_status == "idle":
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if st.button(language_manager.get_text("start_recording"), 
                        type="secondary",
                        use_container_width=True,
                        key="start_recording_btn"):
                start_voice_recording()
        
        with col2:
            if st.button(language_manager.get_text("end_negotiation"),
                        type="tertiary",
                        use_container_width=True,
                        key="end_negotiation_btn"):
                end_negotiation()
    
    elif st.session_state.recording_status == "recording":
        st.markdown(f"""
        <div class="status-indicator status-recording">
            <div class="loading-spinner"></div>
            &nbsp;&nbsp;{language_manager.get_text("recording_in_progress")}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(language_manager.get_text("stop_recording"), 
                    type="primary",
                    use_container_width=True,
                    key="stop_recording_btn"):
            stop_voice_recording()
    
    elif st.session_state.recording_status == "processing":
        st.markdown(f"""
        <div class="status-indicator status-processing">
            <div class="loading-spinner"></div>
            &nbsp;&nbsp;{language_manager.get_text("processing")}
        </div>
        """, unsafe_allow_html=True)
    
    # Display conversation history
    render_conversation_history()


def render_conversation_history():
    """Render the conversation history."""
    
    if st.session_state.conversation_history:
        st.markdown(f'<div class="section-header">{language_manager.get_text("conversation_history")}</div>', 
                    unsafe_allow_html=True)
        
        for i, message in enumerate(st.session_state.conversation_history):
            with st.expander(f"💬 Message {i+1}: {message.get('timestamp', 'Unknown time')}", expanded=i == len(st.session_state.conversation_history)-1):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.write(f"**{language_manager.get_text('language')}:** {message.get('language', 'Unknown')}")
                
                with col2:
                    st.write(f"**Text:** {message.get('text', 'No text')}")
                
                if message.get('extracted_data'):
                    st.markdown("**Extracted Data:**")
                    st.json(message['extracted_data'])


def render_trade_ledger_main():
    """Render the trade ledger in the main area."""
    
    st.markdown(f'<div class="section-header">{language_manager.get_text("trade_ledger")}</div>', 
                unsafe_allow_html=True)
    
    # Trade Summary Dashboard
    if st.session_state.trade_ledger:
        total_value = sum(trade.get('total_amount', 0) for trade in st.session_state.trade_ledger)
        total_cess = sum(trade.get('mandi_cess', 0) for trade in st.session_state.trade_ledger)
        avg_price = total_value / len(st.session_state.trade_ledger) if st.session_state.trade_ledger else 0
        
        st.markdown(f"""
        <div class="trade-summary-dashboard">
            <div class="summary-card">
                <div class="summary-icon">💰</div>
                <div class="summary-content">
                    <div class="summary-value">₹{total_value:,}</div>
                    <div class="summary-label">Total Value</div>
                </div>
            </div>
            <div class="summary-card">
                <div class="summary-icon">📊</div>
                <div class="summary-content">
                    <div class="summary-value">₹{avg_price:.0f}</div>
                    <div class="summary-label">Avg Trade</div>
                </div>
            </div>
            <div class="summary-card">
                <div class="summary-icon">🏛️</div>
                <div class="summary-content">
                    <div class="summary-value">₹{total_cess}</div>
                    <div class="summary-label">Mandi Cess</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons in main area layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button(language_manager.get_text("add_sample_data"),
                    type="tertiary",
                    use_container_width=True,
                    key="add_sample_main_ledger_btn"):
            add_sample_trade_data()
    
    with col2:
        if st.button("📊 Analytics",
                    type="tertiary",
                    use_container_width=True,
                    key="analytics_main_btn"):
            show_analytics_modal()
    
    with col3:
        if st.button("🔄 Reset Data",
                    type="tertiary",
                    use_container_width=True,
                    key="reset_main_btn"):
            reset_application_data()
    
    with col4:
        if st.button("🗑️ Clear Trades",
                    type="tertiary",
                    use_container_width=True,
                    key="clear_main_btn"):
            clear_trade_data()
    
    st.markdown("---")
    
    if not st.session_state.trade_ledger:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📦</div>
            <div class="empty-title">No Trade Records</div>
            <div class="empty-subtitle">Start by adding sample data or begin a negotiation</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display trade records in a grid layout for main area
        cols_per_row = 3
        trades = st.session_state.trade_ledger
        
        for i in range(0, len(trades), cols_per_row):
            cols = st.columns(cols_per_row, gap="medium")
            
            for j, col in enumerate(cols):
                trade_index = i + j
                if trade_index < len(trades):
                    trade = trades[trade_index]
                    profit_margin = (trade.get('unit_price', 0) - 15) / 15 * 100  # Assuming base cost of ₹15
                    status = "profitable" if profit_margin > 20 else "moderate" if profit_margin > 0 else "loss"
                    
                    with col:
                        st.markdown(f"""
                        <div class="trade-card-enhanced {status}">
                            <div class="trade-header">
                                <div class="trade-product">🛒 {trade.get('product_name', 'Unknown Product')}</div>
                                <div class="trade-status">{status.title()}</div>
                            </div>
                            <div class="trade-metrics">
                                <div class="metric">
                                    <span class="metric-value">{trade.get('quantity', 0)}</span>
                                    <span class="metric-unit">{trade.get('unit', '')}</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-value">₹{trade.get('unit_price', 0)}</span>
                                    <span class="metric-unit">per kg</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-value">₹{trade.get('total_amount', 0)}</span>
                                    <span class="metric-unit">total</span>
                                </div>
                            </div>
                            <div class="trade-footer">
                                <span class="trade-time">📅 {trade.get('timestamp', 'Unknown')}</span>
                                <span class="profit-indicator">{profit_margin:+.1f}%</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


def render_sidebar_info():
    """Render additional information in the sidebar."""
    
    # Language selector
    language_manager.render_language_selector()
    
    # App statistics
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Statistics")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Conversations", len(st.session_state.conversation_history))
    with col2:
        st.metric("Trades", len(st.session_state.trade_ledger))
    
    # Quick actions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Quick Actions")
    
    if st.sidebar.button("🔄 Reset All Data", key="reset_data_btn"):
        reset_application_data()
    
    if st.sidebar.button("🗑️ Clear Trade Data", key="clear_trades_btn"):
        clear_trade_data()
    
    if st.sidebar.button("💾 Export Data", key="export_data_btn"):
        export_application_data()


def start_negotiation():
    """Start a new negotiation session."""
    st.session_state.negotiation_active = True
    st.session_state.conversation_history = []
    st.session_state.current_trade_data = None
    st.success("🎯 " + language_manager.get_text("negotiation_active"))
    st.rerun()


def end_negotiation():
    """End the current negotiation session."""
    st.session_state.negotiation_active = False
    st.session_state.recording_status = "idle"
    st.info("✅ Negotiation ended successfully!")
    st.rerun()


def start_voice_recording():
    """Start voice recording."""
    st.session_state.recording_status = "recording"
    # TODO: Implement actual voice recording logic
    st.rerun()


def stop_voice_recording():
    """Stop voice recording and process the audio."""
    st.session_state.recording_status = "processing"
    
    # TODO: Implement actual voice processing logic
    # For now, add a placeholder message
    placeholder_message = {
        'timestamp': '2024-01-26 14:30:00',
        'language': st.session_state.current_language,
        'text': 'आलू 50 किलो 20 रुपये प्रति किलो' if st.session_state.current_language == 'hi' else 'Potato 50 kg at 20 rupees per kg',
        'extracted_data': {
            'product_name': 'आलू (Potato)' if st.session_state.current_language == 'hi' else 'Potato',
            'quantity': 50,
            'unit': 'kg',
            'unit_price': 20
        }
    }
    
    st.session_state.conversation_history.append(placeholder_message)
    st.session_state.recording_status = "idle"
    st.rerun()


def add_sample_trade_data():
    """Add sample trade data for testing."""
    import random
    from datetime import datetime, timedelta
    
    # Sample products in different languages
    products = {
        'en': [
            {'name': 'Potato', 'hindi': 'आलू'},
            {'name': 'Tomato', 'hindi': 'टमाटर'},
            {'name': 'Onion', 'hindi': 'प्याज'},
            {'name': 'Rice', 'hindi': 'चावल'},
            {'name': 'Wheat', 'hindi': 'गेहूं'},
            {'name': 'Carrot', 'hindi': 'गाजर'},
            {'name': 'Cabbage', 'hindi': 'पत्ता गोभी'},
            {'name': 'Cauliflower', 'hindi': 'फूल गोभी'}
        ]
    }
    
    # Select random product
    product = random.choice(products['en'])
    current_lang = st.session_state.current_language
    
    # Generate random trade data
    quantity = random.randint(10, 100)
    unit_price = random.randint(15, 50)
    total_amount = quantity * unit_price
    mandi_cess = int(total_amount * 0.05)  # 5% mandi cess
    
    # Generate timestamp (random time in last 7 days)
    now = datetime.now()
    random_days = random.randint(0, 7)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    timestamp = now - timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
    
    sample_trade = {
        'product_name': f"{product['hindi']} ({product['name']})" if current_lang == 'hi' else product['name'],
        'quantity': quantity,
        'unit': 'kg',
        'unit_price': unit_price,
        'total_amount': total_amount,
        'mandi_cess': mandi_cess,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'language': current_lang
    }
    
    st.session_state.trade_ledger.append(sample_trade)
    st.success(f"✅ Sample trade added: {sample_trade['product_name']} - {quantity}kg @ ₹{unit_price}/kg")
    st.rerun()


def reset_application_data():
    """Reset all application data."""
    st.session_state.conversation_history = []
    st.session_state.trade_ledger = []
    st.session_state.negotiation_active = False
    st.session_state.recording_status = "idle"
    st.success("🔄 All data has been reset!")
    st.rerun()


def clear_trade_data():
    """Clear only trade ledger data."""
    st.session_state.trade_ledger = []
    st.success("🗑️ Trade data cleared!")
    st.rerun()


def run_quick_demo():
    """Run a quick demo of the application."""
    # Add multiple sample trades
    import random
    from datetime import datetime, timedelta
    
    products = [
        {'name': 'Potato', 'hindi': 'आलू'},
        {'name': 'Tomato', 'hindi': 'टमाटर'},
        {'name': 'Onion', 'hindi': 'प्याज'},
        {'name': 'Rice', 'hindi': 'चावल'},
        {'name': 'Wheat', 'hindi': 'गेहूं'}
    ]
    
    # Clear existing data
    st.session_state.trade_ledger = []
    st.session_state.conversation_history = []
    
    # Add 5 sample trades
    for i in range(5):
        product = products[i]
        current_lang = st.session_state.current_language
        
        quantity = random.randint(20, 80)
        unit_price = random.randint(18, 45)
        total_amount = quantity * unit_price
        mandi_cess = int(total_amount * 0.05)
        
        now = datetime.now()
        timestamp = now - timedelta(hours=random.randint(1, 48))
        
        sample_trade = {
            'product_name': f"{product['hindi']} ({product['name']})" if current_lang == 'hi' else product['name'],
            'quantity': quantity,
            'unit': 'kg',
            'unit_price': unit_price,
            'total_amount': total_amount,
            'mandi_cess': mandi_cess,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'language': current_lang
        }
        
        st.session_state.trade_ledger.append(sample_trade)
        
        # Add conversation history
        conversation = {
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'language': current_lang,
            'text': f"{product['hindi']} {quantity} किलो {unit_price} रुपये प्रति किलो" if current_lang == 'hi' else f"{product['name']} {quantity} kg at {unit_price} rupees per kg",
            'extracted_data': {
                'product_name': sample_trade['product_name'],
                'quantity': quantity,
                'unit': 'kg',
                'unit_price': unit_price
            }
        }
        st.session_state.conversation_history.append(conversation)
    
    st.success("🎯 Quick demo loaded! 5 trades and conversations added.")
    st.rerun()


def show_analytics_modal():
    """Show analytics modal with comprehensive trade statistics using full screen space."""
    
    if not st.session_state.trade_ledger:
        st.warning("📊 No trade data available for analytics. Add some sample data first!")
        return
    
    # Calculate comprehensive analytics
    total_trades = len(st.session_state.trade_ledger)
    total_value = sum(trade.get('total_amount', 0) for trade in st.session_state.trade_ledger)
    total_cess = sum(trade.get('mandi_cess', 0) for trade in st.session_state.trade_ledger)
    avg_trade_value = total_value / total_trades if total_trades > 0 else 0
    
    # Product analytics
    product_stats = {}
    for trade in st.session_state.trade_ledger:
        product = trade.get('product_name', 'Unknown')
        if product not in product_stats:
            product_stats[product] = {'count': 0, 'total_value': 0, 'total_quantity': 0}
        product_stats[product]['count'] += 1
        product_stats[product]['total_value'] += trade.get('total_amount', 0)
        product_stats[product]['total_quantity'] += trade.get('quantity', 0)
    
    # Find top performing product
    top_product = max(product_stats.items(), key=lambda x: x[1]['total_value']) if product_stats else ('None', {'total_value': 0})
    
    # Profit analysis
    profitable_trades = 0
    total_profit = 0
    for trade in st.session_state.trade_ledger:
        unit_price = trade.get('unit_price', 0)
        quantity = trade.get('quantity', 0)
        base_cost = 15  # Assuming base cost of ₹15 per kg
        profit = (unit_price - base_cost) * quantity
        total_profit += profit
        if profit > 0:
            profitable_trades += 1
    
    profit_margin = (total_profit / total_value * 100) if total_value > 0 else 0
    success_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
    
    # Create full-width analytics container
    st.markdown("""
    <div class="analytics-fullscreen">
        <div class="analytics-header-full">
            <h2>📈 Advanced Trade Analytics Dashboard</h2>
            <p>Comprehensive analysis of your trading performance</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics in full-width grid
    st.markdown("### 📊 Key Performance Metrics")
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.markdown(f"""
        <div class="analytics-card-full">
            <div class="card-icon">💰</div>
            <div class="card-content">
                <h3>Total Revenue</h3>
                <div class="card-value">₹{total_value:,}</div>
                <div class="card-desc">Across {total_trades} trades</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="analytics-card-full">
            <div class="card-icon">📊</div>
            <div class="card-content">
                <h3>Average Trade</h3>
                <div class="card-value">₹{avg_trade_value:.0f}</div>
                <div class="card-desc">Per transaction</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="analytics-card-full">
            <div class="card-icon">🎯</div>
            <div class="card-content">
                <h3>Success Rate</h3>
                <div class="card-value">{success_rate:.1f}%</div>
                <div class="card-desc">{profitable_trades}/{total_trades} profitable</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="analytics-card-full">
            <div class="card-icon">📈</div>
            <div class="card-content">
                <h3>Profit Margin</h3>
                <div class="card-value">{profit_margin:+.1f}%</div>
                <div class="card-desc">Overall performance</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Product performance in full width
    st.markdown("### 🏆 Top Performing Products")
    
    if product_stats:
        # Sort products by total value
        sorted_products = sorted(product_stats.items(), key=lambda x: x[1]['total_value'], reverse=True)
        
        # Create full-width product performance table
        st.markdown("""
        <div class="product-performance-table">
            <div class="table-header">
                <div class="header-rank">Rank</div>
                <div class="header-product">Product</div>
                <div class="header-trades">Trades</div>
                <div class="header-quantity">Quantity</div>
                <div class="header-value">Total Value</div>
                <div class="header-avg">Avg Price</div>
            </div>
        """, unsafe_allow_html=True)
        
        for i, (product, stats) in enumerate(sorted_products[:5]):  # Top 5 products
            rank_emoji = ["🥇", "🥈", "🥉", "🏅", "🏅"][min(i, 4)]
            avg_price = stats['total_value'] / stats['total_quantity'] if stats['total_quantity'] > 0 else 0
            
            st.markdown(f"""
            <div class="table-row">
                <div class="cell-rank">{rank_emoji}</div>
                <div class="cell-product">{product}</div>
                <div class="cell-trades">{stats['count']}</div>
                <div class="cell-quantity">{stats['total_quantity']} kg</div>
                <div class="cell-value">₹{stats['total_value']:,}</div>
                <div class="cell-avg">₹{avg_price:.0f}/kg</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Market insights in full width
    st.markdown("### 🔍 Market Insights & Recommendations")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown(f"""
        <div class="insights-panel">
            <h4>📊 Trade Distribution Analysis</h4>
            <ul class="insights-list">
                <li><strong>Most traded product:</strong> {top_product[0]}</li>
                <li><strong>Highest value trade:</strong> ₹{max(trade.get('total_amount', 0) for trade in st.session_state.trade_ledger):,}</li>
                <li><strong>Average quantity per trade:</strong> {sum(trade.get('quantity', 0) for trade in st.session_state.trade_ledger) / total_trades:.1f} kg</li>
                <li><strong>Total mandi cess paid:</strong> ₹{total_cess:,}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="recommendations-panel">
            <h4>💡 Strategic Recommendations</h4>
            <ul class="recommendations-list">
                <li>Focus on high-margin products for better profitability</li>
                <li>Consider bulk trading to negotiate better rates</li>
                <li>Monitor seasonal price variations for timing</li>
                <li>Expand successful product lines based on performance</li>
                <li>Optimize trade frequency for cost efficiency</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Export option in full width
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        if st.button("📥 Export Analytics Report", type="primary", use_container_width=True):
            export_analytics_report(total_value, total_trades, profit_margin, success_rate, product_stats)


def export_analytics_report(total_value, total_trades, profit_margin, success_rate, product_stats):
    """Export comprehensive analytics report."""
    import json
    from datetime import datetime
    
    report_data = {
        'report_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'summary': {
            'total_revenue': total_value,
            'total_trades': total_trades,
            'average_trade_value': total_value / total_trades if total_trades > 0 else 0,
            'profit_margin_percent': profit_margin,
            'success_rate_percent': success_rate
        },
        'product_performance': product_stats,
        'trade_details': st.session_state.trade_ledger,
        'language': st.session_state.current_language
    }
    
    st.download_button(
        label="📊 Download Analytics Report",
        data=json.dumps(report_data, indent=2, ensure_ascii=False),
        file_name=f"agritrade_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        type="primary"
    )
    
    st.success("📊 Analytics report ready for download!")


def render_market_insights():
    """Render market insights panel."""
    st.markdown("""
    <div class="market-insights-panel">
        <h3>📈 Today's Market Insights</h3>
        <div class="insights-grid">
            <div class="insight-card trending-up">
                <div class="insight-icon">🥔</div>
                <div class="insight-content">
                    <div class="insight-title">Potato</div>
                    <div class="insight-price">₹22/kg</div>
                    <div class="insight-trend">↗️ +12%</div>
                </div>
            </div>
            <div class="insight-card trending-down">
                <div class="insight-icon">🍅</div>
                <div class="insight-content">
                    <div class="insight-title">Tomato</div>
                    <div class="insight-price">₹35/kg</div>
                    <div class="insight-trend">↘️ -8%</div>
                </div>
            </div>
            <div class="insight-card stable">
                <div class="insight-icon">🧅</div>
                <div class="insight-content">
                    <div class="insight-title">Onion</div>
                    <div class="insight-price">₹28/kg</div>
                    <div class="insight-trend">→ 0%</div>
                </div>
            </div>
        </div>
        <div class="market-alert">
            <span class="alert-icon">⚡</span>
            <span class="alert-text">High demand for potatoes in Delhi market - Consider bulk trading!</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def export_application_data():
    """Export application data."""
    import json
    
    export_data = {
        'conversations': st.session_state.conversation_history,
        'trades': st.session_state.trade_ledger,
        'language': st.session_state.current_language,
        'export_timestamp': '2024-01-26 14:30:00'
    }
    
    st.sidebar.download_button(
        label="📥 Download JSON",
        data=json.dumps(export_data, indent=2, ensure_ascii=False),
        file_name=f"mandi_setu_export_{st.session_state.current_language}.json",
        mime="application/json"
    )


def render_footer():
    """Render the application footer."""
    
    st.markdown("---")
    st.markdown(f"""
    <div class="footer-container">
        <p class="footer-text">
            {language_manager.get_text("built_for_viksit_bharat")}<br>
            <small>Version {st.session_state.config.version} | Environment: {st.session_state.config.environment}</small>
        </p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point."""
    
    # Configure Streamlit page
    st.set_page_config(
        page_title="AgriTrade Pro",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-username/agritrade-pro#readme',
            'Report a bug': 'https://github.com/your-username/agritrade-pro/issues',
            'About': """
            # AgriTrade Pro
            
            A multilingual AI assistant for agricultural market vendors in India.
            
            **Version:** 1.0.0
            **Built for:** Viksit Bharat
            """
        }
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Apply custom theme
    apply_viksit_bharat_theme()
    
    # Render application
    render_header()
    render_main_interface()
    render_footer()
    
    # Render sidebar
    render_sidebar_info()
    



if __name__ == "__main__":
    main()
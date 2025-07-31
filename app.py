import streamlit as st
import os
from dotenv import load_dotenv
from src.citation_analyzer import CitationAnalyzer
from src.file_handlers import FileHandler
from ui.components import render_results_section, render_navbar
from ui.styles import load_custom_css
from config.settings import Settings, AVAILABLE_MODELS, MODEL_PRESETS

# Load environment variables from .env file (for local development)
load_dotenv()

# Initialize session state for API key
if 'api_key' not in st.session_state:
    # Try to get API key from multiple sources
    api_key = None
    
    # First try Streamlit secrets (for cloud deployment)
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except:
        pass
    
    # Then try environment variables (for local development)
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    
    st.session_state.api_key = api_key or ""

# Debug logging (only in local development)
if os.getenv("DEBUG") == "True":
    if st.session_state.api_key:
        print("API key loaded successfully")
    else:
        print("Warning: No API key found")

# Page configuration - no sidebar
st.set_page_config(
    page_title="Psyte - Professional Citation Analysis",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar completely
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Load custom CSS
load_custom_css()

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'processed_text' not in st.session_state:
    st.session_state.processed_text = ""
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'enable_search' not in st.session_state:
    st.session_state.enable_search = False  # Disabled by default for faster results
if 'preferred_model' not in st.session_state:
    st.session_state.preferred_model = "gemini-1.5-flash"
if 'model_preset' not in st.session_state:
    st.session_state.model_preset = "balanced"
if 'show_advanced' not in st.session_state:
    st.session_state.show_advanced = False
if 'current_analyzer' not in st.session_state:
    st.session_state.current_analyzer = None

def main():
    # Render navigation bar
    render_navbar()
    
    # Get settings
    settings = Settings(
        api_provider="gemini",
        api_key=st.session_state.api_key,
        use_mcp=False,
        preferred_style="auto",
        confidence_threshold=0.7,
        show_detailed_analysis=True,
        enable_web_search=st.session_state.enable_search,
        preferred_model=st.session_state.preferred_model,
        enable_model_fallback=True
    )
    
    if not st.session_state.show_results:
        # Homepage
        render_homepage(settings)
    else:
        # Results page
        render_results_page(settings)

def render_homepage(settings: Settings):
    """Render Google-style homepage"""
    # Add spacing after navbar
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    
    # Center column for main content
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Logo and title - using solid theme colors
        st.markdown("""
        <div class="homepage-container">
            <div class="logo-container">
                <h1 class="logo-text">
                    <span class="logo-letter-p">P</span><span class="logo-letter-s">s</span><span class="logo-letter-y">y</span><span class="logo-letter-t">t</span><span class="logo-letter-e">e</span>
                </h1>
                <p class="tagline">Professional Citation Analysis & Discovery</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Scrolling features animation
        st.markdown("""
        <div class="features-scroll-wrapper">
            <div class="features-scroll-content">
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Format Validation
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    APA Style Support
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    MLA Style Support
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Chicago Style Support
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Harvard Style Support
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    IEEE Style Support
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Multiple AI Models
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Auto Model Fallback
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Missing Citation Detection
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Web Search Integration
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    CrossRef Database
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    arXiv Integration
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Semantic Scholar
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    AI-Powered Analysis
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Style Conversion
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Real-time Validation
                </span>
                <!-- Duplicate for seamless scrolling -->
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Format Validation
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    APA Style Support
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    MLA Style Support
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Chicago Style Support
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Harvard Style Support
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    IEEE Style Support
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Multiple AI Models
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Auto Model Fallback
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Missing Citation Detection
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Web Search Integration
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    CrossRef Database
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    arXiv Integration
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Semantic Scholar
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    AI-Powered Analysis
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Style Conversion
                </span>
                <span class="features-scroll-item">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    Real-time Validation
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # API Key input if not set
        if not st.session_state.api_key:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <p style="color: var(--text-secondary); font-size: 16px;">Enter your Gemini API key to get started</p>
            </div>
            """, unsafe_allow_html=True)
            
            api_key_input = st.text_input(
                "Gemini API Key",
                type="password",
                placeholder="Enter your Gemini API key...",
                key="api_key_input",
                label_visibility="collapsed",
                help="Get your API key from Google AI Studio"
            )
            if api_key_input:
                st.session_state.api_key = api_key_input
                st.rerun()
            
            st.markdown("""
            <div class="api-key-help">
                <p>Get your API key from <a href="https://makersuite.google.com/app/apikey" target="_blank">Google AI Studio</a></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Main input area
            text_input = st.text_area(
                "Citation Text",
                height=120,
                placeholder="Paste your text with citations here...",
                key="main_text_input",
                label_visibility="collapsed"
            )
            
            # Advanced options
            with st.expander("⚙️ Advanced Options", expanded=st.session_state.show_advanced):
                col_opt1, col_opt2 = st.columns(2)
                
                with col_opt1:
                    enable_search = st.checkbox(
                        "Enable citation discovery",
                        value=st.session_state.enable_search,
                        key="search_toggle",
                        help="Searches academic databases like CrossRef, arXiv, and Semantic Scholar"
                    )
                    st.session_state.enable_search = enable_search
                    
                    # Model preset selection
                    preset = st.selectbox(
                        "Model Preset",
                        options=list(MODEL_PRESETS.keys()),
                        format_func=lambda x: f"{MODEL_PRESETS[x]['name']} - {MODEL_PRESETS[x]['description']}",
                        index=list(MODEL_PRESETS.keys()).index(st.session_state.model_preset),
                        help="Choose a preset based on your priority"
                    )
                    st.session_state.model_preset = preset
                
                with col_opt2:
                    # Show current model status
                    if st.session_state.current_analyzer:
                        model_info = st.session_state.current_analyzer.api_provider.get_current_model_info()
                        if model_info['rate_limited']:
                            st.error(f"Current model: {model_info['name']} (Rate Limited)")
                        else:
                            st.success(f"Current model: {model_info['name']}")
                    
                    # Manual model selection
                    selected_model = st.selectbox(
                        "Preferred Model",
                        options=list(AVAILABLE_MODELS.keys()),
                        format_func=lambda x: AVAILABLE_MODELS[x]['name'],
                        index=list(AVAILABLE_MODELS.keys()).index(st.session_state.preferred_model),
                        help="Select your preferred model (auto-fallback enabled)"
                    )
                    st.session_state.preferred_model = selected_model
                
                # Model status display
                if st.checkbox("Show all models status", value=False):
                    if st.session_state.current_analyzer:
                        models_status = st.session_state.current_analyzer.api_provider.get_all_models_status()
                        
                        st.markdown("### Model Status")
                        for model_status in models_status:
                            status_icon = "🟢" if model_status['active'] else "🔴" if model_status['rate_limited'] else "⚪"
                            cooldown_text = f" (cooldown: {model_status['cooldown_remaining']}s)" if model_status['cooldown_remaining'] > 0 else ""
                            st.markdown(f"{status_icon} **{model_status['name']}** - {model_status['description']}{cooldown_text}")
            
            # Action buttons
            col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1, 1.5])
            
            with col_btn2:
                analyze_clicked = st.button(
                    "Analyze Citations",
                    type="primary",
                    use_container_width=True,
                    key="analyze_main"
                )
            
            # File upload section
            st.markdown('<div class="divider-text">or</div>', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Upload Document",
                type=['txt', 'pdf', 'docx', 'md'],
                label_visibility="collapsed",
                key="file_upload_main",
                help="Upload a document containing citations"
            )
            
            # Process input
            if analyze_clicked and text_input:
                st.session_state.processed_text = text_input
                st.session_state.show_results = True
                st.rerun()
            
            if uploaded_file is not None:
                file_handler = FileHandler()
                with st.spinner("Extracting text from file..."):
                    extracted_text = file_handler.extract_text(uploaded_file)
                if extracted_text:
                    st.session_state.processed_text = extracted_text
                    st.session_state.show_results = True
                    st.rerun()
                else:
                    st.error("Failed to extract text from the file. Please try a different file.")
            
            # Footer info
            st.markdown("""
            <div class="footer-info">
                <p><strong>Supported Styles:</strong> APA • MLA • Chicago • Harvard • IEEE</p>
                <p><strong>Features:</strong> Format Validation • Missing Info Detection • Citation Discovery • Style Conversion</p>
                <p><strong>Models:</strong> 8 AI models with automatic fallback for uninterrupted service</p>
            </div>
            """, unsafe_allow_html=True)

def render_results_page(settings: Settings):
    """Render results page"""
    # Add spacing after navbar
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    
    # Header with back button
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    
    with col1:
        if st.button("← New Analysis", key="back_button"):
            st.session_state.show_results = False
            st.session_state.analysis_results = None
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="results-header">
            <h2 class="results-title">Citation Analysis Results</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Analyze if not already done
    if not st.session_state.analysis_results and st.session_state.processed_text:
        with st.spinner("Analyzing citations..."):
            analyze_text(st.session_state.processed_text, settings)
    
    # Display results
    if st.session_state.analysis_results:
        # Show which model was used
        if 'summary' in st.session_state.analysis_results:
            model_used = st.session_state.analysis_results['summary'].get('model_used')
            if model_used:
                model_name = AVAILABLE_MODELS.get(model_used, {}).get('name', model_used)
                st.info(f"Analysis performed using: **{model_name}**")
        
        render_results_section(st.session_state.analysis_results)
    
    # Actions at bottom
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col2:
        if st.button("Download Report", type="secondary", use_container_width=True):
            # TODO: Implement report download
            st.info("Report download coming soon!")
    
    with col3:
        if st.button("Analyze New Text", type="primary", use_container_width=True):
            st.session_state.show_results = False
            st.session_state.analysis_results = None
            st.session_state.processed_text = ""
            st.rerun()

def analyze_text(text: str, settings: Settings):
    """Analyze the text for citations"""
    try:
        if not settings.api_key:
            st.error("Please provide a Gemini API key to analyze citations.")
            return
            
        # Initialize citation analyzer
        analyzer = CitationAnalyzer(
            api_provider="gemini",
            api_key=settings.api_key,
            mcp_enabled=False,
            enable_web_search=settings.enable_web_search,
            preferred_model=settings.preferred_model
        )
        
        # Store analyzer in session state for model status
        st.session_state.current_analyzer = analyzer
        
        # Perform analysis
        results = analyzer.analyze(text)
        
        # Store results in session state
        st.session_state.analysis_results = results
        
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        if "API key" in str(e):
            st.info("Please check your Gemini API key and try again.")
            # Clear the API key if it's invalid
            st.session_state.api_key = ""
            st.session_state.show_results = False
            st.rerun()

if __name__ == "__main__":
    main()
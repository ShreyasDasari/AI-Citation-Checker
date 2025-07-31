import streamlit as st

def load_custom_css():
    """Load custom CSS styles with dark mode support"""
    st.markdown("""
    <style>
    /* CSS Variables for theme support */
    :root {
        --primary-color: #1a73e8;
        --success-color: #34a853;
        --error-color: #ea4335;
        --warning-color: #fbbc04;
        --text-primary: #202124;
        --text-secondary: #5f6368;
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-tertiary: #f1f3f4;
        --border-color: #dadce0;
        --border-hover: #d2d3d4;
        --shadow-light: rgba(60,64,67,0.15);
        --shadow-medium: rgba(60,64,67,0.3);
        --accent-blue: #1e3a8a;
        --accent-purple: #7c3aed;
        --accent-cyan: #06b6d4;
        --accent-green: #10b981;
        --accent-amber: #f59e0b;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        :root {
            --text-primary: #e8eaed;
            --text-secondary: #bdc1c6;
            --bg-primary: #202124;
            --bg-secondary: #303134;
            --bg-tertiary: #3c4043;
            --border-color: #5f6368;
            --border-hover: #8ab4f8;
            --shadow-light: rgba(0,0,0,0.3);
            --shadow-medium: rgba(0,0,0,0.5);
        }
        
        /* Dark mode specific overrides */
        .stTextArea > div > div > textarea {
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
        }
        
        .stTextInput > div > div > input {
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
        }
        
        .stButton > button {
            color: var(--text-primary) !important;
        }
        
        .stButton > button[kind="primary"] {
            color: white !important;
        }
        
        .stFileUploader > div {
            background-color: var(--bg-secondary) !important;
        }
        
        [data-testid="metric-container"] {
            background-color: var(--bg-secondary) !important;
        }
        
        .stExpander {
            background-color: var(--bg-secondary) !important;
        }
        
        .stCodeBlock {
            background-color: var(--bg-tertiary) !important;
        }
        
        /* Ensure all custom text is visible */
        .homepage-container, 
        .results-header,
        .api-key-help,
        .footer-info,
        .divider-text {
            color: var(--text-primary) !important;
        }
        
        .streamlit-expanderHeader {
            color: var(--text-primary) !important;
        }
    }
    
    /* Global styles */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Google Sans', Roboto, Arial, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Navigation bar */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background-color: var(--bg-primary);
        border-bottom: none;
        z-index: 1000;
        box-shadow: 0 2px 4px 0 rgba(0,0,0,0.05);
    }
    
    .navbar-content {
        max-width: 1400px;
        margin: 0 auto;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2rem;
    }
    
    .navbar-left {
        display: flex;
        align-items: center;
    }
    
    .navbar-logo {
        display: flex;
        align-items: center;
        text-decoration: none;
        gap: 12px;
        transition: opacity 0.2s ease;
    }
    
    .navbar-logo:hover {
        opacity: 0.8;
    }
    
    .logo-icon {
        width: 32px;
        height: 32px;
    }
    
    .navbar-title {
        font-size: 22px;
        font-weight: 500;
        color: var(--text-primary);
        letter-spacing: -0.5px;
    }
    
    .navbar-center {
        flex: 1;
        display: flex;
        justify-content: center;
        gap: 2rem;
    }
    
    .navbar-right {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .navbar-user-icon {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background-color: var(--bg-secondary);
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
        color: var(--text-secondary);
    }
    
    .navbar-user-icon:hover {
        background-color: var(--bg-tertiary);
        color: var(--text-primary);
    }
    
    /* Main container - adjust for navbar */
    .main {
        padding: 0;
        max-width: 100%;
        background-color: var(--bg-primary);
        padding-top: 64px; /* Account for fixed navbar */
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Homepage styles */
    .homepage-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 280px;
        margin-top: 0.5rem;
    }
    
    .logo-container {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    /* Logo text with academic theme colors */
    .logo-text {
        font-size: 5rem;
        font-weight: 400;
        margin: 0;
        letter-spacing: -3px;
        line-height: 1;
        display: block;
        color: var(--text-primary) !important;
    }
    
    .logo-letter-p { color: #1e3a8a !important; }
    .logo-letter-s { color: #7c3aed !important; }
    .logo-letter-y { color: #06b6d4 !important; }
    .logo-letter-t { color: #10b981 !important; }
    .logo-letter-e { color: #f59e0b !important; }
    
    .logo-text span {
        display: inline-block;
        transition: transform 0.2s ease;
        font-weight: 500;
    }
    
    .logo-text span:hover {
        transform: translateY(-2px) scale(1.05);
    }
    
    .tagline {
        color: var(--text-secondary) !important;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
        letter-spacing: 0.3px;
        display: block;
    }
    
    /* API key help */
    .api-key-help {
        text-align: center;
        margin-top: 1rem;
        font-size: 0.9rem;
    }
    
    .api-key-help p {
        color: var(--text-secondary) !important;
        margin: 0;
    }
    
    .api-key-help a {
        color: var(--primary-color);
        text-decoration: none;
        font-weight: 500;
    }
    
    .api-key-help a:hover {
        text-decoration: underline;
    }
    
    /* Search-style text area */
    .stTextArea > div > div > textarea {
        border: 1px solid var(--border-color);
        border-radius: 24px;
        padding: 16px 24px;
        font-size: 16px;
        resize: none;
        box-shadow: 0 1px 6px 0 var(--shadow-light);
        transition: all 0.2s ease;
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    .stTextArea > div > div > textarea:hover {
        box-shadow: 0 1px 8px 0 var(--shadow-light);
        background-color: var(--bg-secondary);
    }
    
    .stTextArea > div > div > textarea:focus {
        outline: none;
        border-color: var(--primary-color);
        box-shadow: 0 1px 8px 0 var(--shadow-light);
    }
    
    /* Text input for API key */
    .stTextInput > div > div > input {
        border: 1px solid var(--border-color);
        border-radius: 24px;
        padding: 12px 20px;
        font-size: 16px;
        background-color: var(--bg-primary);
        color: var(--text-primary);
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(26,115,232,0.2);
        outline: none;
    }
    
    /* Checkbox styling */
    .stCheckbox {
        margin: 1rem 0;
    }
    
    .stCheckbox > label {
        color: var(--text-secondary) !important;
        font-size: 14px;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 24px;
        padding: 10px 32px;
        font-size: 14px;
        font-weight: 500;
        border: 1px solid transparent;
        cursor: pointer;
        transition: all 0.2s ease;
        min-height: 48px;
        letter-spacing: 0.25px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(to right, #1a73e8, #1967d2);
        color: white !important;
        border: none;
        box-shadow: 0 1px 2px 0 rgba(26,115,232,0.3);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(to right, #1967d2, #1557b0);
        box-shadow: 0 1px 3px 0 rgba(26,115,232,0.4), 0 4px 8px 3px rgba(26,115,232,0.15);
        transform: translateY(-1px);
    }
    
    .stButton > button[kind="secondary"] {
        background-color: var(--bg-primary);
        color: var(--primary-color) !important;
        border: 1px solid var(--border-color);
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: var(--bg-secondary);
        border-color: var(--primary-color);
        box-shadow: 0 1px 2px 0 var(--shadow-light);
    }
    
    /* File uploader */
    .stFileUploader {
        margin-top: 2rem;
    }
    
    .stFileUploader > div {
        border: 2px dashed var(--border-color);
        border-radius: 16px;
        background-color: var(--bg-secondary);
        transition: all 0.2s ease;
        padding: 2.5rem 2rem;
        text-align: center;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--primary-color);
        background-color: var(--bg-tertiary);
        box-shadow: 0 4px 12px 0 var(--shadow-light);
    }
    
    /* Divider */
    .divider-text {
        text-align: center;
        color: var(--text-secondary) !important;
        margin: 2.5rem 0;
        position: relative;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .divider-text::before,
    .divider-text::after {
        content: '';
        position: absolute;
        top: 50%;
        width: 45%;
        height: 1px;
        background-color: var(--border-color);
    }
    
    .divider-text::before {
        left: 0;
    }
    
    .divider-text::after {
        right: 0;
    }
    
    /* Footer info */
    .footer-info {
        text-align: center;
        margin-top: 3rem;
        font-size: 13px;
        line-height: 1.8;
    }
    
    .footer-info p {
        color: var(--text-secondary) !important;
        margin: 0.25rem 0;
    }
    
    .footer-info strong {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    /* Scrolling features animation */
    .features-scroll-wrapper {
        width: 100%;
        max-width: 900px;
        margin: 1.5rem auto 2rem auto;
        position: relative;
        overflow: hidden;
        height: 45px;
        background: var(--bg-secondary);
        border-radius: 24px;
        padding: 0 20px;
    }
    
    .features-scroll-wrapper::before,
    .features-scroll-wrapper::after {
        content: '';
        position: absolute;
        top: 0;
        bottom: 0;
        width: 50px;
        z-index: 2;
        pointer-events: none;
    }
    
    .features-scroll-wrapper::before {
        left: 0;
        background: linear-gradient(to right, var(--bg-secondary), transparent);
    }
    
    .features-scroll-wrapper::after {
        right: 0;
        background: linear-gradient(to left, var(--bg-secondary), transparent);
    }
    
    .features-scroll-content {
        display: flex;
        align-items: center;
        height: 100%;
        animation: scroll-left 30s linear infinite;
        white-space: nowrap;
    }
    
    .features-scroll-item {
        display: inline-flex;
        align-items: center;
        margin: 0 2rem;
        color: var(--text-secondary);
        font-size: 14px;
        font-weight: 500;
        white-space: nowrap;
    }
    
    .features-scroll-item svg {
        width: 16px;
        height: 16px;
        margin-right: 0.5rem;
        color: var(--success-color);
    }
    
    @keyframes scroll-left {
        0% {
            transform: translateX(0);
        }
        100% {
            transform: translateX(-50%);
        }
    }
    
    .features-scroll-wrapper:hover .features-scroll-content {
        animation-play-state: paused;
    }
    
    /* Results page */
    .results-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .results-title {
        font-size: 2.25rem;
        font-weight: 400;
        color: var(--text-primary) !important;
        margin: 0;
        display: block;
        letter-spacing: -0.5px;
    }
    
    /* Back button */
    #back_button {
        background: none;
        border: 1px solid var(--border-color);
        color: var(--text-secondary) !important;
        padding: 8px 20px;
        font-size: 14px;
        font-weight: 500;
        border-radius: 20px;
        transition: all 0.2s ease;
        white-space: nowrap;
        min-width: 140px;
    }
    
    #back_button:hover {
        background-color: var(--bg-secondary);
        border-color: var(--primary-color);
        color: var(--primary-color) !important;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background-color: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.75rem 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(to right, #4285F4, #34A853, #FBBC04, #EA4335);
        opacity: 0;
        transition: opacity 0.2s ease;
    }
    
    [data-testid="metric-container"]:hover {
        box-shadow: 0 4px 12px 0 var(--shadow-light);
        transform: translateY(-2px);
        border-color: transparent;
    }
    
    [data-testid="metric-container"]:hover::before {
        opacity: 1;
    }
    
    [data-testid="metric-container"] [data-testid="metric-label"] {
        color: var(--text-secondary) !important;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 2rem;
        font-weight: 600;
        color: var(--text-primary) !important;
        line-height: 1.2;
    }
    
    [data-testid="metric-container"] [data-testid="metric-delta"] {
        color: var(--success-color) !important;
        font-weight: 500;
        font-size: 0.875rem;
        margin-top: 0.25rem;
    }
    
    /* Cards */
    .stExpander {
        background-color: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        margin-bottom: 0.75rem;
        overflow: visible;
        transition: all 0.2s ease;
    }
    
    .stExpander:hover {
        box-shadow: 0 2px 8px 0 var(--shadow-light);
        border-color: var(--border-hover);
    }
    
    .streamlit-expanderHeader {
        color: var(--text-primary) !important;
        font-weight: 500;
        font-size: 15px;
        padding: 1rem 1.25rem !important;
    }
    
    .streamlit-expanderContent {
        padding: 1.5rem;
        background-color: var(--bg-primary);
        border-top: 1px solid var(--border-color);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(to right, #1a73e8, #34a853);
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    .stProgress > div > div {
        background-color: #e8eaed;
        border-radius: 4px;
        height: 6px;
        overflow: hidden;
    }
    
    /* Tabs */
    .stTabs {
        background-color: transparent;
        margin-top: 1rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid var(--border-color);
        background-color: transparent;
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 15px;
        padding: 12px 24px;
        padding-bottom: 16px;
        border-bottom: 3px solid transparent;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-primary);
        background-color: var(--bg-secondary);
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary-color) !important;
        border-bottom-color: var(--primary-color);
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 12px;
        border: none;
        font-size: 14px;
        padding: 1rem 1.5rem;
    }
    
    .stSuccess {
        background-color: #e6f4ea;
        color: #137333;
        border-left: 4px solid var(--success-color);
    }
    
    .stError {
        background-color: #fce8e6;
        color: #c5221f;
        border-left: 4px solid var(--error-color);
    }
    
    .stWarning {
        background-color: #fef7e0;
        color: #985a0e;
        border-left: 4px solid var(--warning-color);
    }
    
    .stInfo {
        background-color: #e8f0fe;
        color: #1967d2;
        border-left: 4px solid var(--primary-color);
    }
    
    /* Dark mode alert overrides */
    @media (prefers-color-scheme: dark) {
        .stSuccess {
            background-color: rgba(52,168,83,0.15);
            color: #81c995;
        }
        
        .stError {
            background-color: rgba(234,67,53,0.15);
            color: #f28b82;
        }
        
        .stWarning {
            background-color: rgba(251,188,4,0.15);
            color: #fdd663;
        }
        
        .stInfo {
            background-color: rgba(26,115,232,0.15);
            color: #8ab4f8;
        }
        
        .features-scroll-wrapper {
            background: var(--bg-secondary);
        }
        
        .features-scroll-wrapper::before {
            background: linear-gradient(to right, var(--bg-secondary), transparent);
        }
        
        .features-scroll-wrapper::after {
            background: linear-gradient(to left, var(--bg-secondary), transparent);
        }
    }
    
    /* Code blocks */
    .stCodeBlock {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        font-family: 'Roboto Mono', 'Consolas', monospace;
    }
    
    .stCodeBlock code {
        color: var(--text-primary) !important;
        font-size: 13px;
    }
    
    /* Spinner */
    .stSpinner > div {
        color: var(--primary-color);
    }
    
    /* Web search badge */
    .search-badge {
        display: inline-block;
        background: linear-gradient(135deg, #4285F4, #34A853);
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 8px;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .logo-text {
            font-size: 3.5rem;
            letter-spacing: -2px;
        }
        
        .homepage-container {
            margin-top: 0.5rem;
        }
        
        .results-title {
            font-size: 1.75rem;
        }
        
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .stButton > button {
            padding: 10px 24px;
            font-size: 13px;
        }
        
        [data-testid="metric-container"] {
            padding: 1.25rem 1rem;
        }
        
        [data-testid="metric-container"] [data-testid="metric-value"] {
            font-size: 1.5rem;
        }
        
        #back_button {
            font-size: 13px;
            padding: 6px 16px;
        }
        
        .features-scroll-wrapper {
            height: 40px;
            margin: 1rem auto 1.5rem auto;
        }
        
        .features-scroll-item {
            font-size: 12px;
            margin: 0 1.5rem;
        }
    }
    
    /* Model status indicators */
    .model-status {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        font-size: 13px;
        font-weight: 500;
    }
    
    .model-status-active {
        background-color: rgba(16, 185, 129, 0.1);
        color: #10b981;
    }
    
    .model-status-rate-limited {
        background-color: rgba(239, 68, 68, 0.1);
        color: #ef4444;
    }
    
    .model-status-available {
        background-color: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
    }
    
    .model-status-icon {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: currentColor;
    }
    </style>
    """, unsafe_allow_html=True)
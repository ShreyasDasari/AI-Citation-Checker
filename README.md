# Psyte - Professional Citation Analysis Tool

A clean, professional web application for analyzing and improving academic citations using Google's Gemini AI. Built with Python and Streamlit with a Google-inspired minimalist interface.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.29.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)


## Live Demo and Trailer

Experience Psyte in action:

- 🔗 **Try the App**: [https://psytee.streamlit.app/](https://psytee.streamlit.app/)
- 🎥 **Watch the Product Trailer**: [https://youtu.be/cs_QpzKBQ-E](https://youtu.be/cs_QpzKBQ-E)

## Key Features

- **Clean Interface**: Google-inspired minimalist design with excellent dark mode support
- **Multiple Input Methods**: Paste text directly or upload files (PDF, DOCX, TXT, Markdown)
- **AI-Powered Analysis**: Uses Google Gemini AI for intelligent citation checking
- **Multi-Model Support**: 8 different AI models with automatic fallback when rate limits are reached
- **Model Selection**: Choose between speed, quality, or cost-optimized presets
- **Web Search Integration**: Automatically searches academic databases to verify and enhance citations
- **Missing Citation Detection**: Identifies statements that may need citations
- **Style Detection**: Automatically detects citation styles (APA, MLA, Chicago, Harvard)
- **Comprehensive Validation**: Checks format, completeness, and consistency
- **Citation Discovery**: Searches CrossRef, arXiv, and Semantic Scholar for matching sources
- **Detailed Reports**: Get actionable insights and improvement suggestions
- **Professional UI**: Clean, focused experience with colorful accents

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/psyte.git
   cd psyte
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`

## Usage

### Basic Workflow

1. **Start the App**: Launch Psyte and you'll see a clean homepage
2. **Enter API Key**: On first use, enter your Gemini API key (stored locally in session)
3. **Enable Web Search** (Optional): Check "Enable citation discovery" for enhanced analysis
4. **Input Text**: Either:
   - Paste text with citations in the search-style input box
   - Upload a document (PDF, DOCX, TXT, or Markdown)
5. **Analyze**: Click "Analyze Citations" to start the analysis
6. **Review Results**: View detailed analysis with:
   - Validity scores and confidence levels
   - Specific issues found in each citation
   - Web-verified sources and suggestions
   - Missing citation detection
   - Visual charts showing citation distribution

### Supported Citation Styles

- **APA**: (Author, Year) format with reference list
- **MLA**: (Author Page) format with Works Cited
- **Chicago**: Footnotes/endnotes with bibliography
- **Harvard**: (Author Year) format with reference list
- **IEEE**: [Number] format with numbered references

## Configuration

### Environment Variables

Create a `.env` file with:

```bash
# Required
GEMINI_API_KEY=your_key_here    # Get from https://makersuite.google.com/app/apikey

# Optional
DEFAULT_PROVIDER=gemini
DEBUG=False
LOG_LEVEL=INFO
```

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

## Project Structure

```
psyte/
├── app.py                    # Main Streamlit application
├── src/
│   ├── citation_analyzer.py  # Core analysis logic
│   ├── ai_providers.py       # Gemini AI integration
│   ├── web_searcher.py       # Web search for citations
│   ├── file_handlers.py      # File processing
│   └── utils.py              # Utility functions
├── ui/
│   ├── components.py         # UI components
│   └── styles.py            # Custom CSS with dark mode support
├── config/
│   └── settings.py          # Configuration
└── tests/                   # Test suite
```

## UI Features

### Design Philosophy
- **Minimalist**: Clean interface inspired by Google's design language
- **Colorful Accents**: Multi-colored logo with Google's signature colors
- **Focused**: No sidebar or distractions - just the task at hand
- **Responsive**: Works perfectly on desktop and mobile
- **Dark Mode**: Full support for system dark mode preferences
- **Professional**: Clean typography and subtle animations

### Key Interface Elements
- Multi-colored "Psyte" logo with letter-by-letter color scheme
- Search-box style text input with smooth hover effects
- Gradient primary buttons with depth and shadow
- Clean metric cards with colorful top borders on hover
- Professional status indicators (no emojis)
- Smooth animations and micro-interactions
- Web search integration badge

## Web Search Integration

Psyte automatically searches multiple academic databases to enhance your citations:

### Supported Databases
- **CrossRef**: Comprehensive database of scholarly publications
- **arXiv**: Repository for scientific preprints
- **Semantic Scholar**: AI-powered research tool

### Features
1. **Citation Verification**: Validates citations against real academic sources
2. **Missing Reference Detection**: Identifies statements that likely need citations
3. **Format Suggestions**: Provides properly formatted citations based on found sources
4. **No API Keys Required**: Uses free, public APIs for accessibility

### How It Works
1. Enable "Citation discovery" checkbox on the homepage
2. The system automatically:
   - Searches for each citation in academic databases
   - Identifies potential missing citations in your text
   - Suggests properly formatted citations
   - Provides links to original sources

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black .
flake8 .
```

### Adding New Citation Styles

1. Add patterns to `CITATION_PATTERNS` in `citation_analyzer.py`
2. Add style configuration to `CITATION_STYLES` in `settings.py`
3. The AI will automatically adapt to analyze the new style

## API Details

### Google Gemini API
- Models Available:
  - `gemini-2.5-flash-lite` - Fastest, most cost-effective (default)
  - `gemini-2.5-flash` - Balanced speed and quality
  - `gemini-2.5-pro` - Highest quality
  - `gemini-2.0-flash-lite` - Legacy lightweight model
  - `gemini-2.0-flash` - Legacy balanced model
  - `gemma-3-1b-it` - Open model variant
  - `gemma-3n-e2b-it` - Efficient Gemma variant
  - `gemma-3n-e4b-it` - Larger Gemma variant
- Automatic fallback between models when rate limits are reached
- Free tier includes 60 requests per minute
- Get your API key: https://makersuite.google.com/app/apikey

### Model Selection Presets
- **Speed Priority**: Fastest response times
- **Balanced**: Good balance of speed and quality
- **Quality Priority**: Most accurate results
- **Cost Effective**: Minimize API costs

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Gemini API key is valid and has not exceeded quota
2. **Rate Limit Errors**: The app automatically switches to backup models when rate limits are hit
3. **Dark Mode Issues**: The app automatically adapts to your system theme
4. **File Upload Errors**: Ensure files are under 10MB and in supported formats
5. **Analysis Errors**: Check that your text contains recognizable citations
6. **Model Status**: Check the Advanced Options to see which models are available

### Performance Tips

- For best results, include complete citations (not just in-text references)
- The AI works best with English-language citations
- Upload files in UTF-8 encoding when possible
- Use the Speed Priority preset for quick checks
- Use the Quality Priority preset for important documents

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google for the Gemini AI API
- Streamlit for the excellent web framework
- The academic community for citation standards

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: support@psyte.io
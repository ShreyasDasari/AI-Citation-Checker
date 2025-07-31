# AI Citation Checker - Project Structure

```
citation-checker/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── README.md                  # Project documentation
│
├── src/
│   ├── __init__.py
│   ├── citation_analyzer.py   # Core citation analysis logic
│   ├── ai_providers.py        # Gemini AI integration
│   ├── web_searcher.py        # Web search for citation verification
│   ├── file_handlers.py       # File upload and processing
│   └── utils.py               # Utility functions
│
├── ui/
│   ├── __init__.py
│   ├── components.py         # Reusable UI components
│   └── styles.py             # Custom CSS styles
│
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration settings
│
└── tests/
    ├── __init__.py
    └── test_citation_analyzer.py
```
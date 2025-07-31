import pytest
from src.citation_analyzer import Citation, CitationAnalyzer
from src.ai_providers import MockProvider
from src.utils import extract_year, extract_doi, validate_isbn

class TestCitation:
    """Test the Citation class"""
    
    def test_citation_creation(self):
        """Test creating a citation object"""
        citation = Citation(
            text="Smith, J. (2023). Test article. Journal, 1(1), 1-10.",
            style="apa",
            position=0
        )
        
        assert citation.text == "Smith, J. (2023). Test article. Journal, 1(1), 1-10."
        assert citation.style == "apa"
        assert citation.position == 0
        assert citation.is_valid is None
        assert citation.issues == []
        assert citation.suggestions == []
    
    def test_citation_to_dict(self):
        """Test converting citation to dictionary"""
        citation = Citation("Test citation", "mla", 10)
        citation.is_valid = True
        citation.confidence_score = 0.95
        
        result = citation.to_dict()
        
        assert result["text"] == "Test citation"
        assert result["style"] == "mla"
        assert result["position"] == 10
        assert result["is_valid"] is True
        assert result["confidence_score"] == 0.95

class TestCitationAnalyzer:
    """Test the CitationAnalyzer class"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer with mock provider"""
        return CitationAnalyzer(api_provider="mock", api_key=None)
    
    def test_extract_citations_comprehensive(self, analyzer):
        """Test extracting various citation formats"""
        text = """
        According to Vaswani et al. (2017), transformers are effective.
        Brown et al. (2020) demonstrated similar results.
        Recent studies [1] have shown this.
        As noted in [2], this is important.
        Smith (2021) argues differently.
        See reference [3] for more details.
        Lee and Kim (2020) found supporting evidence.
        This was confirmed (Johnson et al., 2019).
        References [4] through [6] discuss this.
        Clark (2022, p. 53) provides specific examples.
        The theory (Ng 2018) has been validated.
        """
        
        citations = analyzer._extract_citations(text)
        
        # Should find all 13 citations (including [4], [5], [6] if range is expanded)
        assert len(citations) >= 11  # At minimum 11 distinct citations
        
        # Check for various styles
        styles = set(c.style for c in citations)
        assert 'apa' in styles  # (Vaswani et al., 2017)
        assert 'ieee' in styles or 'chicago' in styles  # [1], [2], etc.
    
    def test_extract_citations_mla(self, analyzer):
        """Test extracting MLA citations"""
        text = """
        Smith argues that this is important (45).
        According to Johnson, "this is a quote" (Smith 123).
        """
        
        citations = analyzer._extract_citations(text)
        
        assert len(citations) >= 1
        assert any("Smith 123" in c.text for c in citations)
    
    def test_detect_citation_style(self, analyzer):
        """Test citation style detection"""
        apa_citations = [
            Citation("(Smith, 2023)", "apa", 0),
            Citation("(Johnson & Lee, 2022)", "apa", 10),
            Citation("Smith (2023)", "apa", 20)
        ]
        
        style = analyzer._detect_citation_style(apa_citations)
        assert style == "apa"
    
    def test_empty_citations(self, analyzer):
        """Test handling empty citation list"""
        style = analyzer._detect_citation_style([])
        assert style == "unknown"

class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_extract_year(self):
        """Test year extraction"""
        assert extract_year("Smith (2023)") == 2023
        assert extract_year("Published in 1995") == 1995
        assert extract_year("No year here") is None
    
    def test_extract_doi(self):
        """Test DOI extraction"""
        text = "Available at: https://doi.org/10.1234/example.doi"
        assert extract_doi(text) == "10.1234/example.doi"
        
        text_no_doi = "No DOI in this text"
        assert extract_doi(text_no_doi) is None
    
    def test_validate_isbn(self):
        """Test ISBN validation"""
        # Valid ISBN-13
        assert validate_isbn("978-0-596-52068-7") is True
        
        # Invalid ISBN
        assert validate_isbn("123-456-789") is False
        
        # Invalid format
        assert validate_isbn("not-an-isbn") is False

class TestIntegration:
    """Integration tests"""
    
    def test_full_analysis_flow(self):
        """Test complete analysis workflow"""
        analyzer = CitationAnalyzer(api_provider="mock", api_key=None)
        
        text = """
        Recent research (Smith, 2023) has shown significant results.
        This is supported by Johnson and Lee (2022), who found similar patterns.
        
        References:
        Smith, J. (2023). Understanding patterns. Science Journal, 45(2), 123-145.
        Johnson, M., & Lee, K. (2022). Pattern analysis. Nature, 500, 45-67.
        """
        
        results = analyzer.analyze(text)
        
        assert "summary" in results
        assert "citations" in results
        assert results["summary"]["total_citations"] > 0
        assert isinstance(results["citations"], list)

# Run tests with: pytest tests/
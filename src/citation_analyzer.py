# import re
# from typing import List, Dict, Any, Optional
# from datetime import datetime
# from src.ai_providers import AIProvider, GeminiProvider, MockProvider
# from src.web_searcher import WebSearcher
# import json

# class Citation:
#     """Represents a single citation"""
#     def __init__(self, text: str, style: str = "unknown", position: int = 0):
#         self.text = text
#         self.style = style
#         self.position = position
#         self.is_valid = None
#         self.issues = []
#         self.suggestions = []
#         self.confidence_score = 0.0
#         self.model_used = None
        
#     def to_dict(self) -> Dict[str, Any]:
#         result = {
#             "text": self.text,
#             "style": self.style,
#             "position": self.position,
#             "is_valid": self.is_valid,
#             "issues": self.issues,
#             "suggestions": self.suggestions,
#             "confidence_score": self.confidence_score
#         }
#         if self.model_used:
#             result["model_used"] = self.model_used
#         return result

# class CitationAnalyzer:
#     """Main citation analysis engine"""
    
#     # Improved citation patterns - more comprehensive and accurate
#     CITATION_PATTERNS = {
#         # In-text citations
#         'apa_parenthetical': r'\([A-Z][A-Za-z\-\']+(?:\s+(?:et\s+al\.?|&|and)\s+[A-Z][A-Za-z\-\']+)*(?:,\s*\d{4}(?:[a-z])?(?:,\s*p+\.?\s*\d+(?:-\d+)?)?)\)',
#         'apa_narrative': r'\b[A-Z][A-Za-z\-\']+(?:\s+(?:et\s+al\.?|and)\s+[A-Z][A-Za-z\-\']+)*\s+\(\d{4}(?:[a-z])?(?:,\s*p+\.?\s*\d+(?:-\d+)?)?\)',
#         'mla_parenthetical': r'\([A-Z][A-Za-z\-\']+(?:\s+(?:et\s+al\.?|and)\s+[A-Z][A-Za-z\-\']+)*(?:\s+\d+(?:-\d+)?)\)',
#         'mla_with_page': r'\([A-Z][A-Za-z\-\']+\s+\d{4},\s*p\.?\s*\d+(?:-\d+)?\)',
#         'chicago_note': r'\[\d+(?:[-–]\d+)?\]',
#         'ieee_numeric': r'\[\d+\]',
#         'numeric_range': r'\[\d+\]\s*(?:through|to|-|–)\s*\[\d+\]',
#         'harvard_parenthetical': r'\([A-Z][A-Za-z\-\']+(?:\s+(?:et\s+al\.?|&|and)\s+[A-Z][A-Za-z\-\']+)*\s+\d{4}(?:[a-z])?(?::\s*\d+(?:-\d+)?)?\)',
#         'harvard_narrative': r'\b[A-Z][A-Za-z\-\']+(?:\s+(?:et\s+al\.?|and)\s+[A-Z][A-Za-z\-\']+)*\s+\(\d{4}(?:[a-z])?\)',
#         'simple_year_parenthetical': r'\([A-Z][A-Za-z\-\']+\s+\d{4}\)',
        
#         # Reference list patterns
#         'apa_reference': r'^[A-Z][A-Za-z\-\']+,\s+[A-Z]\.(?:\s*[A-Z]\.)*(?:,\s*&\s*[A-Z][A-Za-z\-\']+,\s+[A-Z]\.(?:\s*[A-Z]\.)*)*\s*\(\d{4}\)\.?\s+.+',
#         'mla_reference': r'^[A-Z][A-Za-z\-\']+,\s+[A-Z][a-z]+\.?\s+"[^"]+\.?"',
#         'chicago_reference': r'^[A-Z][A-Za-z\-\']+,\s+[A-Z][a-z]+\.?\s+.+\.\s+[A-Z][a-z]+:\s+.+,\s+\d{4}\.',
#         'harvard_reference': r'^[A-Z][A-Za-z\-\']+,\s+[A-Z]\.(?:\s*[A-Z]\.)*\s+\d{4},\s+.+',
#     }
    
#     def __init__(self, api_provider: str = "gemini", api_key: Optional[str] = None, mcp_enabled: bool = False, enable_web_search: bool = True, preferred_model: Optional[str] = None):
#         self.api_provider = self._initialize_provider(api_provider, api_key, preferred_model)
#         self.mcp_enabled = False  # External verification disabled for now
#         self.enable_web_search = enable_web_search
#         self.web_searcher = WebSearcher() if enable_web_search else None
        
#     def _initialize_provider(self, provider_name: str, api_key: Optional[str], preferred_model: Optional[str] = None) -> AIProvider:
#         """Initialize the AI provider"""
#         if provider_name == "gemini":
#             return GeminiProvider(api_key, preferred_model)
#         elif provider_name == "mock":
#             return MockProvider()
#         else:
#             raise ValueError(f"Unknown provider: {provider_name}")
    
#     def analyze(self, text: str) -> Dict[str, Any]:
#         """Main analysis method"""
#         # Extract citations
#         citations = self._extract_citations(text)
        
#         # Detect citation style
#         detected_style = self._detect_citation_style(citations)
        
#         # Analyze each citation
#         analyzed_citations = []
#         for citation in citations:
#             analyzed = self._analyze_single_citation(citation, detected_style)
#             analyzed_citations.append(analyzed)
        
#         # Generate overall report
#         report = self._generate_report(text, analyzed_citations, detected_style)
        
#         # Add web search results if enabled
#         if self.enable_web_search and self.web_searcher:
#             report = self._enhance_with_web_search(text, report, analyzed_citations)
        
#         return report
    
#     def _extract_citations(self, text: str) -> List[Citation]:
#         """Extract all citations from the text - improved version"""
#         citations = []
#         seen_positions = set()  # Track positions to avoid duplicates
        
#         # First, handle "References [X] through [Y]" pattern
#         ref_range_pattern = r'[Rr]eferences\s*\[(\d+)\]\s*through\s*\[(\d+)\]'
#         for match in re.finditer(ref_range_pattern, text):
#             start_num = int(match.group(1))
#             end_num = int(match.group(2))
#             # Add each number in the range as individual citations
#             for num in range(start_num, end_num + 1):
#                 # Check if this number exists as an individual citation
#                 individual_pattern = rf'\[{num}\]'
#                 ind_matches = list(re.finditer(individual_pattern, text))
#                 if ind_matches:
#                     # Use the actual position of the individual citation
#                     for ind_match in ind_matches:
#                         if ind_match.start() not in seen_positions:
#                             citation = Citation(
#                                 text=f'[{num}]',
#                                 style='ieee',
#                                 position=ind_match.start()
#                             )
#                             citations.append(citation)
#                             seen_positions.add(ind_match.start())
        
#         # Handle regular patterns
#         for style, pattern in self.CITATION_PATTERNS.items():
#             if 'numeric_range' in style:
#                 continue  # Skip range pattern
                
#             try:
#                 matches = re.finditer(pattern, text, re.MULTILINE)
#                 for match in matches:
#                     position = match.start()
                    
#                     # Skip if position already seen
#                     if position in seen_positions:
#                         continue
                    
#                     citation_text = match.group(0).strip()
#                     seen_positions.add(position)
                    
#                     citation = Citation(
#                         text=citation_text,
#                         style=style.split('_')[0],
#                         position=position
#                     )
#                     citations.append(citation)
#             except re.error:
#                 print(f"Invalid regex pattern for {style}")
#                 continue
        
#         # Sort by position
#         citations.sort(key=lambda x: x.position)
        
#         # Final deduplication pass
#         filtered_citations = []
#         last_end = -1
        
#         for citation in citations:
#             citation_start = citation.position
#             citation_end = citation.position + len(citation.text)
            
#             # Keep if non-overlapping
#             if citation_start >= last_end:
#                 filtered_citations.append(citation)
#                 last_end = citation_end
        
#         return filtered_citations
    
#     def _detect_citation_style(self, citations: List[Citation]) -> str:
#         """Detect the predominant citation style"""
#         if not citations:
#             return "unknown"
        
#         # Count style occurrences
#         style_counts = {}
#         for citation in citations:
#             style = citation.style
#             if style != 'unknown':
#                 style_counts[style] = style_counts.get(style, 0) + 1
        
#         if not style_counts:
#             return "mixed"
        
#         # Return the most common style
#         return max(style_counts, key=style_counts.get)
    
#     def _analyze_single_citation(self, citation: Citation, expected_style: str) -> Citation:
#         """Analyze a single citation using AI"""
#         # For numeric citations, apply simpler validation
#         if citation.style in ['ieee', 'chicago'] and re.match(r'^\[\d+\]$', citation.text):
#             citation.is_valid = True
#             citation.confidence_score = 0.95
#             return citation
            
#         # For range citations like "[4] through [6]", validate directly
#         if re.match(r'\[\d+\]\s*(?:through|to|and|-|–)\s*\[\d+\]', citation.text):
#             citation.is_valid = True
#             citation.confidence_score = 0.95
#             return citation
        
#         # Use rule-based validation for common patterns
#         if self._is_valid_by_rules(citation):
#             citation.is_valid = True
#             citation.confidence_score = 0.9
#             return citation
        
#         # Only use AI for complex citations
#         prompt = f"""
#         Analyze this citation: "{citation.text}"
#         Citation style detected: {citation.style}
#         Expected document style: {expected_style}
        
#         Please check:
#         1. Is this a valid {citation.style} style citation?
#         2. What formatting issues exist (if any)?
#         3. What specific improvements would make it better?
        
#         Common valid patterns:
#         - APA: (Author, Year) or Author (Year)
#         - MLA: (Author Page) or (Author Year, p. Page)
#         - Chicago/IEEE: [Number] or (Number)
#         - Harvard: (Author Year) or Author (Year)
        
#         Respond in JSON format:
#         {{
#             "is_valid": boolean,
#             "confidence_score": float (0-1),
#             "issues": ["specific issue 1", "specific issue 2"],
#             "suggestions": ["specific suggestion 1", "specific suggestion 2"]
#         }}
#         """
        
#         try:
#             response = self.api_provider.analyze_citation(prompt)
#             result = json.loads(response)
            
#             citation.is_valid = result.get("is_valid", False)
#             citation.confidence_score = result.get("confidence_score", 0.0)
#             citation.issues = result.get("issues", [])
#             citation.suggestions = result.get("suggestions", [])
#             citation.model_used = result.get("model_used", "unknown")
            
#         except Exception as e:
#             citation.is_valid = None
#             citation.issues = [f"Analysis error: {str(e)}"]
            
#         return citation
    
#     def _is_valid_by_rules(self, citation: Citation) -> bool:
#         """Apply rule-based validation for common citation patterns"""
#         text = citation.text.strip()
        
#         # Numeric citations [1], [2], etc.
#         if re.match(r'^\[\d+\]$', text):
#             return True
            
#         # Numeric ranges
#         if re.match(r'^\[\d+\]\s*(?:through|to|and|-|–)\s*\[\d+\]$', text):
#             return True
        
#         # Basic APA: (Author, Year) or Author (Year)
#         if re.match(r'^\([A-Z][a-z]+(?:\s+et\s+al\.?)?,\s*\d{4}\)$', text):
#             return True
#         if re.match(r'^[A-Z][a-z]+(?:\s+et\s+al\.?)?\s+\(\d{4}\)$', text):
#             return True
            
#         # APA with multiple authors
#         if re.match(r'^\([A-Z][a-z]+\s+(?:&|and)\s+[A-Z][a-z]+,\s*\d{4}\)$', text):
#             return True
#         if re.match(r'^[A-Z][a-z]+\s+(?:and|&)\s+[A-Z][a-z]+\s+\(\d{4}\)$', text):
#             return True
        
#         # Basic Harvard: (Author Year)
#         if re.match(r'^\([A-Z][a-z]+(?:\s+et\s+al\.?)?\s+\d{4}\)$', text):
#             return True
        
#         # MLA with page: (Author Year, p. X)
#         if re.match(r'^\([A-Z][a-z]+\s+\d{4},\s*p\.?\s*\d+\)$', text):
#             return True
        
#         return False
    
#     def _generate_report(self, text: str, citations: List[Citation], style: str) -> Dict[str, Any]:
#         """Generate comprehensive analysis report"""
#         total_citations = len(citations)
#         valid_citations = sum(1 for c in citations if c.is_valid is True)
#         invalid_citations = sum(1 for c in citations if c.is_valid is False)
#         uncertain_citations = sum(1 for c in citations if c.is_valid is None)
        
#         # Calculate overall score
#         if total_citations > 0:
#             validity_score = (valid_citations / total_citations) * 100
#             avg_confidence = sum(c.confidence_score for c in citations) / total_citations
#         else:
#             validity_score = 0
#             avg_confidence = 0
        
#         # Get model used for analysis
#         model_used = None
#         if hasattr(self.api_provider, 'model_name'):
#             model_used = self.api_provider.model_name
        
#         # Common issues
#         all_issues = []
#         for c in citations:
#             all_issues.extend(c.issues)
        
#         issue_counts = {}
#         for issue in all_issues:
#             issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
#         common_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
#         return {
#             "summary": {
#                 "total_citations": total_citations,
#                 "valid_citations": valid_citations,
#                 "invalid_citations": invalid_citations,
#                 "uncertain_citations": uncertain_citations,
#                 "detected_style": style,
#                 "validity_score": validity_score,
#                 "average_confidence": avg_confidence,
#                 "analysis_timestamp": datetime.now().isoformat(),
#                 "model_used": model_used
#             },
#             "citations": [c.to_dict() for c in citations],
#             "common_issues": common_issues,
#             "recommendations": self._generate_recommendations(citations, style),
#             "text_length": len(text),
#             "citation_density": (total_citations / len(text.split())) * 100 if text else 0
#         }
    
#     def _generate_recommendations(self, citations: List[Citation], style: str) -> List[str]:
#         """Generate overall recommendations"""
#         recommendations = []
        
#         # Style consistency
#         styles = set(c.style for c in citations)
#         if len(styles) > 1:
#             recommendations.append("Consider using a consistent citation style throughout your document.")
        
#         # Common issues
#         issue_types = {}
#         for c in citations:
#             for issue in c.issues:
#                 issue_type = issue.split(':')[0] if ':' in issue else issue
#                 issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
        
#         if issue_types:
#             most_common = max(issue_types, key=issue_types.get)
#             recommendations.append(f"Address recurring issue: {most_common}")
        
#         # Style-specific recommendations
#         if style == "apa":
#             recommendations.append("Ensure all in-text citations have corresponding reference list entries.")
#             recommendations.append("Use '&' in parenthetical citations and 'and' in narrative citations.")
#         elif style == "mla":
#             recommendations.append("Include page numbers for all direct quotes.")
#             recommendations.append("Use signal phrases to introduce citations smoothly.")
#         elif style == "chicago":
#             recommendations.append("Maintain consistency between footnotes and bibliography entries.")
#         elif style == "ieee":
#             recommendations.append("Number citations consecutively in order of appearance.")
            
#         return recommendations[:5]  # Limit to top 5 recommendations
    
#     def _enhance_with_web_search(self, text: str, report: Dict[str, Any], citations: List[Citation]) -> Dict[str, Any]:
#         """Enhance report with web search results"""
#         if not self.web_searcher:
#             return report
        
#         # Only search for a sample of citations to speed up
#         max_searches = 5
#         searched = 0
        
#         # Search for missing references (limit to first few)
#         missing_refs = self.web_searcher.find_missing_references(text[:1000])  # Only check first 1000 chars
#         if missing_refs:
#             report["missing_references"] = missing_refs[:3]  # Limit to 3
#             report["recommendations"].insert(0, f"Found {len(missing_refs)} potential missing citations that need references.")
        
#         # Enhance only a few citations with web search
#         for i, citation in enumerate(citations):
#             if searched >= max_searches:
#                 break
                
#             # Skip numeric citations - they don't need web search
#             if citation.style in ['ieee', 'chicago'] and re.match(r'^\[\d+\]', citation.text):
#                 continue
                
#             try:
#                 search_results = self.web_searcher.search_for_citation(citation.text)
                
#                 if search_results["found"]:
#                     searched += 1
#                     # Add search results to citation
#                     report["citations"][i]["web_search"] = {
#                         "found": True,
#                         "sources": search_results["sources"][:1],  # Only top match
#                         "suggestions": search_results["suggestions"][:2]
#                     }
                    
#                     # Add web-based suggestions
#                     if search_results["suggestions"]:
#                         report["citations"][i]["suggestions"].extend(search_results["suggestions"][:1])
#             except:
#                 # Skip on any error
#                 continue
        
#         # Update summary with web search info
#         web_enhanced = sum(1 for c in report["citations"] if "web_search" in c and c["web_search"]["found"])
#         report["summary"]["web_enhanced_citations"] = web_enhanced
        
#         return report

import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.ai_providers import AIProvider, GeminiProvider, MockProvider
from src.web_searcher import WebSearcher
from src.doi_validator import DOIValidator
import json

class Citation:
    """Represents a single citation"""
    def __init__(self, text: str, style: str = "unknown", position: int = 0):
        self.text = text
        self.style = style
        self.position = position
        self.is_valid = None
        self.issues = []
        self.suggestions = []
        self.confidence_score = 0.0
        self.model_used = None
        self.doi = None
        self.doi_valid = None
        self.doi_data = None
        
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "text": self.text,
            "style": self.style,
            "position": self.position,
            "is_valid": self.is_valid,
            "issues": self.issues,
            "suggestions": self.suggestions,
            "confidence_score": self.confidence_score
        }
        if self.model_used:
            result["model_used"] = self.model_used
        if self.doi:
            result["doi"] = self.doi
            result["doi_valid"] = self.doi_valid
            if self.doi_data:
                result["doi_data"] = self.doi_data
        return result

class CitationAnalyzer:
    """Main citation analysis engine"""
    
    # Improved citation patterns - more comprehensive and accurate
    CITATION_PATTERNS = {
        # In-text citations
        'apa_parenthetical': r'\([A-Z][A-Za-z\-\']+(?:\s+(?:et\s+al\.?|&|and)\s+[A-Z][A-Za-z\-\']+)*(?:,\s*\d{4}(?:[a-z])?(?:,\s*p+\.?\s*\d+(?:-\d+)?)?)\)',
        'apa_narrative': r'\b[A-Z][A-Za-z\-\']+(?:\s+(?:et\s+al\.?|and)\s+[A-Z][A-Za-z\-\']+)*\s+\(\d{4}(?:[a-z])?(?:,\s*p+\.?\s*\d+(?:-\d+)?)?\)',
        'mla_parenthetical': r'\([A-Z][A-Za-z\-\']+(?:\s+(?:et\s+al\.?|and)\s+[A-Z][A-Za-z\-\']+)*(?:\s+\d+(?:-\d+)?)\)',
        'mla_with_page': r'\([A-Z][A-Za-z\-\']+\s+\d{4},\s*p\.?\s*\d+(?:-\d+)?\)',
        'chicago_note': r'\[\d+(?:[-–]\d+)?\]',
        'ieee_numeric': r'\[\d+\]',
        'numeric_range': r'\[\d+\]\s*(?:through|to|-|–)\s*\[\d+\]',
        'harvard_parenthetical': r'\([A-Z][A-Za-z\-\']+(?:\s+(?:et\s+al\.?|&|and)\s+[A-Z][A-Za-z\-\']+)*\s+\d{4}(?:[a-z])?(?::\s*\d+(?:-\d+)?)?\)',
        'harvard_narrative': r'\b[A-Z][A-Za-z\-\']+(?:\s+(?:et\s+al\.?|and)\s+[A-Z][A-Za-z\-\']+)*\s+\(\d{4}(?:[a-z])?\)',
        'simple_year_parenthetical': r'\([A-Z][A-Za-z\-\']+\s+\d{4}\)',
        
        # Reference list patterns
        'apa_reference': r'^[A-Z][A-Za-z\-\']+,\s+[A-Z]\.(?:\s*[A-Z]\.)*(?:,\s*&\s*[A-Z][A-Za-z\-\']+,\s+[A-Z]\.(?:\s*[A-Z]\.)*)*\s*\(\d{4}\)\.?\s+.+',
        'mla_reference': r'^[A-Z][A-Za-z\-\']+,\s+[A-Z][a-z]+\.?\s+"[^"]+\.?"',
        'chicago_reference': r'^[A-Z][A-Za-z\-\']+,\s+[A-Z][a-z]+\.?\s+.+\.\s+[A-Z][a-z]+:\s+.+,\s+\d{4}\.',
        'harvard_reference': r'^[A-Z][A-Za-z\-\']+,\s+[A-Z]\.(?:\s*[A-Z]\.)*\s+\d{4},\s+.+',
    }
    
    def __init__(self, api_provider: str = "gemini", api_key: Optional[str] = None, mcp_enabled: bool = False, enable_web_search: bool = True, preferred_model: Optional[str] = None):
        self.api_provider = self._initialize_provider(api_provider, api_key, preferred_model)
        self.mcp_enabled = False  # External verification disabled for now
        self.enable_web_search = enable_web_search
        self.web_searcher = WebSearcher() if enable_web_search else None
        self.doi_validator = DOIValidator()
        
    def _initialize_provider(self, provider_name: str, api_key: Optional[str], preferred_model: Optional[str] = None) -> AIProvider:
        """Initialize the AI provider"""
        if provider_name == "gemini":
            return GeminiProvider(api_key, preferred_model)
        elif provider_name == "mock":
            return MockProvider()
        else:
            raise ValueError(f"Unknown provider: {provider_name}")
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """Main analysis method"""
        # Extract citations
        citations = self._extract_citations(text)
        
        # Detect citation style
        detected_style = self._detect_citation_style(citations)
        
        # Analyze each citation
        analyzed_citations = []
        for citation in citations:
            analyzed = self._analyze_single_citation(citation, detected_style)
            analyzed_citations.append(analyzed)
        
        # Validate DOIs in citations
        doi_results = self._validate_citation_dois(analyzed_citations)
        
        # Generate overall report
        report = self._generate_report(text, analyzed_citations, detected_style)
        
        # Add DOI validation results
        if doi_results['total_dois_found'] > 0:
            report['doi_validation'] = doi_results
        
        # Add web search results if enabled
        if self.enable_web_search and self.web_searcher:
            report = self._enhance_with_web_search(text, report, analyzed_citations)
        
        return report
    
    def _extract_citations(self, text: str) -> List[Citation]:
        """Extract all citations from the text - improved version"""
        citations = []
        seen_positions = set()  # Track positions to avoid duplicates
        
        # First, handle "References [X] through [Y]" pattern
        ref_range_pattern = r'[Rr]eferences\s*\[(\d+)\]\s*through\s*\[(\d+)\]'
        for match in re.finditer(ref_range_pattern, text):
            start_num = int(match.group(1))
            end_num = int(match.group(2))
            # Add each number in the range as individual citations
            for num in range(start_num, end_num + 1):
                # Check if this number exists as an individual citation
                individual_pattern = rf'\[{num}\]'
                ind_matches = list(re.finditer(individual_pattern, text))
                if ind_matches:
                    # Use the actual position of the individual citation
                    for ind_match in ind_matches:
                        if ind_match.start() not in seen_positions:
                            citation = Citation(
                                text=f'[{num}]',
                                style='ieee',
                                position=ind_match.start()
                            )
                            citations.append(citation)
                            seen_positions.add(ind_match.start())
        
        # Handle regular patterns
        for style, pattern in self.CITATION_PATTERNS.items():
            if 'numeric_range' in style:
                continue  # Skip range pattern
                
            try:
                matches = re.finditer(pattern, text, re.MULTILINE)
                for match in matches:
                    position = match.start()
                    
                    # Skip if position already seen
                    if position in seen_positions:
                        continue
                    
                    citation_text = match.group(0).strip()
                    seen_positions.add(position)
                    
                    citation = Citation(
                        text=citation_text,
                        style=style.split('_')[0],
                        position=position
                    )
                    citations.append(citation)
            except re.error:
                print(f"Invalid regex pattern for {style}")
                continue
        
        # Sort by position
        citations.sort(key=lambda x: x.position)
        
        # Final deduplication pass
        filtered_citations = []
        last_end = -1
        
        for citation in citations:
            citation_start = citation.position
            citation_end = citation.position + len(citation.text)
            
            # Keep if non-overlapping
            if citation_start >= last_end:
                filtered_citations.append(citation)
                last_end = citation_end
        
        return filtered_citations
    
    def _detect_citation_style(self, citations: List[Citation]) -> str:
        """Detect the predominant citation style"""
        if not citations:
            return "unknown"
        
        # Count style occurrences
        style_counts = {}
        for citation in citations:
            style = citation.style
            if style != 'unknown':
                style_counts[style] = style_counts.get(style, 0) + 1
        
        if not style_counts:
            return "mixed"
        
        # Return the most common style
        return max(style_counts, key=style_counts.get)
    
    def _analyze_single_citation(self, citation: Citation, expected_style: str) -> Citation:
        """Analyze a single citation using AI"""
        # For numeric citations, apply simpler validation
        if citation.style in ['ieee', 'chicago'] and re.match(r'^\[\d+\]$', citation.text):
            citation.is_valid = True
            citation.confidence_score = 0.95
            return citation
            
        # For range citations like "[4] through [6]", validate directly
        if re.match(r'\[\d+\]\s*(?:through|to|and|-|–)\s*\[\d+\]', citation.text):
            citation.is_valid = True
            citation.confidence_score = 0.95
            return citation
        
        # Use rule-based validation for common patterns
        if self._is_valid_by_rules(citation):
            citation.is_valid = True
            citation.confidence_score = 0.9
            return citation
        
        # Only use AI for complex citations
        prompt = f"""
        Analyze this citation: "{citation.text}"
        Citation style detected: {citation.style}
        Expected document style: {expected_style}
        
        Please check:
        1. Is this a valid {citation.style} style citation?
        2. What formatting issues exist (if any)?
        3. What specific improvements would make it better?
        
        Common valid patterns:
        - APA: (Author, Year) or Author (Year)
        - MLA: (Author Page) or (Author Year, p. Page)
        - Chicago/IEEE: [Number] or (Number)
        - Harvard: (Author Year) or Author (Year)
        
        Respond in JSON format:
        {{
            "is_valid": boolean,
            "confidence_score": float (0-1),
            "issues": ["specific issue 1", "specific issue 2"],
            "suggestions": ["specific suggestion 1", "specific suggestion 2"]
        }}
        """
        
        try:
            response = self.api_provider.analyze_citation(prompt)
            result = json.loads(response)
            
            citation.is_valid = result.get("is_valid", False)
            citation.confidence_score = result.get("confidence_score", 0.0)
            citation.issues = result.get("issues", [])
            citation.suggestions = result.get("suggestions", [])
            citation.model_used = result.get("model_used", "unknown")
            
        except Exception as e:
            citation.is_valid = None
            citation.issues = [f"Analysis error: {str(e)}"]
            
        return citation
    
    def _is_valid_by_rules(self, citation: Citation) -> bool:
        """Apply rule-based validation for common citation patterns"""
        text = citation.text.strip()
        
        # Numeric citations [1], [2], etc.
        if re.match(r'^\[\d+\]$', text):
            return True
            
        # Numeric ranges
        if re.match(r'^\[\d+\]\s*(?:through|to|and|-|–)\s*\[\d+\]$', text):
            return True
        
        # Basic APA: (Author, Year) or Author (Year)
        if re.match(r'^\([A-Z][a-z]+(?:\s+et\s+al\.?)?,\s*\d{4}\)$', text):
            return True
        if re.match(r'^[A-Z][a-z]+(?:\s+et\s+al\.?)?\s+\(\d{4}\)$', text):
            return True
            
        # APA with multiple authors
        if re.match(r'^\([A-Z][a-z]+\s+(?:&|and)\s+[A-Z][a-z]+,\s*\d{4}\)$', text):
            return True
        if re.match(r'^[A-Z][a-z]+\s+(?:and|&)\s+[A-Z][a-z]+\s+\(\d{4}\)$', text):
            return True
        
        # Basic Harvard: (Author Year)
        if re.match(r'^\([A-Z][a-z]+(?:\s+et\s+al\.?)?\s+\d{4}\)$', text):
            return True
        
        # MLA with page: (Author Year, p. X)
        if re.match(r'^\([A-Z][a-z]+\s+\d{4},\s*p\.?\s*\d+\)$', text):
            return True
        
        return False
    
    def _validate_citation_dois(self, citations: List[Citation]) -> Dict[str, Any]:
        """Validate DOIs found in citations"""
        doi_results = []
        
        for citation in citations:
            # Extract DOIs from citation text
            dois = self.doi_validator.extract_dois_from_text(citation.text)
            
            if dois:
                for doi in dois:
                    result = self.doi_validator.get_publication_info(doi)
                    
                    # Store DOI info in citation object
                    citation.doi = doi
                    citation.doi_valid = result['success']
                    if result['success']:
                        citation.doi_data = result.get('data')
                    
                    doi_results.append({
                        'citation': citation.text,
                        'doi': doi,
                        'valid': result['success'],
                        'data': result.get('data') if result['success'] else None,
                        'error': result.get('error') if not result['success'] else None
                    })
        
        return {
            'total_dois_found': len(doi_results),
            'valid_dois': sum(1 for r in doi_results if r['valid']),
            'invalid_dois': sum(1 for r in doi_results if not r['valid']),
            'results': doi_results
        }
    
    def _generate_report(self, text: str, citations: List[Citation], style: str) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        total_citations = len(citations)
        valid_citations = sum(1 for c in citations if c.is_valid is True)
        invalid_citations = sum(1 for c in citations if c.is_valid is False)
        uncertain_citations = sum(1 for c in citations if c.is_valid is None)
        
        # Calculate overall score
        if total_citations > 0:
            validity_score = (valid_citations / total_citations) * 100
            avg_confidence = sum(c.confidence_score for c in citations) / total_citations
        else:
            validity_score = 0
            avg_confidence = 0
        
        # Get model used for analysis
        model_used = None
        if hasattr(self.api_provider, 'model_name'):
            model_used = self.api_provider.model_name
        
        # Common issues
        all_issues = []
        for c in citations:
            all_issues.extend(c.issues)
        
        issue_counts = {}
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        common_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "summary": {
                "total_citations": total_citations,
                "valid_citations": valid_citations,
                "invalid_citations": invalid_citations,
                "uncertain_citations": uncertain_citations,
                "detected_style": style,
                "validity_score": validity_score,
                "average_confidence": avg_confidence,
                "analysis_timestamp": datetime.now().isoformat(),
                "model_used": model_used
            },
            "citations": [c.to_dict() for c in citations],
            "common_issues": common_issues,
            "recommendations": self._generate_recommendations(citations, style),
            "text_length": len(text),
            "citation_density": (total_citations / len(text.split())) * 100 if text else 0
        }
    
    def _generate_recommendations(self, citations: List[Citation], style: str) -> List[str]:
        """Generate overall recommendations"""
        recommendations = []
        
        # Style consistency
        styles = set(c.style for c in citations)
        if len(styles) > 1:
            recommendations.append("Consider using a consistent citation style throughout your document.")
        
        # Common issues
        issue_types = {}
        for c in citations:
            for issue in c.issues:
                issue_type = issue.split(':')[0] if ':' in issue else issue
                issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
        
        if issue_types:
            most_common = max(issue_types, key=issue_types.get)
            recommendations.append(f"Address recurring issue: {most_common}")
        
        # DOI recommendations
        dois_found = sum(1 for c in citations if c.doi)
        if dois_found > 0:
            recommendations.append(f"Found {dois_found} DOI(s) - verify they are correct and accessible.")
        
        # Style-specific recommendations
        if style == "apa":
            recommendations.append("Ensure all in-text citations have corresponding reference list entries.")
            recommendations.append("Use '&' in parenthetical citations and 'and' in narrative citations.")
        elif style == "mla":
            recommendations.append("Include page numbers for all direct quotes.")
            recommendations.append("Use signal phrases to introduce citations smoothly.")
        elif style == "chicago":
            recommendations.append("Maintain consistency between footnotes and bibliography entries.")
        elif style == "ieee":
            recommendations.append("Number citations consecutively in order of appearance.")
            
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _enhance_with_web_search(self, text: str, report: Dict[str, Any], citations: List[Citation]) -> Dict[str, Any]:
        """Enhance report with web search results"""
        if not self.web_searcher:
            return report
        
        # Only search for a sample of citations to speed up
        max_searches = 5
        searched = 0
        
        # Search for missing references (limit to first few)
        missing_refs = self.web_searcher.find_missing_references(text[:1000])  # Only check first 1000 chars
        if missing_refs:
            report["missing_references"] = missing_refs[:3]  # Limit to 3
            report["recommendations"].insert(0, f"Found {len(missing_refs)} potential missing citations that need references.")
        
        # Enhance only a few citations with web search
        for i, citation in enumerate(citations):
            if searched >= max_searches:
                break
                
            # Skip numeric citations - they don't need web search
            if citation.style in ['ieee', 'chicago'] and re.match(r'^\[\d+\]', citation.text):
                continue
                
            try:
                search_results = self.web_searcher.search_for_citation(citation.text)
                
                if search_results["found"]:
                    searched += 1
                    # Add search results to citation
                    report["citations"][i]["web_search"] = {
                        "found": True,
                        "sources": search_results["sources"][:1],  # Only top match
                        "suggestions": search_results["suggestions"][:2]
                    }
                    
                    # Add web-based suggestions
                    if search_results["suggestions"]:
                        report["citations"][i]["suggestions"].extend(search_results["suggestions"][:1])
            except:
                # Skip on any error
                continue
        
        # Update summary with web search info
        web_enhanced = sum(1 for c in report["citations"] if "web_search" in c and c["web_search"]["found"])
        report["summary"]["web_enhanced_citations"] = web_enhanced
        
        return report
import requests
from typing import List, Dict, Any, Optional
import urllib.parse
import json
from datetime import datetime
import time
import re

class WebSearcher:
    """Web search functionality for finding and verifying citations"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Psyte/1.0 (Academic Citation Checker) Mozilla/5.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        
        # Free API endpoints that don't require keys
        self.search_engines = {
            'crossref': 'https://api.crossref.org/works',
            'arxiv': 'http://export.arxiv.org/api/query',
            'semantic_scholar': 'https://api.semanticscholar.org/graph/v1/paper/search'
        }
        
        self.timeout = 15  # Reduced timeout for faster response
        self.max_retries = 2  # Reduced retries
        self.retry_delay = 1  # seconds
    
    def search_for_citation(self, citation_text: str, citation_type: str = "auto") -> Dict[str, Any]:
        """Search for a citation across multiple sources"""
        results = {
            "found": False,
            "sources": [],
            "suggestions": [],
            "missing_references": []
        }
        
        # Extract key information from citation
        search_query = self._build_search_query(citation_text)
        
        if not search_query or len(search_query) < 3:
            return results
        
        # Only try one search engine to speed up
        try:
            # Try CrossRef first as it's most comprehensive
            crossref_results = self._search_crossref(search_query)
            if crossref_results:
                results["found"] = True
                results["sources"].extend(crossref_results[:2])  # Limit results
                results["suggestions"] = self._generate_suggestions(citation_text, results["sources"])
                return results
        except:
            pass
        
        return results
    
    def find_missing_references(self, text: str) -> List[Dict[str, Any]]:
        """Find potential missing references in text"""
        missing_refs = []
        
        # Only check first 1000 characters to speed up
        text_to_check = text[:1000] if len(text) > 1000 else text
        
        # Look for common patterns that might indicate missing citations
        patterns = [
            r'(?:According to|As stated by|Research by|Studies by)\s+([A-Z][a-z]+(?:\s+(?:and|&)\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+(?:\s+(?:and|&)\s+[A-Z][a-z]+)*)\s+(?:found|discovered|showed|demonstrated|argued)',
        ]
        
        found_count = 0
        for pattern in patterns:
            if found_count >= 3:  # Limit to 3 missing refs
                break
                
            matches = re.finditer(pattern, text_to_check, re.IGNORECASE)
            for match in matches:
                if found_count >= 3:
                    break
                    
                # Skip if this is already part of a citation
                if self._is_part_of_citation(text_to_check, match.start(), match.end()):
                    continue
                
                potential_ref = {
                    "text": match.group(0),
                    "position": match.start(),
                    "type": "potential_missing_citation",
                    "suggestion": "This statement may need a citation"
                }
                
                missing_refs.append(potential_ref)
                found_count += 1
        
        return missing_refs
    
    def _is_part_of_citation(self, text: str, start: int, end: int) -> bool:
        """Check if a text span is already part of a citation"""
        # Look for common citation patterns around this text
        before_text = text[max(0, start-50):start]
        after_text = text[end:min(len(text), end+50)]
        
        # Common citation indicators
        citation_patterns = [
            r'\(\d{4}\)',  # (2023)
            r'\[\d+\]',    # [1]
            r'\([\w\s,&]+,\s*\d{4}\)',  # (Smith & Jones, 2023)
            r'et al\.',
            r'p\.\s*\d+',
            r'pp\.\s*\d+-\d+'
        ]
        
        for pattern in citation_patterns:
            if re.search(pattern, before_text) or re.search(pattern, after_text):
                return True
        
        return False
    
    def _build_search_query(self, citation_text: str) -> str:
        """Extract searchable terms from citation text"""
        # Remove common citation formatting
        query = re.sub(r'[(\[]?\d{4}[)\]]?', '', citation_text)  # Remove years in parentheses
        query = re.sub(r'pp?\.\s*\d+[-–]\d+', '', query)  # Remove page numbers
        query = re.sub(r'[Vv]ol\.\s*\d+', '', query)  # Remove volume numbers
        query = re.sub(r'[Nn]o\.\s*\d+', '', query)  # Remove issue numbers
        query = re.sub(r'\[\d+\]', '', query)  # Remove numeric citations
        
        # Extract potential title in quotes
        title_match = re.search(r'"([^"]+)"', query)
        if title_match:
            query = title_match.group(1)
        
        # Clean up
        query = ' '.join(query.split())
        return query.strip()
    
    def _make_request_with_retry(self, url: str, params: Dict[str, Any] = None) -> Optional[requests.Response]:
        """Make HTTP request with retry logic"""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout  # Use self.timeout
                )
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:  # Rate limited
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    return None
                    
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                continue
            except Exception:
                return None
        
        return None
    
    def _search_crossref(self, query: str) -> List[Dict[str, Any]]:
        """Search CrossRef API with improved error handling"""
        if not query:
            return []
            
        try:
            params = {
                'query': query,
                'rows': 3,  # Reduced from 5
                'select': 'DOI,title,author,published-print,container-title'
            }
            
            # Quick timeout for faster response
            response = self.session.get(
                self.search_engines['crossref'],
                params=params,
                timeout=self.timeout  # Uses self.timeout (15 seconds)
            )
            
            if response and response.status_code == 200:
                data = response.json()
                items = data.get('message', {}).get('items', [])
                
                results = []
                for item in items[:2]:  # Only top 2 results
                    result = {
                        'source': 'crossref',
                        'title': item.get('title', [''])[0],
                        'authors': self._format_crossref_authors(item.get('author', [])),
                        'year': self._extract_year_from_date(item.get('published-print')),
                        'journal': item.get('container-title', [''])[0],
                        'doi': item.get('DOI')
                    }
                    results.append(result)
                
                return results
        except requests.exceptions.Timeout:
            print(f"CrossRef timeout after {self.timeout} seconds")
        except Exception as e:
            print(f"CrossRef search error: {e}")
        
        return []
    
    def _search_arxiv(self, query: str) -> List[Dict[str, Any]]:
        """Search arXiv API"""
        if not query:
            return []
            
        try:
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': 3
            }
            
            response = self._make_request_with_retry(
                self.search_engines['arxiv'],
                params=params
            )
            
            if response and response.status_code == 200:
                # Parse XML response
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                
                results = []
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                
                for entry in root.findall('atom:entry', ns):
                    title_elem = entry.find('atom:title', ns)
                    if title_elem is not None:
                        title = title_elem.text.strip()
                        authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns) if author.find('atom:name', ns) is not None]
                        published_elem = entry.find('atom:published', ns)
                        year = published_elem.text.split('-')[0] if published_elem is not None else None
                        id_elem = entry.find('atom:id', ns)
                        arxiv_id = id_elem.text.split('/')[-1] if id_elem is not None else None
                        
                        result = {
                            'source': 'arxiv',
                            'title': title,
                            'authors': authors,
                            'year': year,
                            'arxiv_id': arxiv_id,
                            'url': f'https://arxiv.org/abs/{arxiv_id}' if arxiv_id else None
                        }
                        results.append(result)
                
                return results
        except Exception as e:
            print(f"arXiv search error: {e}")
        
        return []
    
    def _search_semantic_scholar(self, query: str) -> List[Dict[str, Any]]:
        """Search Semantic Scholar API"""
        if not query:
            return []
            
        try:
            params = {
                'query': query,
                'limit': 3,
                'fields': 'title,authors,year,venue,doi,url'
            }
            
            response = self._make_request_with_retry(
                self.search_engines['semantic_scholar'],
                params=params
            )
            
            if response and response.status_code == 200:
                data = response.json()
                papers = data.get('data', [])
                
                results = []
                for paper in papers:
                    result = {
                        'source': 'semantic_scholar',
                        'title': paper.get('title'),
                        'authors': [author.get('name', '') for author in paper.get('authors', [])],
                        'year': paper.get('year'),
                        'venue': paper.get('venue'),
                        'doi': paper.get('doi'),
                        'url': paper.get('url')
                    }
                    results.append(result)
                
                return results
        except Exception as e:
            print(f"Semantic Scholar search error: {e}")
        
        return []
    
    def _format_crossref_authors(self, authors: List[Dict]) -> List[str]:
        """Format CrossRef author data"""
        formatted = []
        for author in authors:
            if 'given' in author and 'family' in author:
                formatted.append(f"{author['given']} {author['family']}")
            elif 'name' in author:
                formatted.append(author['name'])
        return formatted
    
    def _extract_year_from_date(self, date_info: Any) -> Optional[str]:
        """Extract year from various date formats"""
        if isinstance(date_info, dict) and 'date-parts' in date_info:
            date_parts = date_info['date-parts']
            if date_parts and date_parts[0] and date_parts[0][0]:
                return str(date_parts[0][0])
        return None
    
    def _generate_suggestions(self, original_citation: str, found_sources: List[Dict]) -> List[str]:
        """Generate citation improvement suggestions based on found sources"""
        suggestions = []
        
        if found_sources:
            best_match = found_sources[0]
            
            # Check for missing DOI
            if best_match.get('doi') and 'doi' not in original_citation.lower():
                suggestions.append(f"Consider adding DOI: {best_match['doi']}")
            
            # Check for complete author list
            if best_match.get('authors') and len(best_match['authors']) > 1:
                if ' et al' not in original_citation and ' and ' not in original_citation:
                    suggestions.append("Consider listing all authors or using 'et al.' appropriately")
            
            # Check for journal information
            if best_match.get('journal') and best_match['journal'] not in original_citation:
                suggestions.append(f"Include full journal name: {best_match['journal']}")
            
            # Check for volume/issue
            if best_match.get('volume') and f"vol. {best_match['volume']}" not in original_citation.lower():
                suggestions.append(f"Add volume information: Vol. {best_match['volume']}")
        
        return suggestions
    
    def format_as_citation(self, source: Dict[str, Any], style: str = "apa") -> str:
        """Format found source as a proper citation"""
        if style.lower() == "apa":
            # APA format
            authors = source.get('authors', [])
            if authors:
                if len(authors) == 1:
                    author_str = f"{authors[0].split()[-1]}, {authors[0].split()[0][0]}."
                elif len(authors) == 2:
                    author_str = f"{authors[0].split()[-1]}, {authors[0].split()[0][0]}., & {authors[1].split()[-1]}, {authors[1].split()[0][0]}."
                else:
                    author_str = f"{authors[0].split()[-1]}, {authors[0].split()[0][0]}., et al."
            else:
                author_str = "Unknown Author"
            
            year = source.get('year', 'n.d.')
            title = source.get('title', 'Unknown Title')
            journal = source.get('journal', source.get('venue', ''))
            volume = source.get('volume', '')
            issue = source.get('issue', '')
            pages = source.get('pages', '')
            doi = source.get('doi', '')
            
            citation = f"{author_str} ({year}). {title}."
            if journal:
                citation += f" {journal}"
                if volume:
                    citation += f", {volume}"
                    if issue:
                        citation += f"({issue})"
                if pages:
                    citation += f", {pages}"
            citation += "."
            
            if doi:
                citation += f" https://doi.org/{doi}"
            
            return citation
        
        # Add other citation styles as needed
        return str(source)
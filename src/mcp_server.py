import requests
from typing import Optional, Dict, Any
import os
import json
from datetime import datetime

class MCPServer:
    """Model Context Protocol (MCP) server integration for reliable citation verification"""
    
    def __init__(self, server_url: Optional[str] = None):
        # Note: MCP is a new protocol - using established APIs for citation verification
        self.timeout = 10
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CiteScope/1.0 (Citation Verification Tool)'
        })
        
        # API endpoints for citation verification
        self.endpoints = {
            'crossref': 'https://api.crossref.org',
            'openlibrary': 'https://openlibrary.org',
            'pubmed': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils',
            'semantic_scholar': 'https://api.semanticscholar.org/v1'
        }
        
    def verify_citation(self, citation_text: str) -> Optional[Dict[str, Any]]:
        """Verify a citation against external databases"""
        try:
            # Extract key information from citation
            citation_info = self._parse_citation(citation_text)
            
            # Search for the source
            search_results = self._search_source(citation_info)
            
            # Verify the citation details
            verification = self._verify_details(citation_info, search_results)
            
            return verification
            
        except Exception as e:
            return {
                "verified": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _parse_citation(self, citation_text: str) -> Dict[str, Any]:
        """Parse citation text to extract key information"""
        import re
        
        info = {
            "raw_text": citation_text,
            "authors": [],
            "title": "",
            "year": None,
            "source": "",
            "doi": None,
            "isbn": None,
            "pmid": None
        }
        
        # Extract year
        year_match = re.search(r'\b(19|20)\d{2}\b', citation_text)
        if year_match:
            info["year"] = int(year_match.group())
        
        # Extract DOI
        doi_match = re.search(r'10\.\d{4,}/[-._;()/:\w]+', citation_text)
        if doi_match:
            info["doi"] = doi_match.group()
        
        # Extract ISBN
        isbn_match = re.search(r'ISBN[-:\s]*([\d-]+X?)', citation_text, re.IGNORECASE)
        if isbn_match:
            info["isbn"] = isbn_match.group(1).replace("-", "").replace(" ", "")
        
        # Extract PMID (PubMed ID)
        pmid_match = re.search(r'PMID[-:\s]*(\d+)', citation_text, re.IGNORECASE)
        if pmid_match:
            info["pmid"] = pmid_match.group(1)
        
        # Extract title (text in quotes)
        title_match = re.search(r'"([^"]+)"', citation_text)
        if title_match:
            info["title"] = title_match.group(1)
        
        return info
    
    def _search_source(self, citation_info: Dict[str, Any]) -> Dict[str, Any]:
        """Search for the source in external databases"""
        search_results = {
            "found": False,
            "sources": [],
            "confidence": 0.0
        }
        
        # Try different search strategies based on available identifiers
        if citation_info.get("doi"):
            doi_result = self._search_by_doi(citation_info["doi"])
            if doi_result:
                search_results["found"] = True
                search_results["sources"].append(doi_result)
                search_results["confidence"] = 0.95
        
        elif citation_info.get("isbn"):
            isbn_result = self._search_by_isbn(citation_info["isbn"])
            if isbn_result:
                search_results["found"] = True
                search_results["sources"].append(isbn_result)
                search_results["confidence"] = 0.90
        
        elif citation_info.get("pmid"):
            pmid_result = self._search_by_pmid(citation_info["pmid"])
            if pmid_result:
                search_results["found"] = True
                search_results["sources"].append(pmid_result)
                search_results["confidence"] = 0.95
        
        else:
            # Fallback to text search if we have a title
            if citation_info.get("title"):
                text_results = self._search_by_title(citation_info)
                if text_results:
                    search_results["found"] = True
                    search_results["sources"] = text_results
                    search_results["confidence"] = 0.70
        
        return search_results
    
    def _search_by_doi(self, doi: str) -> Optional[Dict[str, Any]]:
        """Search for a source by DOI using CrossRef API"""
        try:
            response = self.session.get(
                f"{self.endpoints['crossref']}/works/{doi}",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                work = data.get("message", {})
                
                return {
                    "type": "journal_article",
                    "title": work.get("title", [""])[0],
                    "authors": self._extract_crossref_authors(work.get("author", [])),
                    "year": work.get("published-print", {}).get("date-parts", [[None]])[0][0],
                    "journal": work.get("container-title", [""])[0],
                    "volume": work.get("volume"),
                    "issue": work.get("issue"),
                    "pages": work.get("page"),
                    "doi": doi,
                    "source": "crossref",
                    "url": work.get("URL")
                }
        except Exception as e:
            print(f"CrossRef API error: {e}")
        
        return None
    
    def _search_by_isbn(self, isbn: str) -> Optional[Dict[str, Any]]:
        """Search for a book by ISBN using Open Library API"""
        try:
            response = self.session.get(
                f"{self.endpoints['openlibrary']}/api/books",
                params={
                    "bibkeys": f"ISBN:{isbn}",
                    "format": "json",
                    "jscmd": "data"
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if f"ISBN:{isbn}" in data:
                    book_data = data[f"ISBN:{isbn}"]
                    
                    return {
                        "type": "book",
                        "title": book_data.get("title", ""),
                        "authors": [author.get("name", "") for author in book_data.get("authors", [])],
                        "year": self._extract_year_from_date(book_data.get("publish_date", "")),
                        "publisher": book_data.get("publishers", [{}])[0].get("name", "") if book_data.get("publishers") else "",
                        "isbn": isbn,
                        "pages": book_data.get("number_of_pages"),
                        "source": "openlibrary",
                        "url": book_data.get("url")
                    }
        except Exception as e:
            print(f"Open Library API error: {e}")
        
        return None
    
    def _search_by_pmid(self, pmid: str) -> Optional[Dict[str, Any]]:
        """Search for an article by PubMed ID"""
        try:
            # Fetch article details from PubMed
            response = self.session.get(
                f"{self.endpoints['pubmed']}/esummary.fcgi",
                params={
                    "db": "pubmed",
                    "id": pmid,
                    "retmode": "json"
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data and pmid in data["result"]:
                    article = data["result"][pmid]
                    
                    return {
                        "type": "journal_article",
                        "title": article.get("title", ""),
                        "authors": [author.get("name", "") for author in article.get("authors", [])],
                        "year": int(article.get("pubdate", "").split()[0]) if article.get("pubdate") else None,
                        "journal": article.get("source", ""),
                        "volume": article.get("volume"),
                        "issue": article.get("issue"),
                        "pages": article.get("pages"),
                        "pmid": pmid,
                        "doi": article.get("elocationid", "").replace("doi: ", "") if "doi" in article.get("elocationid", "") else None,
                        "source": "pubmed"
                    }
        except Exception as e:
            print(f"PubMed API error: {e}")
        
        return None
    
    def _search_by_title(self, citation_info: Dict[str, Any]) -> list:
        """Search by title using CrossRef API"""
        results = []
        
        try:
            # Search CrossRef by title
            response = self.session.get(
                f"{self.endpoints['crossref']}/works",
                params={
                    "query.title": citation_info["title"],
                    "rows": 3,
                    "filter": f"from-pub-date:{citation_info['year']}" if citation_info.get("year") else None
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                items = data.get("message", {}).get("items", [])
                
                for item in items[:1]:  # Take only the best match
                    result = {
                        "type": item.get("type", "unknown"),
                        "title": item.get("title", [""])[0],
                        "authors": self._extract_crossref_authors(item.get("author", [])),
                        "year": item.get("published-print", {}).get("date-parts", [[None]])[0][0],
                        "journal": item.get("container-title", [""])[0] if item.get("container-title") else None,
                        "doi": item.get("DOI"),
                        "source": "crossref",
                        "match_score": item.get("score", 0)
                    }
                    results.append(result)
        except Exception as e:
            print(f"Title search error: {e}")
        
        return results
    
    def _verify_details(self, citation_info: Dict[str, Any], search_results: Dict[str, Any]) -> Dict[str, Any]:
        """Verify citation details against search results"""
        verification = {
            "verified": False,
            "confidence": 0.0,
            "matched_fields": [],
            "mismatched_fields": [],
            "suggestions": [],
            "source_info": None
        }
        
        if not search_results["found"]:
            verification["suggestions"].append("Source not found in external databases")
            return verification
        
        # Compare with the first source found
        source = search_results["sources"][0]
        verification["source_info"] = source
        
        # Check year
        if citation_info.get("year") and source.get("year"):
            if str(citation_info["year"]) == str(source["year"]):
                verification["matched_fields"].append("year")
            else:
                verification["mismatched_fields"].append("year")
                verification["suggestions"].append(f"Year should be {source['year']}")
        
        # Check title similarity if available
        if citation_info.get("title") and source.get("title"):
            # Simple similarity check (could be improved with fuzzy matching)
            if citation_info["title"].lower() in source["title"].lower() or source["title"].lower() in citation_info["title"].lower():
                verification["matched_fields"].append("title")
        
        # Overall verification status
        if len(verification["matched_fields"]) > len(verification["mismatched_fields"]):
            verification["verified"] = True
            verification["confidence"] = search_results["confidence"]
        
        return verification
    
    def _extract_crossref_authors(self, authors: list) -> list:
        """Extract author names from CrossRef format"""
        extracted = []
        for author in authors:
            if "given" in author and "family" in author:
                extracted.append(f"{author['given']} {author['family']}")
            elif "name" in author:
                extracted.append(author["name"])
        return extracted
    
    def _extract_year_from_date(self, date_str: str) -> Optional[int]:
        """Extract year from various date formats"""
        import re
        if date_str:
            year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
            if year_match:
                return int(year_match.group())
        return None
    
    def batch_verify(self, citations: list) -> Dict[str, Any]:
        """Verify multiple citations in batch"""
        results = []
        for citation in citations:
            result = self.verify_citation(citation)
            results.append(result)
        
        return {
            "total": len(citations),
            "verified": sum(1 for r in results if r and r.get("verified", False)),
            "failed": sum(1 for r in results if not r or not r.get("verified", False)),
            "results": results
        }
    
    def check_connection(self) -> bool:
        """Check if external APIs are accessible"""
        try:
            # Test CrossRef API
            response = self.session.get(
                f"{self.endpoints['crossref']}/works",
                params={"rows": 1},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
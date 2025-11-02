import requests
from typing import Optional, Dict, Any, List
import re
from datetime import datetime

class DOIValidator:
    """DOI validation and metadata retrieval using CrossRef API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Psyte/1.0 (Academic Citation Checker)',
            'Accept': 'application/json',
        })
        self.crossref_api = 'https://api.crossref.org/works'
        self.timeout = 15
        
    def clean_doi(self, doi: str) -> str:
        """Clean and normalize DOI"""
        doi = doi.strip()
        # Remove common prefixes
        doi = re.sub(r'^https?://doi\.org/', '', doi)
        doi = re.sub(r'^https?://dx\.doi\.org/', '', doi)
        doi = re.sub(r'^doi:', '', doi, flags=re.IGNORECASE)
        return doi
    
    def validate_doi_format(self, doi: str) -> bool:
        """Check if DOI has valid format"""
        doi_pattern = r'^10\.\d{4,}/[-._;()/:\w]+$'
        return bool(re.match(doi_pattern, doi))
    
    def get_publication_info(self, doi: str) -> Dict[str, Any]:
        """Retrieve publication information from CrossRef"""
        doi = self.clean_doi(doi)
        
        if not self.validate_doi_format(doi):
            return {
                'success': False,
                'error': 'Invalid DOI format',
                'doi': doi
            }
        
        try:
            response = self.session.get(
                f"{self.crossref_api}/{doi}",
                timeout=self.timeout
            )
            
            if response.status_code == 404:
                return {
                    'success': False,
                    'error': 'DOI not found in CrossRef database',
                    'doi': doi
                }
            elif response.status_code != 200:
                return {
                    'success': False,
                    'error': f'Error: {response.status_code} {response.reason}',
                    'doi': doi
                }
            
            data = response.json()
            work = data.get('message', {})
            
            return {
                'success': True,
                'doi': doi,
                'data': self._parse_work_data(work, doi)
            }
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timeout - CrossRef API is not responding',
                'doi': doi
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}',
                'doi': doi
            }
    
    def _parse_work_data(self, work: Dict, doi: str) -> Dict[str, Any]:
        """Parse CrossRef work data into structured format"""
        return {
            'title': self._extract_title(work),
            'authors': self._extract_authors(work),
            'date': self._extract_date(work),
            'journal': self._extract_journal(work),
            'type': work.get('type', 'unknown').replace('-', ' ').title(),
            'publisher': work.get('publisher', 'N/A'),
            'volume': work.get('volume', ''),
            'issue': work.get('issue', ''),
            'pages': work.get('page', ''),
            'citations': work.get('is-referenced-by-count', 0),
            'url': f'https://doi.org/{doi}',
            'abstract': work.get('abstract', ''),
            'issn': work.get('ISSN', []),
            'isbn': work.get('ISBN', []),
            'subjects': work.get('subject', []),
            'license': self._extract_license(work),
        }
    
    def _extract_title(self, work: Dict) -> str:
        """Extract title from work data"""
        title = work.get('title', [])
        if isinstance(title, list) and title:
            return title[0]
        elif isinstance(title, str):
            return title
        return 'No title available'
    
    def _extract_authors(self, work: Dict) -> List[Dict[str, str]]:
        """Extract and format author information"""
        authors = []
        author_list = work.get('author', [])
        
        for author in author_list:
            authors.append({
                'given': author.get('given', ''),
                'family': author.get('family', ''),
                'full_name': f"{author.get('given', '')} {author.get('family', '')}".strip(),
                'orcid': author.get('ORCID', '')
            })
        
        return authors
    
    def _extract_date(self, work: Dict) -> Dict[str, Any]:
        """Extract publication date"""
        date_info = {
            'year': None,
            'month': None,
            'day': None,
            'formatted': 'Date not available'
        }
        
        # Try different date fields in order of preference
        for date_type in ['published-print', 'published-online', 'published', 'created']:
            if work.get(date_type):
                date_parts = work[date_type].get('date-parts', [[]])
                if date_parts and date_parts[0]:
                    parts = date_parts[0]
                    date_info['year'] = parts[0] if len(parts) > 0 else None
                    date_info['month'] = parts[1] if len(parts) > 1 else None
                    date_info['day'] = parts[2] if len(parts) > 2 else None
                    break
        
        # Format date string
        if date_info['year']:
            if date_info['month']:
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                month_name = months[date_info['month'] - 1]
                if date_info['day']:
                    date_info['formatted'] = f"{month_name} {date_info['day']}, {date_info['year']}"
                else:
                    date_info['formatted'] = f"{month_name} {date_info['year']}"
            else:
                date_info['formatted'] = str(date_info['year'])
        
        return date_info
    
    def _extract_journal(self, work: Dict) -> str:
        """Extract journal/container title"""
        container = work.get('container-title', [])
        if isinstance(container, list) and container:
            return container[0]
        elif isinstance(container, str):
            return container
        return ''
    
    def _extract_license(self, work: Dict) -> List[Dict[str, str]]:
        """Extract license information"""
        licenses = []
        for license_info in work.get('license', []):
            licenses.append({
                'url': license_info.get('URL', ''),
                'start': license_info.get('start', {}).get('date-time', ''),
                'delay_in_days': license_info.get('delay-in-days', 0)
            })
        return licenses
    
    def format_citation(self, data: Dict[str, Any], style: str = 'apa') -> str:
        """Format publication data as a citation"""
        if style.lower() == 'apa':
            return self._format_apa_citation(data)
        elif style.lower() == 'mla':
            return self._format_mla_citation(data)
        elif style.lower() == 'chicago':
            return self._format_chicago_citation(data)
        elif style.lower() == 'harvard':
            return self._format_harvard_citation(data)
        elif style.lower() == 'ieee':
            return self._format_ieee_citation(data)
        else:
            return self._format_apa_citation(data)
    
    def _format_apa_citation(self, data: Dict[str, Any]) -> str:
        """Format citation in APA style"""
        authors = data.get('authors', [])
        year = data.get('date', {}).get('year', 'n.d.')
        title = data.get('title', '')
        journal = data.get('journal', '')
        volume = data.get('volume', '')
        issue = data.get('issue', '')
        pages = data.get('pages', '')
        doi = data.get('doi', '')
        
        # Format authors
        if not authors:
            author_str = 'Unknown Author'
        elif len(authors) == 1:
            author_str = f"{authors[0]['family']}, {authors[0]['given'][0]}."
        elif len(authors) <= 20:
            author_list = [f"{a['family']}, {a['given'][0]}." for a in authors[:-1]]
            author_str = ', '.join(author_list) + f", & {authors[-1]['family']}, {authors[-1]['given'][0]}."
        else:
            first_19 = [f"{a['family']}, {a['given'][0]}." for a in authors[:19]]
            author_str = ', '.join(first_19) + f", ... {authors[-1]['family']}, {authors[-1]['given'][0]}."
        
        # Build citation
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
    
    def _format_mla_citation(self, data: Dict[str, Any]) -> str:
        """Format citation in MLA style"""
        authors = data.get('authors', [])
        title = data.get('title', '')
        journal = data.get('journal', '')
        volume = data.get('volume', '')
        issue = data.get('issue', '')
        year = data.get('date', {}).get('year', 'n.d.')
        pages = data.get('pages', '')
        doi = data.get('doi', '')
        
        # Format authors
        if not authors:
            author_str = 'Unknown Author'
        elif len(authors) == 1:
            author_str = f"{authors[0]['family']}, {authors[0]['given']}"
        elif len(authors) == 2:
            author_str = f"{authors[0]['family']}, {authors[0]['given']}, and {authors[1]['given']} {authors[1]['family']}"
        else:
            author_str = f"{authors[0]['family']}, {authors[0]['given']}, et al"
        
        # Build citation
        citation = f'{author_str}. "{title}."'
        
        if journal:
            citation += f" {journal}"
            if volume:
                citation += f", vol. {volume}"
                if issue:
                    citation += f", no. {issue}"
            if year:
                citation += f", {year}"
            if pages:
                citation += f", pp. {pages}"
            citation += "."
        
        if doi:
            citation += f" https://doi.org/{doi}."
        
        return citation
    
    def _format_chicago_citation(self, data: Dict[str, Any]) -> str:
        """Format citation in Chicago style"""
        authors = data.get('authors', [])
        year = data.get('date', {}).get('year', 'n.d.')
        title = data.get('title', '')
        journal = data.get('journal', '')
        volume = data.get('volume', '')
        issue = data.get('issue', '')
        pages = data.get('pages', '')
        doi = data.get('doi', '')
        
        # Format authors
        if not authors:
            author_str = 'Unknown Author'
        elif len(authors) == 1:
            author_str = f"{authors[0]['family']}, {authors[0]['given']}"
        else:
            author_list = [f"{a['given']} {a['family']}" for a in authors[:-1]]
            author_str = ', '.join(author_list) + f", and {authors[-1]['given']} {authors[-1]['family']}"
        
        # Build citation
        citation = f'{author_str}. "{title}."'
        
        if journal:
            citation += f" {journal}"
            if volume:
                citation += f" {volume}"
                if issue:
                    citation += f", no. {issue}"
            if year:
                citation += f" ({year})"
            if pages:
                citation += f": {pages}"
            citation += "."
        
        if doi:
            citation += f" https://doi.org/{doi}."
        
        return citation
    
    def _format_harvard_citation(self, data: Dict[str, Any]) -> str:
        """Format citation in Harvard style"""
        return self._format_apa_citation(data)  # Similar to APA
    
    def _format_ieee_citation(self, data: Dict[str, Any]) -> str:
        """Format citation in IEEE style"""
        authors = data.get('authors', [])
        year = data.get('date', {}).get('year', 'n.d.')
        title = data.get('title', '')
        journal = data.get('journal', '')
        volume = data.get('volume', '')
        issue = data.get('issue', '')
        pages = data.get('pages', '')
        
        # Format authors
        if not authors:
            author_str = 'Unknown Author'
        else:
            author_initials = [f"{a['given'][0]}. {a['family']}" for a in authors[:6]]
            if len(authors) > 6:
                author_str = ', '.join(author_initials) + ', et al.'
            else:
                author_str = ', '.join(author_initials)
        
        # Build citation
        citation = f'{author_str}, "{title},"'
        
        if journal:
            citation += f" {journal}"
            if volume:
                citation += f", vol. {volume}"
                if issue:
                    citation += f", no. {issue}"
            if pages:
                citation += f", pp. {pages}"
            if year:
                citation += f", {year}"
            citation += "."
        
        return citation
    
    def batch_validate(self, dois: List[str]) -> List[Dict[str, Any]]:
        """Validate multiple DOIs"""
        results = []
        for doi in dois:
            result = self.get_publication_info(doi)
            results.append(result)
        return results
    
    def extract_dois_from_text(self, text: str) -> List[str]:
        """Extract DOIs from text"""
        doi_pattern = r'10\.\d{4,}/[-._;()/:\w]+'
        dois = re.findall(doi_pattern, text)
        return list(set(dois))  # Remove duplicates
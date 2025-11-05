"""
DOI import functionality using CrossRef API
"""
import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class DOIImporter:
    """Import research metadata from DOI using CrossRef API"""

    CROSSREF_API = "https://api.crossref.org/works"

    @staticmethod
    def fetch_metadata(doi: str) -> Optional[Dict]:
        """
        Fetch metadata from CrossRef API using DOI

        Args:
            doi: Digital Object Identifier (e.g., "10.1000/xyz123")

        Returns:
            Dictionary with research metadata or None if not found
        """
        try:
            # Clean DOI
            doi = doi.strip().replace('https://doi.org/', '').replace('http://dx.doi.org/', '')

            # Fetch from CrossRef
            url = f"{DOIImporter.CROSSREF_API}/{doi}"
            headers = {'User-Agent': 'ResearchManagementSystem/1.0 (mailto:dev@research.local)'}

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data['status'] != 'ok':
                logger.warning(f'DOI lookup failed: {doi}')
                return None

            # Parse metadata
            message = data['message']
            metadata = DOIImporter._parse_crossref_data(message)
            metadata['doi'] = doi

            logger.info(f'Successfully fetched metadata for DOI: {doi}')
            return metadata

        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching DOI {doi}: {str(e)}')
            return None
        except Exception as e:
            logger.error(f'Unexpected error processing DOI {doi}: {str(e)}')
            return None

    @staticmethod
    def _parse_crossref_data(data: Dict) -> Dict:
        """Parse CrossRef API response to our metadata format"""
        metadata = {}

        # Title
        if 'title' in data and data['title']:
            metadata['title'] = data['title'][0]
            metadata['title_en'] = data['title'][0]

        # Authors
        if 'author' in data:
            authors = []
            for author in data['author']:
                if 'given' in author and 'family' in author:
                    authors.append(f"{author['given']} {author['family']}")
                elif 'family' in author:
                    authors.append(author['family'])
            metadata['authors'] = ', '.join(authors)

        # Abstract
        if 'abstract' in data:
            metadata['abstract'] = data['abstract']

        # Year
        if 'published' in data:
            date_parts = data['published'].get('date-parts', [[]])[0]
            if date_parts:
                metadata['year'] = date_parts[0]
        elif 'created' in data:
            date_parts = data['created'].get('date-parts', [[]])[0]
            if date_parts:
                metadata['year'] = date_parts[0]

        # Publication type
        pub_type = data.get('type', '')
        type_mapping = {
            'journal-article': 'journal',
            'proceedings-article': 'conference',
            'book-chapter': 'book',
            'dissertation': 'thesis',
            'report': 'report'
        }
        metadata['publication_type'] = type_mapping.get(pub_type, 'other')

        # Journal info
        if 'container-title' in data and data['container-title']:
            metadata['journal_name'] = data['container-title'][0]

        if 'volume' in data:
            metadata['volume'] = data['volume']

        if 'issue' in data:
            metadata['issue'] = data['issue']

        if 'page' in data:
            metadata['pages'] = data['page']

        # Keywords/subjects
        if 'subject' in data:
            metadata['keywords'] = ', '.join(data['subject'][:5])  # Limit to 5

        # URL
        if 'URL' in data:
            metadata['url'] = data['URL']

        return metadata


def search_crossref(query: str, limit: int = 10) -> list:
    """
    Search CrossRef database

    Args:
        query: Search query string
        limit: Maximum number of results

    Returns:
        List of DOIs and titles
    """
    try:
        url = f"{DOIImporter.CROSSREF_API}"
        params = {
            'query': query,
            'rows': limit
        }
        headers = {'User-Agent': 'ResearchManagementSystem/1.0'}

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        items = data['message']['items']

        results = []
        for item in items:
            result = {
                'doi': item.get('DOI', ''),
                'title': item.get('title', [''])[0],
                'authors': ', '.join([
                    f"{a.get('given', '')} {a.get('family', '')}"
                    for a in item.get('author', [])
                ][:3]),  # Limit to 3 authors
                'year': item.get('published', {}).get('date-parts', [[None]])[0][0]
            }
            results.append(result)

        return results

    except Exception as e:
        logger.error(f'Error searching CrossRef: {str(e)}')
        return []

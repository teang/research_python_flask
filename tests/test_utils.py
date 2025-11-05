"""
Tests for utility functions
"""
import pytest
from app.utils import (
    format_citation_apa,
    format_citation_mla,
    format_citation_chicago,
    format_citation_bibtex,
    format_citation_ris,
    calculate_statistics
)


class TestCitationFormatters:
    """Test citation formatting functions"""

    def test_apa_format(self, research):
        """Test APA citation format"""
        citation = format_citation_apa(research)
        assert citation is not None
        assert research.authors in citation
        assert str(research.year) in citation
        assert research.title in citation

    def test_mla_format(self, research):
        """Test MLA citation format"""
        citation = format_citation_mla(research)
        assert citation is not None
        assert research.authors in citation
        assert research.title in citation

    def test_chicago_format(self, research):
        """Test Chicago citation format"""
        citation = format_citation_chicago(research)
        assert citation is not None
        assert research.authors in citation

    def test_bibtex_format(self, research):
        """Test BibTeX citation format"""
        citation = format_citation_bibtex(research)
        assert citation is not None
        assert '@' in citation
        assert research.authors in citation
        assert research.title in citation

    def test_ris_format(self, research):
        """Test RIS citation format"""
        citation = format_citation_ris(research)
        assert citation is not None
        assert 'TY  -' in citation
        assert 'ER  -' in citation
        assert research.authors in citation


class TestStatistics:
    """Test statistics calculation"""

    def test_calculate_statistics(self, db_session, research, regular_user):
        """Test statistics calculation"""
        stats = calculate_statistics()

        assert 'total_research' in stats
        assert 'total_users' in stats
        assert 'total_views' in stats
        assert 'total_downloads' in stats
        assert stats['total_research'] >= 1
        assert stats['total_users'] >= 1

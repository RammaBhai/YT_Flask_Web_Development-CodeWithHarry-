# tests/test_advanced.py
import pytest
from unittest.mock import Mock, patch
from app.services.visitor_service import VisitorService


class TestVisitorService:
    @pytest.fixture
    def mock_db(self):
        return Mock()

    @pytest.fixture
    def visitor_service(self, mock_db):
        return VisitorService(mock_db)

    def test_track_visitor_with_bot(self, visitor_service):
        """Test bot detection in visitor tracking"""
        visitor_data = VisitorData(
            ip_address="192.168.1.1",
            user_agent="Googlebot/2.1",
            page_visited="home",
            session_id="abc123",
        )

        with patch("app.utils.user_agent.detect_bot", return_value=True):
            result = visitor_service.track_visitor(visitor_data)

            assert result.is_bot is True
            mock_db.session.add.assert_called_once()
            mock_db.session.commit.assert_called_once()

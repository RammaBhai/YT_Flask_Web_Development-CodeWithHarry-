# app/services/visitor_service.py
from dataclasses import dataclass
from typing import Optional, Dict, Any
from app.models import SiteVisitor
from app.extensions import db
from app.utils.geoip import get_geo_location
from app.utils.user_agent import detect_bot


@dataclass
class VisitorData:
    ip_address: str
    user_agent: str
    page_visited: str
    session_id: str


class VisitorService:
    def __init__(self, db_session):
        self.db = db_session

    def track_visitor(self, visitor_data: VisitorData) -> SiteVisitor:
        """Track visitor with enhanced data collection"""

        # Bot detection
        is_bot = detect_bot(visitor_data.user_agent)

        # GeoIP lookup (async or cached)
        country = get_geo_location(visitor_data.ip_address)

        visitor = SiteVisitor(
            ip_address=visitor_data.ip_address,
            user_agent=visitor_data.user_agent,
            page_visited=visitor_data.page_visited,
            session_id=visitor_data.session_id,
            is_bot=is_bot,
            country=country,
        )

        self.db.session.add(visitor)
        self.db.session.commit()

        return visitor

    def get_visitor_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive visitor statistics"""
        total = SiteVisitor.query.count()
        unique = SiteVisitor.query.distinct(SiteVisitor.session_id).count()
        daily_stats = SiteVisitor.get_daily_visitors(days)
        bots = SiteVisitor.query.filter_by(is_bot=True).count()

        return {
            "total_visitors": total,
            "unique_visitors": unique,
            "bot_visitors": bots,
            "daily_stats": daily_stats,
            "human_visitors": total - bots,
        }

# app/models.py
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Index, func
from sqlalchemy.dialects.postgresql import JSONB  # For PostgreSQL
from app.extensions import db
import uuid


class SiteVisitor(db.Model):
    __tablename__ = "site_visitors"

    id = db.Column(db.Integer, primary_key=True)
    visitor_uuid = db.Column(
        db.String(36), unique=True, default=lambda: str(uuid.uuid4())
    )
    timestamp = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, index=True
    )
    ip_address = db.Column(db.String(45))  # IPv6 support
    user_agent = db.Column(db.Text)
    page_visited = db.Column(db.String(100), default="home")
    session_id = db.Column(db.String(100))
    is_bot = db.Column(db.Boolean, default=False)
    country = db.Column(db.String(2))

    # Indexes
    __table_args__ = (
        Index("idx_visitor_timestamp", timestamp),
        Index("idx_visitor_session", session_id),
    )

    @classmethod
    def get_daily_visitors(cls, days=30):
        """Get visitor statistics for the last N days"""
        from sqlalchemy import cast, Date

        return (
            db.session.query(
                cast(cls.timestamp, Date).label("date"),
                func.count(cls.id).label("count"),
                func.count(db.distinct(cls.session_id)).label("unique_visitors"),
            )
            .filter(cls.timestamp >= datetime.utcnow() - timedelta(days=days))
            .group_by("date")
            .order_by("date")
            .all()
        )

    @property
    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "page": self.page_visited,
            "country": self.country,
        }


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    status = db.Column(
        db.String(20), default="unread", index=True
    )  # unread, read, replied, spam
    metadata = db.Column(JSONB)  # Store additional data

    # For spam detection
    spam_score = db.Column(db.Float, default=0.0)
    is_spam = db.Column(db.Boolean, default=False)

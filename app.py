import os
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# ---------------------------
# Flask App Setup
# ---------------------------
app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "dev-secret-key-change-in-production",  # Use env var in production!
)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///site.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# ---------------------------
# Database Models
# ---------------------------
class SiteVisitor(db.Model):
    __tablename__ = "site_visitors"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<SiteVisitor {self.id}>"


# ---------------------------
# Initialize Database
# ---------------------------
with app.app_context():
    db.create_all()


# ---------------------------
# Sample Website Services
# ---------------------------
SERVICES = [
    {
        "id": 1,
        "title": "Web Development",
        "description": "Custom web applications with modern frameworks",
        "icon": "💻",
        "features": [
            "Responsive Design",
            "API Integration",
            "Performance Optimization",
        ],
    },
    {
        "id": 2,
        "title": "Data Analytics",
        "description": "Transform your data into actionable insights",
        "icon": "📊",
        "features": [
            "Real-time Dashboards",
            "Predictive Modeling",
            "Data Visualization",
        ],
    },
    {
        "id": 3,
        "title": "Cloud Solutions",
        "description": "Scalable cloud infrastructure and deployment",
        "icon": "☁️",
        "features": [
            "AWS/Azure/GCP",
            "Containerization",
            "Serverless Architecture",
        ],
    },
    {
        "id": 4,
        "title": "AI Integration",
        "description": "Intelligent solutions with machine learning",
        "icon": "🤖",
        "features": [
            "Chatbots",
            "Computer Vision",
            "Natural Language Processing",
        ],
    },
]


# ---------------------------
# Helper Functions
# ---------------------------
def add_visitor():
    """Add a new site visitor record safely."""
    try:
        visitor = SiteVisitor()
        db.session.add(visitor)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Error adding visitor: {e}")


# ---------------------------
# Routes
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    """Home page with visitor tracking and optional form submission."""
    if request.method == "POST":
        title = request.form.get("title", "")
        description = request.form.get("description", "")
        icon = request.form.get("icon", "")
        features = request.form.getlist("features")
        app.logger.info(f"Received form: {title}, {description}, {features}")

    # Visitor count tracking via session
    session["visitor_count"] = session.get("visitor_count", 0) + 1

    # Add visitor to DB
    add_visitor()

    all_visitors = SiteVisitor.query.order_by(SiteVisitor.timestamp.desc()).all()

    return render_template(
        "index.html",
        title="Home",
        description="Welcome to our Flask Web Application!",
        icon="🏠",
        all_visitors=all_visitors,
        services=SERVICES,
        visitor_count=session["visitor_count"],
        current_year=datetime.now().year,
    )


@app.route("/about")
def about():
    return render_template("about.html", current_year=datetime.now().year)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact form route with validation."""
    error = success = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not all([name, email, message]):
            error = "All fields are required!"
        else:
            success = f"Thank you {name}! We'll contact you at {email} soon."

    return render_template(
        "contact.html",
        error=error,
        success=success,
        current_year=datetime.now().year,
    )


# ---------------------------
# API Endpoints
# ---------------------------
@app.route("/api/services", methods=["GET"])
def get_services():
    return jsonify(SERVICES)


@app.route("/api/contact", methods=["POST"])
def api_contact():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not all([name, email, message]):
        return jsonify({"error": "All fields are required"}), 400

    return jsonify(
        {"success": True, "message": f"Message received from {name}", "email": email}
    )


@app.route("/greet", methods=["GET", "POST"])
def greet():
    """Personal greeting page with session tracking."""
    if request.method == "POST":
        name = request.form.get("name", "Guest")
        session["last_greeted"] = name
        return render_template("greet_result.html", name=name)

    return render_template("greet_form.html")


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})


@app.route("/visitors")
def visitors():
    """Return total visitor count from DB."""
    total_visitors = SiteVisitor.query.count()
    return jsonify({"total_visitors": total_visitors})


# ---------------------------
# Run the App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

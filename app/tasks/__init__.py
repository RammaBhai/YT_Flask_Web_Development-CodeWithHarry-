# app/tasks/__init__.py
from celery import Celery
from flask import current_app
import requests
from app.services.email_service import send_contact_email


def make_celery(app):
    """Initialize Celery with Flask context"""
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


@celery.task(bind=True, max_retries=3)
def process_contact_form(self, form_data):
    """Background task for processing contact forms"""
    try:
        # Send email
        send_contact_email(form_data)

        # Log to analytics
        log_contact_to_analytics(form_data)

        # Check for spam
        spam_score = check_spam(form_data["message"])

        return {"status": "processed", "spam_score": spam_score}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


# In your route:
@app.route("/api/contact", methods=["POST"])
@rate_limit(max_per_minute=10)
def api_contact():
    data = request.get_json()

    # Validate with schema
    errors = ContactSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # Queue background task
    task = process_contact_form.delay(data)

    return jsonify(
        {"success": True, "task_id": task.id, "message": "Processing your request"}
    )

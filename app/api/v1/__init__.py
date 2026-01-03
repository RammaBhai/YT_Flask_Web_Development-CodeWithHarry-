# app/api/v1/__init__.py
from flask_restx import Api, Resource, fields
from app.services.visitor_service import VisitorService

api = Api(
    version="1.0", title="Website API", description="A fully featured website API"
)

# Namespaces
ns_visitors = api.namespace("visitors", description="Visitor operations")
ns_services = api.namespace("services", description="Service operations")

# Models for documentation
visitor_model = api.model(
    "Visitor",
    {
        "id": fields.Integer(readOnly=True),
        "timestamp": fields.DateTime,
        "country": fields.String,
    },
)


@ns_visitors.route("/")
class VisitorList(Resource):
    @api.marshal_list_with(visitor_model)
    @api.doc(params={"days": "Number of days of data to return"})
    def get(self):
        """Return list of visitors"""
        days = request.args.get("days", 30, type=int)
        service = VisitorService(db.session)
        return service.get_visitor_statistics(days)

from flask import Flask, Blueprint
from flask_restful import Api

from models import db
from resources import LineResourceCreation, LineResourceSearch, LineResourcePhonecall, LineResourceRecharge

app = Flask(__name__)
app.config.from_object("config")

api_bp = Blueprint('lines', __name__)
api = Api(api_bp)
app.register_blueprint(api_bp, url_prefix='/lines')

with app.app_context():
    db.init_app(app)
    db.create_all()

# Route
api.add_resource(LineResourceCreation, '/create')
api.add_resource(LineResourceSearch, '/<phone_number>')
api.add_resource(LineResourcePhonecall, '/<phone_number>/phonecall')
api.add_resource(LineResourceRecharge, '/<phone_number>/charge')

if __name__ == '__main__':
    app.run(debug=True)

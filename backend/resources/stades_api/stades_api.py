from flask import Blueprint
from models.stades import stades_schema, Stade
from resources.config import db


bp = Blueprint('stades_api', __name__)
session = db.session


@bp.route('/stades', methods=(['GET']))
def stades():
    res = Stade.query.all()
    return stades_schema.jsonify(res)

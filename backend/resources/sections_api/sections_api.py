from flask import Blueprint

from models.sections import Section, sections_schema
from resources.config import db


bp = Blueprint('sections_api', __name__)
session = db.session


@bp.route('/sections', methods=(['GET']))
def stades():
    res = Section.query.all()
    return sections_schema.jsonify(res)

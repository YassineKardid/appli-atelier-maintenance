from flask import Blueprint

from models.roles import roles_schema, Role
from resources.config import db


bp = Blueprint('roles_api', __name__)
session = db.session


@bp.route('/roles', methods=(['GET']))
def stades():
    res = Role.query.all()
    return roles_schema.jsonify(res)
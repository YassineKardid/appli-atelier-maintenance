from flask import Blueprint, request, abort
from models.actions import Action, actions_schema, action_schema
from resources.config import db


bp = Blueprint('actions_api', __name__)
session = db.session


@bp.route('/actions', methods=(['GET', 'POST']))
def actions():
    if request.method == 'GET':
        equipment = request.args.get('equipment')
        search = request.args.get('search')
        q = Action.query
        if equipment is not None:
            q = q.filter(Action.equipmentId == equipment)
        if search is not None:
            q = q.filter(Action.name.like(search + '%'))

        actions = q.order_by(Action.name).all()

        return actions_schema.jsonify(actions)
    elif request.method == 'POST':
        equipment = request.json['equipmentId']
        name = request.json['name']
        action = Action.query.filter(Action.equipmentId == equipment, Action.name.like(name)).first()
        if action is not None:
            abort(400)

        action = Action(equipmentId = equipment, name = name)
        session.add(action)

        session.commit()

        return action_schema.jsonify(action)


from flask import Blueprint, request, abort
from sqlalchemy import desc


from flask import session as user_session
from resources.config import db
from datetime import datetime
from models.ot_events import OtEvent, ot_event_schema, ot_events_schema

bp = Blueprint('ot_events_api', __name__)
session = db.session

@bp.route('/ot_events', methods=('GET', 'POST'))
def ot_events():
    if request.method == 'POST':
        date_now= datetime.utcnow()
        ot_event = OtEvent(ot_id = request.json['ot_id'], timestamp = date_now, key = request.json['key'], value = request.json['value'])
        session.add(ot_event)
        session.commit()
        return ot_event_schema.jsonify(ot_event)
    elif request.method == 'GET':
        ot_events = OtEvent.query.order_by(desc(OtEvent.timestamp)).all()
        return ot_events_schema.jsonify(ot_events)



@bp.route('/ot_events/<int:ot_id>', methods=('GET', 'POST'))
def ot(ot_id):
    if request.method == 'GET':
        ot_events = OtEvent.query.filter(OtEvent.ot_id == ot_id).order_by(desc(OtEvent.timestamp)).all()
        return ot_events_schema.jsonify(ot_events)
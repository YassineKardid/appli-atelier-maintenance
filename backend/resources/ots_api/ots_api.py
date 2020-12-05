from flask import Blueprint, request, abort
from flask import session as user_session
from sqlalchemy import desc
from datetime import datetime

from models.ot_operators import OtOperator
from models.ot_team_leads import OtTeamLead
from models.comments import Comment
from models.ots import Ot, ot_schema, ots_schema, OtSchema
from models.pauses import Pause
from models.users import User
from resources.config import db


bp = Blueprint('ots_api', __name__)
session = db.session


@bp.route('/ots', methods=('GET', 'POST'))
def ots():
    if request.method == 'POST':
        ot = ot_schema.load(request.json, session=session).data
        session.add(ot)
        session.commit()
        return ot_schema.jsonify(ot)
    elif request.method == 'GET':
        q = Ot.query
        q = q.filter(Ot.status == 2)
        user = User.query.filter(User.username == user_session['username']).first()
        role = user.role
        stade = request.args.get('stade')
        section = request.args.get('section')
    
        if role.id == 4:  #operateur
            q = q.join(OtOperator, OtOperator.ot_id == Ot.id)\
                .filter(OtOperator.operator_id == user.id)
        elif role.id == 3:  #chef equipe
            q = q.filter(Ot.teamLeadId == user.id)
        elif role.id == 2:  #chef atelier
            stade = user.stade_id
            section = user.section_id

        if stade is not None:
            q = q.filter(Ot.stadeId == stade)

        if section is not None:
            q = q.filter(Ot.sectionId == section)

        date_from = request.args.get('date_from')
        if date_from is not None:
            q = q.filter(Ot.scheduledDate >= date_from)

        date_to = request.args.get('date_to')
        if date_to is not None:
            q = q.filter(Ot.scheduledDate <= date_to)

        #scheduled = request.args.get('scheduled') OPM => non planifie, GMAO => planifie  
        #if scheduled is not None:
        #    if scheduled =="True":
        #        q = q.filter(Ot.scheduledDate is not None)
        #    else:
        #        q = q.filter(Ot.scheduledDate is None)

        type = request.args.get('type')
        if type is not None:
            typeNum = OtSchema.read_maintenance_type(type)
            q = q.filter(Ot.maintenanceType == typeNum)

        priority = request.args.get('priority')
        if priority is not None:
            prioNum = OtSchema.read_priority(priority)
            q = q.filter(Ot.priority == prioNum)

        work_status = request.args.get('work_status')
        if work_status is not None:
            statNum = OtSchema.read_work_status(work_status)#read_status
            q = q.filter(Ot.workStatus == statNum) #status

        sort = request.args.get('sort')
        if sort == 'priority':
            q = q.order_by(Ot.priority.desc())
        elif sort == 'date':
            q = q.order_by(Ot.scheduledDate)

        res = q.order_by(desc(Ot.id)).all()
        
        return ots_schema.jsonify(res)

@bp.route('/ots_not_launched', methods=('GET', 'POST'))
def ots_not_launched():
    q = Ot.query
    q = q.filter(Ot.status == 1)
    date_from = request.args.get('date_from')
    if date_from is not None:
        q = q.filter(Ot.scheduledDate >= date_from)
    date_to = request.args.get('date_to')
    if date_to is not None:
        q = q.filter(Ot.scheduledDate <= date_to)
    stade = request.args.get('stade')
    if stade is not None:
        q = q.filter(Ot.stadeId == stade)
    section = request.args.get('section')
    if section is not None:
        q = q.filter(Ot.sectionId == section)
    
    res = q.order_by(desc(Ot.id)).all()

    return ots_schema.jsonify(res)

@bp.route('/ots/<int:ot_id>', methods=('GET', 'POST'))
def ot(ot_id):
    if request.method == 'POST':
        ot = ot_schema.load(request.json, session=session).data
        ot.id = ot_id
        merged_ot = session.merge(ot)
        session.commit()
        return ot_schema.jsonify(merged_ot)
        
    elif request.method == 'GET':
        ot = Ot.query.filter(Ot.id == ot_id).first()

        return ot_schema.jsonify(ot)

@bp.route('/ots/reassignSection', methods=(['POST']))
def reassignSection():
    assert request.method == 'POST'
    id = request.json['id']
    section_id = request.json['section']
    ot = Ot.query.filter(Ot.id == id).first()
    ot.sectionId = section_id
    session.merge(ot)
    session.commit()

    return ot_schema.jsonify(ot)

@bp.route('/ots/status', methods=(['POST']))
def status():
    assert request.method == 'POST'
    id = request.json['id']
    status = request.json['status']
    ot = Ot.query.filter(Ot.id == id).first()
    ot.status = OtSchema.read_status(status)
    session.merge(ot)
    session.commit()

    return ot_schema.jsonify(ot)

@bp.route('/ots/atelier', methods=(['POST']))
def atelier():
    assert request.method == 'POST'
    id = request.json['id']
    stade = request.json['stade']
    section = request.json['section']
    ot = Ot.query.filter(Ot.id == id).first()
    ot.stadeId = stade
    ot.sectionId = section
    session.merge(ot)
    session.commit()

    return ot_schema.jsonify(ot)


@bp.route('/ots/assign', methods=(['POST']))
def assign():
    assert request.method == 'POST'
    id = request.json['id']
    teamLead = request.json.get('teamLeadId', None)
    operators = request.json.get('operators', None)
    ot = Ot.query.filter(Ot.id == id).first()

    if teamLead is not None:
        if teamLead != ot.teamLeadId:
            ot.teamLeadId = teamLead
            rel = OtTeamLead(ot_id = id, user_id = teamLead, timestamp = datetime.utcnow())
            session.add(rel)
    else:
        teamLead = ot.teamLeadId

    if operators is not None:
        OtOperator.query.filter(OtOperator.ot_id == id, OtOperator.team_lead_id == teamLead).delete()
        for op in operators:
            otOpe = OtOperator(ot_id = id, team_lead_id = teamLead, operator_id = op)
            session.merge(otOpe)

    session.commit()

    return ot_schema.jsonify(ot)


@bp.route('/ots/schedule', methods=['POST'])
def schedule():
    if request.json.get('comment'):
        date_now= datetime.utcnow()
        user = User.query.filter(User.username == user_session['username']).first()
        comment =Comment(text = request.json['comment'], date = date_now, userId = user.id, otId = request.json['id'])
        session.add(comment)
    ot = ot_schema.load(request.json, session=session).data
    ot.scheduledDate = request.json['scheduledDate']
    merged_ot = session.merge(ot)
    session.commit()

    return ot_schema.jsonify(merged_ot)

@bp.route('/ots/start', methods=['POST'])
def start():
    assert request.method == 'POST'
    id = request.json['id']
    date_now = datetime.utcnow()
    ot = Ot.query.filter(Ot.id == id).first()
    if ot.start is not None:
        abort(400)

    ot.start = date_now
    ot.workStatus = 1
    session.commit()

    return ot_schema.jsonify(ot)

@bp.route('/ots/end', methods=['POST'])
def end():
    assert request.method == 'POST'
    id = request.json['id']
    date_now = datetime.utcnow()
    ot = Ot.query.filter(Ot.id == id).first()

    if ot.start is None:
        abort(400)

    if ot.end is not None:
        abort(400)

    pause = Pause.query.filter(Pause.ot_id == id, Pause.stop == None).order_by(Pause.start.desc()).first()
    if pause is not None:
        pause.stop = date_now

    ot.workStatus = 3
    ot.end = date_now
    session.commit()

    return ot_schema.jsonify(ot)


@bp.route('/ots/pause', methods=['POST'])
def pause():
    assert request.method == 'POST'
    id = request.json['id']
    date_now = datetime.utcnow()
    ot = Ot.query.filter(Ot.id == id).first()

    if ot.start is None:
        abort(400)

    if ot.end is not None:
        abort(400)

    pause = Pause.query.filter(Pause.ot_id == id, Pause.stop == None).order_by(Pause.start.desc()).first()
    if pause is not None:
        abort(400)

    pause = Pause(ot_id = id, start = date_now)
    session.merge(pause)
    ot.workStatus = 2

    session.commit()

    return ot_schema.jsonify(ot)

@bp.route('/ots/resume', methods=['POST'])
def resume():
    assert request.method == 'POST'
    id = request.json['id']
    date_now = datetime.utcnow()
    ot = Ot.query.filter(Ot.id == id).first()

    if ot.start is None:
        abort(400)

    if ot.end is not None:
        abort(400)

    pause = Pause.query.filter(Pause.ot_id == id, Pause.stop == None).order_by(Pause.start.desc()).first()
    if pause is None:
        abort(400)

    pause.stop = date_now
    ot.workStatus = 1

    session.commit()

    return ot_schema.jsonify(ot)
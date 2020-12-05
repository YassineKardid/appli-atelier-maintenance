from marshmallow import fields
from datetime import datetime
from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.actions import Action, ActionSchema
from models.comments import Comment, CommentSchema
from models.documents import docs_schema
from models.ot_events import OtEvent, OtEventSchema
from models.ot_operators import OtOperator
from models.equipments import EquipmentSchema, Equipment
from models.sections import Section, SectionSchema
from models.stades import Stade, StadeSchema
from models.users import User, UserSchema, users_schema
from models.pauses import Pause
from resources.config import db, ma



class Ot(db.Model):
    __tablename__ = 'ot'
    id = Column(Integer, primary_key=True)
    workStatus = Column('work_status', Integer)
    priority = Column(Integer)
    maintenanceType = Column('maintenance_type', Integer)
    withStop = Column('type_arret', Integer)
    scheduledDate = Column('scheduled_date', Date)
    uoEstimated = Column('uo_estimated', Integer)
    uoActual = Column('uo_actual', Integer)
    status = Column(Integer)
    start = Column(DateTime)
    end = Column(DateTime)
    actionId = Column('action_id', Integer, ForeignKey('action.id'))
    action = relationship(Action)
    equipmentId = Column('equipment_id', Integer, ForeignKey('equipment.id'))
    equipment = relationship(Equipment)
    comments = relationship(Comment)
    stadeId = Column('stade_id', Integer, ForeignKey('stade.id'))
    sectionId = Column('section_id', Integer, ForeignKey('section.id'))
    stade = relationship(Stade)
    section = relationship(Section)
    teamLeadId = Column('team_lead_id', Integer, ForeignKey('user.id'))
    teamLead = relationship(User)
    events = relationship(OtEvent)



class OtSchema(ma.ModelSchema):
    class Meta:
        model = Ot
        #exclude = ['typeArret']
    workStatusMap = {
        0: 'notStarted',
        1: 'started',
        2: 'paused',
        3: 'finished'
    }

    workStatusMapReverse = {
        'notStarted': 0,
        'started': 1,
        'paused': 2,
        'finished': 3
    }

    priorityMap = {
        0: 'Faible',
        1: 'Normale',
        2: 'Critique'
    }

    priorityMapReverse = {
        'Faible': 0,
        'Normale': 1,
        'Critique': 2
    }
    maintenanceTypeMap = {
        0: 'Curative',
        1: 'Systématique',
        2: 'Conditionnelle'
    }

    maintenanceTypeMapReverse = {
        'Curative': 0,
        'Systématique': 1,
        'Conditionnelle': 2
    }

    statusMap = {
        0: 'provisional',
        1: 'notLaunched',
        2: 'launched'
    }

    statusMapReverse = {
        'provisional': 0,
        'notLaunched': 1,
        'launched': 2
    }


    action = fields.Nested(ActionSchema)
    equipment = fields.Nested(EquipmentSchema)
    teamLead = fields.Nested(UserSchema, exclude=['stade', 'section', 'role'])
    comments = ma.Nested(CommentSchema, many=True)
    stade = fields.Nested(StadeSchema, exclude=['sections'])
    section = fields.Nested(SectionSchema)
    workStatus = fields.Method("convert_work_status", deserialize='read_work_status')
    priority = fields.Method("convert_priority", deserialize='read_priority')
    documents = fields.Method("get_documents")
    maintenanceType = fields.Method('convert_maintenance_type', deserialize='read_maintenance_type')
    withStop = fields.Method('convert_with_stop', deserialize='read_with_stop')
    status = fields.Method("convert_status", deserialize='read_status')
    operators = fields.Method('get_operators')
    events = ma.Nested(OtEventSchema, many=True)
    start = fields.DateTime('%Y-%m-%d %H:%M')
    end = fields.DateTime('%Y-%m-%d %H:%M')
    uoActual = fields.Method("calculate_actual_uo")

    @staticmethod
    def calculate_actual_uo(obj):
        uo_actual = 0
        if obj.start is not None:
            nbr_operators = User.query\
                .join(OtOperator, OtOperator.operator_id == User.id)\
                .filter(OtOperator.ot_id == obj.id, OtOperator.team_lead_id == obj.teamLeadId)\
                .all()

            pauses = Pause.query.filter(Pause.ot_id == obj.id).all()
            sum_minutes_pauses = 0

            for pause in pauses :
                if pause.stop is None :
                    stop = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                else:
                    stop = pause.stop
                time_delta = datetime.strptime(str(stop),'%Y-%m-%d %H:%M:%S') - datetime.strptime(str(pause.start),'%Y-%m-%d %H:%M:%S')
                nbr_minutes_pause = time_delta.total_seconds()/60
                sum_minutes_pauses = sum_minutes_pauses + int(nbr_minutes_pause)

            if obj.end is None :
                end = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            else:
                end = obj.end

            end_start = datetime.strptime(str(end),'%Y-%m-%d %H:%M:%S') - datetime.strptime(str(obj.start),'%Y-%m-%d %H:%M:%S')
            nbr_minutes_work = end_start.total_seconds()/60
            works_duration = (nbr_minutes_work - sum_minutes_pauses)/60 #houres

            uo_actual = works_duration*len(nbr_operators)
        
        return uo_actual

    @staticmethod
    def convert_work_status(obj):
        return OtSchema.workStatusMap.get(obj.workStatus, None)

    @staticmethod
    def read_work_status(value):
        return OtSchema.workStatusMapReverse.get(value, None)

    @staticmethod
    def convert_priority(obj):
        return OtSchema.priorityMap.get(obj.priority, None)

    @staticmethod
    def read_priority(value):
        return OtSchema.priorityMapReverse.get(value, None)
    @staticmethod
    def convert_maintenance_type(obj):
        return OtSchema.maintenanceTypeMap.get(obj.maintenanceType, None)

    @staticmethod
    def read_maintenance_type(value):
        return OtSchema.maintenanceTypeMapReverse.get(value, None)

    @staticmethod
    def convert_with_stop(obj):
        if obj.withStop is None:
            return False
        elif obj.withStop == 0:
            return False
        else:
            return True

    @staticmethod
    def read_with_stop(value):
        if value:
            return 1
        else:
            return 0

    @staticmethod
    def convert_status(obj):
        if obj.status is None:
            return 'provisional'

        return OtSchema.statusMap.get(obj.status, None)

    @staticmethod
    def read_status(value):
        return OtSchema.statusMapReverse.get(value, None)


    @staticmethod
    def get_documents(obj):
        return docs_schema.dump(obj.action.documents)

    @staticmethod
    def get_operators(obj):
        operators = User.query\
            .join(OtOperator, OtOperator.operator_id == User.id)\
            .filter(OtOperator.ot_id == obj.id, OtOperator.team_lead_id == obj.teamLeadId)\
            .all()
        return operators_schema.dump(operators).data



ot_schema = OtSchema()
ots_schema = OtSchema(many=True)
operators_schema = UserSchema(many=True, exclude=['email','role','section','stade','photo'])
#operators_schema = UserSchema(many=True)
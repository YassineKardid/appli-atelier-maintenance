from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from models.documents import Document
from models.equipments import Equipment
from resources.config import db, ma

action_doc_pivot = Table('action_document', db.Model.metadata,
    Column('action_id', Integer, ForeignKey('action.id')),
    Column('document_id', Integer, ForeignKey('document.id'))
)

class Action(db.Model):
    __tablename__ = 'action'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    equipmentId = Column('equipment_id', Integer, ForeignKey('equipment.id'))
    equipment = relationship(Equipment)
    documents = relationship(Document, secondary=action_doc_pivot)


class ActionSchema(ma.ModelSchema):
    class Meta:
        model = Action
        exclude = ['equipment', 'documents']


action_schema = ActionSchema()
actions_schema = ActionSchema(many=True)
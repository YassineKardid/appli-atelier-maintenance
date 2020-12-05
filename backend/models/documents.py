from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from models.equipments import Equipment
from resources.config import db, ma


class Document(db.Model):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True)
    link = Column(String(255))
    title = Column(String(45))
    description = Column(String())
    mimeType = Column('mime_type', String(255))
    equipmentId = Column('equipment_id', Integer, ForeignKey('equipment.id'))
    equipment = relationship(Equipment)


class DocumentSchema(ma.ModelSchema):
    class Meta:
        model = Document


doc_schema = DocumentSchema()
docs_schema = DocumentSchema(many=True)
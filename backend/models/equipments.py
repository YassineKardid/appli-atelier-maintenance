from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from models.sections import Section
from models.stades import Stade
from resources.config import db, ma


class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    stade_id =Column(Integer, ForeignKey('stade.id'))
    section_id = Column(Integer, ForeignKey('section.id'))
    section = relationship(Section)
    stade = relationship(Stade)


class EquipmentSchema(ma.ModelSchema):
    class Meta:
        model = Equipment
        exclude = ['stade', 'section']


equip_schema = EquipmentSchema()
equips_schema = EquipmentSchema(many=True)
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from models.sections import Section, SectionSchema
from resources.config import ma, db

stade_section_pivot = Table('stade_section', db.Model.metadata,
    Column('stade_id', Integer, ForeignKey('stade.id')),
    Column('section_id', Integer, ForeignKey('section.id'))
)

class Stade(db.Model):
    __tablename__ = 'stade'
    id = Column(Integer, primary_key=True)
    name = Column(String(45),nullable=False)
    imgUrl = Column('img_url', String(255))
    sections = relationship(Section, secondary=stade_section_pivot)


class StadeSchema(ma.ModelSchema):
    class Meta:
        model = Stade

    sections = ma.Nested(SectionSchema, many=True)


stade_schema = StadeSchema()
stades_schema = StadeSchema(many=True)
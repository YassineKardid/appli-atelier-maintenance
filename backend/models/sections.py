from sqlalchemy import Column, Integer, String

from resources.config import ma, db


class Section(db.Model):
    __tablename__ = 'section'
    id = Column(Integer, primary_key=True)
    name = Column(String(45),nullable=False)


class SectionSchema(ma.ModelSchema):
    class Meta:
        model = Section


section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)
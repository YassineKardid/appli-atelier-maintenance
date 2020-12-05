from marshmallow import fields
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.sections import Section, SectionSchema
from models.stades import Stade, StadeSchema
from models.roles import Role, RoleSchema
from resources.config import db, ma


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(45),nullable=False)
    firstname = Column(String(45))
    lastname = Column(String(45))
    email = Column(String(255),nullable=False)
    password = Column(String(45),nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'))
    stade_id =Column(Integer, ForeignKey('stade.id'))
    section_id = Column(Integer, ForeignKey('section.id'))
    role = relationship(Role)
    stade = relationship(Stade)
    section = relationship(Section)
    photo_file_name = Column(String(255))


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ['password', 'photo_file_name']

    photo = fields.String(attribute='photo_file_name')
    role = fields.Nested(RoleSchema)
    stade = fields.Nested(StadeSchema)
    #stade = fields.Nested(StadeSchema, exclude=['sections'])
    section = fields.Nested(SectionSchema)



user_schema = UserSchema()
users_schema = UserSchema(many=True)


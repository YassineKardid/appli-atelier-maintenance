from marshmallow import fields
from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from resources.config import db, ma
from marshmallow_sqlalchemy import ModelSchema, field_for
from models.users import User


class Comment(db.Model):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    text = Column(String(2048))
    date = Column(DateTime)
    otId = Column('ot_id', Integer, ForeignKey('ot.id'))
    userId = Column('user_id', Integer, ForeignKey('user.id'))

class CommentSchema(ma.ModelSchema):
    class Meta:
        model = Comment
    date = fields.DateTime('%Y-%m-%d %H:%M')

com_schema = CommentSchema()
coms_schema = CommentSchema(many=True)

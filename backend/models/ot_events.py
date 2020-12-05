from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from marshmallow import fields
from resources.config import ma, db


class OtEvent(db.Model):
    __tablename__ = 'ot_event'
    id = Column(Integer, primary_key=True)
    ot_id = Column(Integer, ForeignKey('ot.id'))
    timestamp = Column(DateTime)
    key = Column(String(255)) # the variable changed
    value = Column(String(255)) # the new value of the variable


class OtEventSchema(ma.ModelSchema):
    class Meta:
        model = OtEvent
        exclude = ['ot_id']
    timestamp = fields.DateTime('%Y-%m-%d %H:%M')


ot_event_schema = OtEventSchema()
ot_events_schema = OtEventSchema(many=True)
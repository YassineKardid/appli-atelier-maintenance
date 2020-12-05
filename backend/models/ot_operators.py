from sqlalchemy import Integer, Column, ForeignKey

from resources.config import db


class OtOperator(db.Model):
    __tablename__ = 'ot_operator'
    ot_id = Column(Integer, ForeignKey('ot.id'), primary_key=True)
    operator_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    team_lead_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
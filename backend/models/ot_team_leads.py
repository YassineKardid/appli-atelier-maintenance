from sqlalchemy import Integer, Column, ForeignKey, DateTime

from resources.config import db


class OtTeamLead(db.Model):
    __tablename__ = 'ot_team_lead'
    ot_id = Column(Integer, ForeignKey('ot.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
from sqlalchemy import Column, Integer, DateTime, ForeignKey

from resources.config import db


class Pause(db.Model):
    __tablename__ = 'pause'
    ot_id = Column(Integer, ForeignKey('ot.id'), primary_key=True)
    start = Column(DateTime, primary_key=True)
    stop = Column(DateTime)

from sqlalchemy import Column, Integer, String

from resources.config import ma, db


class Role(db.Model):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(45),nullable=False)


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
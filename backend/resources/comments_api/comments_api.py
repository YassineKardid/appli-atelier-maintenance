from flask import Blueprint, request
from flask import session as user_session
from models.comments import Comment, com_schema,coms_schema
from resources.config import db
from models.users import User
from datetime import datetime


bp = Blueprint('comments_api', __name__) 

session = db.session

@bp.route('/ots/comments', methods=('GET', 'POST'))
def comments():
    if request.method == 'POST':
        date_now= datetime.utcnow()
        user = User.query.filter(User.username == user_session['username']).first()
        comment = Comment(text=request.json['comment'], date=date_now, userId=user.id, otId = request.json['id'])
        session.add(comment)
        session.commit()
        return com_schema.jsonify(comment)
    elif request.method == 'GET':
        res = Comment.query.all()
        
        return coms_schema.jsonify(res)


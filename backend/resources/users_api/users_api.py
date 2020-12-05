import hashlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
import string

from flask import Blueprint, request, abort
from flask import session as user_session
from marshmallow import fields, Schema
from models.users import User, user_schema,users_schema,UserSchema
from models.ot_operators import OtOperator

from models.ots import Ot

from functools import wraps
from resources.config import db

session = db.session
bp = Blueprint('users_api', __name__)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not 'username' in user_session :
            abort(401)
        return f(*args, **kwargs)
    
    return decorated

def random_char(y):

    return ''.join(random.choice(string.ascii_letters) for x in range(y))


def sendEmail(email, username, newPassword, lastname): 
    msg = MIMEMultipart()
    message = "Bonjour Mr " + lastname + " ; " + "\nvotre nom d'utilisateur est : " + username + "\nvotre nouveau mot de passe est : " + newPassword +"\nMerci."
    password = "enter your password" #activate gmail application less security [compte google]
    msg['From'] = "enter your email"
    msg['To'] = "yassine.kardid@um6p.ma"
    msg['Subject'] = "Réinitialisation de vos informations d'accès"
    msg.attach(MIMEText(message, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    

class LoginRequestSchema(Schema):
    username = fields.String()
    password = fields.String()


login_schema = LoginRequestSchema()


@bp.route('/users/login', methods=(['POST']))
def login():
    data = login_schema.load(request.json).data
    hash = hashlib.sha1(data['password'].encode('utf-8')).hexdigest()
    user = User.query.filter(User.username == data['username'], User.password == hash).first()
    if user is None:
        abort(401)
    else:
        user_session['username'] = user.username

        return user_schema.jsonify(user)


@bp.route('/users/modifyProfile', methods=(['POST']))
def modifyProfile():
    
    hash = hashlib.sha1(request.json['old_password'].encode('utf-8')).hexdigest()
    user = User.query.filter(User.username == request.json['username'], User.password == hash).first()
    if user is None:
        abort(401)
    else:
        newPasswordHash = hashlib.sha1(request.json['new_password'].encode('utf-8')).hexdigest()
        user.password = newPasswordHash
        merged_user = session.merge(user)
        session.commit()

        return user_schema.jsonify(user)

@bp.route('/users/forgotPassword', methods=(['POST']))
def forgotPassword():
    email = request.json['email']  #admin1@um6p.ma
    newpassword = random_char(8)
    newPasswordHash = hashlib.sha1(newpassword.encode('utf-8')).hexdigest()
    user = User.query.filter(User.email == email).first()
    if user is None :
        abort(401)
    else :
        
        user.password = newPasswordHash
        merged_user = session.merge(user)
        session.commit()
        #sendEmail(email, user.username, newpassword, user.lastname)

    return user_schema.jsonify(merged_user)     

@bp.route('/users', methods=(['GET']))
#@requires_auth
def getUsers():
    users = User.query.all()

    return users_schema.jsonify(users)

@bp.route('/users/teamLeaders', methods=(['GET']))
def getTeamLeaders():
    teamLeaders = User.query.filter(User.role_id == 3)

    return users_schema.jsonify(teamLeaders)

@bp.route('/users/operators', methods=(['GET']))
def getOperators():
    operators = User.query.filter(User.role_id == 4)
    
    return users_schema.jsonify(operators)

@bp.route('/users/operatorsAvailable/<int:ot_id>', methods=(['GET']))
def getAvailableOperators(ot_id):
    ots = Ot.query.filter(Ot.start != None, Ot.end == None, Ot.id != ot_id).all()

    search = request.args.get('search')
    
    operators_not_available = []
    operators_schema = UserSchema(many=True, exclude=['email','role','section','stade','photo'])
    for ot in ots :
        operators = User.query\
                .join(OtOperator, OtOperator.operator_id == User.id)\
                .filter(OtOperator.ot_id == ot.id, OtOperator.team_lead_id == ot.teamLeadId)\
                .all()
        operators_not_available.extend(operators)

    all_operators = User.query.filter(User.role_id == 4).all()

    operators_available = []
    for op in all_operators:
        if op not in operators_not_available:
            operators_available.append(op)

    if search is not None:
        operators_available = [op for op in operators_available if search.casefold() in op.lastname.casefold() or search in op.firstname.casefold()]
        
    return operators_schema.jsonify(operators_available)

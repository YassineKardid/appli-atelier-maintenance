from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import params

password=params.password
user=params.user
databaseName=params.databaseName
host=params.host
port=params.port
MySQLDriver=params.MySQLDriver

dbUrl = MySQLDriver+'://'+user+':'+password+'@'+host+'/'+databaseName

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbUrl
CORS(app, supports_credentials=True, origins=['http://127.0.0.1:4200']) #
# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Requirement


## Software:
        python3

## Libraries:

### Flask

        sudo pip3 install Flask

        sudo pip3 install flask_restful

### Marshmallow

        sudo pip3 install marshmallow

### SQLAlchemy

        sudo pip3 install sqlalchemy
        
        
### Flask + SQLAlchemy + Marshmallow integration
        pip install flask-marshmallow
        pip install flask-sqlalchemy
        pip install marshmallow-sqlalchemy
        
### MySQL

        sudo apt-get install mysql-server
        sudo apt-get install python-pip libmysqlclient-dev python-dev python-mysqldb
        sudo pip3 install setuptools
        sudo apt-get install python3-mysqldb
        sudo apt-get install python3-mysql.connector

#### On Windows:
        pip install --only-binary :all: mysqlclient

#### On Mac:
        pip install mysqlclient

### Enable CORS
        pip install flask-cors

## Configuration:
Copy params.py.dist to params.py
Change database settings if necessary in params.py




Run the appllication by the folowing command :

        #uwsgi --ini uwsgi.ini
        uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi        
        sudo service nginx stop
        sudo service nginx start
        sudo service nginx restart


URL

        http://127.0.0.1:5000


/users  :method GET

/users/login :method POST


        {
            "username" : "yourUsername",
            "password" :  "yourPassword"
        }

/ots : method GET & POST

/ots/comment : method GET & POST

/stades: method GET

/sections: method GET

/roles: method GET


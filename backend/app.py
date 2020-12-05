import os

from resources.actions_api import actions_api
from resources.config import app
from resources import config, jsend
from resources.ots_api import ots_api
from resources.roles_api import roles_api
from resources.sections_api import sections_api
from resources.stades_api import stades_api
from resources.users_api import users_api
from resources.comments_api import comments_api
from resources.ot_events_api import ot_events_api

app.register_blueprint(ots_api.bp)
app.register_blueprint(stades_api.bp)
app.register_blueprint(sections_api.bp)
app.register_blueprint(roles_api.bp)
app.register_blueprint(users_api.bp)
app.register_blueprint(comments_api.bp)
app.register_blueprint(actions_api.bp)
app.register_blueprint(ot_events_api.bp)

app.secret_key = os.urandom(12)

@app.after_request
def wrap_jsend(response):
    return jsend.wrap(response)

application = app

"""

if __name__ == '__main__':   #running the main application in the port 5000
    
    app.run(debug=True,host='0.0.0.0', threaded=True, port=config.port) #  Start a development server
    #host='0.0.0.0'
    """
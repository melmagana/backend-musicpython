from flask import Flask

from resources.users import users

import models

from flask_cors import CORS

from flask_login import LoginManager



DEBUG=True
PORT=8000

app = Flask(__name__)


### LoginManager Configuration ###

# SECRET/KEY FOR SESSIONS
app.secret_key = 'Milo is the best puppy in the universe! This is not a secret.'
# INSTANTIATE LoginManager
login_manager = LoginManager()
# CONNECT APP WITH THE LOGIN MANAGER
login_manager.init_app(app)



### CORS -- CROSS ORIGIN RESOURCE SHARING ###
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)


### "CONTROLLERS" ###
app.register_blueprint(users, url_prefix='/api/v1/users')



@app.route('/')
def hello():
	return 'Hello, World!'

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)
from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
import models
from routes import Register, CustomersList, CustomerByEmail, LogIn
#LogOut
from config import Config


app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.init_app(app)

#SQL Configuration for connection
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{username}:{password}@{host}/{dbname}' \
     .format(**app.config['PG_CONFIG'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#connect to mysql
models.init_app(app)
models.create_tables(app)

api = Api(app) #Api constructor for RESTFUL APIs

#Map your resources to routes
api.add_resource(Register, '/register') #here we create route /add for Add resource
api.add_resource(CustomersList, '/customers')
api.add_resource(CustomerByEmail, '/customer/<email>')
api.add_resource(LogIn, '/login')
api.add_resource(LogOut, '/logout')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')

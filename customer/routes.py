from flask import jsonify, request, abort, g, session
from flask_restful import Resource
from flask_login import current_user, login_user, logout_user, login_required, user_loaded_from_header
from passlib.hash import sha256_crypt
from models import db, Customer
from app import login_manager

def EmailExists(email):
    email = Customer.query.filter_by(email=email).first()
    if email is not None:
        return True
    else:
        return False

#0. Generate JSON Dictionary as response
def GenerateResponse(status, message):
    response_dict = {
    "status": status,
    "message": message
    }
    return response_dict

#1. Check if customer exist
def CustomerExist(username):
    customer = Customer.query.filter_by(username=username).first()
    if customer is not None:
        return True
    else:
        return False

def VerifyCredentials(username, password_entered):
    if not CustomerExist(username):
        return False
    customer = Customer.query.filter_by(username=username).first()
    stored_password = customer.password
    if sha256_crypt.verify(password_entered, stored_password):
        return True
    else:
        return False

"""
user_loader callback. This callback is used to reload the user object
from the user ID stored in the session. It should take the unicode ID
of a user, and return the corresponding user object.
"""

@login_manager.user_loader
def load_user(user_id):
    return models.UserAccount.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):

    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = models.UserAccount.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = models.UserAccount.query.filter_by(api_key=api_key).first()
        if user:
            return user

    return None

@user_loaded_from_header.connect
def user_loaded_from_header(self, user=None):
    g.login_via_header = True

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized user or session timeout! Please login'

#Timeout a login user session after 1 minute
@app.before_request
def before_request():
    session.permanent = True
    #session.permanent flag and app.permanent_session_lifetime
    # will allow flask to  know that you want to timeout the session
    app.permanent_session_lifetime = timedelta(hours=24)
    #To timeout the user only because of inactivity
    #session.modified = True which is on each request
    # and this resets the session timeout timer.
    session.modified = True
    #retrieves the logged in user from flask_login and sets the Flask global user so that it can be used by the Jinja templates
    g.user = current_user

#Create register resource here
class Register(Resource):
    def post(self):
        posted_data = request.get_json()

        email = posted_data["email"]
        username = posted_data["username"]
        password = posted_data["password"]

        if CustomerExist(username):

            message =  "User with {} Already exists".format(username)
            status = 301
            response = GenerateResponse(status,message)
            return jsonify(response)
        else:
            #hash its password
            # hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
            hashed_password = sha256_crypt.hash((str(password)))
            customer = Customer()
            customer.email = email
            customer.username = username
            customer.password = hashed_password
            customer.active = True #will be used later for login
            customer.authenticated = True

            db.session.add(customer)
            db.session.commit()

            status = 200
            message = "Customer created Successfully"
            response = GenerateResponse(status, message)
            return jsonify(response)


class CustomersList(Resource):
    @login_required
    def get(self):
        
        customer_list = []
        for customer in Customer.query.all():
            customer_list.append(customer.to_json())
        response = jsonify(customer_list)
        return response

class CustomerByEmail(Resource):
    def get(self, email):
        if not EmailExists(email):
            message = "Customer Email doesn't exist"
            status = 201
            response = GenerateResponse(message, status)
            return jsonify(response)
            # abort(404)

        customer_data = Customer.query.filter_by(email=email).first()
        message = customer_data.to_json()
        status = 200
        response = GenerateResponse(status, message)
        return jsonify(response)

class LogIn(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]
        if VerifyCredentials(username, password):
            user = Customer.query.filter_by(username=username).first()
            # user.encode_api_key()
            # db.session.commit()
            login_user(user)

            message = "User Logged in Successfully"
            # message = user.api_key
            status = 200
            response = GenerateResponse(status, message)
            return response
        message = "Invalid Username/password"
        status = 201
        response = GenerateResponse(status, message)
        return response

class LogOut(Resource):
    def post(self):
        if current_user.is_authenticated():
            logout_user
            message = "{} is now Logged out".format(current_user.username)
            status = 200
            response = GenerateResponse(status, message)
            return response
        message = "You are not logged in"
        status = 201
        response = GenerateResponse(status, message)
        return response

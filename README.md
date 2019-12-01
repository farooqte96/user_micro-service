# user_micro-service
A flask based user-micro-service to register, login and show registered users 

# API end-points for micro-service:
This micro-service when deployed through DockerFile using docker-compose, deploy a flask application on port 5000 with following api end-points:

/register: user entered username and email is used to register a user
/login : then user is able to login to application after he has registered
/users: This api end point uses flask-login login_required decorator to allow only logged-in users to view the list of registered users.

# from flask import Flask, session
# from flask.sessions import SecureCookieSessionInterface
# from datetime import timedelta
# from .models.database import user 
# from flask import request

# userr=user
# app = Flask(__name__)
# app.secret_key = 'shahodaaaaa'
# app.config['SESSION_COOKIE_NAME'] = 'shahodadoda'
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
# app.config['SESSION_TYPE'] = 'filesystem'

# @app.route('/signup', methods=['POST'])
# def index():
#     # email=request.form.get('email')
#     # session['username'] = userr.get_id(email)
#     # return 'Session data set.'
#     session['example_data'] = 'This is an example session data.'
#     return 'Session data set.'
# @app.route('/clear_session')
# def clear_session():
#     session.pop('username', None)
#     return 'Username cleared from the session.'
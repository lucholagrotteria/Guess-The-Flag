from flask import Flask
from .views import views

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(views, url_prefix='/')
    app.config['SECRET_KEY'] = 'paosiduf019,.¿+{cd14278'
    
    return app
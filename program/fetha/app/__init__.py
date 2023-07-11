from flask import Flask,render_template
from config import Config
from app.extensions import db
import os


def create_app(config_class=Config):
    PHOTOS = os.path.join('app','static', 'photos')

    app = Flask(__name__)
    app.config.from_object(config_class)
    # Initialize Flask extensions here
    
    db.init_app(app)

    #Register blueprint here
    from app.main import bp as main_dp
    app.register_blueprint(main_dp)
    
    from app.register import bp as register_bp
    app.register_blueprint(register_bp, url_prefix='/register')

    from app.deposit import bp as questions_bp
    app.register_blueprint(questions_bp, url_prefix='/deposit')

    from app.family import bp as family_bp
    app.register_blueprint(family_bp, url_prefix='/family')

    from app.reports import bp as reports_bp
    app.register_blueprint(reports_bp, url_prefix='/reports')

    app.config['UPLOAD_FOLDER'] = PHOTOS
    @app.route('/index')
    def show_index():
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'],'africa.jpg')
        return render_template('index.html', user_image = full_filename)

    return app
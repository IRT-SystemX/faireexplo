
###############################################################################

import io, os, json, glob, datetime
import flask
from flask import Flask, request, jsonify, make_response, send_file, send_from_directory, abort, render_template, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.settings import logger
from modules.routes import onto_eval_bp
from modules.models import UploadedOntology, db
from modules.services.ontology_eval import OFAIRE, FOOPS, FAIRCHECKER
from modules.services.ontology_metadata_percentage import CalculateMetadataPercentage
from modules.services.download_ontology_from_portal import Download
from modules.settings import GET_DATABASE_URL, UPLOAD_PATH, DOWNLOAD_PATH, MINIMAL_METADATA_FILE_PATH

#######################################

FLASK_APP = 'app'

DEFAULT_SERVER_HOST = "0.0.0.0"
DEFAULT_SERVER_PORT = 5000

root_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resources'))

########################################

class Server():

    @staticmethod
    def db_init():
        engine = create_engine(GET_DATABASE_URL())
        # create the users table
        db.metadata.create_all(engine)
        # create a session to manage the connection to the database
        Session = sessionmaker(bind=engine)
        db.session = Session()

    @staticmethod
    def load():
        app = Flask(FLASK_APP, root_path=root_folder_path)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
        CORS(app)
        app.register_blueprint(onto_eval_bp, url_prefix='/api/metafair')        
        return app

    @staticmethod
    def serve(app):
        app.run(host=DEFAULT_SERVER_HOST, port=DEFAULT_SERVER_PORT, threaded=True)

################################################################################

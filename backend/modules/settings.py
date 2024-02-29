import os

###############################################################################

RESSOURCES_PATH='resources'
UPLOAD_PATH=f'{RESSOURCES_PATH}/uploaded_ontologies'
DOWNLOAD_PATH=f'{RESSOURCES_PATH}/downloaded_ontologies/'

MINIMAL_METADATA_FILE_PATH=f'{RESSOURCES_PATH}/minimal_metadata.json'
MANDATORY_FINDABLE_METADATA_FILE_PATH=f'{RESSOURCES_PATH}/mandatory_findable_metadata.json'
MANDATORY_REUSABLE_METADATA_FILE_PATH=f'{RESSOURCES_PATH}/mandatory_reusable_metadata.json'
RECOMMENDED_FINDABLE_METADATA_FILE_PATH=f'{RESSOURCES_PATH}/recommended_findable_metadata.json'
RECOMMENDED_REUSABLE_METADATA_FILE_PATH=f'{RESSOURCES_PATH}/recommended_reusable_metadata.json'
OPTIONAL_REUSABLE_METADATA_FILE_PATH=f'{RESSOURCES_PATH}/optional_reusable_metadata.json'

def GET_SERVER_URL():
    return os.getenv('SERVER_URL', f'http://localhost:5000')

def GET_FOOPS_API():
    FOOPS_URL = os.getenv('FOOPS_URL', f'http://localhost:5000')
    return FOOPS_URL+"/assessOntology"

def GET_METAFAIR_HOST():
    return os.getenv('METAFAIR_HOST', '127.0.0.1')

def GET_METAFAIR_PORT():
    return int(os.getenv('METAFAIR_PORT', '25333'))

def GET_DATABASE_URL(): 
    return os.getenv("DATABASE_URL")

################################################################################

import logging
from logging.handlers import RotatingFileHandler

########################################

LOG_LEVEL = eval("logging." + os.environ.get("LOG_LEVEL", "DEBUG"))
LOG_FILE = 'app.log'

#log_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=10)

log_handler = logging.StreamHandler()
log_handler.setLevel(LOG_LEVEL)
log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

###############################################################################

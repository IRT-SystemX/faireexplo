#!/usr/bin/env python

################################################################################

import os, json, argparse
from dotenv import load_dotenv
from modules.settings import logger
from modules.server import Server

#######################################

load_dotenv(".env")
logger.debug("env: "+(os.environ["ENV"] if "ENV" in os.environ else "dev"))

try:
    Server.db_init()
except Exception as err:
    logger.error(err)

app = Server.load()

##
# MAIN
##
if __name__ == "__main__":

    Server.serve(app)

################################################################################


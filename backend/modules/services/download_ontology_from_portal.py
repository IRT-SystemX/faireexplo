import os
from py4j.java_gateway import (JavaGateway, GatewayParameters)
from modules.settings import DOWNLOAD_PATH, GET_SERVER_URL, GET_METAFAIR_HOST, GET_METAFAIR_PORT
from modules.services.semantic_artefacts import SemanticArtefacts
from modules.settings import logger

###############################################################################

BIOPORTAL = "https://data.bioportal.lirmm.fr/"
AGROPORTAL = "https://data.agroportal.lirmm.fr/"
INDUSTRYPORTAL = "http://data.industryportal.enit.fr/"

#######################################

class Download:
    
    @staticmethod
    def download_ontology_from_portal(pname, oname, api_key):
        url=None
        if pname=='industryportal':
            url = INDUSTRYPORTAL
        elif pname=='agroportal' :
            url = AGROPORTAL
        elif pname=='bioportal' :
            url= BIOPORTAL
      
        s = SemanticArtefacts(url, oname, api_key)

        gateway = JavaGateway(gateway_parameters=GatewayParameters(address=GET_METAFAIR_HOST(), port=GET_METAFAIR_PORT(), auto_field=False))

        # read the original ontology file
        r = gateway.loadOntology(s.get_source())
        # save the original ontology
        #st = gateway.saveOntology(DOWNLOAD_PATH+oname+"-orig.owl")

        resources_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources'))
        original_ontology_path=resources_folder_path+"/downloaded_ontologies/"+oname+"-orig.owl"

        logger.debug(original_ontology_path)
        st = gateway.saveOntology(original_ontology_path)
        logger.debug(st)

        # remove all original metadata annotations
        gateway.deleteAnnotations()

        # get all metadata and annotate
        for m in s.get_metadata():
            ms = s.get_metadata_value(m)
            if len(ms) >= 2:
                # ignore if no value is curated for the metadata
                if (ms[1] == None):
                    continue
                # for 'contacts' only pick up the name
                if (m == "contacts"):
                    if (len(ms[1]) == 0):
                        continue
                    for mi in ms[1]:

                        gateway.addAnnotations(str(ms[0]), str(mi['name']))
                    continue
                # for tuple or list metadata value assert annotations separately for each member
                if type(ms[1]) is list or type(ms[1]) is tuple:
                    if (len(ms[1]) == 0):
                        continue
                    for mi in ms[1]:
                        gateway.addAnnotations(str(ms[0]), str(mi))
                    continue
                # general singleton metadata
                gateway.addAnnotations(str(ms[0]), str(ms[1]))

        # save the curated ontology
        #st = gateway.saveOntology(DOWNLOAD_PATH + oname + "-curated.owl")
        
        curatedOntologyPath=resources_folder_path+"/downloaded_ontologies/" + oname + "-curated.owl"
        
        logger.debug(curatedOntologyPath)
        st = gateway.saveOntology(curatedOntologyPath)
        logger.debug(st)

        return GET_SERVER_URL()+"/downloaded_ontologies/" + oname + "-curated.owl"

###################

    @staticmethod
    def get_all_metadata_from_portal(pname, oname, api_key):
        url=None
        if(pname=='industryportal'):
            url = INDUSTRYPORTAL
        elif(pname=='agroportal'):
            url = AGROPORTAL
        elif(pname=='bioportal'):
            url= BIOPORTAL
        
        s = SemanticArtefacts(url, oname, api_key)
        gateway = JavaGateway()
        metadata_label=s.get_metadata()

        # Create a dictionary with only the desired keys and their values
        #filtered_values = [ value for key, value in {m: s.get_metadata_value(m) for m in metadata_label}.items() ]        
        # Flatten the list of sublists into a single list
        #flattened_values = [item for sublist in filtered_values for item in sublist]

        return {m: s.get_metadata_value(m) for m in metadata_label} 

###############################################################################

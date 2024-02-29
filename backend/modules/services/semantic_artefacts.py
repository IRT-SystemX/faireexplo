import json
import requests
import logging

###############################################################################

class SemanticArtefacts:

    def __init__(self, url, onto, apiKey) -> None:
        self.url = url
        self.onto = onto
        self.apiKey = apiKey
        self.__load()

    def __load(self):
        endpoint = self.url+"/ontologies/"+self.onto+'/latest_submission'+'?display=all&apikey='+self.apiKey
        response = requests.get(endpoint)
        print("loading all metadata from " + endpoint)
        self.data = json.loads(response.text)    
    
    def get_source(self):
        print("loading all metadata from " + self.url+"/ontologies/"+self.onto+'/download?apikey='+self.apiKey)
        return self.url+"/ontologies/"+self.onto+'/download?apikey='+self.apiKey
    
    def get_metadata(self):
        self.metadata = self.data['@context']
        meta = []
        for m in self.metadata:
            #print("meta",self.metadata)
            #print("m",m)
            if(m not in ["@vocab", "metrics", "ontology", "submissionStatus"]):
                meta.append(m)
        return meta
    
    def get_metadata_value(self, md):
        self.metadata = self.data['@context']
        t = (self.metadata[md], self.data[md]) if md in self.metadata and md in self.data else ()
        return t

###############################################################################

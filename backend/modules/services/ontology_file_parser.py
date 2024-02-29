import json
from lxml import etree
import requests
from rdflib import URIRef, BNode, Literal, Namespace, RDF, FOAF, Graph

###############################################################################

class OntologyFileParser:

    def __init__(self, onto_url):
        self.onto_url = onto_url
        self.__load(self.onto_url)

    def __load(self,onto_url):
        self.g = Graph()
        self.data=self.g.parse(self.onto_url, format='xml')

    def get_metadata(self):
        # Extract namespaces
        namespaces = self.g.namespaces()

        # Print the namespaces
        namespaces = {}
        for prefix, uri in namespaces.items():
            namespaces[prefix] = uri
            print(namespaces)

        query = """
                    SELECT ?p ?o
                    WHERE {
                        ?ontology rdf:type owl:Ontology .
                        ?ontology ?p ?o .
                    }
                """
        results = self.g.query(query, initNs=namespaces)

        # Execute the query and save the results in a dictionary
        metadata_dict = {}
        for row in self.g.query(query, initNs=namespaces):
            metadata_dict[row['p']] = row['o']

        return metadata_dict

    def get_metadata_without_namespaces(self):
        # Extract namespaces
        namespaces = self.g.namespaces()

        # Print the namespaces
        namespaces = {}
        for prefix, uri in namespaces.items():
            namespaces[prefix] = uri
            print(namespaces)

        query = """
                    SELECT ?p ?o
                    WHERE {
                        ?ontology rdf:type owl:Ontology .
                        ?ontology ?p ?o .
                    }
                """
        results = self.g.query(query, initNs=namespaces)

        # Execute the query and save the results in a dictionary
        metadata_dict = {}
        metadata= {}
        for row in results:
            predicate = str(row["p"])
            if "#" in predicate:
                local_name = predicate.split("#")[-1]
            else:
                local_name = predicate.split("/")[-1]
            object_value = str(row["o"])
            metadata[local_name] = object_value

        return metadata

    def get_metadata_value(self,metadata_dict,md):
        if URIRef(md) in metadata_dict:
            value = metadata_dict[URIRef(md)]
        else:
            value = None
        return value

    def get_ontology_semantic_artefacts(self,metadata_dict):
        print(metadata_dict)
        ontologyVersion=[]
        ontologyTitle=[]
        ontologyCreator=[]
        ontologyContributor=[]

        for k in metadata_dict.keys():
            if "Version" in k:
                ontologyVersion.append(k)
            elif "version" in k:
                ontologyVersion.append(k)
            elif "Title" in k:
                ontologyTitle.append(k)

            elif "title" in k:
                ontologyTitle.append(k)

            elif "creator" in k:
                ontologyCreator.append(k)
            elif "Creator" in k:
                ontologyCreator.append(k)
            elif "contributor" in k:
                ontologyContributor.append(k)
            elif "Contributor" in k:
                ontologyContributor.append(k)
            else:
                ontologyVersion=ontologyVersion
                ontologyTitle=ontologyTitle
                ontologyCreator=ontologyCreator
                ontologyContributor=ontologyContributor

        return ontologyTitle,ontologyVersion,ontologyCreator,ontologyContributor

###############################################################################

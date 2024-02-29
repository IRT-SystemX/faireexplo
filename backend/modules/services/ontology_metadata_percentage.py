import json
from rdflib import URIRef
from modules.settings import logger

###############################################################################

class CalculateMetadataPercentage:

    @staticmethod
    def calculate_metadata_percentage(json_file_path, ontology_metadata):
        # Load the minimal metadata list from the JSON file
        try:
            with open(json_file_path) as file:
                minimal_metadata_list = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError

        # Initialize the ontology_minimal_metadata_list
        ontology_minimal_metadata_list = {}

        # Count the number of minimal metadata elements present in the ontology_metadata
        metadata_count = 0

        for metadata_element in minimal_metadata_list:
            for name in metadata_element["name"]:
                for k in ontology_metadata.keys():
                    if name in k:
                        if name in ontology_minimal_metadata_list:
                            ontology_minimal_metadata_list[name].append(k)
                        else:
                            ontology_minimal_metadata_list[name] = [k]
                        metadata_count += 1
                        break

        # Calculate the percentage of minimal metadata present
        total_metadata_elements = len(minimal_metadata_list)
        percentage = (metadata_count / total_metadata_elements) * 100

        return percentage,ontology_minimal_metadata_list

    @staticmethod
    def calculate_metadata_percentage2(json_file_path, ontology_metadata):
        #print('ontology_metadata',ontology_metadata)
        # Load the new JSON format from the JSON file
        try:
            with open(json_file_path) as file:
                json_data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError

        # Initialize the ontology_minimal_metadata_list
        ontology_minimal_metadata_list = {}

        # Count the number of minimal metadata elements present in the ontology_metadata
        metadata_count = 0

        for metadata_element in json_data:
            metadata_mappings = metadata_element.get("metadataMappings")
            if metadata_mappings is not None:
                #print('metadata_mappings is not null', metadata_mappings)
                for mapping in metadata_mappings:
                    label_uri = mapping.get("label_uri")
                    if label_uri is not None:
                        #print('label_uri',label_uri)
                        for k in ontology_metadata.keys():
                            #print('compare',k , 'and ', label_uri)
                            if URIRef(label_uri) == URIRef(k):
                                #print('yes found one',label_uri)
                                if label_uri in ontology_minimal_metadata_list:
                                    ontology_minimal_metadata_list[label_uri].append(k)
                                else:
                                    ontology_minimal_metadata_list[label_uri] = [k]
                                metadata_count += 1
                                break


        # Count the number of "@id" elements
        total_metadata_elements = len(json_data)
        percentage = (metadata_count / total_metadata_elements) * 100

        return percentage, ontology_minimal_metadata_list
    
    @staticmethod
    def calculate_metadata_percentage_via_portal(json_file_path, ontology_metadata):
        #print('ontology_metadata',ontology_metadata)
        # Load the new JSON format from the JSON file
        try:
            with open(json_file_path) as file:
                json_data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError

        # Initialize the ontology_minimal_metadata_list
        ontology_minimal_metadata_list = {}

        # Count the number of minimal metadata elements present in the ontology_metadata
        metadata_count = 0

        for metadata_element in json_data:
            metadata_mappings = metadata_element.get("metadataMappings")
            if metadata_mappings is not None:
                #print('metadata_mappings is not null', metadata_mappings)
                for mapping in metadata_mappings:
                    label_uri = mapping.get("label")
                    if len(label_uri.split(":")) > 1:
                        _, label = label_uri.split(":", 1)  # Split and get the second part
                    else:
                        label = label_uri
                    if label is not None:
                        #print('label_uri',label)
                        for k in ontology_metadata.keys():
                            #print('compare',k , 'and ', label)
                            if label == k:
                                #print('yes found one',label)
                                if not(label in ontology_minimal_metadata_list):
                                    ontology_minimal_metadata_list[label] = [k]
                                    metadata_count += 1
                                break


        # Count the number of "@id" elements
        total_metadata_elements = len(json_data)
        print('total_metadata_elements',total_metadata_elements)
        percentage = (metadata_count / total_metadata_elements) * 100

        return percentage, ontology_minimal_metadata_list
    
    @staticmethod
    def calculate_metadata_percentage_onto_portal(json_file_path, ontology_metadata):
        #print('ontology_metadata',ontology_metadata)
        # Load the new JSON format from the JSON file
        try:
            with open(json_file_path) as file:
                json_data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError

        # Initialize the ontology_minimal_metadata_list
        ontology_minimal_metadata_list = {}

        # Count the number of minimal metadata elements present in the ontology_metadata
        metadata_count = 0

        for metadata_element in json_data:
            metadata_mappings = metadata_element.get("metadataMappings")
            if metadata_mappings is not None:
                print('metadata_mappings is not null', metadata_mappings)
                for mapping in metadata_mappings:
                    label_uri = mapping.get("label_uri")
                    if label_uri is not None:
                        try:
                            uri_ref_label = URIRef(label_uri)
                        except ValueError:
                            print('Error converting label_uri to URIRef:', label_uri)
                            continue  # Skip to the next mapping if conversion fails

                        for k in ontology_metadata:
                            print('compare', k, 'and ', label_uri)
                            if uri_ref_label == URIRef(k):
                                print('yes found one', label_uri)
                                if label_uri in ontology_minimal_metadata_list:
                                    ontology_minimal_metadata_list[label_uri].append(k)
                                else:
                                    ontology_minimal_metadata_list[label_uri] = [k]
                                metadata_count += 1
                                break

        # Count the number of "@id" elements
        total_metadata_elements = len(json_data)
        percentage = (metadata_count / total_metadata_elements) * 100

        return percentage, ontology_minimal_metadata_list

###############################################################################

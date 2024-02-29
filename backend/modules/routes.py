import os, json
import base64
import requests
from datetime import datetime
from flask import Blueprint, Flask, jsonify, request, make_response, render_template, url_for,send_file
from werkzeug.utils import secure_filename
from weasyprint import HTML, CSS
from modules.models import UploadedOntology, OntologyViaURL, OntologyViaPortal, OntologyEvaluation, db
from modules.services.ontology_eval import OFAIRE, FOOPS, FAIRCHECKER
from modules.services.ontology_metadata_percentage import CalculateMetadataPercentage
from modules.services.ontology_file_parser import OntologyFileParser
from modules.services.download_ontology_from_portal import Download
from modules.services.generate_report import Report
from modules.settings import logger, UPLOAD_PATH, DOWNLOAD_PATH, MINIMAL_METADATA_FILE_PATH, MANDATORY_FINDABLE_METADATA_FILE_PATH, MANDATORY_REUSABLE_METADATA_FILE_PATH,RECOMMENDED_FINDABLE_METADATA_FILE_PATH, RECOMMENDED_REUSABLE_METADATA_FILE_PATH, OPTIONAL_REUSABLE_METADATA_FILE_PATH 

###############################################################################

template_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resources', 'templates'))

REPORT_HTML = "report.html"
REPORT_CSS = template_folder_path+"/report.css"
RENDER_URL = "http://localhost:5000"

pdf_link = 'generated_reports/MetaFAIRreport.pdf'
pdf_path = 'resources/'+pdf_link

onto_eval_bp = Blueprint('onto_eval', __name__, template_folder=template_folder_path)

@onto_eval_bp.route('/ontologyeval', methods=['GET'])
def get_OntologyEvaluation():
        
        acronym = request.args.get('ontologyAcronym')
        portalName = request.args.get('portalName')
        apikey = request.args.get('apiKey')
        ontology_url = request.args.get('ontology_url')
        ofaire_result=None
        foops_result=None
        fairchecker_result=None
        
        xstr = lambda s: s or ""
        logger.debug("ofaire:"+xstr(acronym)+xstr(portalName)+xstr(apikey))
        if ((acronym) and (portalName) and (apikey)):            
            # Call the OFaire API and retrieve the score
            ofaire_result = OFAIRE.evaluate_ontology_ofaire_api(portalName,apikey,acronym)
            # Call the Foops API and retrieve the score
            overall_score_foops = 'no overall score returned by foops'
            principle_scores = 'no principle scores returned by foops'
            # Call the Fairchecker API and retrieve the score
            overall_score_fairchecker = 'no overall score returned by fairchecker'
            fairchecker_scores_by_principle = 'no principle scores returned by fairchecker'

            #in the new iteraction : download ontology file
            #save it in repo git and try to pass it to foops and fc
        elif (ontology_url):
            ofaire_result = 'no result returned by ofaire'
            # Call the Foops API and retrieve the score
            foops_result=FOOPS.evaluate_ontology_foops_api(ontology_url)
            # Call the Fairchecker API and retrieve the score
            fairchecker_result=FAIRCHECKER.evaluate_ontology_fairchecker_api(ontology_url)

        # Create the response dictionary
        response = {
            "ofaire": ofaire_result,
            "foops": foops_result,
            "fairchecker": fairchecker_result,
            # Add the other APIs and their respective scores to the response dictionary
        }
        
        # Return the response as a JSON response
        return jsonify(response)

#Retrieve Metadata Percentages
#tested (works only with curated version)
#"https://raw.githubusercontent.com/arsarkar/meta-fair/main/metafair/src/test/resources/AGRO-curated.owl"

@onto_eval_bp.route('/ontologymetadata', methods=['POST'])
def get_ontology_metadata():
    data = request.get_json()
    if onto_url := data.get('onto_url'):
        semart = OntologyFileParser(onto_url)
        metadata = semart.get_metadata()
        return jsonify(metadata)
    else:
        return jsonify({"error": "Ontology URL not provided"})

@onto_eval_bp.route('/ontologymetadatavalue', methods=['POST'])
def get_ontology_metadata_value():
    requestBody = request.get_json()
    onto_url = requestBody.get('onto_url')
    metadata = requestBody.get('metadata')
    if onto_url:
        semart = OntologyFileParser(onto_url)
        metadata_dict = semart.get_metadata()
        metadata_value = semart.get_metadata_value(metadata_dict,metadata)
        #print("metdata_value",metadata_value)
        return jsonify(metadata_value)
    else:
        return jsonify({"error": "Ontology URL / or metadata not provided"})

#Retreive ontology semantic artefacts
@onto_eval_bp.route('/ontologysemanticartifacts', methods=['POST'])
def get_ontology_semantic_artifacts():
    requestBody = request.get_json()
    onto_url = requestBody.get('onto_url')
    if onto_url:
        semart = OntologyFileParser(onto_url)
        metadata_dict = semart.get_metadata_without_namespaces()
        return jsonify(metadata_dict)
    else:
        return jsonify({"error": "Ontology URL not provided"})

@onto_eval_bp.route('/semantic-artifacts-via-portals', methods=['POST'])
def get_ontology_semantic_artifacts_via_Portals():
    requestBody = request.get_json()
    onto_url = requestBody.get('onto_url')
    if onto_url:
        semart = OntologyFileParser(onto_url)
        metadata_dict = semart.get_metadata_without_namespaces()
        return jsonify(metadata_dict)
    else:
        return jsonify({"error": "Ontology URL not provided"})

#Ontology mandetory/extended/optional metadata
@onto_eval_bp.route('/ontology-mandatory-findable-metadata-percentage', methods=['POST'])
def ontology_mandatory_findable_metadata_percentage():
    requestBody = request.get_json()
    onto_url = requestBody.get('onto_url')
    if onto_url:
        semart = OntologyFileParser(onto_url)
        metadata_dict = semart.get_metadata()
        mandatory_findable_metadata_percentage,ontology_mandatory_findable_metadata_list=CalculateMetadataPercentage.calculate_metadata_percentage2(MANDATORY_FINDABLE_METADATA_FILE_PATH,metadata_dict)
        return jsonify({"mandatory_findable_metadata_percentage":mandatory_findable_metadata_percentage},
                       {"ontology_mandatory_findable_metadata_list":ontology_mandatory_findable_metadata_list})
    else:
        return jsonify({"error": "Ontology URL not provided"})

@onto_eval_bp.route('/ontology-mandatory-reusable-metadata-percentage', methods=['POST'])
def ontology_mandatory_reusable_metadata_percentage():
    requestBody = request.get_json()
    onto_url = requestBody.get('onto_url')
    if onto_url:
        semart = OntologyFileParser(onto_url)
        metadata_dict = semart.get_metadata()
        mandatory_reusable_metadata_percentage,ontology_minimal_metadata_list=CalculateMetadataPercentage.calculate_metadata_percentage2(MANDATORY_REUSABLE_METADATA_FILE_PATH,metadata_dict)
        return jsonify({"mandatory_reusable_metadata_percentage":mandatory_reusable_metadata_percentage},
                       {"ontology_mandatory_reusable_metadata_list":ontology_minimal_metadata_list})
    else:
        return jsonify({"error": "Ontology URL not provided"})

#ontology-recommended-findable-metadata-percentage
#ontology-recommended-reusable-metadata-percentage
@onto_eval_bp.route('/ontology-recommended-findable-metadata-percentage', methods=['POST'])
def ontology_recommended_findable_metadata_percentage():
    requestBody = request.get_json()
    onto_url = requestBody.get('onto_url')
    if onto_url:
        semart = OntologyFileParser(onto_url)
        metadata_dict = semart.get_metadata()
        recommended_findable_metadata_percentage,ontology_recommended_findable_metadata_list=CalculateMetadataPercentage.calculate_metadata_percentage2(RECOMMENDED_FINDABLE_METADATA_FILE_PATH,metadata_dict)
        return jsonify({"recommended_findable_metadata_percentage":recommended_findable_metadata_percentage},
                       {"ontology_recommended_findable_metadata_list":ontology_recommended_findable_metadata_list})
    else:
        return jsonify({"error": "Ontology URL not provided"})

@onto_eval_bp.route('/ontology-recommended-reusable-metadata-percentage', methods=['POST'])
def ontology_recommended_reusable_metadata_percentage():
    requestBody = request.get_json()
    onto_url = requestBody.get('onto_url')
    if onto_url:
        semart = OntologyFileParser(onto_url)
        metadata_dict = semart.get_metadata()
        recommended_reusable_metadata_percentage,ontology_recommended_reusable_metadata_list=CalculateMetadataPercentage.calculate_metadata_percentage2(RECOMMENDED_REUSABLE_METADATA_FILE_PATH,metadata_dict)
        return jsonify({"recommended_reusable_metadata_percentage":recommended_reusable_metadata_percentage},
                       {"ontology_recommended_reusable_metadata_list":ontology_recommended_reusable_metadata_list})
    else:
        return jsonify({"error": "Ontology URL not provided"})
    
#ontology-optional-reusable-metadata-percentage
@onto_eval_bp.route('/ontology-optional-reusable-metadata-percentage', methods=['POST'])
def ontology_optional_reusable_metadata_percentage():
    requestBody = request.get_json()
    onto_url = requestBody.get('onto_url')
    if onto_url:
        semart = OntologyFileParser(onto_url)
        metadata_dict = semart.get_metadata()
        optional_reusable_metadata_percentage,ontology_optional_reusable_metadata_list=CalculateMetadataPercentage.calculate_metadata_percentage2(OPTIONAL_REUSABLE_METADATA_FILE_PATH,metadata_dict)
        return jsonify({"optional_reusable_metadata_percentage":optional_reusable_metadata_percentage},
                       {"ontology_optional_reusable_metadata_list":ontology_optional_reusable_metadata_list})
    else:
        return jsonify({"error": "Ontology URL not provided"})
   
#Retreive onto metadata from portal by acronym
@onto_eval_bp.route('/ofaire/ontology-portals-all-metadata', methods=['POST'])
def ontology_all_metadata():
        requestBody = request.get_json()
        portal_name = requestBody.get('portal_name')
        onto_acronym = requestBody.get('onto_acronym')
        api_key = requestBody.get("api_key")
        response = Download.get_all_metadata_from_portal(portal_name, onto_acronym, api_key)
        return jsonify({"ontologyAcronym":f"{onto_acronym}"},
                       {"ontologyMetadata": response})
    
#Retreive onto metadata percentage from portal by acronym
@onto_eval_bp.route('/ofaire/ontology-metadata-percentage', methods=['POST'])
def ontology_metadata_percentage():
        requestBody = request.get_json()
        portal_name = requestBody.get('portal_name')
        onto_acronym = requestBody.get('onto_acronym')
        api_key = requestBody.get("api_key")
        response = Download.get_all_metadata_from_portal(portal_name,onto_acronym, api_key)
        minimal_metadata_percentage,ontology_minimal_metadata_list=CalculateMetadataPercentage.calculate_metadata_percentage(MANDATORY_FINDABLE_METADATA_FILE_PATH,response)
        return jsonify({"minimal_metadata_percentage":minimal_metadata_percentage},
                       {"ontology_minimal_metadata_list":ontology_minimal_metadata_list})

@onto_eval_bp.route('/ofaire/ontology-mandatory-findable-metadata-percentage', methods=['POST'])
def ontology_portal_mandatory_findable_metadata_percentage():
        requestBody = request.get_json()
        portal_name = requestBody.get('portal_name')
        onto_acronym = requestBody.get('onto_acronym')
        api_key=requestBody.get("api_key")
        response = Download.get_all_metadata_from_portal(portal_name, onto_acronym, api_key)
        mandatory_findable_metadata_percentage,ontology_mandatory_findable_metadata_list=CalculateMetadataPercentage.calculate_metadata_percentage_via_portal(MANDATORY_FINDABLE_METADATA_FILE_PATH,response)
        return jsonify({"mandatory_findable_metadata_percentage":mandatory_findable_metadata_percentage},
                       {"ontology_mandatory_findable_metadata_list":ontology_mandatory_findable_metadata_list})

@onto_eval_bp.route('/ofaire/ontology-mandatory-reusable-metadata-percentage', methods=['POST'])
def ontology_portal_mandatory_reusable_metadata_percentage():
        requestBody = request.get_json()
        portal_name = requestBody.get('portal_name')
        onto_acronym = requestBody.get('onto_acronym')
        api_key = requestBody.get("api_key")
        response = Download.get_all_metadata_from_portal(portal_name, onto_acronym, api_key)
        mandatory_reusable_metadata_percentage,ontology_minimal_metadata_list=CalculateMetadataPercentage.calculate_metadata_percentage_via_portal(MANDATORY_REUSABLE_METADATA_FILE_PATH,response)
        return jsonify({"mandatory_reusable_metadata_percentage":mandatory_reusable_metadata_percentage},
                       {"ontology_mandatory_reusable_metadata_list":ontology_minimal_metadata_list})

#ontology-recommended-findable-metadata-percentage
#ontology-recommended-reusable-metadata-percentage
@onto_eval_bp.route('/ofaire/ontology-recommended-findable-metadata-percentage', methods=['POST'])
def ontology_portal_recommended_findable_metadata_percentage():
        requestBody = request.get_json()
        portal_name = requestBody.get('portal_name')
        onto_acronym = requestBody.get('onto_acronym')
        api_key = requestBody.get("api_key")
        response = Download.get_all_metadata_from_portal(portal_name, onto_acronym, api_key)
        recommended_findable_metadata_percentage,ontology_recommended_findable_metadata_list=CalculateMetadataPercentage.calculate_metadata_percentage_via_portal(RECOMMENDED_FINDABLE_METADATA_FILE_PATH,response)
        return jsonify({"recommended_findable_metadata_percentage":recommended_findable_metadata_percentage},
                       {"ontology_recommended_findable_metadata_list":ontology_recommended_findable_metadata_list})

@onto_eval_bp.route('/ofaire/ontology-recommended-reusable-metadata-percentage', methods=['POST'])
def ontology_portal_recommended_reusable_metadata_percentage():
        requestBody = request.get_json()
        portal_name = requestBody.get('portal_name')
        onto_acronym = requestBody.get('onto_acronym')
        api_key = requestBody.get("api_key")
        response = Download.get_all_metadata_from_portal(portal_name, onto_acronym, api_key)
        recommended_reusable_metadata_percentage,ontology_recommended_reusable_metadata_list=CalculateMetadataPercentage.calculate_metadata_percentage_via_portal(RECOMMENDED_REUSABLE_METADATA_FILE_PATH,response)
        return jsonify({"recommended_reusable_metadata_percentage":recommended_reusable_metadata_percentage},
                       {"ontology_recommended_reusable_metadata_list":ontology_recommended_reusable_metadata_list})
    
#ontology-optional-reusable-metadata-percentage
@onto_eval_bp.route('/ofaire/ontology-optional-reusable-metadata-percentage', methods=['POST'])
def ontology_portal_optional_reusable_metadata_percentage():
        requestBody = request.get_json()
        portal_name = requestBody.get('portal_name')
        onto_acronym = requestBody.get('onto_acronym')
        api_key = requestBody.get("api_key")
        response = Download.get_all_metadata_from_portal(portal_name, onto_acronym, api_key)
        optional_reusable_metadata_percentage,ontology_optional_reusable_metadata_list=CalculateMetadataPercentage.calculate_metadata_percentage_via_portal(OPTIONAL_REUSABLE_METADATA_FILE_PATH,response)
        return jsonify({"optional_reusable_metadata_percentage":optional_reusable_metadata_percentage},
                       {"ontology_optional_reusable_metadata_list":ontology_optional_reusable_metadata_list})

#######################################

#Download ontology file from portal by acronym 
@onto_eval_bp.route('/ofaire/ontology-download-from-portal', methods=['POST'])
def download_ontology_from_portals():
        requestBody = request.get_json()
        portal_name = requestBody.get('portal_name')
        onto_acronym = requestBody.get('onto_acronym')
        api_key = requestBody.get("api_key")
        curatedOntologyPath = Download.download_ontology_from_portal(portal_name, onto_acronym, api_key)
        return curatedOntologyPath

#uploadontofromOfaireandpasspathontotofoops
#upload_file
@onto_eval_bp.route('/ontology-upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return {'error': 'No files part'}, 400

    files = request.files.getlist('files')
    if not files:
        return {'error': 'No selected files'}, 400

    try:
        upload_folder = UPLOAD_PATH
        os.makedirs(upload_folder, exist_ok=True)  # Create the upload folder if it doesn't exist

        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            # Save data to UploadedOntology model
            upload_date = datetime.now()
            uploaded = UploadedOntology(file_path=file_path, upload_date=upload_date)
            db.session.add(uploaded)
        
        db.session.commit()

        return {'message': 'Files uploaded successfully'}
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        db.session.close()
        
@onto_eval_bp.route('/generate_report', methods=['POST'])
def generate_report():
    semantic_artefact_source={}
    summary_of_extracted_metadata={}
    semantic_artefact_evaluation={}
    landscape_charts={}
    
    requestBody = request.get_json()
    semantic_artefact_source = requestBody.get("semantic_artefact_source")
    #print('requestbody semantic_artefact_source',semantic_artefact_source)   

    summary_of_extracted_metadata = requestBody.get("summary_of_extracted_metadata")
    #print('requestbody summary_of_extracted_metadata',summary_of_extracted_metadata) 
    semantic_artefact_evaluation = requestBody.get("semantic_artefact_evaluation")
    summary_transformed = []
    
    for item in summary_of_extracted_metadata:
        new_item = {item['title']: item['stats']}
        summary_transformed.append(new_item)

    #print('requestbody summary_transformed',summary_transformed) 
    metadata_charts= requestBody.get("metadata_charts")
    metadata_percentages= requestBody.get("metadata_percentages")
    landscape_charts = requestBody.get("landscape_charts")
    
    # Calculate averages for each key in metadata_percentages
    averages = {}
    for key, data_list in metadata_percentages.items():
        total_data = [data_dict['data'] for data_dict in data_list][0]
        #we divide by 2 an not len(total_data) because A and I ane not counted
        average = sum(total_data) / 2
        averages[key.lower()+'_chart'] = average
    
    # Get the current date and time
    creation_date = datetime.now().strftime('%Y-%m-%d')
    logger.debug("creation_date", creation_date)
    
    # Create the context 
    context = {
        "semantic_artefact_source" : semantic_artefact_source,
        "summary_of_extracted_metadata":summary_transformed,
        "semantic_artefact_evaluation":semantic_artefact_evaluation,
        "metadata_charts":metadata_charts,
        "metadata_percentages":averages,
        "landscape_charts":landscape_charts,
        "creation_date": creation_date
    }

    # Generate the report PDF using weasyprint
    html_content = render_template(REPORT_HTML, context=context)
    html = HTML(string=html_content,base_url=RENDER_URL)    
    css = CSS(filename=REPORT_CSS)
    
    # Apply the CSS to the HTML content    
    report_pdf = html.write_pdf(stylesheets=[css])
    
    # Save the PDF to the specified path
    with open(pdf_path, 'wb') as f:
        f.write(report_pdf)

    # Return a response to the user
    #return f"Report generated and saved to: {pdf_path}"
    # Set the appropriate response headers for file download
    response = send_file(pdf_link, as_attachment=True)
    response.headers["Content-Disposition"] = "attachment; filename=MetaFAIRreport.pdf"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

#######################################

@onto_eval_bp.route('/ofaire/ontology-eval-of-three-apis', methods=['GET'])
def get_onto_eval_for_three_apis():
        acronym = request.args.get('ontologyAcronym')
        portalName = request.args.get('portalName')
        apikey = request.args.get('apiKey')
        ontology_url = request.args.get('ontology_url')
        
        ofaire_result=None
        foops_result=None
        fairchecker_result=None
        
        xstr = lambda s: s or ""
        logger.debug("ofaire:"+xstr(acronym)+xstr(portalName)+xstr(apikey))
        if ((acronym) and (portalName) and (apikey)):            
            # Call the OFaire API and retrieve the score
            ofaire_result = OFAIRE.evaluate_ontology_ofaire_api(portalName, apikey, acronym)
            
            # Download ontology file from portal 
            curatedOntologyPath = Download.download_ontology_from_portal(portalName, acronym, apikey)
            
            # Call the Foops API and retrieve the score
            foops_result=FOOPS.evaluate_ontology_foops_api(curatedOntologyPath)
            # Uncomment Fairchecker part when the app got deployed
            # Call the Fairchecker API and retrieve the score
            #fairchecker_result=FAIRCHECKER.evaluate_ontology_fairchecker_api(curatedOntologyPath)
        elif (ontology_url):
            #ofaire_result = 'no result returned by ofaire'
            # Call the Foops API and retrieve the score
            foops_result=FOOPS.evaluate_ontology_foops_api(ontology_url)
            
            # Call the Fairchecker API and retrieve the score
            fairchecker_result=FAIRCHECKER.evaluate_ontology_fairchecker_api(ontology_url) 

        # Create the response dictionary
        response = {
            "ofaire": ofaire_result,
            "foops": foops_result,
            "fairchecker": fairchecker_result,
            # Add the other APIs and their respective scores to the response dictionary
        }        
        # Return the response as a JSON response
        return jsonify(response)
    
#chart generation for report
@onto_eval_bp.route('/generate-charts', methods=['POST'])
def generate_charts():
    requestBody = request.get_json()
    metadata_list = requestBody.get("metadata_list")
    #print("metadata list", metadata_list)
    return jsonify(Report.generate_charts(metadata_list))

@onto_eval_bp.route('/get-ontology-via-url', methods=['GET'])
def get_ontology_via_url():
    try:
        # Fetch all rows from the OntologyViaURL table
        ontology_rows = db.session.query(OntologyEvaluation).all()
        
        # Serialize the rows to a list of dictionaries
        serialized_rows = [{
            'id': row.id,
            'source': row.source,
            'portal_name': row.portal_name,
            'semantic_artefact_acronym': row.semantic_artefact_acronym,
            'semantic_artefact_URL': row.semantic_artefact_URL,
            'semantic_artefact_domain': row.semantic_artefact_domain,
            'semantic_artefact_version': row.semantic_artefact_version,
            'evaluation_date': row.evaluation_date.strftime('%Y-%m-%d'),
            'ofaire_score': row.ofaire_score,
            'fairchecker_score': row.fairchecker_score,
            'foops_score': row.foops_score,
            'user_id': row.user_id
        } for row in ontology_rows]
        
        return jsonify(serialized_rows), 200

    except Exception as e:
        print(f"Error occurred while fetching data: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500
    
    finally:
        db.session.close()
        
@onto_eval_bp.route('/generate-landscape', methods=['POST'])
def generate_landscape():
    # Get the data from the request body
    request_data = request.get_json()
    tool_data_list = request_data
    
    if not tool_data_list:
        return jsonify({'message': 'No data provided'}), 400
    
    try:
        AllChartsPaths = {}  # Dictionary to store chart paths for all tools
        
        for tool_data in tool_data_list:
            tool_name = tool_data.get('toolName', None)
            scatter_data = tool_data.get('points', [])
            #print('tool_name', tool_name, 'scatter_data', scatter_data)
            if not tool_name or not scatter_data:
                continue
            
            # Process scatter_data to format y_date
            processed_scatter_data = []
            for point in scatter_data:
                y_date = point.get('y_date')
                if y_date:
                    y_date_formatted = datetime.strptime(y_date, '%Y-%m-%d').strftime('%Y-%m')
                    processed_scatter_data.append({"y_date": y_date_formatted, "x_score": float(point.get('x_score', 0))})
            #print('processed_scatter_data', processed_scatter_data)
            # Generate the scatter chart and get the image path
            img_path = f'{tool_name}_chart.png'
            Report.generate_and_save_scatter_chart_plotly(img_path, processed_scatter_data)
            
            # Store the chart path in the response dictionary
            AllChartsPaths[tool_name + "_chart"] = img_path
            
        #print('AllChartsPaths', AllChartsPaths)
        # Return the scatter chart image paths
        return jsonify(AllChartsPaths)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@onto_eval_bp.route('/save-onto-eval', methods=['POST'])
def save_onto_eval_data():
    semantic_artefact_URL = ""
    requestBody = request.get_json()
    semantic_artefact_URL = requestBody.get("semantic_artefact_URL")
    ofaire_score = requestBody.get("ofaire_score")
    fairchecker_score = requestBody.get("fairchecker_score")
    foops_score = requestBody.get("foops_score")
    #it must be gotten from emit of semantic art vue
    semantic_artefact_version = requestBody.get("semantic_artefact_version")
    semantic_artefact_domain = requestBody.get("semantic_artefact_domain")
    source = requestBody.get("source")
    portal_name = requestBody.get("portal_name")
    semantic_artefact_acronym = requestBody.get("semantic_artefact_acronym")
    currentUserId = requestBody.get("currentUserId")
    #OntologyViaPortal = requestBody.get("OntologyViaPortal")
    #ontology_eval = requestBody.get("ontology_eval")
    if not semantic_artefact_version and not semantic_artefact_domain:
        return make_response(jsonify({"error": "Semantic artefact version and domain are missing."}), 400)

    if not semantic_artefact_version:
        return make_response(jsonify({"error": "Semantic artefact version is missing."}), 400)
    
    if not semantic_artefact_domain:
        return make_response(jsonify({"error": "Semantic artefact domain is missing."}), 400)
    # Add the instance to the session and commit to save it to the database
    if (semantic_artefact_URL!=None):        

        # Save data to OntologyViaURL model
        ontology_eval_instance = OntologyEvaluation(
            source=source,
            portal_name=portal_name,
            semantic_artefact_acronym=semantic_artefact_acronym,
            semantic_artefact_URL=semantic_artefact_URL,
            semantic_artefact_domain=semantic_artefact_domain,
            semantic_artefact_version=semantic_artefact_version,
            evaluation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ofaire_score=ofaire_score,
            fairchecker_score=fairchecker_score,
            foops_score=foops_score,
            user_id= currentUserId
        )
    elif (portal_name!="" and semantic_artefact_acronym!=""):
        # Save data to OntologyViaURL model
        ontology_eval_instance = OntologyEvaluation(
            source=source,
            portal_name=portal_name,
            semantic_artefact_acronym=semantic_artefact_acronym,
            semantic_artefact_URL=semantic_artefact_URL,
            semantic_artefact_domain=semantic_artefact_domain,
            semantic_artefact_version=semantic_artefact_version,
            evaluation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ofaire_score=ofaire_score,
            fairchecker_score=fairchecker_score,
            foops_score=foops_score,
            user_id= currentUserId
        )
    else:
        return jsonify({"error": "Ontology URL not provided"})
    
    try:
        existing = False
        ontology_rows = db.session.query(OntologyEvaluation).all()
        serialized_rows = [{
            'id': row.id,
            'source': row.source,
            'portal_name': row.portal_name,
            'semantic_artefact_acronym': row.semantic_artefact_acronym,
            'semantic_artefact_URL': row.semantic_artefact_URL,
            'semantic_artefact_domain': row.semantic_artefact_domain,
            'semantic_artefact_version': row.semantic_artefact_version,
            'evaluation_date': row.evaluation_date.strftime('%Y-%m-%d'),
            'ofaire_score': row.ofaire_score,
            'fairchecker_score': row.fairchecker_score,
            'foops_score': row.foops_score,
            'user_id': row.user_id
        } for row in ontology_rows]

        for instance in serialized_rows:
            if instance['semantic_artefact_acronym'] == ontology_eval_instance.semantic_artefact_acronym and instance['semantic_artefact_URL'] == ontology_eval_instance.semantic_artefact_URL and instance['semantic_artefact_domain'] == ontology_eval_instance.semantic_artefact_domain and instance['semantic_artefact_version'] == ontology_eval_instance.semantic_artefact_version:
                existing = True
                break

        if not existing:
            db.session.add(ontology_eval_instance)
            db.session.commit()

    except Exception as e:
        print(f"Error occurred while fetching data: {e}")    
    
    finally:
        db.session.close()
    
    # Once the data is successfully saved, return the response with a success message
    return make_response(jsonify({"message": "ontology data has been successfully saved ! "}), 200)

###############################################################################
        

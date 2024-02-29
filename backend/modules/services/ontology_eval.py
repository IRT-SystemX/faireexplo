import os, requests
from requests import HTTPError
from flask import jsonify
from modules.settings import GET_FOOPS_API 
from modules.settings import logger

###############################################################################

AGROPORTAL = 'https://services.agroportal.lirmm.fr/'
INDUSTRYPORTAL = 'http://services.industryportal.enit.fr/'
BIOPORTAL = 'https://services.bioportal.lirmm.fr/'
FAIR_CHECKER = 'https://fair-checker.france-bioinformatique.fr/api/check/metrics_all'

#######################################

class OFAIRE:

    @staticmethod
    def evaluate_ontology_ofaire_api(portalName, apikey, acronym):
        tool_result=None
        try:

            # Call the OFaire API and retrieve the score based on portalName
            if (portalName=='agroportal'):
                response_ofaire = requests.get(AGROPORTAL + "ofaire",
                                               params={'portal': portalName, 'ontologies': acronym, 'apikey': apikey})
            elif (portalName=='industryportal'):
                response_ofaire = requests.get(INDUSTRYPORTAL + "fair",
                                               params={'portal':portalName, 'ontologies': acronym, 'apikey': apikey})
            elif (portalName=='bioportal'):
                response_ofaire = requests.get(BIOPORTAL + "ofaire",
                                               params={'portal': portalName, 'ontologies': acronym, 'apikey': apikey})

            if response_ofaire.status_code == 200:
                response_data_ofaire = response_ofaire.json()
                if response_data_ofaire["status"]["success"]==True:
                    main_principles = response_data_ofaire["ontologies"][acronym]
                    overall_score_ofaire = main_principles["normalizedScore"]

                    tool_result = {"toolName": "ofaire", "overallScore": overall_score_ofaire, "principleResults": []}

                    for main_principle_key, main_principle_value in main_principles.items():
                        if main_principle_key in ["Findable", "Accessible", "Interoperable", "Reusable"]:

                            for principle_key, principle_value in main_principle_value.items():
                                if not isinstance(principle_value, float) and not isinstance(principle_value, int):
                                    principle_result = {"principleName": principle_key,
                                                        "principleScore": principle_value["normalizedScore"],
                                                        "metricResults": []}
                                    for metric_key, metric_value in principle_value["results"].items():
                                        metric_result = {"metricName": metric_key,
                                                        "metricScore": metric_value["score"],
                                                        "description": metric_value["question"],
                                                        "resultExplanation": metric_value["explanation"],
                                                        "alertGroup": "groupName",
                                                        "status":""}
                                        if metric_value["score"] == 0:
                                            metric_result["status"] = "FAILED"
                                        elif metric_value["score"] < metric_value["maxCredits"]:
                                            metric_result["status"] = "PARTIALLY_PASSED"
                                        else:
                                            metric_result["status"] = "PASSED"
                                        principle_result["metricResults"].append(metric_result)
                                    tool_result["principleResults"].append(principle_result)
                else: response_ofaire=None                    
            else: response_ofaire=None
        except HTTPError as e:
            return jsonify({"error": e.response.reason})
        return tool_result

#######################################

class FOOPS:

    @staticmethod
    def evaluate_ontology_foops_api(ontology_url):
        try:
            # Call the Foops API and retrieve the score
            headers = {
                'accept': 'application/json;charset=UTF-8',
                'Content-Type': 'application/json;charset=UTF-8',
            }
            json_data = {
                'ontologyUri': ontology_url,
            }
            
            response_foops = requests.post(GET_FOOPS_API(), headers=headers, json=json_data)
            if response_foops.status_code == 200:
                response_data_foops = response_foops.json()
                overall_score_foops = response_data_foops["overall_score"]*100

                tool_result = {"toolName": "foops", "overallScore": overall_score_foops, "principleResults": []}
                
                for check in response_data_foops["checks"]:
                    #current_metric_score = (check["total_passed_tests"] / check["total_tests_run"])
                    current_metric_score = (check["total_passed_tests"] / check["total_tests_run"]) * 100
                    metric_status = "PASSED"
                    if check["status"] == "error":
                        if check["total_passed_tests"] > 0:
                            metric_status = "PARTIALLY_PASSED"
                        else:
                            metric_status = "FAILED"
                    metric_result= {
                        "metricName": check["id"],
                        "metricScore": current_metric_score,
                        "description": check["description"],
                        "resultExplanation": check["explanation"],
                        "alertGroup": "groupName",
                        "status": metric_status
                        }
                    if not any(pr["principleName"] == check["principle_id"] for pr in tool_result["principleResults"]):
                        principle_result = {"principleName": check["principle_id"],
                                            "principleScore": 0,
                                            "metricScores": [current_metric_score],
                                            "metricResults": [metric_result]
                                            }
                        tool_result["principleResults"].append(principle_result)
                    else:
                        for pr in tool_result["principleResults"]:
                            if pr["principleName"] == check["principle_id"]:
                                pr["metricResults"].append(metric_result)
                                pr["metricScores"].append(current_metric_score)
                for pr in tool_result["principleResults"]:
                    pr["principleScore"] = sum(pr["metricScores"]) / len(pr["metricScores"])
            else:
                tool_result = None

            return tool_result

        except HTTPError as e:
            return jsonify({"error": str(e.response.reason)})

        except Exception as e:
            logger.debug(e)
            return None

#######################################

class FAIRCHECKER:

    @staticmethod
    def evaluate_ontology_fairchecker_api(ontology_url):
        try:
            # Call the Fairchecker API and retrieve the score
            response_fairchecker = requests.get(FAIR_CHECKER, params={ 'url': ontology_url })
            
            if response_fairchecker.status_code == 200:
                response_data_fairchecker = response_fairchecker.json()
                score_by_principle=[int(item['score']) for item in response_data_fairchecker]
                #calculate normalized score
                F_norm = 0
                A_norm = 0
                I_norm = 0
                R_norm = 0
                FAIR_norm = 0
                
                for item in response_data_fairchecker:
                    if str(item['metric']).startswith("F"):
                        print(item['metric'],':',item['score'])
                        F_norm += int(item['score'])
                    elif str(item['metric']).startswith("A"):
                        A_norm += int(item['score'])
                    elif str(item['metric']).startswith("I"):
                        I_norm += int(item['score'])
                    elif str(item['metric']).startswith("R"):
                        R_norm += int(item['score'])
                
                FAIR_norm = round((F_norm + A_norm + I_norm + R_norm) / 28 * 100)
                overall_score_fairchecker = FAIR_norm
                #score moyen*100
                tool_result = {"toolName": "fairchecker", "overallScore": overall_score_fairchecker, "principleResults": []}
                for metric_data in response_data_fairchecker:
                    metric_id = str(metric_data["metric"])
                    score = metric_data["score"]
                    '''principle_result = {"principleName": metric_id,
                                        "principleScore": int(score),
                                        "metricResults": []}
                    tool_result["principleResults"].append(principle_result)'''
                    
                    if metric_id.startswith("F"):
                        principle_result = {"principleName": metric_id,
                                        "principleScore": int(score)/ 8* 100,
                                        "metricResults": []}
                        tool_result["principleResults"].append(principle_result)
                    elif metric_id.startswith("A"):
                        principle_result = {"principleName": metric_id,
                                        "principleScore": int(score),
                                        "metricResults": []}
                        tool_result["principleResults"].append(principle_result)
                    elif metric_id.startswith("I"):
                        principle_result = {"principleName": metric_id,
                                        "principleScore": int(score)/ 14 * 100,
                                        "metricResults": []}
                        tool_result["principleResults"].append(principle_result)
                    elif metric_id.startswith("R"):
                        principle_result = {"principleName": metric_id,
                                        "principleScore": int(score)/ 6 * 100,
                                        "metricResults": []}
                        tool_result["principleResults"].append(principle_result)

            else:
                tool_result = None
            
            return tool_result

        except HTTPError as e:
            return jsonify({"error": str(e.response.reason)})

        except Exception as e:
            logger.debug(e)
            return None

###############################################################################


const API_BASE_URL = import.meta.env.VITE_BACKEND_URL ? import.meta.env.VITE_BACKEND_URL : '/api/metafair/';

const FAIRCHECKER_WEBSITE="https://github.com/IFB-ElixirFr/fair-checker";
const FOOPS_WEBSITE="https://github.com/oeg-upm/fair_ontologies";
const OFAIRE_WEBSITE="https://github.com/agroportal/fairness";

import axios from 'axios';
axios.defaults.timeout = 120000;

export default {
  apiBaseUrl: API_BASE_URL,
  FAIRCHECKER_WEBSITE:FAIRCHECKER_WEBSITE,
  FOOPS_WEBSITE:FOOPS_WEBSITE,
  OFAIRE_WEBSITE:OFAIRE_WEBSITE,

  endpoints: {
    ontologyUpload: `${API_BASE_URL}ontology-upload`,
    ontologySemanticArtifacts: `${API_BASE_URL}ontologysemanticartifacts`,
    
    ontologyDownload: `${API_BASE_URL}ontologydownload`,
    ontologyGet: `${API_BASE_URL}get-ontology-via-url`,
    pdfGenerator: `${API_BASE_URL}generate_report`,
    saveSemanticArtefactEval: `${API_BASE_URL}save-onto-eval`,
    generateReportCharts: `${API_BASE_URL}generate-charts`,
    generateReportLandscape: `${API_BASE_URL}generate-landscape`,

    mandatoryFindableMetadataPercentage: `${API_BASE_URL}ontology-mandatory-findable-metadata-percentage`,
    mandatoryReusableMetadataPercentage: `${API_BASE_URL}ontology-mandatory-reusable-metadata-percentage`,
    recommendedFindableMetadataPercentage: `${API_BASE_URL}ontology-recommended-findable-metadata-percentage`,
    recommendedReusableMetadataPercentage: `${API_BASE_URL}ontology-recommended-reusable-metadata-percentage`,
    optionalReusableMetadataPercentage: `${API_BASE_URL}ontology-optional-reusable-metadata-percentage`,

    mandatoryFindableMetadataPercentageViaPortal: `${API_BASE_URL}ofaire/ontology-mandatory-findable-metadata-percentage`,
    mandatoryReusableMetadataPercentageViaPortal: `${API_BASE_URL}ofaire/ontology-mandatory-reusable-metadata-percentage`,
    recommendedFindableMetadataPercentageViaPortal: `${API_BASE_URL}ofaire/ontology-recommended-findable-metadata-percentage`,
    recommendedReusableMetadataPercentageViaPortal: `${API_BASE_URL}ofaire/ontology-recommended-reusable-metadata-percentage`,
    optionalReusableMetadataPercentageViaPortal: `${API_BASE_URL}ofaire/ontology-optional-reusable-metadata-percentage`,

    ofaireMetadataPercentage: `${API_BASE_URL}ofaire/ontology-metadata-percentage`,
    ofaireMetadataAll: `${API_BASE_URL}ofaire/ontology-portals-all-metadata`,
    ofaireEvalByThreeAPIS: `${API_BASE_URL}ofaire/ontology-eval-of-three-apis`,    
  },
};

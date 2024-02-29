<script>
import axios from 'axios';
import config from '@/config.js';
import SemanticArtefacts from '@/views/dashboard/SemanticArtefacts.vue';

export default {

    inject: ['emitter'],
    data() {
        return {
            extractedMetadata: [],
            semArtURL: '',
            semArtDataPortal: {},
            ontologyEvaluationPortal: {},
            ontologyEvaluationURL: {},
            series: reactive({}),
            ontologyChartsPaths: {},
            ontologyLandscapePaths: {},
            allOntologies: {},
        };
    },
    mounted() {
        //Receiving data about Semantic artefact Source
        this.receiveSemanticArtefactURL();
        this.receiveSemanticArtefactPortalData();
        //Receiving data about Summary of extracted metadata
        this.receiveExtractedMetadata();
        //Receiving data about FAIR overall score
        this.receiveOntoEvalFromURL();
        this.receiveOntoEvalFromPortal();
        //Receiving data about metadata percentages
        this.receiveMetdataPercentage();
        //Receiving data about alerts
        console.log('Component PDF generator is listening for extracted metadata event');
    },
    methods: {
        //Receiving data about Semantic artefact Source

        //Add receiveSemanticArtefactFileName or path

        receiveSemanticArtefactURL() {
            this.emitter.on('onto_url', (data) => {
                //emptying variables

                this.semArtURL = '';
                this.semArtDataPortal = {};

                this.semArtURL = data;
                console.log('received sem art url by pdf generator:', data);
                console.log('var sem art url by pdf generator:', this.semArtURL);
            });
        },

        receiveSemanticArtefactPortalData() {
            this.emitter.on('semantic_artifacts_data_via_portal', (data) => {
                //emptying variables

                this.semArtURL = '';
                this.semArtDataPortal = {};

                this.semArtDataPortal = data;
                console.log('received sem art portaldata by pdf generator:', data);
                console.log('var sem art portaldata by pdf generator:', this.semArtDataPortal);
            });
        },

        receiveExtractedMetadata() {
            this.emitter.on('extracted_metadata', (data) => {
                //this.extractedMetadata = [];
                this.extractedMetadata = data;
                console.log('received extracted metadata by pdf generator:', data);
                console.log('var extracted metadata by pdf generator:', this.extractedMetadata);
            });
        },

        receiveOntoEvalFromPortal() {

            this.emitter.on('onto_eval_via_portal', (data) => {
                this.ontologyEvaluationURL, this.ontologyEvaluationPortal = {};
                this.ontologyEvaluationPortal = data;
                console.log('onto_eval_via_portal', data);
                console.log('var onto_eval_via_portal:', this.ontologyEvaluationPortal);
            });

        },

        receiveOntoEvalFromURL() {


            this.emitter.on('onto_eval_via_url', (data) => {
                this.ontologyEvaluationURL, this.ontologyEvaluationPortal = {};
                this.ontologyEvaluationURL = data;
                console.log('onto_eval_via_url', data);
                console.log('var onto_eval_via_url:', this.ontologyEvaluationURL);
            });

        },

        receiveMetdataPercentage() {
            this.emitter.on('new_series_variable', (data) => {
                this.series = reactive({});
                this.series = data;
                console.log('new_series_variable', data);
                console.log('var new_series_variable:', this.series);
            });

        },

        async generateReportCharts() {
            console.log('generateReportCharts new_series_variable:', this.series);
            // Create an array of objects with wrapped key-value pairs
            const metadata_list = Object.entries(this.series).map(([key, value]) => ({ [key]: value }));
            console.log('generateReportCharts metadata_list:', metadata_list);

            const requestBody = {
                "metadata_list": metadata_list
            };

            try {
                const response = await axios.post(config.endpoints.generateReportCharts, requestBody);
                console.log('POST endpoint response:', response.data);
                return response.data; // Return the response data

            } catch (error) {
                // Handle errors
                console.error('Error consuming POST endpoint:', error);
                return null; // or throw an error 
            }

        },

        async getAllOntologies() {
            console.log('getAllOntologies');
            try {
                const response = await axios.get(config.endpoints.ontologyGet);
                console.log('get-ontology endpoint response:', response.data);
                return response.data; // Return the response data

            } catch (error) {
                // Handle errors
                console.error('Error consuming get-ontology endpoint:', error);
                return null; // or throw an error 
            }
        },

        async generateReportLandscape() {
            console.log('generateReportLandscape');

            try {
                // Call getAllOntologies() to get the ontology data
                const ontologyData = await this.getAllOntologies();

                // Construct dataList for multiple tools
                const dataList = [
                    {
                        "toolName": "foops",
                        "points": []
                    },
                    {
                        "toolName": "ofaire",
                        "points": []
                    },
                    {
                        "toolName": "fairchecker",
                        "points": []
                    }
                ];

                if (ontologyData) {
                    // Check each ontology data item
                    ontologyData.forEach(item => {
                        if (item.foops_score !== null) {
                            dataList[0].points.push({ "y_date": item.evaluation_date, "x_score": parseFloat(item.foops_score).toFixed(2) });
                        }
                        if (item.ofaire_score !== null) {
                            dataList[1].points.push({ "y_date": item.evaluation_date, "x_score": parseFloat(item.ofaire_score).toFixed(2) });
                        }
                        if (item.fairchecker_score !== null) {
                            dataList[2].points.push({ "y_date": item.evaluation_date, "x_score": parseFloat(item.fairchecker_score).toFixed(2) });
                        }
                    });
                }

                console.log('dataList', dataList);
                const response = await axios.post(config.endpoints.generateReportLandscape, dataList);
                console.log('POST endpoint generateReportLandscape response:', response.data);

                return response.data; // Return the response data

            } catch (error) {
                // Handle errors
                console.error('Error consuming generateReportLandscape endpoint:', error);
                return null; // or throw an error 
            }
        },



        async generatePDF() {

            //TODO: check if needed
            this.receiveSemanticArtefactURL();
            this.receiveSemanticArtefactPortalData();
            this.receiveExtractedMetadata();
            this.receiveOntoEvalFromURL();
            this.receiveOntoEvalFromPortal();
            this.receiveMetdataPercentage();

            this.ontologyChartsPaths = await this.generateReportCharts();
            /*this.ontologyLandscapePaths = {
                "fairchecker_chart": "scatter_chart.png",
                "foops_chart": "scatter_chart.png",
                "ofaire_chart": "scatter_chart.png"
            }*/
            this.ontologyLandscapePaths = await this.generateReportLandscape();
            //this.allOntologies = await this.getAllOntologies();

            console.log('this.ontologyLandscapePaths:', this.ontologyChartsPaths);

            //console.log('this.allOntologies:', await this.getAllOntologies());

            const requestBody = {
                "semantic_artefact_source": {
                    "semantic_artefact_file": "None",
                    "semantic_artefact_url": this.semArtURL,
                    "semantic_artefact_from_portal": this.semArtDataPortal

                },
                "summary_of_extracted_metadata": this.extractedMetadata,
                "semantic_artefact_evaluation": {},
                "metadata_charts": this.ontologyChartsPaths,
                "metadata_percentages": this.series,
                "landscape_charts": this.ontologyLandscapePaths
            };

            if (this.semArtURL != '') {
                requestBody.semantic_artefact_evaluation = this.ontologyEvaluationURL;
                console.log('if1');
            }
            else if (this.semArtDataPortal != {}) {
                requestBody.semantic_artefact_evaluation = this.ontologyEvaluationPortal;
                console.log('if2');
            }
            else {
                requestBody.semantic_artefact_evaluation = {};
                console.log('if3');
            }
            console.log('generatePDF endpoint requestBody:', requestBody);
            try {
                const response = await axios.post(config.endpoints.pdfGenerator, requestBody,
                    {
                        responseType: 'blob', // Set the responseType to 'blob' to get the binary data as Blob
                        headers: {
                            'Content-Disposition': 'attachment; filename="report_FAIR_explore.pdf"',
                        },
                    }
                );

                console.log('POST endpoint response:', response.data);
                // Check if the response status is okay (e.g., 200)
                if (response.status === 200) {
                    // Create a Blob URL from the response data
                    const pdfBlob = new Blob([response.data], { type: 'application/pdf' });
                    const pdfUrl = URL.createObjectURL(pdfBlob);

                    // Open the PDF in a new window
                    window.open(pdfUrl, '_blank');
                } else {
                    // Handle the case when the response status is not okay
                    console.error('Failed to generate the report.');
                }
            } catch (error) {
                // Handle errors
                console.error('Error consuming POST endpoint:', error);
            }
        },
    },
}
</script>

<template>
    <VBtn color="primary" @click="generatePDF">Generate PDF Report</VBtn>
</template>
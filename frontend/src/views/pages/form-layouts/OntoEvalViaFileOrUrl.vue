<script>
import axios from 'axios';
import config from '@/config.js';
import { inject } from 'vue'
export default {
  inject: ['emitter'],
  data() {
    return {
      selectedFiles: [],
      ontologyURI: '',
      ontologyEvaluation: {},
      showPopup: false,
      ontologySavingStatus: {},
      semanticArtefactVersion: '',
      semanticArtefactDomain: '',
      semanticArtifactsData: {},
      currentUserId:null,
    };
  },
  methods: {
    handleFileUpload() {
      // No need to do anything here, v-model already updates selectedFiles
    },
    uploadFiles() {
      const formData = new FormData();
      for (let i = 0; i < this.selectedFiles.length; i++) {
        formData.append('files', this.selectedFiles[i]);
      }

      axios
        .post(config.endpoints.ontologyUpload, formData)
        .then(response => {
          console.log(response.data);
          // Handle the response as needed
        })
        .catch(error => {
          console.error(error);
          // Handle the error as needed
        });
    },

    async fetchSemanticArtifacts() {
      let ontoUrl = this.ontologyURI;

      if (ontoUrl.startsWith('https://github.com/')) {
        ontoUrl = ontoUrl.replace('https://github.com/', 'https://raw.githubusercontent.com/');
      }
      if (ontoUrl.includes('blob/')) {
        ontoUrl = ontoUrl.replace('blob/', '');
      }


      try {
        const response = await axios.post(config.endpoints.ontologySemanticArtifacts, {
          onto_url: ontoUrl,
        });

        console.log('semanticArtifactsDatasource', response.data, this.ontologyURI);
        this.semanticArtifactsData = response.data; // Save the emitted data in the variable

        // Emit the response data
        this.emitter.emit('semanticArtifactsData', response.data);
        // Emit the response data
        this.emitter.emit('onto_url', ontoUrl);

        return response.data; // Return the response data

      } catch (error) {
        console.error(error);
        throw error; // Throw the error to be caught later
      }
    },

    async fetchOntologyEvaluation() {
      const ontologyUrl = this.ontologyURI;
      try {
        const response = await axios.get(config.endpoints.ofaireEvalByThreeAPIS, {
          params: {
            ontology_url: ontologyUrl,
          },
        });
        console.log('Ontology Evaluation:', response.data);

        this.ontologyEvaluation = response.data; // Save the emitted data in the variable
        // Emit the response data
        this.emitter.emit('onto_eval_via_url', response.data);

        // Emit that response is loaded
        this.emitter.emit('SemanticArtifactsLoaded', true);

        return response.data; // Return the response data
      } catch (error) {
        console.error(error);
        throw error; // Throw the error to be caught later
      }
    },

    setSemanticArtefactVersion() {
      let semanticArtefactVersion = {};
      // Loop through the keys of semanticArtifactsData
      for (const key in this.semanticArtifactsData) {
        // Check if the key contains the word "Version" or "version"
        if (key.toLowerCase().includes('version')) {
          semanticArtefactVersion = this.semanticArtifactsData[key];
          break; // Stop the loop once a matching key is found
        }
      }
      return semanticArtefactVersion;
    },

    saveOntologyEvaluation() {

      const ontologyUrl = this.ontologyURI;
      
      const requestBody = {
        source: "URL",
        portal_name:null,
        semantic_artefact_acronym:null,
        semantic_artefact_URL: ontologyUrl,
        semantic_artefact_version: this.setSemanticArtefactVersion(),
        ofaire_score: this.ontologyEvaluation["ofaire"] ? this.ontologyEvaluation["ofaire"]["overallScore"] : null,
        fairchecker_score: this.ontologyEvaluation["fairchecker"] ? this.ontologyEvaluation["fairchecker"]["overallScore"] : null,
        foops_score: this.ontologyEvaluation["foops"] ? this.ontologyEvaluation["foops"]["overallScore"] : null,
        currentUserId: this.currentUserId
      };

      axios.post(config.endpoints.saveSemanticArtefactEval, requestBody)
        .then(response => {
          console.log('Ontology saving:', response.data);
          // Check if the API response contains an error message
          if (response.data.error) {
            this.ontologySavingStatus = response.data.error;
          } else {
            // If no error, store the success message
            this.ontologySavingStatus = response.data.message;
          }
          console.log('Ontology saved:', this.ontologySavingStatus);
          // Show the popup
          this.showPopup = true;
          // Emit the response data
          // this.emitter.emit('onto_eval_storing', response.data);
        })
        .catch(error => {
          console.error(error);
          // Handle the error as needed
          if (error.response && error.response.data && error.response.data.error) {
            // If the error response contains a message, display it in the popup
            this.ontologySavingStatus = error.response.data.error;
          } else {
            // If there's no specific error message, display a generic error message
            this.ontologySavingStatus = "An error occurred while saving the ontology data.";
          }
          // Show the popup with the error message
          this.showPopup = true;
        });

    },
    async evaluateOntology() {
      //emit message to dashboard to start loader
      this.emitter.emit('startLoader', true);
      try {
        await this.fetchSemanticArtifacts();
        await this.fetchOntologyEvaluation();
        this.saveOntologyEvaluation();
      } catch (error) {
        console.error(error);
        // Handle the error as needed
      }
    },
    async saveWithVersion() {
      // Check if the version is provided
      if (!this.semanticArtefactVersion) {
        this.ontologySavingStatus = "Semantic artefact version cannot be empty.";
        return;
      }

      const ontologyUrl = this.ontologyURI;
      const requestBody = {
        source: "URL",
        semantic_artefact_URL: ontologyUrl,
        semantic_artefact_version: this.semanticArtefactVersion,
        //semantic_artefact_domain: this.semanticArtefactDomain,
        ofaire_score: this.ontologyEvaluation["ofaire"] ? this.ontologyEvaluation["ofaire"]["overallScore"] : null,
        fairchecker_score: this.ontologyEvaluation["fairchecker"] ? this.ontologyEvaluation["fairchecker"]["overallScore"] : null,
        foops_score: this.ontologyEvaluation["foops"] ? this.ontologyEvaluation["foops"]["overallScore"] : null,
        currentUserId: this.currentUserId
      };

      try {
        const response = await axios.post(config.endpoints.saveSemanticArtefactEval, requestBody);
        console.log('Ontology saving:', response.data);
        this.ontologySavingStatus = response.data.message;
        // Show the popup
        this.showPopup = true;
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.error) {
          this.ontologySavingStatus = error.response.data.error;
        } else {
          this.ontologySavingStatus = "An error occurred while saving the ontology data.";
        }
        this.showPopup = true;
      }
    },

    saveWithDomain() {
      const ontologyUrl = this.ontologyURI;

      const requestBody = {
        source: "URL",
        semantic_artefact_URL: ontologyUrl,
        semantic_artefact_version: this.setSemanticArtefactVersion(),
        ofaire_score: this.ontologyEvaluation['ofaire'] ? this.ontologyEvaluation['ofaire']['overallScore'] : null,
        fairchecker_score: this.ontologyEvaluation['fairchecker']
          ? this.ontologyEvaluation['fairchecker']['overallScore']
          : null,
        foops_score: this.ontologyEvaluation['foops'] ? this.ontologyEvaluation['foops']['overallScore'] : null,
        semantic_artefact_domain: this.semanticArtefactDomain,
        currentUserId: this.currentUserId
      };
      // Display the requestBody in the console log
      console.log('requestBody:', requestBody);

      axios
        .post(config.endpoints.saveSemanticArtefactEval, requestBody)
        .then(response => {
          console.log('Ontology saving:', response.data);
          this.ontologySavingStatus = response.data.message;
          console.log('Ontology saved:', this.ontologySavingStatus);
          // Show the popup
          this.showPopup = true;
        })
        .catch(error => {
          console.error(error);
          this.ontologySavingStatus = error;
          // Handle the error as needed
        });
    },

    saveWithVersionAndDomain() {
      // Check if the version is provided
      if (!this.semanticArtefactDomain) {
        this.ontologySavingStatus = "Semantic artefact domain cannot be empty.";
        return;
      }
      const ontologyUrl = this.ontologyURI;

      const requestBody = {
        source: "URL",
        semantic_artefact_URL: ontologyUrl,
        ofaire_score: this.ontologyEvaluation['ofaire'] ? this.ontologyEvaluation['ofaire']['overallScore'] : null,
        fairchecker_score: this.ontologyEvaluation['fairchecker']
          ? this.ontologyEvaluation['fairchecker']['overallScore']
          : null,
        foops_score: this.ontologyEvaluation['foops'] ? this.ontologyEvaluation['foops']['overallScore'] : null,
        semantic_artefact_version: this.semanticArtefactVersion,
        semantic_artefact_domain: this.semanticArtefactDomain,
        currentUserId: this.currentUserId
      };

      axios
        .post(config.endpoints.saveSemanticArtefactEval, requestBody)
        .then(response => {
          console.log('Ontology saving:', response.data);
          this.ontologySavingStatus = response.data.message;
          console.log('Ontology saved:', this.ontologySavingStatus, requestBody.data);
          // Show the popup
          this.showPopup = true;
        })
        .catch(error => {
          console.error(error);
          this.ontologySavingStatus = error;
          // Handle the error as needed
        });
    },

  },
  watch: {
    filtered(newOntoUrl) {
      this.emitter.emit('onto_url', newOntoUrl);
    },

  },
};
</script>

<!--
<VCol cols="12">
<VCardTitle>Upload your semantic artefact</VCardTitle>
<v-file-input multiple label="Select files" v-model="selectedFiles" @change="handleFileUpload"></v-file-input>
<v-btn @click="uploadFiles">Evaluate via file</v-btn>
</VCol>
<VCardTitle>Enter your semantic artefact URL</VCardTitle>
<v-btn :v-slot:activator="{ on }" @click="evaluateOntology">Evaluate via URL</v-btn>
-->

<template>
<div>
  <VForm>
    <VRow>
      <VCol cols="12">        
        <VTextField v-model="ontologyURI" label="Ontology URI"></VTextField>
      </VCol>
      <VCol cols="12">
        <VBtn @click="evaluateOntology">Evaluate via URL</VBtn>
      </VCol>
    </VRow>
  </VForm>
  <v-dialog v-model="showPopup" persistent max-width="500px">
    <v-card>
      <v-card-title>Save process</v-card-title>
      <v-card-text>
        <template v-if="ontologySavingStatus === 'Semantic artefact version and domain are missing.'">
          <pre>{{ ontologySavingStatus }}</pre>
          <v-row>
            <v-col cols="12">
              <v-select v-model="semanticArtefactDomain" label="Select Semantic Artefact Domain"
                        :items="['Industry', 'Biomedical', 'Agriculture', 'CrossDomain']"></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="semanticArtefactVersion" label="Enter Semantic Artefact Version"
                            outlined></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-btn @click="saveWithVersionAndDomain">Save</v-btn>
            </v-col>
          </v-row>
        </template>
        <template v-else-if="ontologySavingStatus === 'Semantic artefact version is missing.'">
          <pre>{{ ontologySavingStatus }}</pre>
          <v-row>
        <v-col cols="12">
          <v-text-field v-model="semanticArtefactVersion" label="Enter Semantic Artefact Version"
            outlined></v-text-field>
            </v-col>
            </v-row>
            <v-row>
        <v-col cols="12">
          <v-btn @click="saveWithVersion">Save</v-btn>
          </v-col>
          </v-row>
        </template>
        <template v-else-if="ontologySavingStatus === 'Semantic artefact domain is missing.'">
          <pre>{{ ontologySavingStatus }}</pre>
          <v-row>
        <v-col cols="12">
          <v-select v-model="semanticArtefactDomain" label="Select Semantic Artefact Domain"
            :items="['Industry', 'Biomedical', 'Agriculture', 'CrossDomain']"></v-select>
            </v-col>
            </v-row>
            <v-row>
        <v-col cols="12">
          <v-btn @click="saveWithDomain">Save</v-btn>
          </v-col>
          </v-row>
        </template>
        <template v-else>
          <pre>{{ ontologySavingStatus }}</pre>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="showPopup = false" class="pop-up-btn">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</div>
</template>

<style scoped>
.v-file-input {
  margin-right: 8px;
  margin-top: 10px;
  align-self: center;
}

.v-text-field {
  margin-left: 20px;
  margin-right: 8px;
  margin-top: 10px;
  align-self: center;
}

.v-btn {
  margin-left: 40px;
  margin-top: 10px;
  margin-bottom: 10px;
  align-self: center;
}

.pop-up-btn {
  margin-left: 400px;
  margin-top: 10px;
  margin-bottom: 10px;
  align-self: center;
}

/* Add margin to separate sections */
.v-row {
  margin-bottom: 10px;
}

/* Align the button to the left */
.v-btn {
  align-self: flex-start;
}

/* Adjust button position in the popup */
.pop-up-btn {
  margin-left: auto;
}
</style>
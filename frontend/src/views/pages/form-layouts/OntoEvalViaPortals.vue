<script setup>
import { ref, inject, watch } from 'vue'
import axios from 'axios'
import config from '@/config.js';

const portalName = ref('')
const ontologyAcronym = ref('')
const apiKey = ref('')
const semanticArtifactsDataViaPortal = ref(null) // Reactive variable for emitted data
const emitter = inject('emitter') // Inject the emitter
const ontologyEvaluation = ref(null)
const currentUserId = ref(null)
const showPopup = ref(false)
const ontologySavingStatus = ref({})
const semanticArtifactsViaPortal = ref(null) // Reactive variable for emitted data

// Function to handle form submission
const handleSubmit = async () => {
  try {
    //emit message to dashboard to start loader
    emitter.emit('startLoader', true);
    // Call the handleSubmit function to get the response data
    const response = await handleSubmitAPI()

    // Save the response data in ontologyEvaluation
    ontologyEvaluation.value = response.data

    // Emit the response data
    emitter.emit('onto_eval_via_portal', response.data)

    // Emit the semantic artifacts data
    emitter.emit('semantic_artifacts_data_via_portal', {
      ontologyAcronym: ontologyAcronym.value,
      portalName: portalName.value,
      apiKey: apiKey.value,
    })

    // Handle the response
    console.log('Response:', response.data)

    // After handleSubmit is done, call the saveOntologyEvaluation function
    console.log('Im before save function')
    saveOntologyEvaluation()
  } catch (error) {
    // Handle the error
    console.error('Error:', error)
  }
}
// Function to call the API and get the response data
const handleSubmitAPI = async () => {
  return await axios.get(config.endpoints.ofaireEvalByThreeAPIS, {
    params: {
      portalName: portalName.value,
      ontologyAcronym: ontologyAcronym.value,
      apiKey: apiKey.value
    }
  })
}

watch(semanticArtifactsDataViaPortal, (newValue) => {
  // Handle the emitted value here
  console.log('Received semantic_artifacts_data_via_portal:', newValue)
})

// Watch for changes in the emitted value and update the reactive variable
emitter.on('semantic_artifacts_data_via_portal', (data) => {
  semanticArtifactsViaPortal.value = data
})

emitter.on('semanticArtifactsViaPortals', (data) => {
  semanticArtifactsDataViaPortal.value = data
})

// Function to save the ontology evaluation
const saveOntologyEvaluation = async () => {
  console.log('Im in top save function')
  let semantic_artefact_domain = '';

  // Set semantic_artefact_domain based on portalName.value
  if (portalName.value === 'agroportal') {
    semantic_artefact_domain = 'Agriculture';
  } else if (portalName.value === 'industryportal') {
    semantic_artefact_domain = 'Industry';
  } else if (portalName.value === 'bioportal') {
    semantic_artefact_domain = 'Biomedical';
  }
  const requestBody = {
    source: "Portal",
    portal_name: portalName.value,
    semantic_artefact_acronym: ontologyAcronym.value,
    semantic_artefact_URL: null,
    semantic_artefact_domain: semantic_artefact_domain,
    semantic_artefact_version: "1.0",
    ofaire_score: ontologyEvaluation.value["ofaire"] ? ontologyEvaluation.value["ofaire"]["overallScore"] : null,
    fairchecker_score: ontologyEvaluation.value["fairchecker"] ? ontologyEvaluation.value["fairchecker"]["overallScore"] : null,
    foops_score: ontologyEvaluation.value["foops"] ? ontologyEvaluation.value["foops"]["overallScore"] : null,
    currentUserId: currentUserId.value

  };

  await axios
    .post(config.endpoints.saveSemanticArtefactEval, requestBody)
    .then((response) => {
      console.log('Ontology saving:', response.data);
      // Check if the API response contains an error message
      if (response.data.error) {
        ontologySavingStatus.value = response.data.error;
      } else {
        // If no error, store the success message
        ontologySavingStatus.value = response.data.message;
      }
      console.log('Ontology saved:', ontologySavingStatus.value);
      // Show the popup
      showPopup.value = true;
      // Emit the response data
      // this.emitter.emit('onto_eval_storing', response.data);
    })
    .catch((error) => {
      console.error(error);
      // Handle the error as needed
      if (error.response && error.response.data && error.response.data.error) {
        // If the error response contains a message, display it in the popup
        ontologySavingStatus.value = error.response.data.error;
      } else {
        // If there's no specific error message, display a generic error message
        ontologySavingStatus.value = 'An error occurred while saving the ontology data.';
      }
      // Show the popup with the error message
      showPopup.value = true;
    });
  console.log('Im in tail of save function')
};
</script>

<template>
  <VForm @submit.prevent="handleSubmit">
    <VRow>
      <VCol cols="12">
        <v-select v-model="portalName" label="Portal Name" placeholder="Select Portal"
          :items="['agroportal', 'industryportal', 'bioportal']"></v-select>
      </VCol>

      <VCol cols="12">
        <VTextField v-model="ontologyAcronym" prepend-inner-icon="mdi-book-open-variant" label="Ontology acronym"
          placeholder="Ontology acronym" />
      </VCol>

      <VCol cols="12">
        <VTextField v-model="apiKey" prepend-inner-icon="mdi-key" label="Portal API Key" placeholder="Portal API Key" />
      </VCol>

      <VCol cols="12">
        <VBtn type="submit" class="me-2">Evaluate via portal</VBtn>
        <!-- <VBtn color="primary" type="reset" variant="tonal">Reset</VBtn> -->
      </VCol>      
    </VRow>
  </VForm>
</template>
<style scoped>
.pop-up-btn {
  margin-left: 400px;
  margin-top: 10px;
  margin-bottom: 10px;
  align-self: center;
}
</style>
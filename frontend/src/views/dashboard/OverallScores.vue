<script>
import faircheckerLogo from '@/assets/images/logos/fairchecker.png';
import foopsLogo from '@/assets/images/logos/foops.png';
import ofaireLogo from '@/assets/images/logos/ofaire.png';

import { ref, inject } from 'vue'
import config from '@/config.js';

const show = ref(false)
export default {
  inject: ['emitter', 'store'],
  data() {
    return {
      //statistics: [], // Populate with the response from the endpoint
      ontologyEvaluation: {},
      abox: false,
      tbox: false,
      hover: false,
      show: false,

    };
  },
  mounted() {
    this.OntologyEvaluationViaPortals();
    this.OntologyEvaluationViaURL();
    console.log('OverallScores Component is listening for ontologyEvaluation event');
  },
  computed: {
    //for dashboard loading on endpoint response
    isDataLoaded() {
      return this.store.state.isDataLoaded; // Access state from the Vuex store
    },
    isLoading() {
      return this.store.state.loading; // Access state from the Vuex store
    },
    
    filteredOntologyEvaluation() {

      let filteredOntoEval = Object.keys(this.ontologyEvaluation).filter((key) => {
        if (this.abox == false && this.tbox == false) {
          return true;
        }
        else if (key === 'fairchecker') {
          return this.abox;
        } else {
          return this.tbox;
        }
      }).reduce((filteredObj, key) => {
        filteredObj[key] = this.ontologyEvaluation[key];
        return filteredObj;
      }, {});

      this.emitter.emit('filtered_eval', filteredOntoEval)

      return filteredOntoEval;
    }
  },
  methods: {
    OntologyEvaluationViaPortals() {
      this.emitter.on('onto_eval_via_portal', (data) => {
        this.ontologyEvaluation = {};
        // Handle the emitted response
        console.log('Received response:', data)
        this.ontologyEvaluation = data // Save the emitted data in the variable
        console.log('Received response data:', this.ontologyEvaluation)
        // Perform any further actions with the response data
      });
    },
    OntologyEvaluationViaURL() {
      this.emitter.on('onto_eval_via_url', (data) => {
        this.ontologyEvaluation = {};
        // Handle the emitted response
        this.ontologyEvaluation = data // Save the emitted data in the variable
        console.log('Received response data:', this.ontologyEvaluation)

       
      });
       
    },
    

    getImageSource(key) {
      if (key === 'fairchecker') {
        return faircheckerLogo;
      } else if (key === 'foops') {
        return foopsLogo;
      } else if (key === 'ofaire') {
        return ofaireLogo;
      } else {
        // Return a default image source if needed
        return zipcar;
      }
    },

    getWebsiteURL(index) {
      if (index === 'fairchecker') {
        return config.FAIRCHECKER_WEBSITE;
      } else if (index === 'foops') {
        return config.FOOPS_WEBSITE;
      } else if (index === 'ofaire') {
        return config.OFAIRE_WEBSITE;
      }
      // Default fallback URL if none of the conditions match
      return '#';
    },

  },
};

</script>


<template>
  <VCard>
    <VCardItem class="title">
      <div>
        <div class="title-content font-size-small" @mouseover="hover = true" @mouseout="hover = false">
          <VCardTitle>FAIR overall scores</VCardTitle>
          <v-tooltip v-model="show" location="right" class="ml-15">
            <template v-slot:activator="{ props }">
              <v-btn icon v-bind="props">
                <v-icon color="grey-lighten-1">
                  mdi-information
                </v-icon>
              </v-btn>
            </template>
            <span class="tooltip-text">The ABOX option enables the evaluation of the semantic annotations, and the TBOX enables the assessment of the semantic terms.</span>
          </v-tooltip>
        </div>

      </div>

    </VCardItem>

    <VCardText v-if="isDataLoaded && isLoading === false">
      <VList class="card-list">
        <!-- Checkbox for ABOX -->
        <VListItem class="list-item">

          <template #prepend>
            <div class="me-6 text-center ">
              <h4 class="font-weight-medium">Filter by type:</h4>
            </div>
          </template>
          <div>
            <VCheckbox v-model="abox" label="ABOX"></VCheckbox>
          </div>
          <!-- Checkbox for TBOX -->
          <template #append>
            <VCheckbox class="ml-5" v-model="tbox" label="TBOX"></VCheckbox>
          </template>
        </VListItem>

        <VListItem class="list-item">
          <template #prepend>
            <h4 rounded class="me-15 ms-5" :size="40">
              LOGO
            </h4>
          </template>

          <div class="me-15 text-center ">
            <h4 class="font-weight-medium">TOOL</h4>
          </div>
          <template #append>
            <div class="ms-3 score-container">
              <h4 class="font-weight-medium">SCORE</h4>
            </div>
          </template>
        </VListItem>
        <!-- Display data for 'fairchecker' when abBoxCheckbox is checked -->
        <VListItem class="list-item">
          <VListItem v-for="(value, index) in filteredOntologyEvaluation" :key="index" class="list-item">
            <template #prepend>
              <VAvatar rounded class="me-15 ms-5" :size="index === 'foops' ? '40' : '40'">
                <img :src="getImageSource(index)" alt="Logo" height="40" width="50" />
              </VAvatar>
            </template>

            <div class="me-4 text-center" v-if="index === 'fairchecker'">
              <a :href="getWebsiteURL(index)" target="_blank" class="font-weight-medium ">{{ index.toUpperCase() }}</a>
            </div>
            <div class="me-16 text-center" v-else>
              <a :href="getWebsiteURL(index)" target="_blank" class="font-weight-medium ">{{ index.toUpperCase() }}</a>
            </div>


            <template #append>

              <div class="score-container" v-if="value !== null && value.overallScore !== undefined">
                <h4 class="font-weight-medium">{{ value.overallScore.toFixed(2) }} %</h4>
              </div>

              <div class="score-container" v-else>
                <h4 class="font-weight-medium">N/A</h4>
              </div>

            </template>
          </VListItem>
        </VListItem>
      </VList>
    </VCardText>
    <VCardText v-if="isLoading" class="text-center py-5">
            <VProgressCircular indeterminate color="primary"></VProgressCircular>
    </VCardText>
  </VCard>
</template>

<style lang="scss" scoped>
.v-card {
  min-height: fit-content;
}

.title {
  min-height: fit-content;
}

.card-list {
  --v-card-list-gap: 1.5rem;
}

.list-item {
  display: flex;
  align-items: center;
}




.item-label h4 {
  margin-bottom: 0;
}

.VList {
  display: grid;
  grid-template-columns: 1fr;
  grid-gap: 10px;
  /* Adjust the gap as needed */
}

.score-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.title-content {
  display: flex;
  align-items: center;
}
.tooltip-text {
  max-width: 20px; /* Set the desired maximum width */
  overflow: hidden;
}
.v-btn--icon.v-btn--density-default{
  margin-left: 20px
}


/* Adjust font size for different zoom levels */
@media screen and (min--moz-device-pixel-ratio: 0.75),
       screen and (-o-min-device-pixel-ratio: 3/4),
       screen and (-webkit-min-device-pixel-ratio: 0.75),
       screen and (min-device-pixel-ratio: 0.75) {
.font-size-small {
    font-size: 14px; /* Adjust the font size as needed */
  }
}

/* Default font size for 100% zoom */
.title-content {
  font-size: 16px; /* Adjust the font size as needed */
}
</style>

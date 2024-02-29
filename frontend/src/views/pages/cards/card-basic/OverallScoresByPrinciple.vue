<template>
  <VCard>
    <VCardTitle>
      FAIR score by {{ selectedPrinciple }} principle
    </VCardTitle>

    <VTabs v-model="navigationTab" >
      <VTab v-for="item in principles" :key="item" :value="item" @click="selectedPrinciple = item">
        {{ item }}
      </VTab>
    </VTabs>

    <VDivider />

    <!-- tabs content -->
    <VWindow v-model="navigationTab">
      <VWindowItem v-for="item in principles" :key="item" :value="item">
        
        <VCardText class="pt-4" v-if="isDataLoaded && isLoading === false">
          <VList class="card-list">
            <VListItem v-for="toolResult in principlesTools[navigationTab]" :key="toolResult">

              <VListItem v-for="(value, key) in toolResult" :key="key" class="d-flex align-center">
                <template #prepend>
                <VAvatar rounded color="white" class="ms-8 me-16">
                  <img :src="getImageSource(key)" alt="Logo" height="40" width="50" />
                </VAvatar>
              </template>
              <VListItemTitle class="text-sm font-weight-medium mb-1 ms-16 me-2" v-if="key === 'fairchecker'" >
                {{ key.toUpperCase() }}
              </VListItemTitle>
              <VListItemTitle class="text-sm font-weight-medium mb-1 ms-16 me-16" v-else>
                {{ key.toUpperCase() }}
              </VListItemTitle>
              
              <template #append>
                <div class="d-flex align-center ms-16">
                  
                  <div class="ml-4 ">
                    <h6 class="text-sm font-weight-medium mb-2" v-if="value !== 'N/A'">
                    {{ value.toFixed(2) }}%
                  </h6>
                  <h6 class="text-sm font-weight-medium mb-2" v-else>
                    {{ value }}
                  </h6>
 
                    <v-progress-linear
                        height="8" 
                        :model-value="calculateProgress(value)"
                        bg-color="info"
                        color="info"
                        width="500"
                        v-if="value !== 'N/A'" ></v-progress-linear>

                  </div>
                </div>
              </template>
            </VListItem>
            </VListItem>
          </VList>
        </VCardText>
        <VCardText v-if="isLoading" class="text-center py-5">
            <VProgressCircular indeterminate color="primary"></VProgressCircular>
        </VCardText>
      </VWindowItem>
    </VWindow>

    
    
  </VCard>
  
</template>

<script>
import axios from 'axios';
import faircheckerLogo from '@/assets/images/logos/fairchecker.png';
import foopsLogo from '@/assets/images/logos/foops.png';
import ofaireLogo from '@/assets/images/logos/ofaire.png';
import { inject } from 'vue';

export default {
  inject: ['emitter','store'],
  data() {
    return {
      navigationTab: 'A1.1',
      ontologyEvaluation: {},
      principlesTools: {},
      principles: [],
      selectedPrinciple: null,

    };
  },
  computed: {
    calculateProgress() {
      return function(value) {
        // Calculate the percentage progress based on the value
        // Adjust the formula as needed for your specific progress calculation
        const progress = (value / 100) * 100; 
        return Math.min(progress, 100); 
      };
    },
    //for dashboard loading on endpoint response
    isDataLoaded() {
      return this.store.state.isDataLoaded; // Access state from the Vuex store
    },
    isLoading() {
      return this.store.state.loading; // Access state from the Vuex store
    },
  },
  mounted() {
    this.saveOntologyEvaluationViaPortals();
    this.saveOntologyEvaluationViaUrl();
    console.log('Component score by principle is listening for ontologyEvaluation event');
    
  },
  methods: {
    saveOntologyEvaluationViaPortals() {
      this.emitter.on('filtered_eval', (data) => {
        // Handle the emitted response
        console.log('Received response score by principle:', data)
        this.ontologyEvaluation = data // Save the emitted data in the variable
        console.log('Received response data score by principle:', this.ontologyEvaluation)
        this.principlesTools= {}
        this.principles= []
        for (const [key, toolResult] of Object.entries(this.ontologyEvaluation)) {
          console.log(key);
          console.log(toolResult);
          if (typeof toolResult === 'object' && toolResult !== null) {
            for (const principleResult of toolResult.principleResults) {
              if (!this.principles.includes(principleResult['principleName'])) {
                this.principles.push(principleResult['principleName']);
              }
              if (this.principlesTools.hasOwnProperty(principleResult['principleName'])) {
                this.principlesTools[principleResult['principleName']].push({ [key]: principleResult['principleScore'] });
              } else {
                this.principlesTools[principleResult['principleName']] = [{ [key]: principleResult['principleScore'] }];
              }
            }
          }
        }
        console.log('pppp',this.principlesTools)
        for (const [principleName, scoreByTool] of Object.entries(this.principlesTools)){
          if(!scoreByTool.some(obj => obj.hasOwnProperty('fairchecker'))){
            
            scoreByTool.push({ "fairchecker": "N/A" })
          }
          if(!scoreByTool.some(obj => obj.hasOwnProperty('foops'))){
            scoreByTool.push({ "foops": "N/A" })
          }
          if(!scoreByTool.some(obj => obj.hasOwnProperty('ofaire'))){
            scoreByTool.push({ "ofaire": "N/A" })
          }
        
        }
      });
    },
    saveOntologyEvaluationViaUrl() {
      this.emitter.on('filtered_eval', (data) => {
        // Handle the emitted response
        console.log('Received response score by principle via url:', data)
        this.ontologyEvaluation = data // Save the emitted data in the variable
        console.log('Received response data score by principle via url:', this.ontologyEvaluation)
        this.principlesTools= {}
        this.principles= []
        for (const [key, toolResult] of Object.entries(this.ontologyEvaluation)) {
          console.log(key);
          console.log(toolResult);
          if (typeof toolResult === 'object' && toolResult !== null) {
            for (const principleResult of toolResult.principleResults) {
              if (!this.principles.includes(principleResult['principleName'])) {
                this.principles.push(principleResult['principleName']);
              }
              if (this.principlesTools.hasOwnProperty(principleResult['principleName'])) {
                this.principlesTools[principleResult['principleName']].push({ [key]: principleResult['principleScore'] });
              } else {
                this.principlesTools[principleResult['principleName']] = [{ [key]: principleResult['principleScore'] }];
              }
            }
          }
        }

        for (const [principleName, scoreByTool] of Object.entries(this.principlesTools)){
          if(!scoreByTool.some(obj => obj.hasOwnProperty('fairchecker'))){
            
            scoreByTool.push({ "fairchecker": "N/A" })
          }
          if(!scoreByTool.some(obj => obj.hasOwnProperty('foops'))){
            scoreByTool.push({ "foops": "N/A" })
          }
          if(!scoreByTool.some(obj => obj.hasOwnProperty('ofaire'))){
            scoreByTool.push({ "ofaire": "N/A" })
          }
        
        }
      
      });
    },
    getPrincipleScore(toolResult, principleName) {
      const principleResult = toolResult.principleResults.find(result => result.principleName === principleName);
      if (principleResult) {
        return `Tool: ${toolResult.toolName}, Principle: ${principleResult.principleScore}`;
      } else {
        return '';
      }
    },
    isNumber(value) {
      return typeof value === 'number';
    },
    getColor(key) {
      if (key === 'fairchecker') {
        return 'info';
      } else if (key === 'foops') {
        return 'primary';
      } else if (key === 'ofaire') {
        return 'secondary';
      } else {
        return 'error'; // Default color if key doesn't match any condition
      }
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
      return null;
    }
  }
  }
};
</script>

<style lang="scss" scoped>
.card-list {
  --v-card-list-gap: 2.625rem;
}
</style>

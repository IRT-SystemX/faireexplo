<script setup>
import FAIRMetadataAnalysis from '@/views/dashboard/FAIRMetadataAnalysis.vue';
import OverallScores from '@/views/dashboard/OverallScores.vue';
import SemanticArtefacts from '@/views/dashboard/SemanticArtefacts.vue';
import AlertsTable from '@/views/dashboard/AlertsTable.vue';
import OntoEvalViaFileOrUrl from '@/views/pages/form-layouts/OntoEvalViaFileOrUrl.vue';
import OntoEvalViaPortals from '@/views/pages/form-layouts/OntoEvalViaPortals.vue';
import OverallScoresByPrinciple from '@/views/pages/cards/card-basic/OverallScoresByPrinciple.vue'
import PDFGenerator from '@/views/dashboard/PDFGenerator.vue';
import { ref, inject, provide } from 'vue';
import { createStore } from 'vuex';
const store = createStore({
  state() {
    return {
      isDataLoaded: false,
      loading: false
      // Other state properties...
    };
  },
  mutations: {
    setIsDataLoaded(state, payload) {
      state.isDataLoaded = payload;
    },
    setLoading(state, payload) {
      state.loading = payload;
    },
    // Other mutations...
  },
});
const semanticArtifactsLoaded = ref(false)
const emitter = inject('emitter');   // Inject `emitter`
provide('store', store);
emitter.on('startLoader', (data) => {
  store.commit('setLoading', true); // Update state in the Vuex store
});
emitter.on('SemanticArtifactsLoaded', (data) => {
    store.commit('setIsDataLoaded', data); // Update state in the Vuex store
    store.commit('setLoading', false); // Update state in the Vuex store
});
</script>

<template>
  <VRow class="match-height">
    <VCol cols="12">
      <VRow class="match-height">
        <VCol cols="12" md="6">
          <VCard title="Enter your semantic artefact URL">
            <VCardText>
              <OntoEvalViaFileOrUrl />
            </VCardText>            
          </VCard>
        </VCol>
        <VCol cols="12" md="6">
          <VCard title="Use portals to evalute">
            <VCardText>
              <OntoEvalViaPortals />
            </VCardText>            
          </VCard>
        </VCol>
      </VRow>

      <VRow class="match-height">
        <VCol cols="12" md="5">
          <SemanticArtefacts  />
        </VCol>

        <VCol cols="12" md="7">
          <FAIRMetadataAnalysis  />
        </VCol>
      </VRow>
       
      <VRow class="match-height">
        <VCol cols="5">
          <OverallScores  />
        </VCol>

        <VCol cols="7">
          <OverallScoresByPrinciple  />
        </VCol>
      </VRow>

      <VRow >
        <VCol cols="12">
          <AlertsTable />
        </VCol>
      </VRow>

      <VRow >
        <VCol cols="12">
          <PDFGenerator />
        </VCol>
      </VRow>
    </VCol>
  </VRow>
</template>

<script>
/*
import { inject } from 'vue';
export default {
  inject: ['emitter'],
  data() {
    return {
      isDataLoaded: true,
      loading: true,
    };
  },
  methods: {
    handleFileUpload() {
    },
  },
  mounted () {
    var self = this;
    this.emitter.on('startLoader', (data) => {
      self.loading = true;
    });
    this.emitter.on('SemanticArtifactsLoaded', (data) => {
      self.isDataLoaded = false;
      self.loading = false;
    });
  }
};
*/
</script>

<style>
.fill-height {
  min-height: 100px;
  min-width: 250px;
}

.tabWithWindows {
  min-width: 70px;

}
</style>
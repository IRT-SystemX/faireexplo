<script setup>
import { computed, inject } from 'vue'
import axios from 'axios'
import config from '@/config.js';
const emitter = inject('emitter');   // Inject `emitter`
const state = reactive({
  benchmarkList: [],
  pagination: {
    page: 1,        // Current page
    itemsPerPage: 5, // Number of items to display per page
    totalItems: 0   // Total number of items
  }
})
const itemsPerPageOptions = [5, 10, 20]; // You can customize this array based on your preferences

// define selectedTool
const selectedTool = ref('Choose a domain');

const totalPages = computed(() => {
  return Math.ceil(state.pagination.totalItems / state.pagination.itemsPerPage);
})

// Computed property to return the paginated alerts based on the current page and items per page
const paginatedBenchMarkList = computed(() => {
  const startIndex = (state.pagination.page - 1) * state.pagination.itemsPerPage;
  const endIndex = startIndex + state.pagination.itemsPerPage;
  return filteredBenchMarkList.value.slice(startIndex, endIndex);
})

const updatePage = (page) => {
  state.pagination.page = page;
}

const statusColor = {
  '01': 'primary',
  '02': 'success',
  '03': 'error',
  '04': 'warning',
  '05': 'info',
  '06': 'primary',
  '07': 'success',
  '08': 'error',
  '09': 'warning',
  '10': 'info',
  '11': 'primary',
  '12': 'success',
};

const getStatusColor = (evaluation_date) => {
  const month = evaluation_date.substr(5, 2); // Extract the month part from the date
  return statusColor[month] || ''; // Return the corresponding color if found, or an empty string if not found
};

const headers = [
  'Domain',
  'Acronym',
  'Source',
  'Version',
  'FairChecker',
  'Foops',
  'O\'FAIRe',
  'Evaluation date',
  'URL',
]

// Function to fetch the data from the API
async function fetchOntologyViaUrlData() {
  try {
    state.benchmarkList = []
    const response = await axios.get(config.endpoints.ontologyGet)
    // Update the ontologyViaUrlData ref with the fetched data
    state.benchmarkList = response.data
    state.pagination.totalItems = state.benchmarkList.length;
    console.log('ontologyViaUrlData', state.benchmarkList)

    // Emit the metadata_percentage
    emitter.emit('nonFilteredBenchmarkList', state.benchmarkList)
  } catch (error) {
    console.error('Error occurred while fetching data:', error)
  }
}

const filteredBenchMarkList = computed(() => {
  if (!selectedTool.value || selectedTool.value === 'Choose a domain') {
    // If no domain is selected, return the paginatedBenchMarkList as is
    return state.benchmarkList;
    
  } else {
    // If a domain is selected, filter the paginatedBenchMarkList based on the selected domain
    let filtered = state.benchmarkList.filter((row) => row.semantic_artefact_domain === selectedTool.value);
    state.pagination.totalItems = filtered.length;
    // Emit the metadata_percentage
    emitter.emit('benchmarkList', filtered)
    return filtered;
  }
});

// Call the fetchOntologyViaUrlData function when the component is mounted
onMounted(fetchOntologyViaUrlData)

// Watcher for the selectedTool
watch(selectedTool, (newValue, oldValue) => {
  
  // Update the pagination page to 1 when the selected domain changes
  state.pagination.page = 1;
  // Recalculate the filteredBenchMarkList based on the new selected domain
  filteredBenchMarkList.value = state.benchmarkList.filter((row) => row.semantic_artefact_domain === newValue);
});

emitter.on('selectedCardTitle', (data) => {
  selectedTool.value = data;
});
</script>

<template>
  <VCard>
    <!-- Header using v-row and v-col -->
    <v-row align="center" class="mb-4">
      <v-col cols="auto">
        <VCardTitle class="mb-0 mr-15">ALL SEMANTIC ARTEFACTS</VCardTitle>
      </v-col>
      <v-col cols="auto" flex="none" class="ml-auto mt-3 mr-3">
        <VSelect
          v-model="selectedTool"
          :items="['Industry', 'Biomedical', 'Agriculture', 'CrossDomain']"
          label="Filter by domain"
          outlined
          dense
        
        ></VSelect>
      </v-col>
    </v-row>
    <VTable :headers="headers" :items="paginatedBenchMarkList.value" item-key="id" class="table-rounded" hide-default-footer
      disable-sort>
      <thead>
        <tr>
          <th v-for="header in headers" :key="header">
            {{ header }}
          </th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="row in paginatedBenchMarkList" :key="row.id">
          <td class="text-sm" v-text="row.semantic_artefact_domain" />
          <td class="text-sm" v-text="row.semantic_artefact_acronym !== null ? row.semantic_artefact_acronym : 'N/A'" />
          <!-- name -->
          <td>
            <div class="d-flex flex-column">
              <h6 class="text-sm font-weight-medium">
               {{row.source}}
              </h6>
              <!--span class="text-xs">text</span-->
            </div>
          </td>
          <td class="text-sm" v-text="row.semantic_artefact_version" />
          <td class="text-sm" v-text="row.fairchecker_score === null ? 'N/A' : row.fairchecker_score.toFixed(2) + ' %'" />
          <td class="text-sm" v-text="row.foops_score !== null ? row.foops_score.toFixed(2) + ' %' : 'N/A'" />
          <td class="text-sm justify-center" v-text="row.ofaire_score === null ? 'N/A' : row.ofaire_score.toFixed(2) + ' %'" />
          <!-- status -->
          <td>
            <VChip size="small" :color="getStatusColor(row.evaluation_date)" class="text-capitalize">
              {{ row.evaluation_date }}
            </VChip>
          </td>
          <td class="text-sm" v-text="row.semantic_artefact_URL !== null ? row.semantic_artefact_URL : 'N/A'" />
        </tr>
      </tbody>
    </VTable>
   <!-- Footer (Centered) using v-row and v-col -->
  <v-row class="d-flex justify-center mt-4">
    <v-col cols="auto">
      <VPagination
        v-model="state.pagination.page"
        :length="totalPages"
        @input="updatePage"
        total-visible="5"
        prev-icon="mdi-chevron-left"
        next-icon="mdi-chevron-right"
        hide-delimiter-background
        class="mt-2"
      />
    </v-col>
    <v-col cols="auto">
      <VSelect
        v-model="state.pagination.itemsPerPage"
        :items="itemsPerPageOptions"
        label="Items per page"
        outlined
        dense
        
      ></VSelect>
    </v-col>
  </v-row>
  </VCard>
</template>



<script setup>
import { computed, inject } from 'vue'
const emitter = inject('emitter');   // Inject `emitter`
const store = inject('store');

const isDataLoaded = computed(() => store.state.isDataLoaded)
const isLoading = computed(() => store.state.loading)

const selectedTool = ref(''); // Define the selectedTool property
const state = reactive({
  alerts: [],
    pagination: {
        page: 1,        // Current page
        itemsPerPage: 5, // Number of items to display per page
        totalItems: 0   // Total number of items
      }
})


function prepareAlerts(evaluationData){
  state.alerts=[]
  for (const [key, toolResult] of Object.entries(evaluationData)) {
    if (typeof toolResult === 'object' && toolResult !== null) {
      for (const principleResult of toolResult.principleResults) {
        for (const metricResult of principleResult.metricResults){
          if (metricResult.status !== "PASSED"){
            state.alerts.push({tool: key,
            principle: principleResult.principleName,
            metricName: metricResult.metricName,
            description: metricResult.description,
            status: metricResult.status,
            explanation: metricResult.resultExplanation
            })
          }
          
        }
      }
    }
  }
  state.pagination.totalItems = state.alerts.length;
}
const totalPages = computed(() => {
      return Math.ceil(state.pagination.totalItems / state.pagination.itemsPerPage);
    })

// Computed property to return the paginated alerts based on the current page and items per page
const paginatedAlerts = computed(() => {
  const startIndex = (state.pagination.page - 1) * state.pagination.itemsPerPage;
      const endIndex = startIndex + state.pagination.itemsPerPage;
      return state.alerts.slice(startIndex, endIndex);
})

function getUniqueTools() {
      const uniqueTools = [];
      for (const row of this.paginatedAlerts) {
        if (!uniqueTools.includes(row.tool)) {
          uniqueTools.push(row.tool);
        }
      }
      return uniqueTools;
    }

const updatePage = (page) => {
      state.pagination.page = page;
    }

emitter.on('filtered_eval', (data) => {
  prepareAlerts(data);
});



const statusColor = {
  PASSED: 'primary',
  Professional: 'success',
  FAILED: 'error',
  PARTIALLY_PASSED: 'warning',
  Applied: 'info',
}

const headers = [
          'Tool',
          'Principle',
          'Metric name',
          'Description',
          'Status',
          'Explanation'
]

</script>

<template>
  <VCard>
    <div class="d-flex align-center">
      <VCardTitle class="mr-4">Alerts</VCardTitle>
     
    </div>
    <VTable
      :headers="headers"
      :items="paginatedAlerts"
      item-key="description"
      class="table-rounded"
      hide-default-footer
      disable-sort 
    >
      <thead >
        <tr>
          <th
            v-for="header in headers"
            :key="header"
          >
            {{ header }}
          </th>
        </tr>
      </thead>

      <tbody v-if="isDataLoaded && isLoading === false">
        <tr
          v-for="row in paginatedAlerts"
          :key="row.description"
          
        >
          
          <!-- name -->

          <td>
            <div class="d-flex flex-column">
              <h6 class="text-sm font-weight-medium">
                {{ row.tool }}
              </h6>
             
            </div>
          </td>

          <td
            class="text-sm"
            v-text="row.principle"
          />
          <td
            class="text-sm"
            v-text="row.metricName"
          />
          <td
            class="text-sm"
            v-text="row.description"
          />
          <!-- status -->
          <td>
            <VChip
              size="small"
              :color="statusColor[row.status]"
              class="text-capitalize"
            >
              {{ row.status }}
            </VChip>
          </td>
          <td
            class="text-sm"
            v-text="row.explanation"
          />
          
        </tr>
      </tbody>
    </VTable>
    <div class="d-flex justify-center mt-4" v-if="isDataLoaded">
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

    </div>

    <VCardText v-if="isLoading" class="text-center py-5">
            <VProgressCircular indeterminate color="primary"></VProgressCircular>
    </VCardText>
  </VCard>
</template>

<style>
.select-sm {
  margin-left: 800px;
  margin-top: 10px;
  margin-right: 10px;
  width: 50px; /* Adjust the width as needed */
}
</style>
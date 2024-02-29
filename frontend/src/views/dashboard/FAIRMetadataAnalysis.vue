<script setup>
import VueApexCharts from 'vue3-apexcharts'

import { useTheme } from 'vuetify'
import axios from 'axios'
import { inject, reactive, watch, computed, ref } from 'vue'
import config from '@/config.js';

const vuetifyTheme = useTheme()
const currentTheme = controlledComputed(() => vuetifyTheme.name.value, () => vuetifyTheme.current.value.colors)

const chart = ref(null)

const store = inject('store');
const navigationTab = ref('Minimal')
const metadatas = ['Minimal', 'Recommended', 'Extended']
const themeColors = [{ errorColor: currentTheme.value.error },
{ successColor: currentTheme.value.success },
{ infoColor: currentTheme.value.info }]

const isDataLoaded = computed(() => store.state.isDataLoaded)
const isLoading = computed(() => store.state.loading)
const series = reactive({
  Minimal: [{
    name: 'Minimal metadata',
    data: [20, 0, 0, 100],
  }],

  Recommended: [{
    name: 'Recommended metadata',
    data: [40, 0, 0, 100],
  }],

  Extended: [{
    name: 'Extended metadata',
    data: [60, 0, 0, 100],
  }],

});
const maxDataValue = 100; // Maximum value for the data
// Update the colors dynamically based on the value of the data
const legendLabels = computed(() => {
  const errorColor = currentTheme.value.error;
  const successColor = currentTheme.value.success;
  const infoColor = currentTheme.value.info;

  return {
    [errorColor]: 'Missing',
    [infoColor]: 'Partially completed',
    [successColor]: 'Totally completed metadata',
  };
});

// Define a computed property to map navigationTab values to labels
const mappedTabLabels = computed(() => {
  const mapping = {
    Minimal: 'mandatory',
    Recommended: 'recommended',
    Extended: 'optional',
    // Add more mappings if needed
  };
  return mapping;
});

const colors = computed(() => {
  return series[navigationTab.value][0].data.map(value => {
    if (value === 0) {
      return currentTheme.value.error;
    } else if (value === 100) {
      return currentTheme.value.success;
    } else {
      return currentTheme.value.info;
    }
  });
});

const chartOptions = computed(() => {
  let backgroundColor = currentTheme.value.background;
  let chartColors = colors.value;
  console.log('colors in char toptions', chartColors);

  return {
    chart: {
      type: 'bar',
      stacked: false,
      parentHeightOffset: 50,
      toolbar: {
        show: false,
        offsetY: -16,
        style: {
          color: '#FFFFFF'
        }
      },
    },
    title: {
      text: 'FAIR metadata distribution',
      align: 'center',
      style: {
        //fontSize: '12px',
        color: '#ffffff' // Set the color to white
      }
    },
    grid: {
      show: true,
      padding: {
        top: -10,
        left: -7,
        right: 0,
        bottom: -16,
      },
    },
    colors: chartColors,
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '17%',
        borderRadius: 4,
        startingShape: 'rounded',
        endingShape: 'rounded',
        distributed: true,
        colors: {
          backgroundBarColors: [
            //currentTheme.value.warning,
            backgroundColor,
            backgroundColor,
            backgroundColor,
            backgroundColor,
          ],
          backgroundBarRadius: 5,
        },
      },
    },
    legend: {
      show: false,
      offsetY: 10,
      customLegendItems: [
        'F completed metadata ',
        'A completed metadata ',
        'I completed metadata ',
        'R completed metadata '

      ],
      labels: {
        colors: '#ffffff', // Set the color to white
        formatter: function (value, { seriesIndex }) {
          const color = currentTheme.value[seriesIndex];
          return legendLabels.value[color] || value;
        },

      },
      useSeriesColors: false, // Use the same colors as the series
    },
    dataLabels: {
      enabled: true,
      formatter: function (value) {
        // Customize the formatting of the y-axis labels
        return value + ' %'; // Add the desired metric or unit, e.g., percentage (%)
      },
    },
    xaxis: {
      labels: {
        show: true,
        style: {
          colors: '#ffffff', // Set the color to white
        },

      },
      categories: ['F', 'A', 'I', 'R'],

      axisBorder: { show: false },
      axisTicks: { show: true },
      offsetY: -5,
    },
    yaxis: {
      show: true,
      labels: {
        show: true,
        style: {
          colors: '#ffffff', // Set the color to white
        },
        formatter: function (value) {
          // Customize the formatting of the y-axis labels
          return value + ' %'; // Add the desired metric or unit, e.g., percentage (%)
        },
      },

      max: maxDataValue, // Set the maximum value for the y-axis
      tickAmount: 5, // Set the desired number of ticks or intervals
    },
    tooltip: {
      enabled: true,
      theme: 'dark', // Set the tooltip theme to "dark"
    },
  }
})
console.log('Legend Labels:', legendLabels);

const emitter = inject('emitter');   // Inject `emitter`

// Listen for the 'onto_url' event
emitter.on('onto_url', (url) => {
  // Call the fetchData function with the received onto_url
  fetchData(url);
});

// Listen for the 'onto_url' event
emitter.on('semantic_artifacts_data_via_portal', (ontologyData) => {
  console.log('in metadat percentage got :', ontologyData);
  // Call the fetchData function with the received onto_url
  fetchOntoPortalsMetadataPercentage(ontologyData);
  // Handle the response

});

function handleResponseDataDummy() {

  series.Minimal[0].data[0] = 0;
  series.Minimal[0].data[1] = 30;
  series.Minimal[0].data[2] = 100;
  series.Minimal[0].data[3] = 50;


}

// Function to handle the response data
async function handleResponseData(responseData) {
  // Extract the value of minimal_metadata_percentage
  //const minimalMetadataPercentage = responseData[0].minimal_metadata_percentage;


  // Update each data value with the corresponding value from minimalMetadataPercentage
  //update minimal(mandatory) findable 
  series.Minimal[0].data[0] = responseData[0];
  //update minimal(mandatory) reusable 
  series.Minimal[0].data[3] = responseData[1];

  //update Recommended findable 
  series.Recommended[0].data[0] = responseData[2];
  //update Recommended reusable 
  series.Recommended[0].data[3] = responseData[3];

 
  //update Extended(optional) findable 
  series.Extended[0].data[3] =  responseData[4];

  // Update the chartOptions with the new colors based on the updated data
  const newChartColors = series[navigationTab.value][0].data.map(value => {
    if (value === 0) {
      return currentTheme.value.error;
    } else if (value === 100) {
      return currentTheme.value.success;
    } else {
      return currentTheme.value.info;
    }
  });

  chartOptions.value.colors = newChartColors;

  // Emit the metadata_percentage
  emitter.emit('new_series_variable', series)
  // Update the recommendedMetadataPercentage in the series constant
  // Update the extendedMetadataPercentage in the series constant
  // Call the updateOptions method on the VueApexCharts component to apply the updated colors
  const chartRef = ref(null); // Add this line to create a ref for the VueApexCharts component
  watch(() => series, () => {
    if (chartRef.value) {
      chartRef.value.updateOptions({ colors: newChartColors });
    }
  }, { deep: true });
  // Log the updated series
  console.log('colors after in handleResponseData', chartOptions.value.colors);
}


// Separate async function to fetch data from each endpoint
async function fetchEndpointData(endpoint, requestBody) {
  try {
    const response = await axios.post(endpoint, requestBody);
    return response.data;
  } catch (error) {
    console.error(`Error fetching data from ${endpoint}:`, error);
    return null;
  }
};


// Function to fetch data
async function fetchData(onto_url) {
  const requestBody = {
    onto_url: onto_url,
  };

  try {
    const endpoints = [
      config.endpoints.mandatoryFindableMetadataPercentage,
      config.endpoints.mandatoryReusableMetadataPercentage,
      config.endpoints.recommendedFindableMetadataPercentage,
      config.endpoints.recommendedReusableMetadataPercentage,
      config.endpoints.optionalReusableMetadataPercentage
    ];

    const responses = await Promise.all(endpoints.map(endpoint => fetchEndpointData(endpoint, requestBody)));

    const metadataPercentages = [
      Number((responses[0]?.[0]?.mandatory_findable_metadata_percentage || 0).toFixed(2)),
      Number((responses[1]?.[0]?.mandatory_reusable_metadata_percentage || 0).toFixed(2)),
      Number((responses[2]?.[0]?.mandatory_findable_metadata_percentage || 0).toFixed(2)),
      Number((responses[3]?.[0]?.mandatory_reusable_metadata_percentage || 0).toFixed(2)),
      Number((responses[4]?.[0]?.optional_reusable_metadata_percentage || 0).toFixed(2))
    ];

    console.log('Metadata Percentages:', metadataPercentages);

    // Call the handleResponseData function with the response data
    await handleResponseData(metadataPercentages); // Or any other response you want to use
  } catch (error) {
    // Handle the error
    console.error(error);
  }
};


// Function to fetch data
async function fetchOntoPortalsMetadataPercentage(ontologyData) {
  const requestBody = {
    portal_name: ontologyData.portalName,
    onto_acronym: ontologyData.ontologyAcronym,
    api_key: ontologyData.apiKey

  };

  try {
    const endpoints = [
      config.endpoints.mandatoryFindableMetadataPercentageViaPortal,
      config.endpoints.mandatoryReusableMetadataPercentageViaPortal,
      config.endpoints.recommendedFindableMetadataPercentageViaPortal,
      config.endpoints.recommendedReusableMetadataPercentageViaPortal,
      config.endpoints.optionalReusableMetadataPercentageViaPortal
    ];

    const responses = await Promise.all(endpoints.map(endpoint => fetchEndpointData(endpoint, requestBody)));

    const metadataPercentages = [
      Number((responses[0]?.[0]?.mandatory_findable_metadata_percentage || 0).toFixed(2)),
      Number((responses[1]?.[0]?.mandatory_reusable_metadata_percentage || 0).toFixed(2)),
      Number((responses[2]?.[0]?.mandatory_findable_metadata_percentage || 0).toFixed(2)),
      Number((responses[3]?.[0]?.mandatory_reusable_metadata_percentage || 0).toFixed(2)),
      Number((responses[4]?.[0]?.optional_reusable_metadata_percentage || 0).toFixed(2))
    ];

    // Call the handleResponseData function with the response data
    handleResponseData(metadataPercentages);
  } catch (error) {
    // Handle the error
    console.error(error);
  }
};

const legend = computed(() => {
  const currentSeries = series[navigationTab.value][0].data;
  const legendItems = [];

  for (let i = 0; i < currentSeries.length; i++) {
    const value = currentSeries[i];

    if (value === 0 && !legendItems.includes('No metadata found')) {
      legendItems.push('No metadata found');
    } else if (value === maxDataValue && !legendItems.includes('Totally Completed')) {
      legendItems.push('Totally Completed');
    } else if (value !== 0 && value !== maxDataValue) {
      const missingPercentage = maxDataValue - value;
      const partiallyCompletedMetadata = `Partially completed (${missingPercentage}% missing)`;

      if (!legendItems.includes(partiallyCompletedMetadata)) {
        legendItems.push(partiallyCompletedMetadata);
      }
    }
  }

  return legendItems;
});

const legendColors = computed(() => {
  const currentSeries = series[navigationTab.value][0].data;
  const legendItems = [];
  const legendColors = [];

  for (let i = 0; i < currentSeries.length; i++) {
    const value = currentSeries[i];

    if (value === 0 && !legendItems.includes('Missing')) {
      legendItems.push('Missing');
      legendColors.push(currentTheme.value.error);
    } else if (value === maxDataValue && !legendItems.includes('Totally Completed')) {
      legendItems.push('Totally Completed');
      legendColors.push(currentTheme.value.success);
    } else if (value !== 0 && value !== maxDataValue) {
      const missingPercentage = maxDataValue - value;
      const partiallyCompletedMetadata = `Partially completed (${missingPercentage}% missing)`;

      if (!legendItems.includes(partiallyCompletedMetadata)) {
        legendItems.push(partiallyCompletedMetadata);
        legendColors.push(currentTheme.value.info);
      }
    }
  }

  return legendColors;
});


</script>




<template>
  <VCard>
    <VCardTitle class="mt-3">
      FAIR metadata analysis
    </VCardTitle>

    <VTabs v-model="navigationTab">
      <VTab v-for="item in metadatas" :key="item" :value="item">
        {{ mappedTabLabels[item] }}
      </VTab>
    </VTabs>
    <VDivider />

    <!-- tabs content -->
    <div class="chart-container">
      <VWindow v-model="navigationTab">
        <VWindowItem v-for="item in metadatas" :key="item" :value="item">
          <VCardText v-if="isDataLoaded && isLoading === false">
            <div class="chart-wrapper">
              <VueApexCharts :options="chartOptions" :series="series[navigationTab]" :height="180" ref="chart"
                :width="500" />
              <!--
              <div class="legend-container">
                <ul class="legend">
                  <li v-for="(item, index) in legend" :key="index" class="legend-item">
                    <div class="legend-color" :style="{ background: legendColors[index] }"></div>
                    {{ item }}
                  </li>
                </ul>
              </div>
              -->
            </div>
          </VCardText>

          <VCardText v-if="isLoading" class="text-center py-5">
            <VProgressCircular indeterminate color="primary"></VProgressCircular>
          </VCardText>
        </VWindowItem>
      </VWindow>
    </div>
  </VCard>
</template>


<style lang="scss" scoped>
/* Add this style rule to override the text color of the Menu */
.apexcharts-menu-item {
  color: black !important;
  /* Set the desired text color, e.g., black */
}

.apexcharts-menu.apexcharts-menu-open {
  background: black;
}

.chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart-wrapper {
  position: relative;
  // background-color: red;
  height: 310px;
  width: 500px;
  padding: 10px;
}

.legend-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  margin-top: -38px;
  /* Add margin-top to create space between the chart and legend */
}

.legend {
  list-style-type: none;
  padding: 0;
  margin: 10px 0;
}

.legend-item {
  display: flex;
  align-items: center;
  word-break: break-word;
  margin-bottom: 5px;
}

.legend-color {
  width: 10px;
  height: 10px;
  margin-right: 5px;
  border-radius: 2px;
}
</style>

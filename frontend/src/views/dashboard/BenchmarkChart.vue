<template>
    <VCard>
        <VCardText>
            <h6 class="text-h6 mb-6">FOOPS! analysis</h6>
            <!-- Scatter Chart -->
            <VueApexCharts v-if="scatterFoopsSeries.length > 0" :options="foopsChartOptions" :series="scatterFoopsSeries"
                :height="400" />
            <div v-else>No data available</div>
        </VCardText>

        <VCardText class="mt-8">
            <h6 class="text-h6 mb-6">FAIR-Checker analysis</h6>
            <!-- Scatter Chart -->
            <VueApexCharts v-if="scatterFCSeries.length > 0" :options="FCChartOptions" :series="scatterFCSeries"
                :height="400" />
            <div v-else>No data available</div>
        </VCardText>

        <VCardText class="mt-8">
            <h6 class="text-h6 mb-6">O'FAIRe analysis</h6>
            <!-- Scatter Chart -->
            <VueApexCharts v-if="scatterOfaireSeries.length > 0" :options="ofaireChartOptions" :series="scatterOfaireSeries"
                :height="400" />
            <div v-else>No data available</div>
        </VCardText>

        <VCardText class="mt-8">
            <h6 class="text-h6 mb-6">Aggregated FAIR score</h6>
            <!-- Scatter Chart -->
            <VueApexCharts v-if="scatterAggregatedSeries.length > 0" :options="aggregatedChartOptions"
                :series="scatterAggregatedSeries" :height="400" />

            <div v-else>No data available</div>
        
        </VCardText>
    </VCard>
</template>
  
<script setup>
import VueApexCharts from 'vue3-apexcharts'
import { useTheme } from 'vuetify'
import { hexToRgb } from '@layouts/utils'
import { inject, ref } from 'vue'

// Inject `emitter`
const emitter = inject('emitter');

const colorVariables = themeColors => {
    const themeSecondaryTextColor = `rgba(${hexToRgb(themeColors.colors['on-surface'])},${themeColors.variables['medium-emphasis-opacity']})`
    const themeDisabledTextColor = `rgba(${hexToRgb(themeColors.colors['on-surface'])},${themeColors.variables['disabled-opacity']})`
    const themeBorderColor = `rgba(${hexToRgb(String(themeColors.variables['border-color']))},${themeColors.variables['border-opacity']})`
    const themePrimaryTextColor = `rgba(${hexToRgb(themeColors.colors['on-surface'])},${themeColors.variables['high-emphasis-opacity']})`

    return { themeSecondaryTextColor, themeDisabledTextColor, themeBorderColor, themePrimaryTextColor }
}

const vuetifyTheme = useTheme()
const currentTheme = ref(vuetifyTheme.current.value.colors)

// Function to format data for scatter chart series
const getFormattedData = (data, scoreKey, keys) => {    
    return data.map((item) => {
        var identifier = ""; keys.forEach(d => { if (item[d] != null) identifier += identifier.length > 0 ? "-"+item[d] : item[d]; });
        return {
            x: new Date(item.evaluation_date).getTime(),
            y: item[scoreKey],
            z: identifier
        };
    });
};

const toAggregatedSerie = (foopsSeries, FCseries, ofaireSeries) => {
    return [
        { name: "Score by Foops", data: foopsSeries },
        { name: "Score by FC", data: FCseries },
        { name: "Score by ofaire", data: ofaireSeries}
    ];
};
// Create arrays to store original data for daily and monthly views
const originalMetafairSemArtFoops = ref([]);
const originalMetafairSemArtFC = ref([]);
const originalMetafairSemArOfaire = ref([]);
const aggregatedSemArt = ref([]);

// Listen for the 'benchmarkList' event
emitter.on('benchmarkList', (benchmarkList) => {
    console.log('benchmarkList received', benchmarkList)
   

    // Update the original data arrays
    originalMetafairSemArtFoops.value = getFormattedData(benchmarkList, 'foops_score', ['semantic_artefact_URL', 'semantic_artefact_acronym', 'semantic_artefact_version']);
    originalMetafairSemArtFC.value = getFormattedData(benchmarkList, 'fairchecker_score', ['semantic_artefact_URL', 'semantic_artefact_acronym', 'semantic_artefact_version']);
    originalMetafairSemArOfaire.value = getFormattedData(benchmarkList, 'ofaire_score', ['semantic_artefact_URL', 'semantic_artefact_acronym', 'semantic_artefact_version']);

    console.log('originalMetafairSemArtFC.value', originalMetafairSemArtFC.value);
    console.log('originalMetafairSemArOfaire.value', originalMetafairSemArOfaire.value);
    // Initialize the scatter chart series with the default view (daily)
    updateScatterChartSeries(originalMetafairSemArtFoops.value, scatterFoopsSeries);
    updateScatterChartSeries(originalMetafairSemArtFC.value, scatterFCSeries);
    updateScatterChartSeries(originalMetafairSemArOfaire.value, scatterOfaireSeries);
    console.log('scatterFoopsSeries', scatterFoopsSeries);
    console.log('scatterFCSeries', scatterFCSeries);
    console.log('scatterOfaireSeries', scatterOfaireSeries.value);
    // Combine the data from different series into aggregatedSemArt
    scatterAggregatedSeries.value=[];
    toAggregatedSerie(
    originalMetafairSemArtFoops.value,
    originalMetafairSemArtFC.value,
    originalMetafairSemArOfaire.value
    ).forEach(series => {
    scatterAggregatedSeries.value.push(series);
    });

    console.log('scatterAggregatedSeries', scatterAggregatedSeries.value);
});

// Listen for the 'nonFilteredBenchmarkList' event
emitter.on('nonFilteredBenchmarkList', (benchmarkList) => {
    console.log('nonFilteredBenchmarkList received', benchmarkList)
    

    // Update the original data arrays
    originalMetafairSemArtFoops.value = getFormattedData(benchmarkList, 'foops_score', ['semantic_artefact_URL', 'semantic_artefact_acronym', 'semantic_artefact_version']);
    originalMetafairSemArtFC.value = getFormattedData(benchmarkList, 'fairchecker_score', ['semantic_artefact_URL', 'semantic_artefact_acronym', 'semantic_artefact_version']);
    originalMetafairSemArOfaire.value = getFormattedData(benchmarkList, 'ofaire_score', ['semantic_artefact_URL', 'semantic_artefact_acronym', 'semantic_artefact_version']);

    console.log('originalMetafairSemArtFC.value', originalMetafairSemArtFC.value);
    console.log('originalMetafairSemArOfaire.value', originalMetafairSemArOfaire.value);
    
    // Initialize the scatter chart series with the default view (daily)
    updateScatterChartSeries(originalMetafairSemArtFoops.value, scatterFoopsSeries, "Score by Foops");
    updateScatterChartSeries(originalMetafairSemArtFC.value, scatterFCSeries, "Score by Fair-checker");
    updateScatterChartSeries(originalMetafairSemArOfaire.value, scatterOfaireSeries, "Score by ofaire");
    console.log('scatterFoopsSeries', scatterFoopsSeries);
    console.log('scatterFCSeries', scatterFCSeries);
    console.log('scatterOfaireSeries', scatterOfaireSeries.value);

    scatterAggregatedSeries.value=[];
    toAggregatedSerie(
        originalMetafairSemArtFoops.value,
        originalMetafairSemArtFC.value,
        originalMetafairSemArOfaire.value
    ).forEach(series => {
        scatterAggregatedSeries.value.push(series);
    });

    console.log('scatterAggregatedSeries', scatterAggregatedSeries.value);

});

// Initialize an empty array for the scatter chart series
const scatterFoopsSeries = ref([]);
const scatterFCSeries = ref([]);
const scatterOfaireSeries = ref([]);
const scatterAggregatedSeries = ref([]);
// Update the scatter chart series
const updateScatterChartSeries = (metafairSemArt, seriesRef, toolName) => {
    const filteredData = metafairSemArt.filter(point => point.y !== null);
    const data = [
        {
            name: toolName,
            data: filteredData.map(point => ({
                x: point.x,
                y: point.y,
                z: point.z // Include the z value
            })),
        },
    ];

    seriesRef.value = data;
};




const foopsChartOptions = computed(() => {
    const backgroundColor = currentTheme.value.background

    return {
        chart: {
            type: 'scatter', // Set the chart type to scatter
            stacked: false,
            parentHeightOffset: 0,
            toolbar: { show: true },
            zoom: {
                type: 'xy',
                enabled: true,
            },
        },
        grid: {
            borderColor: colorVariables.themeBorderColor,
            xaxis: {
                lines: { show: true },
            },
            show: true,
        },
        colors: [
            currentTheme.value.error,
            currentTheme.value.info,
        ],
        plotOptions: {
            scatter: {
                markers: {
                    size: 6,
                    strokeWidth: 0,
                    hover: { size: 9 },
                },
            },
        },
        legend: {
            show: true,
            labels: { colors: '#ffffff' },
            position: 'top',
            horizontalAlign: 'left',
            markers: { offsetX: -3 },
            itemMargin: {
                vertical: 3,
                horizontal: 10,
            },
        },
        dataLabels: { enabled: false },
        xaxis: {
            labels: {
                show: true,
                style: {
                    colors: '#ffffff', // Set the color to white
                },
                //formatter: (val) => new Date(val).toLocaleDateString(), // Format the x-axis labels as dates
                formatter: (val) => {
                    const date = new Date(val);
                    const month = date.toLocaleString('default', { month: 'short' }); // Get the short month name
                    const year = date.getFullYear(); // Get the full year
                    return `${month} ${year}`;
                },
            },
            axisBorder: { show: true },
            axisTicks: { show: true },
            tickAmount: 1, // Set the maximum number of x-axis ticks to be displayed
        },
        yaxis: {
            show: true,
            labels: {
                show: true,
                style: {
                    colors: '#ffffff', // Set the color to white
                },
                formatter: (val) => val, // Format the y-axis labels to two decimal places
            },
            min: 0,
            max: 100, // Set the y-axis range from 0 to 100%
        },
        tooltip: {
            enabled: true,
            theme: 'dark',
            y: {
                formatter: (val) => val.toFixed(2), // Format the tooltip data value to two decimal places
            },
            z: {
                title: "ID:",
                formatter: (val) => val, // Format the tooltip data value to two decimal places
            },


        },
    }
});

const FCChartOptions = computed(() => {
    const backgroundColor = currentTheme.value.background

    return {
        chart: {
            type: 'scatter', // Set the chart type to scatter
            stacked: false,
            parentHeightOffset: 0,
            toolbar: { show: true },
            zoom: {
                type: 'xy',
                enabled: true,
            },
        },
        grid: {
            borderColor: colorVariables.themeBorderColor,
            xaxis: {
                lines: { show: true },
            },
            show: true,
        },
        colors: [
            currentTheme.value.info,
        ],
        plotOptions: {
            scatter: {
                markers: {
                    size: 6,
                    strokeWidth: 0,
                    hover: { size: 9 },
                },
            },
        },
        legend: {
            show: true,
            labels: { colors: '#ffffff' },
            position: 'top',
            horizontalAlign: 'left',
            markers: { offsetX: -3 },
            itemMargin: {
                vertical: 3,
                horizontal: 10,
            },
        },
        dataLabels: { enabled: false },
        xaxis: {
            labels: {
                show: true,
                style: {
                    colors: '#ffffff', // Set the color to white
                },
                formatter: (val) => new Date(val).toLocaleDateString(), // Format the x-axis labels as dates
            },
            axisBorder: { show: true },
            axisTicks: { show: true },
            tickAmount: 2, // Set the maximum number of x-axis ticks to be displayed
        },
        yaxis: {
            show: true,
            labels: {
                show: true,
                style: {
                    colors: '#ffffff', // Set the color to white
                },
                formatter: (val) => val, // Format the y-axis labels to two decimal places
            },
            min: 0,
            max: 100, // Set the y-axis range from 0 to 100%
        },
        tooltip: {
            enabled: true,
            theme: 'dark',
            y: {
                formatter: (val) => val.toFixed(2), // Format the tooltip data value to two decimal places
            },
            z: {
                title: "ID:",
                formatter: (val) => val, // Format the tooltip data value to two decimal places
            },


        },
    }
});

const ofaireChartOptions = computed(() => {
    const backgroundColor = currentTheme.value.background

    return {
        chart: {
            type: 'scatter', // Set the chart type to scatter
            stacked: false,
            parentHeightOffset: 0,
            toolbar: { show: true },
            zoom: {
                type: 'xy',
                enabled: true,
            },
        },
        grid: {
            borderColor: colorVariables.themeBorderColor,
            xaxis: {
                lines: { show: true },
            },
            show: true,
        },
        colors: [
            currentTheme.value.warning,
        ],
        plotOptions: {
            scatter: {
                markers: {
                    size: 6,
                    strokeWidth: 0,
                    hover: { size: 9 },
                },
            },
        },
        legend: {
            show: true,
            labels: { colors: '#ffffff' },
            position: 'top',
            horizontalAlign: 'left',
            markers: { offsetX: -3 },
            itemMargin: {
                vertical: 3,
                horizontal: 10,
            },
        },
        dataLabels: { enabled: false },
        xaxis: {
            labels: {
                show: true,
                style: {
                    colors: '#ffffff', // Set the color to white
                },
                formatter: (val) => new Date(val).toLocaleDateString(), // Format the x-axis labels as dates
            },
            axisBorder: { show: true },
            axisTicks: { show: true },
            tickAmount: 0, // Set the maximum number of x-axis ticks to be displayed
        },
        yaxis: {
            show: true,
            labels: {
                show: true,
                style: {
                    colors: '#ffffff', // Set the color to white
                },
                formatter: (val) => val, // Format the y-axis labels to two decimal places
            },
            min: 0,
            max: 100, // Set the y-axis range from 0 to 100%
        },
        tooltip: {
            enabled: true,
            theme: 'dark',
            y: {
                formatter: (val) => val.toFixed(2), // Format the tooltip data value to two decimal places
            },
            z: {
                title: "ID:",
                formatter: (val) => val, // Format the tooltip data value to two decimal places
            },


        },
    }
});

const aggregatedChartOptions = computed(() => {
    const backgroundColor = currentTheme.value.background

    return {
        chart: {
            type: 'scatter', // Set the chart type to scatter
            stacked: false,
            parentHeightOffset: 0,
            toolbar: { show: true },
            zoom: {
                type: 'xy',
                enabled: true,
            },
        },
        grid: {
            borderColor: colorVariables.themeBorderColor,
            xaxis: {
                lines: { show: true },
            },
            show: true,
        },
        colors: [
            currentTheme.value.error,
            currentTheme.value.info,
            currentTheme.value.warning,

        ],
        plotOptions: {
            scatter: {
                markers: {
                    size: 6,
                    strokeWidth: 0,
                    hover: { size: 9 },
                },
            },
        },
        legend: {
            show: true,
            labels: { colors: '#ffffff' },
            position: 'top',
            horizontalAlign: 'left',
            markers: { offsetX: -3 },
            itemMargin: {
                vertical: 3,
                horizontal: 10,
            },
        },
        dataLabels: { enabled: false },
        xaxis: {
            labels: {
                show: true,
                style: {
                    colors: '#ffffff', // Set the color to white
                },
                formatter: (val) => new Date(val).toLocaleDateString(), // Format the x-axis labels as dates
            },
            axisBorder: { show: true },
            axisTicks: { show: true },
            tickAmount: 2, // Set the maximum number of x-axis ticks to be displayed
        },
        yaxis: {
            show: true,
            labels: {
                show: true,
                style: {
                    colors: '#ffffff', // Set the color to white
                },
                formatter: (val) => val, // Format the y-axis labels to two decimal places
            },
            min: 0,
            max: 100, // Set the y-axis range from 0 to 100%
        },
        tooltip: {
            enabled: true,
            theme: 'dark',
            y: {
                formatter: (val) => val.toFixed(2), // Format the tooltip data value to two decimal places
            },
            z: {
                title: "ID:",
                formatter: (val) => val, // Format the tooltip data value to two decimal places
            },


        },
    }
});
</script>
  
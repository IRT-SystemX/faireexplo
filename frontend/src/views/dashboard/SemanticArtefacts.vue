<template>
  <VCard>
    <VCardItem>
      <VCardTitle>
        Summary of extracted metadata
      </VCardTitle>
      
    </VCardItem>

    <VCardText v-if="isDataLoaded && isLoading === false">
      
      <VRow v-if="filteredSemanticArtifactsViaPortals.length > 0">
        <VCol
          v-for="(item, index) in filteredSemanticArtifactsViaPortals"
          :key="item.title"
          cols="6"
          sm="6"
        >
          <div class="mb-20">
            <VCard class="custom-card">
              <div class="me-3 mb-2">
                  <VIcon  size="40" :color="iconColor[index]">{{ icons[index] }}</VIcon>
              </div>
              <div class="mb-3">
                <span class=" text-center font-weight-medium mb-0 white-text" >{{ item.title }}</span>
              </div>
              <div>
                <template v-if="item.stats.includes(',')">
                  <div class="text-caption ">
                    <span>{{ item.stats.split(',')[0] }}</span>
                  </div>
                  <div class="text-caption ">
                    <span>{{ item.stats.split(',')[1] }}</span>
                  </div>
                </template>
                <template v-else>
                  <div class="text-caption ">
                    <span>{{ item.stats }}</span>
                  </div>
                </template>
              </div>

            </VCard>
          </div>
        </VCol>
      </VRow>
      <VRow v-else-if="filteredStatistics.length > 0">
        <VCol
          v-for="(item, index) in filteredStatistics"
          :key="item.title"
          cols="6"
          sm="6"
        >
        <div class="mb-20">
            <VCard class="custom-card mt-8">
              <div class="me-3">
                <div class="me-3 mb-2">
                  <VIcon  size="40" :color="iconColor[index]">{{ icons[index] }}</VIcon>
              </div>
              </div>
              <div>
                <span class="text-center font-weight-medium mb-0 white-text">{{ item.title }} </span>
              </div>
              <div>
                <span class="text-caption">{{ item.stats }}</span>
              </div>
            </VCard>
          </div>
        </VCol>
      </VRow>
      <VRow v-else>
        <VCol
          v-for="(item, index) in notAvailable"
          :key="item.title"
          cols="6"
          sm="6"
        >
          <div class="mb-20">
            <VCard class="custom-card">
              <div class="me-3 mb-3">
                <div class="me-3 mb-2">
                  <VIcon  size="40" :color="iconColor[index]">{{ icons[index] }}</VIcon>
              </div>
              </div>
              <div class="mb-3">
                <span class="text-center font-weight-medium mb-0 purple-text" >{{ item.title }}</span>
              </div>
              <div class="mb-3">
                <span class="text-caption">{{ item.stats }}</span>
              </div>
            </VCard>
          </div>
        </VCol>
      </VRow>
    
    </VCardText>

    <VCardText v-if="isLoading" class="text-center py-5">
            <VProgressCircular indeterminate color="primary"></VProgressCircular>
    </VCardText>
  </VCard>
</template>

<script>
import axios from 'axios';
import config from '@/config.js';

export default {
  inject: ['emitter','store'],
  data() {
    return {
      ontologyAcronym: '',
      portal_name:'',
      api_key:'',
      statistics: [], // Populate with the response from the endpoint
      filteredStatistics: [],
      filteredSemanticArtifactsViaPortals: [],
      semanticArtifactsData: {},
      semanticArtifactsViaPortals: null,
      icons: [
        'mdi-dictionary', // Icon for "Acronym"
        'mdi-flask-empty', // Icon for "Domain"
        'mdi-alpha-v-circle', // Icon for "Version"
        'mdi-pencil', // Icon for "Created by"
      ],
      iconColor: [
        'info', // Color for "Dictionary" icon
        'warning', // Color for "Domain" icon
        'primary', // Color for "Version" icon
        'success', // Color for "Created by" icon
      ],
      notAvailable:[
      { title:"Acronym", stats: "Not found" },
      { title:"Domain", stats: "Not found" },
      { title:"Version", stats: "Not found" },
      { title:"Created by", stats: "Not found" }
      ]
    };
  },
  computed: {

    //for dashboard loading on endpoint response
    isDataLoaded() {
      return this.store.state.isDataLoaded; // Access state from the Vuex store
    },

    isLoading() {
      return this.store.state.loading; // Access state from the Vuex store
    },
  },
  mounted() {
    this.updateStatistics();
    this.semanticArtefactsFromPortals();
    console.log('Component Semantic Artefacts is listening for semanticArtifactsData event');
  },
  /*
  watch: {
    filtered(newFiltered) {
      this.emitter.emit('extracted_metadata', newFiltered);
    },
  },
  */
  methods: {
    updateStatistics() {
      this.emitter.on('semanticArtifactsData', (data) => {
        if(this.semanticArtifactsViaPortals) this.semanticArtifactsViaPortals = null;
        this.semanticArtifactsData ={};

        this.semanticArtifactsData = data
        this.statistics = Object.entries(data)
          .map(([key, value]) => ({ title: key, stats: value }));

        console.log('Response semantic:', this.statistics);
        if (this.statistics) {
          console.log('Component Semantic Artefacts received semanticArtifactsData:', data);
          this.setFilteredStatistics();
        }        
      });
    },

    semanticArtefactsFromPortals() {
      this.emitter.on('semantic_artifacts_data_via_portal', (data) => {
        this.semanticArtifactsViaPortals= null;
        this.semanticArtifactsData ={};
        //this.semanticArtifactsData = data
        this.portal_name=data.portalName;
        this.ontologyAcronym=data.ontologyAcronym;
        this.api_key=data.apiKey;
        this.ontoPortalsMetadata(); // Call the function to consume the POST endpoint
        console.log('Component Semantic Artefacts received semanticArtifactsViaPortals:', this.ontologyAcronym);
        
      });
    },
    //Retrieve Semantic artefacts for ontologies from Portals 
    async ontoPortalsMetadata() {
      const requestBody = {
        portal_name:this.portal_name,
        onto_acronym: this.ontologyAcronym,
        api_key:this.api_key

      };
      console.log('POST endpoint requestBody:', requestBody);
      try {
        const response = await axios.post(config.endpoints.ofaireMetadataAll, requestBody);
        this.semanticArtifactsViaPortals = response.data;
        // Emit that response is loaded
        this.emitter.emit('SemanticArtifactsLoaded', true);
        this.emitter.emit('semanticArtifactsViaPortals', this.semanticArtifactsViaPortals);
        
        this.setFilteredSemanticArtifactsViaPortals();

        console.log('POST endpoint response:', response.data);
        console.log('POST endpoint response var semart:', this.semanticArtifactsViaPortals);
      } catch (error) {
        // Handle errors
        console.error('Error consuming POST endpoint:', error);
      }
    },
    
    setFilteredStatistics() {
      const titles = {
        Acronym: ["Acronym", "Title"],
        Domain: ["Domain"],
        Version: ["Version", "VersionInfo"],
        Createdby: ["Created by", "Creator"]
      };

      const filtered = [];

      for (const key in titles) {
        const values = titles[key];
        let item;

        for (const value of values) {
          item = this.statistics.find((stat) =>
            stat.title.toLowerCase().includes(value.toLowerCase())
          );

          if (item) {
            break;
          }
        }

        if (item) {
          filtered.push(item);
        } else {
          filtered.push({ title: key, stats: "Not found" });
        }
      }

      this.emitter.emit('extracted_metadata', filtered);
      this.filteredStatistics = filtered;
    },
    setFilteredSemanticArtifactsViaPortals() {
      
      const titles = ["acronym", "domain", "version", "created by"];
      const filtered = [];

      if (this.semanticArtifactsViaPortals) {
        // Filter for the first title "Acronym"
        filtered.push({ title: titles[0], stats: this.semanticArtifactsViaPortals[0].ontologyAcronym });

        // Filter for the rest of the titles
        for (const title of titles.slice(1)) {
          const key = title.toLowerCase();
          if (this.semanticArtifactsViaPortals[1] && key in this.semanticArtifactsViaPortals[1].ontologyMetadata) {
            const values = this.semanticArtifactsViaPortals[1].ontologyMetadata[key];
            filtered.push({ title, stats: values.join(",") });
          } else {
            filtered.push({ title, stats: "Not found" });
          }
        }
      }
      this.emitter.emit('extracted_metadata', filtered);
      this.filteredSemanticArtifactsViaPortals = filtered;
    },

  },
};
</script>


<style>
.purple-text {
  color: rgb(153, 97, 252);
}
.custom-card {
  margin-left: 50px;
  width: 180px; /* Set the width as per your requirement */
  height: 100px; /* Set the height as per your requirement */
  color: white;
}

</style>
<script setup>
import { inject, ref } from 'vue'; // Import ref function
const selectedCardTitle = ref(null); // Create a reactive variable
const emitter = inject('emitter');   // Inject `emitter`

const solidCardData = [
  { 
    title: 'Industry domain',
    icon: 'mdi-factory',
    text: 'List of evaluated semantic artefacts covering industries such as technology, healthcare, finance, manufacturing, energy, and more.',
  },

  {
    title: 'Biomedical domain',
    icon: 'mdi-flask',
    text: ' List of evaluated semantic artefacts representing the human body, its functions, diseases, medical treatments, and clinical decisions.',
    
  },

  {
    title: 'Agriculture domain',
    icon: 'mdi-seed',
    text: 'List of evaluated semantic artefacts representing crop cultivation, raising livestock, and producing food, fibres, and raw materials for various purposes.',
   
  },
]

const showResult = (title) => {
  const firstWord = title.split(' ')[0]; // Get the first word from the title
  selectedCardTitle.value = firstWord; // Update the selected card title
  emitter.emit('selectedCardTitle', selectedCardTitle.value);
  console.log('emitted data', selectedCardTitle.value);
};

</script>

<template>
  <VRow class="match-height">
    <VCol
      v-for="data in solidCardData"
      :key="data.icon"
      cols="12"
      md="6"
      lg="4"
    >
      <VCard >
        <VCardItem>
          <template #prepend>
            <VIcon
              size="1.9rem"
              color="white"
              :icon="data.icon"
            />
          </template>
          <VCardTitle class="text-white">
            {{ data.title }}
          </VCardTitle>
        </VCardItem>

        <VCardText>
          <p class=" text-white mb-0">
            {{ data.text }}
          </p>
        </VCardText>

        <VCardText class="d-flex justify-space-between align-center flex-wrap">
          <div class="d-flex align-center">
            <v-btn @click="showResult(data.title)">
              Show result
            </v-btn>
          </div>
        </VCardText>

      </VCard>
    </VCol>
  </VRow>
</template>

<style scoped>
.v-btn {
color : white;
 
}
</style>
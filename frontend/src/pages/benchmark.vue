<script setup>

import CardSolid from '@/views/pages/cards/card-basic/BenchmarkCards.vue'
import BenchmarkList from '@/views/dashboard/BenchmarkList.vue'
import BenchmarkChart from '@/views/dashboard/BenchmarkChart.vue'
</script>

<template>
  <div>
   
    <p class="text-2xl mt-2 mb-6 ">
      Discover by domain
    </p>

    <CardSolid />

    <p class="text-2xl mt-14 mb-6 ">
      
    </p>

    <BenchmarkList />

    <p class="text-2xl mt-14 mb-6 ">
      <router-link to="/dashboard"><VBtn color="primary">Add artefact</VBtn></router-link>
    </p>

    <p class="text-2xl mt-14 mb-6 ">
      FAIR landscape analysis
    </p>
    <BenchmarkChart />
  </div>
</template>

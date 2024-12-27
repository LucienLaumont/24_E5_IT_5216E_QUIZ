<script setup>
import { RouterView } from 'vue-router';
import Header from './components/Header.vue';
</script>

<template>
  <div id="app">
    <Header />
    <router-view />
  </div>
</template>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

router-view {
  flex: 1;
}
</style>

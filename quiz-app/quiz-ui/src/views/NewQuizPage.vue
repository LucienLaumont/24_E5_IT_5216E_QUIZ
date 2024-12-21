<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <p class="form-label">Saisissez votre nom :</p>
        <div class="mb-3">
          <input
            type="text"
            v-model="playerName"
            class="form-control"
            placeholder="Username"
          />
        </div>
        <button @click="launchNewQuiz" class="btn btn-outline-danger btn-lg">
          GO!
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import participationStorageService from '@/services/ParticipationStorageService';

// Variable réactive pour stocker le nom du joueur
const playerName = ref('');
const router = useRouter();

// Fonction appelée lors du clic sur le bouton
function launchNewQuiz() {
  if (playerName.value.trim() !== '') {
    participationStorageService.savePlayerName(playerName.value);
    console.log('Launch new quiz with', playerName.value);

    router.push('/questions'); // Redirection vers la première question
  } else {
    alert('Veuillez saisir votre nom.');
  }
}
</script>

<style scoped>
.btn {
  width: 100%;
  margin-top: 10px;
}
</style>

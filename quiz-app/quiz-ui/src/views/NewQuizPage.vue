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
        <button @click="submitName" class="btn btn-outline-danger btn-lg">
          GO!
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Variable réactive pour stocker le nom du joueur
const playerName = ref('');

// Fonction appelée lors du clic sur le bouton
const submitName = () => {
  if (playerName.value.trim() !== '') {
    console.log('Nom du joueur :', playerName.value);
    // Vous pouvez ajouter une logique supplémentaire ici
  } else {
    alert('Veuillez saisir votre nom.');
  }
};
</script>

<style scoped>
.btn {
  width: 100%;
  margin-top: 10px;
}
</style>

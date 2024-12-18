<template>
  <div>
    <h1>Scores enregistrés</h1>
    <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
      {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
    </div>
    <router-link to="/new-quiz">Démarrer le quiz !</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted, toDisplayString } from 'vue';
import quizApiService from '@/services/QuizApiService';

// Déclare une variable réactive pour les scores
const registeredScores = ref([]);

onMounted(async () => {
  try {
    const response = await quizApiService.getQuizInfo();
    if (response && response.data && response.data.scores) {
      registeredScores.value = response.data.scores; // Accédez au tableau 'scores'
    } else {
      console.error('Erreur : Aucune donnée trouvée.');
    }
  } catch (error) {
    console.error(
      'Erreur lors de la récupération des informations du quiz :',
      error
    );
  }
});
</script>

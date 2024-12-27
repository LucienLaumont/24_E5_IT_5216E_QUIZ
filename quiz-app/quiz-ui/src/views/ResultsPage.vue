<template>
  <div class="results-page">
    <h1>Résultats</h1>

    <!-- Affichage du score -->
    <div class="score-section">
      <h2>Votre Score</h2>
      <p>{{ score }} / {{ totalQuestions }}</p>
    </div>

    <!-- Affichage du classement -->
    <div class="ranking-section">
      <h2>Classement Général</h2>
      <ul>
        <li v-for="(participant, index) in rankings" :key="index">
          {{ index + 1 }}. {{ participant.name }} - {{ participant.score }}
        </li>
      </ul>
    </div>

    <!-- Affichage des meilleurs scores -->
    <div class="top-scores-section">
      <h2>Meilleurs Scores</h2>
      <ul>
        <li v-for="(topScore, index) in topScores" :key="index">
          {{ index + 1 }}. {{ topScore.name }} - {{ topScore.score }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import QuizApiService from '@/services/QuizApiService';

const router = useRouter();

// Variables réactives
const score = ref(0);
const totalQuestions = ref(0);
const rankings = ref([]);
const topScores = ref([]);

// Charger les données des résultats
onMounted(async () => {
  const participationId = localStorage.getItem('participationId');
  if (!participationId) {
    console.error('Aucun ID de participation trouvé dans le localStorage.');
    router.push('/');
    return;
  }

  try {
    // Récupérer les détails de la participation
    const quizInfo = await QuizApiService.getQuizInfo();
    const participationResponse = await QuizApiService.call(
      'get',
      `/participations/${participationId}`
    );
    if (participationResponse?.status === 200) {
      score.value = participationResponse.data.score;
      totalQuestions.value = quizInfo.data.size;
    }

    // Récupérer le classement général
    const rankingsResponse = await QuizApiService.call(
      'get',
      '/participations/rankings'
    );
    if (rankingsResponse?.status === 200) {
      rankings.value = rankingsResponse.data;
    }

    // Récupérer les meilleurs scores
    const topScoresResponse = await QuizApiService.call(
      'get',
      '/participations/top-scores'
    );
    if (topScoresResponse?.status === 200) {
      topScores.value = topScoresResponse.data;
    }
  } catch (error) {
    console.error(
      'Erreur lors du chargement des données de résultats :',
      error
    );
  }
});
</script>

<style scoped>
.results-page {
  text-align: center;
  margin: 20px auto;
  max-width: 600px;
}

.score-section,
.ranking-section,
.top-scores-section {
  margin: 20px 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 5px 0;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>

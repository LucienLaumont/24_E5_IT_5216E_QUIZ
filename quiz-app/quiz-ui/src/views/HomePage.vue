<template>
  <div class="home-page">
    <div class="row">
      <!-- Colonne de gauche : Descriptif du projet -->
      <div class="column column-left">
        <h2>🏆 Quiz sur les Jeux Olympiques</h2>
        <p>
          Bienvenue sur le projet
          <strong>Quiz sur les Jeux Olympiques</strong> réalisé dans le cadre de
          la matière <strong>Développement Web Fullstack</strong> 🖥️ à
          l'<strong>ESIEE</strong>, école d'ingénieurs. Ce projet s'inscrit dans
          le programme de l'UE <strong>E5</strong> et a été conçu par :
        </p>
        <ul>
          <li>
            👨‍💻 Nathan Balluais :
            <a href="mailto:nathan.balluais@edu.esiee.fr"
              >nathan.balluais@edu.esiee.fr</a
            >
          </li>
          <li>
            👩‍💻 Anthinea Camman :
            <a href="mailto:anthinea.camman@edu.esiee.fr"
              >anthinea.camman@edu.esiee.fr</a
            >
          </li>
          <li>
            👨‍💻 Lucien Laumont :
            <a href="mailto:lucien.laumont@edu.esiee.fr"
              >lucien.laumont@edu.esiee.fr</a
            >
          </li>
        </ul>
        <p>
          Ce quiz interactif permet de tester vos connaissances 🧠 sur les Jeux
          Olympiques, tout en accédant à un classement dynamique en temps réel.
          🥇🥈🥉
        </p>

        <h3>🛠️ Composants clés du projet</h3>
        <ul>
          <li>
            🏠 <strong>Page d'accueil</strong> : Introduction au quiz et accès
            rapide au jeu.
          </li>
          <li>
            📊 <strong>Classement interactif</strong> : Suivi des meilleurs
            scores avec un leaderboard dynamique.
          </li>
          <li>
            📝 <strong>Système de quiz</strong> : Répondez à une série de
            questions sur les Jeux Olympiques et découvrez votre score.
          </li>
          <li>
            🔒 <strong>Back-office</strong> : Gestion des questions et
            administration des scores, réservé aux administrateurs.
          </li>
          <li>
            📱 <strong>Responsivité</strong> : Une interface fluide et
            ergonomique pour tous les appareils.
          </li>
        </ul>

        <h3>📌 Informations pratiques</h3>
        <p>
          Retrouvez le projet sur GitHub :
          <a
            href="https://github.com/LucienLaumont/24_E5_IT_5216E_QUIZ"
            target="_blank"
          >
            https://github.com/LucienLaumont/24_E5_IT_5216E_QUIZ
          </a>
        </p>
        <p>
          Un grand merci à tous ceux qui participent à rendre ce projet vivant !
          🌟 Testez vos connaissances et plongez dans l'univers des Jeux
          Olympiques ! 🚴‍♀️🏊‍♂️🏋️‍♀️
        </p>
      </div>

      <!-- Colonne de droite : Bouton dans une ligne + Leaderboard -->
      <div class="column column-right">
        <!-- Ligne du bouton -->
        <div class="button-row">
          <router-link to="/new-quiz" class="start-quiz-button">
            🚀 Démarrer le quiz !
          </router-link>
        </div>
        <!-- Ligne du leaderboard -->
        <div class="leaderboard-row">
          <Leaderboard :leaderboard-data="leaderboardData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import Leaderboard from '@/components/Leaderboard.vue'; // Import du composant Leaderboard

// Variables réactives
const leaderboardData = ref({
  scores: [],
  size: 0,
});

onMounted(async () => {
  try {
    const response = await quizApiService.getQuizInfo();
    if (response && response.data && response.data.scores) {
      leaderboardData.value.scores = response.data.scores.map((score) => ({
        playerName: score.playerName,
        score: score.score,
      }));
      leaderboardData.value.size = response.data.scores.length;
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

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  padding-top: 6%;
  font-size: 18px;
}

.row {
  display: flex;
  flex-wrap: nowrap; /* Empêche l'empilement vertical des colonnes */
  gap: 1rem; /* Espacement entre les colonnes */
}

.column {
  box-sizing: border-box;
  border-radius: 8px;
  color: black;
}

.column-left {
  flex: 5;
  padding: 20px;
  background-color: #f9f9f9;
}

.column-right {
  flex: 2; /* 40% */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px; /* Espacement entre les lignes */
}

.button-row {
  width: 100%;
  display: flex;
  justify-content: center; /* Centre le bouton horizontalement */
}

.start-quiz-button {
  background-color: rgb(219, 170, 8);
  color: white;
  padding: 10px 20px;
  width: 100%;
  text-decoration: none;
  border-radius: 8px;
  text-align: center;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.start-quiz-button:hover {
  background-color: rgb(182, 140, 4);
}

.leaderboard-row {
  width: 100%;
}
</style>

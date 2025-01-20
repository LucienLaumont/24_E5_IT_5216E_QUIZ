<template>
  <!-- 
    On remplace l'enveloppe .results-page par
    .page-container + .grid-container pour la grille de 16 GIFs. 
    On y centre la "carte" (ou le bloc) contenant Podium, ScoreCard, et Leaderboard. 
  -->
  <div
    class="results-page page-container d-flex justify-content-center align-items-center"
  >
    <div class="grid-container">
      <!-- Génération dynamique des GIFs (16 cases) -->
      <div
        v-for="(gif, index) in gifs"
        :key="index"
        class="grid-item"
        :style="{
          backgroundImage: `url(${gif})`,
          animationDelay: `${index * 0.2}s`,
        }"
      ></div>

      <!-- 
        Bloc centré au-dessus de la grille contenant les 2 colonnes :
        - Podium et ScoreCard dans la "first-column"
        - Leaderboard dans la "last-column"
      -->
      <div class="center-card">
        <div class="first-column">
          <div class="podium-wrapper">
            <Podium :scores="podiumWinners" />
          </div>
          <div class="scorecard-wrapper">
            <ScoreCard :score="score" :totalQuestions="totalQuestions" />
          </div>
        </div>
        <div class="last-column">
          <Leaderboard :leaderboard-data="leaderboardData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ScoreCard from '@/components/ScoreCard.vue';
import Leaderboard from '@/components/Leaderboard.vue';
import Podium from '@/components/Podium.vue';
import QuizApiService from '@/services/QuizApiService';

// Liste des GIFs (16 éléments) pour la grille
const gifs = [
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTYwdDEwNjF5NTB3OGIxcXFvaW1ucDJ4bXBxeHlxcmpkdHpsMGQwayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ohzgMcA2PxS5ae7T2/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGd6Y3VrZmkzMTFhMmZweG03cWc2MGJ3Mm00bDFtbnZ6N3dvOHY2ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Vz5zgjOO7khaoAIesM/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXhxejZqNTRwNXdxdHN1cGdyam1uaWp4dWR3dmZrcW5nZ2ViZjhieCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RLm3ZunaMZzMmkk5Ht/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnNkOHg3Y3lucmozdzZpM3ltZGczZGZkdW5meGRlbjNlb3c2ZjNqbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KcWQdNihMEkYMI1EJp/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdm96dTk4ZnkwZThyYzludm81NHVybjFjeTB4MXpsZm95bzdyamxsNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dAJTNv2EHxDIk/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWd0OGthbDlmaHJxOGt1cGc2Y2E2b2ticmtrenQ0OTc5NDd2aDI3biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/gD3hLJgMLWmVW/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNW5xeTZxYTA3NHhxYTdkaWp2ZjR6d2hjOTN5MHQyeWVqOGo1d2YwcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XeY0cFOr2IWYGfJpQz/giphy-downsized-large.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnFrOWd5ZzVia241cDc3ZmIzZmd0dHBrZ3JrdjhqcGxwajFhdGlrZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7vB7MdHThlWESpkpMk/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXl6NTFvbWt2cXh3ZG43NmwwNmtlNHhlazlraHRzd3NxZ25nbmcxaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RJgjZ7a6lxyCKIwxAD/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcG96b2FhM3hqaDQ5enhzZ2JzeTY5ZXl4Y2h0dGxxNm1jOGNscDFndSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/msZFkfFhLHAZFuokpm/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExem9ueDI2ZTVhcmo4emFlNTA4aTluZmx5bWlqaGR2Nmk0YW9wbTR3bSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fadzmZStobRICiFXLU/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmw5ZW1lZ3Q2dGxyd2ptMjdrMGM1amFnZWlkcGRzNGw3b2wxYjhsNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/2knEjjTqja0taarfeP/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExem82NGNsY3kwOGVpa2hoenRpb3NvcWFuczlmcGJrc2pkbXl4ZGw2cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ItHnwCKCoAu2PS2wFC/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjk2OHpncW82cWc5ZHI2ODFmZDB0eWM0aWY5ZW5zYnZsdGFtejRsYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vwjfBggP3Q5vEdTx9H/giphy-downsized-large.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3hoYXMwZDh0dWVxbDcxYzZzdzFuajFkcmF1ZzY3bWhuNTZwMmp2byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/U1gkiAV2IbeZJiFT0k/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWQwazNxbzMxZHc2YnVhdm4wMWFxcGdlZml6amp4NnNtaG5oMXFiNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/39uiVjumlJkYqAXil1/giphy-downsized-large.gif',
];

const score = ref(0);
const totalQuestions = ref(0);
const leaderboardData = ref({ scores: [], size: 0 });
const podiumWinners = ref([]);
const router = useRouter();

onMounted(async () => {
  const participationId = localStorage.getItem('participationId');

  if (!participationId) {
    console.warn('Aucun ID de participation trouvé dans le localStorage.');
    score.value = 0; // Score par défaut
    totalQuestions.value = 0; // Valeur par défaut
  }

  try {
    const [quizInfo, participationResponse] = await Promise.all([
      QuizApiService.getQuizInfo(),
      participationId ? QuizApiService.getParticipation(participationId) : null,
    ]);

    if (participationResponse?.status === 200) {
      score.value = participationResponse.data.score;
      totalQuestions.value = quizInfo.data.size;
    } else if (!participationId) {
      console.warn('Participation non valide. Score par défaut utilisé.');
      score.value = 0; // Score par défaut pour les non-participants
      totalQuestions.value = quizInfo?.data?.size || 0; // Total des questions par défaut
    }

    leaderboardData.value = quizInfo.data.scores
      ? {
          scores: quizInfo.data.scores.map((entry) => ({
            playerName: entry.playerName,
            score: entry.score,
          })),
          size: quizInfo.data.scores.length,
        }
      : { scores: [], size: 0 };

    // Extraire les 3 meilleurs scores pour le podium
    podiumWinners.value =
      quizInfo.data.scores && quizInfo.data.scores.length >= 3
        ? quizInfo.data.scores.slice(0, 3).map((entry) => ({
            playerName: entry.playerName,
            score: entry.score,
          }))
        : [
            { playerName: '---', score: 0 },
            { playerName: '---', score: 0 },
            { playerName: '---', score: 0 },
          ];
  } catch (error) {
    console.error('Erreur lors de la récupération des résultats :', error);
    score.value = 0; // Score par défaut en cas d'erreur
    totalQuestions.value = 0; // Valeur par défaut en cas d'erreur
  }
});
</script>

<style scoped>
/* 
  On combine .results-page (héritée du code précédent) et 
  .page-container pour centrer verticalement/horizontalement.
*/
.results-page.page-container {
  padding-top: 6%;
  height: 98vh;
}

/* Grille de 4x4 = 16 carrés */
.grid-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4 colonnes */
  grid-template-rows: repeat(4, 1fr); /* 4 lignes */
  height: 100%;
  width: 100%;
  position: relative;
}

/* Chaque GIF */
.grid-item {
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0; /* invisible avant l'anim */
  animation: fadeIn 1s ease-in-out forwards;
}

/* Animation d'apparition progressive */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 
  Conteneur centré par-dessus la grille 
  (l'équivalent de la "carte" du fichier d'exemple).
*/
.center-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10; /* Au-dessus de la grille */
  display: flex;
  gap: 3rem; /* Pour espacer les deux colonnes */
}

/* Colonnes Podium/Score et Leaderboard */
.first-column,
.last-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
  min-width: 300px; /* Ajustez si besoin */
  max-height: 800px; /* Ajustez si besoin */
}

.podium-wrapper,
.scorecard-wrapper {
  width: 100%;
  min-height: 200px;
  max-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
}

.podium-wrapper {
  margin-bottom: 3rem;
}
</style>

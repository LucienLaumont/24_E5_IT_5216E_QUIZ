<template>
  <div>
    <h1>
      Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}
    </h1>
    <QuestionDisplay
      v-if="currentQuestion"
      :currentQuestion="currentQuestion"
      @answer-clicked="answerClickedHandler"
    />
    <div v-else>
      <p>Chargement de la question...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import QuestionDisplay from '../components/QuestionDisplay.vue';
import QuizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';
import { useRouter } from 'vue-router';

const router = useRouter();

// Variables réactives
const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const userAnswers = ref([]); // Liste des réponses sélectionnées

// Méthode pour charger une question par sa position
const loadQuestionByPosition = async (position) => {
  try {
    const response = await QuizApiService.getQuestion(position);
    if (response?.status === 200) {
      currentQuestion.value = response.data;
    } else {
      console.error('Erreur : Question introuvable');
    }
  } catch (error) {
    console.error('Erreur lors du chargement de la question :', error);
  }
};

// Méthode pour gérer la sélection d'une réponse
const answerClickedHandler = async (answerId) => {
  console.log('Réponse sélectionnée :', answerId + 1);

  // Ajouter la réponse sélectionnée à la liste des réponses utilisateur
  userAnswers.value.push(answerId + 1); // Ajouter 1 à l'index pour correspondre à l'ID attendu

  if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
    currentQuestionPosition.value += 1;
    await loadQuestionByPosition(currentQuestionPosition.value);
  } else {
    endQuiz();
  }
};

// Méthode pour terminer le quiz
const endQuiz = async () => {
  console.log('Fin du quiz !');
  await submitParticipation(); // Soumettre les réponses utilisateur
  router.push('/results'); // Redirection vers la page des résultats
};

const submitParticipation = async () => {
  try {
    const playerName = participationStorageService.getPlayerName();
    if (!playerName) {
      console.error('Nom du joueur introuvable dans le localStorage.');
      return;
    }

    const response = await QuizApiService.call('post', '/participations', {
      playerName,
      answers: userAnswers.value, // Liste des réponses de l'utilisateur
    });

    if (response?.status === 200) {
      participationStorageService.saveParticipationScore(response.data.score);
      participationStorageService.saveParticipationId(
        response.data.participationId
      ); // Sauvegarder l'ID de participation
      router.push('/results'); // Redirection vers la page des résultats
    } else {
      console.error(
        "Erreur lors de l'enregistrement de la participation :",
        response
      );
    }
  } catch (error) {
    console.error('Erreur lors de la soumission de la participation :', error);
  }
};

// Initialisation du composant
onMounted(async () => {
  try {
    const quizInfo = await QuizApiService.getQuizInfo();
    if (quizInfo?.status === 200) {
      totalNumberOfQuestions.value = quizInfo.data.size;
      await loadQuestionByPosition(currentQuestionPosition.value);
    } else {
      console.error(
        'Erreur : Impossible de récupérer les informations du quiz.'
      );
    }
  } catch (error) {
    console.error("Erreur lors de l'initialisation :", error);
  }
});
</script>

<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
}
</style>

<template>
  <div class="page-container d-flex justify-content-center align-items-center">
    <div class="grid-container">
      <!-- Génération dynamique des GIFs -->
      <div
        v-for="(gif, index) in gifs"
        :key="index"
        class="grid-item"
        :style="{
          backgroundImage: `url(${gif})`,
          animationDelay: `${index * 0.2}s`,
        }"
      ></div>

      <!-- Carte centrée -->
      <div class="center-card">
        <div class="card shadow-lg border-0">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">Bienvenue aux JO !</h3>
            <div class="mb-3">
              <input
                type="text"
                v-model="playerName"
                class="form-control form-control-lg"
                placeholder="Entrez votre pseudo"
              />
            </div>
            <button @click="launchNewQuiz" class="btn btn-danger btn-lg w-100">
              Lancer le Quiz 🚀
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService';

// Liste des liens GIF
const gifs = [
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWd0OGthbDlmaHJxOGt1cGc2Y2E2b2ticmtrenQ0OTc5NDd2aDI3biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/gD3hLJgMLWmVW/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdm96dTk4ZnkwZThyYzludm81NHVybjFjeTB4MXpsZm95bzdyamxsNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dAJTNv2EHxDIk/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXhxejZqNTRwNXdxdHN1cGdyam1uaWp4dWR3dmZrcW5nZ2ViZjhieCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RLm3ZunaMZzMmkk5Ht/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjk2OHpncW82cWc5ZHI2ODFmZDB0eWM0aWY5ZW5zYnZsdGFtejRsYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vwjfBggP3Q5vEdTx9H/giphy-downsized-large.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExem82NGNsY3kwOGVpa2hoenRpb3NvcWFuczlmcGJrc2pkbXl4ZGw2cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ItHnwCKCoAu2PS2wFC/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnFrOWd5ZzVia241cDc3ZmIzZmd0dHBrZ3JrdjhqcGxwajFhdGlrZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7vB7MdHThlWESpkpMk/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTYwdDEwNjF5NTB3OGIxcXFvaW1ucDJ4bXBxeHlxcmpkdHpsMGQwayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ohzgMcA2PxS5ae7T2/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExem9ueDI2ZTVhcmo4emFlNTA4aTluZmx5bWlqaGR2Nmk0YW9wbTR3bSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fadzmZStobRICiFXLU/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcG96b2FhM3hqaDQ5enhzZ2JzeTY5ZXl4Y2h0dGxxNm1jOGNscDFndSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/msZFkfFhLHAZFuokpm/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWQwazNxbzMxZHc2YnVhdm4wMWFxcGdlZml6amp4NnNtaG5oMXFiNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/39uiVjumlJkYqAXil1/giphy-downsized-large.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmw5ZW1lZ3Q2dGxyd2ptMjdrMGM1amFnZWlkcGRzNGw3b2wxYjhsNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/2knEjjTqja0taarfeP/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGd6Y3VrZmkzMTFhMmZweG03cWc2MGJ3Mm00bDFtbnZ6N3dvOHY2ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Vz5zgjOO7khaoAIesM/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3hoYXMwZDh0dWVxbDcxYzZzdzFuajFkcmF1ZzY3bWhuNTZwMmp2byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/U1gkiAV2IbeZJiFT0k/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNW5xeTZxYTA3NHhxYTdkaWp2ZjR6d2hjOTN5MHQyeWVqOGo1d2YwcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XeY0cFOr2IWYGfJpQz/giphy-downsized-large.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXl6NTFvbWt2cXh3ZG43NmwwNmtlNHhlazlraHRzd3NxZ25nbmcxaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RJgjZ7a6lxyCKIwxAD/giphy.gif',
  'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnNkOHg3Y3lucmozdzZpM3ltZGczZGZkdW5meGRlbjNlb3c2ZjNqbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KcWQdNihMEkYMI1EJp/giphy.gif',
];

// Gestion du pseudo
const playerName = ref('');
const router = useRouter();

function launchNewQuiz() {
  if (playerName.value.trim() !== '') {
    participationStorageService.savePlayerName(playerName.value);
    router.push('/questions');
  } else {
    alert('Veuillez saisir un pseudo valide avant de commencer.');
  }
}
</script>

<style scoped>
/* Page container centré verticalement et horizontalement */
.page-container {
  padding-top: 6%;
  height: 98vh;
}

/* Grille divisée en 16 carrés */
.grid-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* Quatre colonnes */
  grid-template-rows: repeat(4, 1fr); /* Quatre lignes */
  height: 100%; /* La hauteur de la grille */
  width: 100%;
}

.grid-item {
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0; /* GIFs invisibles par défaut */
  animation: fadeIn 1s ease-in-out forwards;
}

/* Animation pour les GIFs */
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

/* Carte centrée au-dessus de la grille */
.center-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
}

.card {
  border-radius: 15px;
  color: black;
  padding: 20px;
  max-width: 500px;
  background-color: white;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}

.btn {
  margin-top: 15px;
  transition: transform 0.2s ease-in-out;
}

.btn:hover {
  transform: scale(1.05);
}
</style>

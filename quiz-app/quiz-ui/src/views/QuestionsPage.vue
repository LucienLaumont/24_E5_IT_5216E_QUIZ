<template>
  <div>
    <QuestionsManager />
  </div>
</template>

<script setup>
import QuestionsManager from './QuestionsManager.vue';
import participationStorageService from '@/services/ParticipationStorageService';

// Charger le nom du joueur depuis le localStorage
const playerName = participationStorageService.getPlayerName();
if (!playerName) {
  console.error('Nom du joueur introuvable dans le localStorage.');
}
</script>

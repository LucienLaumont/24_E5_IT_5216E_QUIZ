<template>
  <div class="question-display">
    <h2>{{ currentQuestion.title }}</h2>
    <p>{{ currentQuestion.text }}</p>
    <img
      v-if="currentQuestion.image"
      :src="currentQuestion.image"
      alt="Illustration de la question"
    />

    <ul>
      <li
        v-for="(answer, index) in currentQuestion.possibleAnswers"
        :key="index"
      >
        <button @click="emit('answer-clicked', index)">
          {{ answer.text }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

// Props pour recevoir la question
const props = defineProps({
  currentQuestion: {
    type: Object,
    required: true,
  },
});

// Émettre un événement lorsque l'utilisateur clique sur une réponse
const emit = defineEmits(['answer-clicked']);
</script>

<style scoped>
.question-display {
  text-align: center;
}

.question-display img {
  max-width: 100%;
  height: auto;
  margin: 20px 0;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin: 10px 0;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>

<template>
  <div v-if="currentQuestion" class="quiz-container-wrapper">
    <div class="quiz-container">
      <div class="content-column">
        <div class="question-header">
          <h1 class="question-title">{{ currentQuestion.title }}</h1>
          <p class="question-text">{{ currentQuestion.text }}</p>
        </div>
        <div class="image-container">
          <img :src="currentQuestion.image" alt="Question illustration" />
        </div>
      </div>

      <div class="answers-column">
        <div class="answers-grid">
          <button
            v-for="(answer, index) in currentQuestion.possibleAnswers"
            :key="index"
            class="answer-button"
            @click="$emit('answer-clicked', index)"
          >
            {{ answer.text }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  currentQuestion: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.quiz-container-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90vh;
  width: 100%;
  overflow: hidden;
}

.quiz-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  max-width: 1400px;
  margin: 2rem auto;
  padding: 2rem;
  background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%);
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.5s ease-out;
  height: auto; /* Adjust height dynamically */
  min-height: 600px; /* Minimum height to keep consistent structure */
}

.question-header {
  text-align: center;
  margin-bottom: 2rem;
}

.question-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(120deg, #2b5876 0%, #4e4376 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  max-height: 4rem; /* Limit height */
  overflow: hidden;
  text-overflow: ellipsis;
}

.question-text {
  font-size: 1.25rem;
  line-height: 1.6;
  color: #2d3748;
  max-height: 5rem; /* Limit height for multiline text */
  overflow: hidden;
  text-overflow: ellipsis;
}

.image-container {
  position: relative;
  margin: 2rem 0;
  border-radius: 15px;
  overflow: hidden;
  max-height: 300px; /* Set a maximum height for the image */
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 15px;
  transition: transform 0.3s ease;
}

.image-container img:hover {
  transform: scale(1.02);
}

.content-column {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.answers-column {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
}

.answers-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  width: 100%;
}

.answer-button {
  padding: 1.5rem; /* Adjust padding for uniformity */
  font-size: 1.2rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  color: #000000;
  height: auto; /* Allow height to adjust dynamically */
  min-height: 4rem; /* Ensure buttons have consistent minimum height */
  overflow-wrap: break-word; /* Prevent text from overflowing */
  word-wrap: break-word;
  white-space: normal; /* Allow text wrapping */
}

.answer-button:hover:not(:disabled) {
  transform: translateX(10px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #4299e1;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1024px) {
  .quiz-container {
    grid-template-columns: 1fr;
    max-width: 800px;
  }

  .answer-button:hover:not(:disabled) {
    transform: translateY(-5px);
  }
}
</style>

<script setup lang="ts">
defineProps<{
  score: number;
  totalQuestions: number;
}>();

const calculatePercentage = (score: number, total: number) => {
  return Math.round((score / total) * 100);
};
</script>

<template>
  <div class="score-card">
    <h2 class="score-card-title">Résultat du Quiz JO</h2>

    <div class="olympic-rings">
      <span class="ring blue"></span>
      <span class="ring yellow"></span>
      <span class="ring black"></span>
      <span class="ring green"></span>
      <span class="ring red"></span>
    </div>

    <div class="score-display">
      <div class="score-circle">
        <span class="score">{{ score }}/{{ totalQuestions }}</span>
        <span class="percentage">
          {{ calculatePercentage(score, totalQuestions) }}%
        </span>
      </div>
    </div>

    <div
      class="medal"
      :class="{
        gold: calculatePercentage(score, totalQuestions) >= 80,
        silver:
          calculatePercentage(score, totalQuestions) >= 60 &&
          calculatePercentage(score, totalQuestions) < 80,
        bronze:
          calculatePercentage(score, totalQuestions) >= 40 &&
          calculatePercentage(score, totalQuestions) < 60,
      }"
    >
      <span v-if="calculatePercentage(score, totalQuestions) >= 80"
        >🏅 Médaille d'Or</span
      >
      <span v-else-if="calculatePercentage(score, totalQuestions) >= 60"
        >🏎️ Médaille d'Argent</span
      >
      <span v-else-if="calculatePercentage(score, totalQuestions) >= 40"
        >🏆 Médaille de Bronze</span
      >
      <span v-else>Continuez vos efforts ! 💪</span>
    </div>
  </div>
</template>

<style scoped>
.score-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
  text-align: center;
  max-width: 60vh;
  min-width: 45vh;
  color: #2c3e50;
}

.score-card-title {
  color: black;
  margin-bottom: 20px;
  font-size: 1.8em;
}

.olympic-rings {
  display: flex;
  justify-content: center;
  gap: 5px;
  margin-bottom: 1.5rem;
}

.ring {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 3px solid;
}

.blue {
  border-color: #0085c7;
}
.yellow {
  border-color: #f4c300;
}
.black {
  border-color: #000000;
}
.green {
  border-color: #009f3d;
}
.red {
  border-color: #df0024;
}

.score-display {
  margin: 2rem 0;
}

.score-circle {
  background: linear-gradient(145deg, #ffffff, #f0f0f0);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  box-shadow: inset 0 4px 15px rgba(0, 0, 0, 0.1);
  max-width: 150px;
  min-width: 100px;
  max-height: 150px;
  min-height: 100px;
  border-radius: 50%;
}

.score {
  font-size: 2.5rem;
  font-weight: bold;
  color: #2c3e50;
}

.percentage {
  font-size: 1.2rem;
  color: #666;
}

.medal {
  margin-top: 1.5rem;
  padding: 1rem;
  border-radius: 10px;
  font-weight: bold;
}

.medal.gold {
  background-color: rgba(255, 215, 0, 0.1);
  color: #b5a642;
}

.medal.silver {
  background-color: rgba(192, 192, 192, 0.1);
  color: #808080;
}

.medal.bronze {
  background-color: rgba(205, 127, 50, 0.1);
  color: #cd7f32;
}
</style>

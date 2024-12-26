<script setup lang="ts">
interface Winner {
  playerName: string;
  score: number;
}

defineProps<{
  winners: Winner[];
}>();
</script>

<template>
  <div class="podium-container">
    <!-- Deuxième place -->
    <div class="podium-column silver-column">
      <div class="winner-info silver-winner">
        <div class="medal">🥈</div>
        <div class="winner-name">{{ winners[1].playerName }}</div>
        <div class="winner-score">{{ winners[1].score }} pts</div>
      </div>
      <div class="podium-block silver">2</div>
    </div>

    <!-- Première place -->
    <div class="podium-column gold-column">
      <div class="winner-info gold-winner">
        <div class="crown">👑</div>
        <div class="medal">🥇</div>
        <div class="winner-name">{{ winners[0].playerName }}</div>
        <div class="winner-score">{{ winners[0].score }} pts</div>
      </div>
      <div class="podium-block gold">1</div>
    </div>

    <!-- Troisième place -->
    <div class="podium-column bronze-column">
      <div class="winner-info bronze-winner">
        <div class="medal">🥉</div>
        <div class="winner-name">{{ winners[2].playerName }}</div>
        <div class="winner-score">{{ winners[2].score }} pts</div>
      </div>
      <div class="podium-block bronze">3</div>
    </div>
  </div>
</template>

<style scoped>
.podium-container {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 10px;
  height: 400px;
  margin: 40px 0;
  perspective: 1000px;
}

.podium-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  transform-style: preserve-3d;
  animation: rotateIn 1s ease-out forwards;
}

.winner-info {
  text-align: center;
  margin-bottom: 15px;
  padding: 15px;
  border-radius: 12px;
  background: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transform: translateY(0);
  transition: transform 0.3s ease;
}

.winner-info:hover {
  transform: translateY(-10px);
}

.medal {
  font-size: 2.5em;
  margin-bottom: 10px;
  animation: bounce 1s ease infinite;
}

.crown {
  font-size: 2em;
  margin-bottom: -10px;
  animation: floating 3s ease-in-out infinite;
}

.winner-name {
  font-weight: bold;
  font-size: 1.2em;
  margin: 5px 0;
  color: #2c3e50;
}

.winner-score {
  font-weight: bold;
  color: #666;
}

.podium-block {
  width: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.5em;
  border-radius: 8px 8px 0 0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Hauteurs des podiums */
.gold-column .podium-block {
  height: 200px;
}
.silver-column .podium-block {
  height: 150px;
}
.bronze-column .podium-block {
  height: 100px;
}

/* Styles spécifiques aux médailles */
.gold {
  background: linear-gradient(145deg, #ffd700, #ffa500);
}
.silver {
  background: linear-gradient(145deg, #c0c0c0, #a9a9a9);
}
.bronze {
  background: linear-gradient(145deg, #cd7f32, #a0522d);
}

.gold-winner .winner-info {
  border: 2px solid #ffd700;
}
.silver-winner .winner-info {
  border: 2px solid #c0c0c0;
}
.bronze-winner .winner-info {
  border: 2px solid #cd7f32;
}

/* Animations */
@keyframes rotateIn {
  from {
    transform: rotateX(90deg);
    opacity: 0;
  }
  to {
    transform: rotateX(0);
    opacity: 1;
  }
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

@keyframes floating {
  0%,
  100% {
    transform: translateY(0) rotate(-10deg);
  }
  50% {
    transform: translateY(-8px) rotate(10deg);
  }
}

/* Animation séquentielle pour chaque colonne */
.silver-column {
  animation-delay: 0.2s;
}
.gold-column {
  animation-delay: 0.4s;
}
.bronze-column {
  animation-delay: 0.6s;
}
</style>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';

interface Score {
  playerName: string;
  score: number;
}

interface PodiumProps {
  scores: Score[];
}

const props = defineProps<PodiumProps>();
const showThird = ref(false);
const showSecond = ref(false);
const showFirst = ref(false);

const topThree = computed(() => {
  return [...props.scores].sort((a, b) => b.score - a.score).slice(0, 3);
});

onMounted(() => {
  // Sequence the animations
  setTimeout(() => {
    showThird.value = true;
  }, 500);
  setTimeout(() => {
    showSecond.value = true;
  }, 1000);
  setTimeout(() => {
    showFirst.value = true;
  }, 1500);
});
</script>

<template>
  <div class="podium-container">
    <h2 class="podium-title">🏆 Podium des Champions 🏆</h2>

    <div class="podium">
      <!-- 2ème place -->
      <Transition name="slide-up">
        <div v-if="showSecond && topThree[1]" class="podium-spot silver">
          <div class="player-info">
            <span class="medal">🥈</span>
            <span class="name">{{ topThree[1].playerName }}</span>
            <span class="score">{{ topThree[1].score }} pts</span>
          </div>
          <div class="podium-block">2</div>
        </div>
      </Transition>

      <!-- 1ère place -->
      <Transition name="slide-up">
        <div v-if="showFirst && topThree[0]" class="podium-spot gold">
          <div class="player-info">
            <span class="medal">🥇</span>
            <span class="name">{{ topThree[0].playerName }}</span>
            <span class="score">{{ topThree[0].score }} pts</span>
          </div>
          <div class="podium-block">1</div>
        </div>
      </Transition>

      <!-- 3ème place -->
      <Transition name="slide-up">
        <div v-if="showThird && topThree[2]" class="podium-spot bronze">
          <div class="player-info">
            <span class="medal">🥉</span>
            <span class="name">{{ topThree[2].playerName }}</span>
            <span class="score">{{ topThree[2].score }} pts</span>
          </div>
          <div class="podium-block">3</div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
.podium-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
  text-align: center;
  max-width: 60vh;
  min-width: 45vh;
}

.podium-title {
  color: black;
  margin-bottom: 20px;
  font-size: 1.8em;
}

.podium {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 10px;
  max-height: 250px;
  min-height: 200px;
}

.podium-spot {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 120px;
  min-width: 100px;
}

.player-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 10px;
  min-height: 80px;
}

.medal {
  font-size: 2rem;
  margin-bottom: 5px;
}

.name {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 3px;
  word-break: break-word;
}

.score {
  color: #666;
  font-size: 0.9rem;
}

.podium-block {
  width: 100%;
  background: linear-gradient(145deg, #ffffff, #f0f0f0);
  border-radius: 8px 8px 0 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: bold;
  font-size: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.gold .podium-block {
  background: linear-gradient(145deg, #ffd700, #ffc600);
}

.silver .podium-block {
  background: linear-gradient(145deg, #c0c0c0, #b0b0b0);
}

.bronze .podium-block {
  background: linear-gradient(145deg, #cd7f32, #bd6f22);
}

/* Animation styles */
.slide-up-enter-active {
  transition: all 0.5s ease-out;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-up-enter-to {
  opacity: 1;
  transform: translateY(0);
}
</style>

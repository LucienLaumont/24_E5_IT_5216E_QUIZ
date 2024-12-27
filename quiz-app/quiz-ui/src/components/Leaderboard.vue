<script setup lang="ts">
import { ref, computed } from 'vue';
import Pagination from './Pagination.vue';

interface Score {
  playerName: string;
  score: number;
}

interface LeaderboardData {
  scores: Score[];
  size: number;
}

const props = defineProps<{
  leaderboardData: LeaderboardData;
}>();

const currentPage = ref(1);
const itemsPerPage = 9;

const totalPages = computed(() =>
  Math.ceil(props.leaderboardData.scores.length / itemsPerPage)
);

const paginatedScores = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  const scores = props.leaderboardData.scores.slice(start, end);

  // Ajouter des lignes vides pour maintenir une hauteur constante
  const emptyRows = Array(itemsPerPage - scores.length).fill({
    playerName: '\u00A0',
    score: null,
  });

  return [...scores, ...emptyRows];
});

const handlePageChange = (page: number) => {
  currentPage.value = page;
};
</script>

<template>
  <div class="leaderboard">
    <h2 class="leaderboard-title">Classement 🏆</h2>
    <div class="leaderboard-table">
      <div class="header">
        <div class="rank">Position</div>
        <div class="name">Joueur</div>
        <div class="score">Score</div>
      </div>
      <div
        v-for="(player, index) in paginatedScores"
        :key="index"
        class="row"
        :class="{
          gold: (currentPage - 1) * itemsPerPage + index === 0,
          silver: (currentPage - 1) * itemsPerPage + index === 1,
          bronze: (currentPage - 1) * itemsPerPage + index === 2,
          'empty-row': player.score === null,
        }"
      >
        <div class="rank">
          {{
            player.score !== null
              ? (currentPage - 1) * itemsPerPage + index + 1
              : ''
          }}
        </div>
        <div class="name">{{ player.playerName }}</div>
        <div class="score">
          {{ player.score !== null ? `${player.score} pts` : '' }}
        </div>
      </div>
    </div>

    <Pagination
      :current-page="currentPage"
      :total-pages="totalPages"
      @page-change="handlePageChange"
    />
  </div>
</template>

<style scoped>
.leaderboard {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
  color: black;
}

.leaderboard-title {
  text-align: center;
  color: black;
  margin-bottom: 20px;
  font-size: 1.8em;
}

.leaderboard-table {
  width: 100%;
}

.header {
  display: grid;
  grid-template-columns: 80px 1fr 100px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px 8px 0 0;
  font-weight: bold;
  color: black;
}

.row {
  display: grid;
  grid-template-columns: 80px 1fr 100px;
  padding: 12px;
  border-bottom: 1px solid #eee;
  transition: all 0.3s ease;
  min-height: 48px;
}

.row:not(.empty-row):hover {
  background-color: #f8f9fa;
  transform: scale(1.01);
}

.empty-row {
  background: transparent;
  border-bottom: 1px solid #f5f5f5;
}

.rank {
  text-align: center;
  font-weight: bold;
}

.name {
  text-align: left;
}

.score {
  text-align: right;
  font-weight: bold;
}

.gold {
  background: linear-gradient(
    145deg,
    rgba(255, 215, 0, 0.15),
    rgba(255, 215, 0, 0.05)
  );
  border-left: 4px solid gold;
}

.gold:hover {
  background: linear-gradient(
    145deg,
    rgba(255, 215, 0, 0.25),
    rgba(255, 215, 0, 0.15)
  );
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

.silver {
  background: linear-gradient(
    145deg,
    rgba(192, 192, 192, 0.15),
    rgba(192, 192, 192, 0.05)
  );
  border-left: 4px solid silver;
}

.silver:hover {
  background: linear-gradient(
    145deg,
    rgba(192, 192, 192, 0.25),
    rgba(192, 192, 192, 0.15)
  );
  box-shadow: 0 2px 8px rgba(192, 192, 192, 0.3);
}

.bronze {
  background: linear-gradient(
    145deg,
    rgba(205, 127, 50, 0.15),
    rgba(205, 127, 50, 0.05)
  );
  border-left: 4px solid #cd7f32;
}

.bronze:hover {
  background: linear-gradient(
    145deg,
    rgba(205, 127, 50, 0.25),
    rgba(205, 127, 50, 0.15)
  );
  box-shadow: 0 2px 8px rgba(205, 127, 50, 0.3);
}
</style>

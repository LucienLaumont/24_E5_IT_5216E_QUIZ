<template>
  <div class="leaderboard">
    <div class="flex items-center gap-3 mb-6">
      <h2 class="text-xl font-bold text-gray-800">Classement</h2>
    </div>
    <div class="space-y-4">
      <div
        v-for="player in players"
        :key="player.rank"
        class="flex items-center gap-4 p-3 rounded-lg transition-all hover:bg-gray-50"
      >
        <div
          :class="[
            'w-10 h-10 rounded-full flex items-center justify-center text-white font-bold',
            getRankColor(player.rank),
          ]"
        >
          {{ player.rank }}
        </div>
        <div
          class="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center font-semibold text-gray-600"
        >
          {{ player.avatar }}
        </div>
        <div class="flex-grow">
          <div class="font-semibold text-gray-800">{{ player.name }}</div>
          <div class="text-sm text-gray-500">{{ player.score }} pts</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  players: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const getRankColor = (rank: number) => {
  switch (rank) {
    case 1:
      return 'bg-gradient-to-r from-olympic-gold to-yellow-500';
    case 2:
      return 'bg-gradient-to-r from-olympic-silver to-gray-400';
    case 3:
      return 'bg-gradient-to-r from-olympic-bronze to-orange-700';
    default:
      return 'bg-gray-100';
  }
};
</script>

<style scoped>
.leaderboard {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

h2 {
  text-align: center;
}
</style>

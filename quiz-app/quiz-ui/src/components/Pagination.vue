<script setup lang="ts">
defineProps<{
  currentPage: number;
  totalPages: number;
}>();

const emit = defineEmits<{
  (e: 'pageChange', page: number): void;
}>();
</script>

<template>
  <div class="pagination">
    <button
      class="pagination-button"
      :disabled="currentPage === 1"
      @click="emit('pageChange', currentPage - 1)"
    >
      ←
    </button>

    <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>

    <button
      class="pagination-button"
      :disabled="currentPage === totalPages"
      @click="emit('pageChange', currentPage + 1)"
    >
      →
    </button>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 20px;
}

.pagination-button {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 16px;
  color: #2c3e50;
  font-size: 1.1em;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-button:hover:not(:disabled) {
  background: #f8f9fa;
  border-color: #cbd5e0;
  transform: translateY(-1px);
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 1.1em;
  color: #2c3e50;
  font-weight: 500;
}
</style>

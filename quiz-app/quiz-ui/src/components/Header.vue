<script setup lang="ts">
import { useRouter } from 'vue-router';

const routes = [
  { name: 'Accueil', path: '/', class: 'gold' },
  { name: 'Classement', path: '/results', class: 'silver' },
  { name: 'Admin', path: '/admin', class: 'bronze' },
];

const router = useRouter();

const navigate = (path: string) => {
  router.push(path);
};
</script>

<template>
  <header class="header">
    <div class="logo-container">
      <img src="@/assets/olympic-rings.svg" alt="Logo JO" class="logo" />
    </div>
    <nav class="nav-buttons">
      <button
        v-for="route in routes"
        :key="route.name"
        :class="['nav-button', route.class]"
        @click="() => navigate(route.path)"
      >
        {{ route.name }}
      </button>
    </nav>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  height: 40px;
  width: auto;
}

.nav-buttons {
  display: flex;
  gap: 1rem;
}

.nav-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  color: #fff;
}

.nav-button::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 45%,
    rgba(255, 255, 255, 0.8) 50%,
    transparent 55%
  );
  opacity: 0;
  transition: opacity 0.3s;
}

.nav-button:hover::after {
  opacity: 1;
  animation: sparkle 1s linear infinite;
}

@keyframes sparkle {
  0% {
    background-position: -100% 100%;
  }
  100% {
    background-position: 100% -100%;
  }
}

.gold {
  background: linear-gradient(45deg, #ffd700, #fdb931);
}

.silver {
  background: linear-gradient(45deg, #c0c0c0, #e8e8e8);
}

.bronze {
  background: linear-gradient(45deg, #cd7f32, #be6e3f);
}

.gold:hover {
  box-shadow: 0 0 15px #ffd700;
}

.silver:hover {
  box-shadow: 0 0 15px #c0c0c0;
}

.bronze:hover {
  box-shadow: 0 0 15px #cd7f32;
}
</style>

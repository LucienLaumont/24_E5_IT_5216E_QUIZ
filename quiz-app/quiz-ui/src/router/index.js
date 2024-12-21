import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import NewQuizPage from '../views/NewQuizPage.vue';
import QuestionsPage from '../views/QuestionsPage.vue';
import ResultsPage from '../views/ResultsPage.vue';

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/new-quiz',
    name: 'NewQuizPage',
    component: NewQuizPage,
  },
  {
    path: '/questions',
    name: 'QuestionsPage',
    component: QuestionsPage,
  },
  {
    path: '/results',
    name: 'ResultsPage',
    component: ResultsPage,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;

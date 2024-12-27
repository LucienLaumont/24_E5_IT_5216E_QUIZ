import axios from 'axios';

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true,
});

export default {
  async call(method, resource, data = null, token = null) {
    const headers = {
      'Content-Type': 'application/json',
    };
    if (token) headers.authorization = `Bearer ${token}`;

    return instance({
      method,
      headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(
          `Erreur lors de l'appel API : ${method} ${resource}`,
          error
        );
        return null; // Vous pouvez également propager l'erreur ou gérer autrement
      });
  },

  // Méthode pour récupérer les informations générales du quiz
  getQuizInfo() {
    return this.call('get', 'quiz-info');
  },

  // Méthode pour récupérer une question par sa position
  async getQuestion(position) {
    return this.call('get', `questions?position=${position}`);
  },

  async getParticipation(participationId) {
    return this.call('get', `/participations/${participationId}`);
  },
};

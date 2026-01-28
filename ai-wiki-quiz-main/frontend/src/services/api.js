const API_BASE_URL = 'http://localhost:8000';

/**
 * Generate a quiz from a Wikipedia URL
 * @param {string} url - Wikipedia article URL
 * @returns {Promise<Object>} Quiz data
 */
export const generateQuiz = async (url) => {
  try {
    const response = await fetch(`${API_BASE_URL}/generate_quiz`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      let errorMessage = 'Failed to generate quiz';
      try {
        const error = await response.json();
        errorMessage = error.detail || error.message || errorMessage;
      } catch (e) {
        errorMessage = `Server error: ${response.status} ${response.statusText}`;
      }
      throw new Error(errorMessage);
    }

    return response.json();
  } catch (error) {
    // Handle network errors
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Cannot connect to server. Make sure the backend is running on http://localhost:8000');
    }
    throw error;
  }
};

/**
 * Get history of all generated quizzes
 * @returns {Promise<Array>} List of quiz history items
 */
export const getHistory = async () => {
  const response = await fetch(`${API_BASE_URL}/history`);

  if (!response.ok) {
    throw new Error('Failed to fetch history');
  }

  return response.json();
};

/**
 * Get a specific quiz by ID
 * @param {number} quizId - Quiz ID
 * @returns {Promise<Object>} Quiz data
 */
export const getQuiz = async (quizId) => {
  const response = await fetch(`${API_BASE_URL}/quiz/${quizId}`);

  if (!response.ok) {
    throw new Error('Failed to fetch quiz');
  }

  return response.json();
};


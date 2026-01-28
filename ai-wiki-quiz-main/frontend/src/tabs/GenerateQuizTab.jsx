import { useState } from 'react';
import { generateQuiz } from '../services/api';
import QuizDisplay from '../components/QuizDisplay';

const GenerateQuizTab = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quizData, setQuizData] = useState(null);

  const validateUrl = (url) => {
    try {
      const urlObj = new URL(url);
      return urlObj.hostname === 'en.wikipedia.org' && urlObj.pathname.startsWith('/wiki/');
    } catch {
      return false;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setQuizData(null);

    if (!url.trim()) {
      setError('Please enter a Wikipedia URL');
      return;
    }

    if (!validateUrl(url)) {
      setError('Please enter a valid Wikipedia URL (e.g., https://en.wikipedia.org/wiki/Alan_Turing)');
      return;
    }

    setLoading(true);
    try {
      console.log('Generating quiz for URL:', url);
      const data = await generateQuiz(url);
      console.log('Quiz generated successfully:', data);
      setQuizData(data);
      setUrl(''); // Clear input after successful generation
    } catch (err) {
      console.error('Error generating quiz:', err);
      setError(err.message || 'Failed to generate quiz. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-white-900 mb-2">Generate Quiz</h2>
        <p className="text-gray-600">
          Enter a Wikipedia article URL to generate an AI-powered quiz
        </p>
      </div>

      <form onSubmit={handleSubmit} className="mb-8">
        <div className="flex gap-4">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://en.wikipedia.org/wiki/Alan_Turing"
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Generating...' : 'Generate Quiz'}
          </button>
        </div>
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}
      </form>

      {loading && (
        <div className="flex flex-col items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600">Scraping article and generating quiz...</p>
          <p className="text-sm text-gray-500 mt-2">This may take a few moments</p>
        </div>
      )}

      {quizData && !loading && (
        <div className="mt-8">
          <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
            <h3 className="font-semibold text-green-900">
              Quiz Generated Successfully!
            </h3>
            <p className="text-sm text-green-700 mt-1">
              Article: <span className="font-medium">{quizData.title}</span>
            </p>
          </div>
          <QuizDisplay quizData={quizData} showAnswers={true} />
        </div>
      )}
    </div>
  );
};

export default GenerateQuizTab;


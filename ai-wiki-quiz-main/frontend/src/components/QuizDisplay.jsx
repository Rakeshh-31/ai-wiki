const QuizDisplay = ({ quizData, showAnswers = true }) => {
  if (!quizData) {
    return <div className="text-center text-gray-500">No quiz data available</div>;
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'easy':
        return 'bg-green-100 text-green-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'hard':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Summary Section */}
      {quizData.summary && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-900 mb-2">Article Summary</h3>
          <p className="text-blue-800">{quizData.summary}</p>
        </div>
      )}

      {/* Key Entities */}
      {quizData.key_entities && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <h3 className="font-semibold text-gray-900 mb-3">Key Entities</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {quizData.key_entities.people?.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-1">People</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  {quizData.key_entities.people.map((person, idx) => (
                    <li key={idx}>• {person}</li>
                  ))}
                </ul>
              </div>
            )}
            {quizData.key_entities.organizations?.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-1">Organizations</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  {quizData.key_entities.organizations.map((org, idx) => (
                    <li key={idx}>• {org}</li>
                  ))}
                </ul>
              </div>
            )}
            {quizData.key_entities.locations?.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-1">Locations</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  {quizData.key_entities.locations.map((location, idx) => (
                    <li key={idx}>• {location}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Sections */}
      {quizData.sections && quizData.sections.length > 0 && (
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <h3 className="font-semibold text-purple-900 mb-2">Main Sections</h3>
          <div className="flex flex-wrap gap-2">
            {quizData.sections.map((section, idx) => (
              <span
                key={idx}
                className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm"
              >
                {section}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Quiz Questions */}
      {quizData.quiz && quizData.quiz.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Quiz Questions</h3>
          {quizData.quiz.map((question, idx) => (
            <div
              key={idx}
              className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-3">
                <h4 className="text-lg font-semibold text-gray-900 flex-1">
                  {idx + 1}. {question.question}
                </h4>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-medium ${getDifficultyColor(
                    question.difficulty
                  )}`}
                >
                  {question.difficulty || 'N/A'}
                </span>
              </div>

              <div className="space-y-2 mb-4">
                {question.options?.map((option, optIdx) => {
                  const isCorrect = option === question.answer;
                  const optionLabel = String.fromCharCode(65 + optIdx); // A, B, C, D

                  return (
                    <div
                      key={optIdx}
                      className={`p-3 rounded border ${
                        showAnswers && isCorrect
                          ? 'bg-green-50 border-green-300 font-semibold'
                          : 'bg-gray-50 border-gray-200'
                      }`}
                    >
                      <span className="font-medium mr-2">{optionLabel}.</span>
                      {option}
                      {showAnswers && isCorrect && (
                        <span className="ml-2 text-green-600">✓ Correct</span>
                      )}
                    </div>
                  );
                })}
              </div>

              {showAnswers && question.explanation && (
                <div className="bg-blue-50 border-l-4 border-blue-400 p-3 rounded">
                  <p className="text-sm text-blue-900">
                    <span className="font-semibold">Explanation:</span> {question.explanation}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Related Topics */}
      {quizData.related_topics && quizData.related_topics.length > 0 && (
        <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4 mt-6">
          <h3 className="font-semibold text-indigo-900 mb-3">Related Topics</h3>
          <div className="flex flex-wrap gap-2">
            {quizData.related_topics.map((topic, idx) => (
              <span
                key={idx}
                className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm"
              >
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default QuizDisplay;


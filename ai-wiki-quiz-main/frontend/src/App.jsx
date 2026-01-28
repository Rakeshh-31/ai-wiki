import { useState } from 'react';
import GenerateQuizTab from './tabs/GenerateQuizTab';
import HistoryTab from './tabs/HistoryTab';

function App() {
  const [activeTab, setActiveTab] = useState('generate');

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-gray-100">
      
      {/* Header */}
      <header className="bg-gradient-to-r from-red-900 to-black border-b border-red-800">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <h1 className="text-3xl font-extrabold tracking-wide text-white">
            AI Wiki Quiz Generator
          </h1>
          <p className="text-sm text-red-200 mt-2 max-w-2xl">
            Instantly convert Wikipedia articles into intelligent quizzes using AI
          </p>
        </div>
      </header>

      {/* Tabs */}
      <div className="bg-black/80 backdrop-blur border-b border-red-800">
        <div className="max-w-7xl mx-auto px-6">
          <nav className="flex gap-10">
            <button
              onClick={() => setActiveTab('generate')}
              className={`py-4 text-sm font-semibold tracking-wide transition ${
                activeTab === 'generate'
                  ? 'text-red-500 border-b-2 border-red-600'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Generate Quiz
            </button>

            <button
              onClick={() => setActiveTab('history')}
              className={`py-4 text-sm font-semibold tracking-wide transition ${
                activeTab === 'history'
                  ? 'text-red-500 border-b-2 border-red-600'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Quiz History
            </button>
          </nav>
        </div>
      </div>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-6 py-10">
        <div className="bg-black/60 rounded-2xl shadow-lg border border-red-900/40 p-6">
          {activeTab === 'generate' && <GenerateQuizTab />}
          {activeTab === 'history' && <HistoryTab />}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-red-900 bg-black/90">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <p className="text-center text-xs text-gray-400 tracking-wide">
            © 2026 AI Wiki Quiz Generator • Built using FastAPI, React & Gemini AI
          </p>
        </div>
      </footer>

    </div>
  );
}

export default App;

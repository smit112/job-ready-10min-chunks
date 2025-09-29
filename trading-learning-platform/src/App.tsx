import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useStore } from './hooks/useStore';
import Layout from './components/shared/Layout';
import HomePage from './components/shared/HomePage';
import ModulePage from './components/lessons/ModulePage';
import LessonPage from './components/lessons/LessonPage';
import QuizPage from './components/quizzes/QuizPage';
import Dashboard from './components/shared/Dashboard';
import InteractiveTools from './components/interactive/InteractiveTools';
import Achievements from './components/shared/Achievements';

function App() {
  const { toggleDarkMode, isDarkMode } = useStore();

  useEffect(() => {
    // Apply dark mode class on mount
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  return (
    <Router>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/module/:moduleId" element={<ModulePage />} />
            <Route path="/lesson/:lessonId" element={<LessonPage />} />
            <Route path="/quiz/:quizId" element={<QuizPage />} />
            <Route path="/tools" element={<InteractiveTools />} />
            <Route path="/achievements" element={<Achievements />} />
          </Routes>
        </Layout>
      </div>
    </Router>
  );
}

export default App;

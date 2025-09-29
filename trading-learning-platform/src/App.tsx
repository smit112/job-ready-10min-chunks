import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAppStore } from './stores/appStore';
import Navigation from './components/shared/SimpleNavigation';
import Dashboard from './components/shared/Dashboard';
import LessonView from './components/lessons/LessonView';
import ModuleView from './components/lessons/ModuleView';
import InteractiveTool from './components/interactive/InteractiveTool';
import QuizView from './components/quizzes/QuizView';
import ProgressView from './components/shared/ProgressView';
import './App.css';

function App() {
  const { theme } = useAppStore();

  return (
    <div style={{ minHeight: '100vh', transition: 'colors 0.3s' }}>
      <Router>
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Navigation />
          
          <main style={{ flex: 1, marginLeft: '256px' }}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              style={{ padding: '1.5rem' }}
            >
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/module/:moduleId" element={<ModuleView />} />
                <Route path="/lesson/:lessonId" element={<LessonView />} />
                <Route path="/quiz/:quizId" element={<QuizView />} />
                <Route path="/tool/:toolId" element={<InteractiveTool />} />
                <Route path="/progress" element={<ProgressView />} />
              </Routes>
            </motion.div>
          </main>
        </div>
      </Router>
    </div>
  );
}

export default App;

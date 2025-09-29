import React from 'react';
import { motion } from 'framer-motion';
import { useParams } from 'react-router-dom';

const QuizPage: React.FC = () => {
  const { quizId } = useParams<{ quizId: string }>();

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center py-12"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Quiz: {quizId}
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Quiz functionality coming soon!
        </p>
      </motion.div>
    </div>
  );
};

export default QuizPage;
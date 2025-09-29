import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, XCircle, ArrowRight, RotateCcw, Trophy } from 'lucide-react';
import { QuizQuestion } from '../../types';

interface QuizComponentProps {
  questions: QuizQuestion[];
  onComplete: (score: number) => void;
}

const QuizComponent: React.FC<QuizComponentProps> = ({ questions, onComplete }) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [isCompleted, setIsCompleted] = useState(false);
  const [score, setScore] = useState(0);

  const currentQuestion = questions[currentQuestionIndex];
  const isLastQuestion = currentQuestionIndex === questions.length - 1;

  const handleAnswerSelect = (answer: string) => {
    setSelectedAnswer(answer);
  };

  const handleSubmitAnswer = () => {
    if (!selectedAnswer) return;

    const newAnswers = { ...answers, [currentQuestionIndex]: selectedAnswer };
    setAnswers(newAnswers);
    setShowResult(true);

    // Check if answer is correct
    const isCorrect = selectedAnswer === currentQuestion.correctAnswer;
    if (isCorrect) {
      setScore(prev => prev + 1);
    }
  };

  const handleNext = () => {
    if (isLastQuestion) {
      // Quiz completed
      const finalScore = Math.round((score / questions.length) * 100);
      setIsCompleted(true);
      onComplete(finalScore);
    } else {
      setCurrentQuestionIndex(prev => prev + 1);
      setSelectedAnswer(null);
      setShowResult(false);
    }
  };

  const handleRestart = () => {
    setCurrentQuestionIndex(0);
    setSelectedAnswer(null);
    setShowResult(false);
    setAnswers({});
    setIsCompleted(false);
    setScore(0);
  };

  if (isCompleted) {
    const percentage = Math.round((score / questions.length) * 100);
    const isPassing = percentage >= 70;

    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center py-12"
      >
        <div className="mb-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="w-24 h-24 mx-auto mb-6 rounded-full flex items-center justify-center"
            style={{ backgroundColor: isPassing ? '#10B981' : '#EF4444' }}
          >
            <Trophy size={48} className="text-white" />
          </motion.div>
          
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Quiz Complete!
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            You scored {score} out of {questions.length} questions
          </p>
          
          <div className="text-4xl font-bold mb-4" style={{ color: isPassing ? '#10B981' : '#EF4444' }}>
            {percentage}%
          </div>
          
          <div className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium ${
            isPassing 
              ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
              : 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
          }`}>
            {isPassing ? 'Great job!' : 'Keep studying!'}
          </div>
        </div>

        <div className="flex justify-center space-x-4">
          <button
            onClick={handleRestart}
            className="btn-secondary flex items-center space-x-2"
          >
            <RotateCcw size={16} />
            <span>Retake Quiz</span>
          </button>
        </div>
      </motion.div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Progress */}
      <div className="mb-8">
        <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
          <span>Question {currentQuestionIndex + 1} of {questions.length}</span>
          <span>{Math.round(((currentQuestionIndex + 1) / questions.length) * 100)}% Complete</span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
          />
        </div>
      </div>

      {/* Question */}
      <motion.div
        key={currentQuestionIndex}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        className="card mb-6"
      >
        <div className="mb-4">
          <div className="flex items-center space-x-2 mb-2">
            <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
              {currentQuestion.difficulty.toUpperCase()}
            </span>
            <span className="text-sm text-gray-500 dark:text-gray-500">
              • {currentQuestion.xpReward} XP
            </span>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
            {currentQuestion.question}
          </h3>
        </div>

        <div className="space-y-3">
          {currentQuestion.options?.map((option, index) => (
            <motion.button
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => !showResult && handleAnswerSelect(option)}
              disabled={showResult}
              className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                showResult
                  ? option === currentQuestion.correctAnswer
                    ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                    : selectedAnswer === option
                    ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                    : 'border-gray-200 dark:border-gray-700'
                  : selectedAnswer === option
                  ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                  : 'border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-600'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-gray-900 dark:text-white">{option}</span>
                {showResult && (
                  <div>
                    {option === currentQuestion.correctAnswer ? (
                      <CheckCircle size={20} className="text-green-500" />
                    ) : selectedAnswer === option ? (
                      <XCircle size={20} className="text-red-500" />
                    ) : null}
                  </div>
                )}
              </div>
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* Result and Explanation */}
      <AnimatePresence>
        {showResult && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="card mb-6"
          >
            <div className="flex items-start space-x-3">
              {selectedAnswer === currentQuestion.correctAnswer ? (
                <CheckCircle size={24} className="text-green-500 mt-1" />
              ) : (
                <XCircle size={24} className="text-red-500 mt-1" />
              )}
              <div className="flex-1">
                <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                  {selectedAnswer === currentQuestion.correctAnswer ? 'Correct!' : 'Incorrect'}
                </h4>
                <p className="text-gray-700 dark:text-gray-300">
                  {currentQuestion.explanation}
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Navigation */}
      <div className="flex justify-between">
        <div></div>
        <div className="flex space-x-4">
          {!showResult ? (
            <button
              onClick={handleSubmitAnswer}
              disabled={!selectedAnswer}
              className={`btn-primary flex items-center space-x-2 ${
                !selectedAnswer ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              <span>Submit Answer</span>
            </button>
          ) : (
            <button
              onClick={handleNext}
              className="btn-primary flex items-center space-x-2"
            >
              <span>{isLastQuestion ? 'Finish Quiz' : 'Next Question'}</span>
              <ArrowRight size={16} />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuizComponent;
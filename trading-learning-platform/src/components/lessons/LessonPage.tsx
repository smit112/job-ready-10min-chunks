import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  ArrowRight, 
  CheckCircle, 
  Clock, 
  Star,
  Lightbulb,
  Calculator,
  BookOpen,
  Play,
  Trophy
} from 'lucide-react';
import { useStore, useProgress } from '../../hooks/useStore';
import { tradingFundamentalsLessons } from '../../data/lessons/trading-fundamentals';
import { optionsBasicsLessons } from '../../data/lessons/options-basics';
import { swingTradingBasicsLessons } from '../../data/lessons/swing-trading-basics';
import { Lesson } from '../../types';

const LessonPage: React.FC = () => {
  const { lessonId } = useParams<{ lessonId: string }>();
  const navigate = useNavigate();
  const { completeLesson, addNotification } = useStore();
  const progress = useProgress();
  const [currentContentIndex, setCurrentContentIndex] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);

  // Combine all lessons
  const allLessons = [...tradingFundamentalsLessons, ...optionsBasicsLessons, ...swingTradingBasicsLessons];
  const lesson = allLessons.find(l => l.id === lessonId);

  useEffect(() => {
    if (lesson) {
      setIsCompleted(progress.completedLessons.includes(lesson.id));
    }
  }, [lesson, progress.completedLessons]);

  if (!lesson) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Lesson not found
        </h1>
        <Link
          to="/"
          className="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300"
        >
          Return to home
        </Link>
      </div>
    );
  }

  const currentContent = lesson.content[currentContentIndex];
  const isLastContent = currentContentIndex === lesson.content.length - 1;

  const handleNext = () => {
    if (isLastContent) {
      // Complete lesson
      if (!isCompleted) {
        completeLesson(lesson.id);
        addNotification({
          type: 'success',
          title: 'Lesson Completed! 🎉',
          message: `You earned ${lesson.xpReward} XP for completing "${lesson.title}"`,
        });
        setIsCompleted(true);
      }
    } else {
      setCurrentContentIndex(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentContentIndex > 0) {
      setCurrentContentIndex(prev => prev - 1);
    }
  };

  const renderContent = (content: any) => {
    switch (content.type) {
      case 'explanation':
        return (
          <div className="space-y-4">
            {content.title && (
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                {content.title}
              </h3>
            )}
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              {content.text}
            </p>
          </div>
        );

      case 'analogy':
        return (
          <div className="bg-warning-50 dark:bg-warning-900/20 rounded-xl p-6 border-l-4 border-warning-500">
            <div className="flex items-start space-x-3">
              <Lightbulb className="w-6 h-6 text-warning-600 dark:text-warning-400 mt-1 flex-shrink-0" />
              <div>
                <h3 className="text-lg font-semibold text-warning-800 dark:text-warning-200 mb-2">
                  {content.title || 'Think of it like this...'}
                </h3>
                <p className="text-warning-700 dark:text-warning-300 leading-relaxed">
                  {content.analogy}
                </p>
              </div>
            </div>
          </div>
        );

      case 'example':
        return (
          <div className="bg-primary-50 dark:bg-primary-900/20 rounded-xl p-6 border-l-4 border-primary-500">
            <div className="flex items-start space-x-3">
              <BookOpen className="w-6 h-6 text-primary-600 dark:text-primary-400 mt-1 flex-shrink-0" />
              <div>
                <h3 className="text-lg font-semibold text-primary-800 dark:text-primary-200 mb-2">
                  {content.title || 'Real Example'}
                </h3>
                <p className="text-primary-700 dark:text-primary-300 leading-relaxed">
                  {content.text}
                </p>
              </div>
            </div>
          </div>
        );

      case 'interactive':
        return (
          <div className="bg-success-50 dark:bg-success-900/20 rounded-xl p-6 border-l-4 border-success-500">
            <div className="flex items-start space-x-3">
              <Calculator className="w-6 h-6 text-success-600 dark:text-success-400 mt-1 flex-shrink-0" />
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-success-800 dark:text-success-200 mb-2">
                  Interactive Tool
                </h3>
                <p className="text-success-700 dark:text-success-300 mb-4">
                  Try out this interactive tool to better understand the concept.
                </p>
                <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-success-200 dark:border-success-700">
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Interactive component: {content.component}
                  </p>
                  {content.params && (
                    <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                      Parameters: {JSON.stringify(content.params)}
                    </p>
                  )}
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return (
          <div className="bg-gray-50 dark:bg-gray-800 rounded-xl p-6">
            <p className="text-gray-700 dark:text-gray-300">
              {content.text || 'Content not available'}
            </p>
          </div>
        );
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="mb-8"
      >
        <div className="flex items-center space-x-4 mb-6">
          <button
            onClick={() => navigate(-1)}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <ArrowLeft className="w-5 h-5 text-gray-600 dark:text-gray-300" />
          </button>
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              {lesson.title}
            </h1>
            <p className="text-gray-600 dark:text-gray-300 mt-2">
              {lesson.description}
            </p>
          </div>
        </div>

        {/* Lesson Info */}
        <div className="flex items-center space-x-6 text-sm text-gray-600 dark:text-gray-400">
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4" />
            <span>{lesson.estimatedTime} minutes</span>
          </div>
          <div className="flex items-center space-x-2">
            <Star className="w-4 h-4" />
            <span>{lesson.xpReward} XP</span>
          </div>
          <div className="flex items-center space-x-2">
            <Trophy className="w-4 h-4" />
            <span className="capitalize">{lesson.difficulty}</span>
          </div>
        </div>
      </motion.div>

      {/* Progress Bar */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="mb-8"
      >
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Progress
          </span>
          <span className="text-sm font-bold text-gray-900 dark:text-white">
            {currentContentIndex + 1}/{lesson.content.length}
          </span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <motion.div
            className="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${((currentContentIndex + 1) / lesson.content.length) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </motion.div>

      {/* Content */}
      <motion.div
        key={currentContentIndex}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg mb-8"
      >
        {renderContent(currentContent)}
      </motion.div>

      {/* Navigation */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="flex items-center justify-between"
      >
        <button
          onClick={handlePrevious}
          disabled={currentContentIndex === 0}
          className={`flex items-center px-6 py-3 rounded-lg font-medium transition-colors ${
            currentContentIndex === 0
              ? 'text-gray-400 dark:text-gray-600 cursor-not-allowed'
              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
          }`}
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Previous
        </button>

        <div className="flex items-center space-x-2">
          {lesson.content.map((_, index) => (
            <div
              key={index}
              className={`w-2 h-2 rounded-full ${
                index <= currentContentIndex
                  ? 'bg-primary-500'
                  : 'bg-gray-300 dark:bg-gray-600'
              }`}
            />
          ))}
        </div>

        <button
          onClick={handleNext}
          className={`flex items-center px-6 py-3 rounded-lg font-medium transition-colors ${
            isCompleted
              ? 'bg-success-600 hover:bg-success-700 text-white'
              : 'bg-primary-600 hover:bg-primary-700 text-white'
          }`}
        >
          {isLastContent ? (
            isCompleted ? (
              <>
                <CheckCircle className="w-4 h-4 mr-2" />
                Completed
              </>
            ) : (
              <>
                <CheckCircle className="w-4 h-4 mr-2" />
                Complete Lesson
              </>
            )
          ) : (
            <>
              Next
              <ArrowRight className="w-4 h-4 ml-2" />
            </>
          )}
        </button>
      </motion.div>
    </div>
  );
};

export default LessonPage;
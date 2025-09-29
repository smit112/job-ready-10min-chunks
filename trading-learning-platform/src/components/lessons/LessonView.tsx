import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, 
  ArrowRight, 
  CheckCircle, 
  Clock, 
  Star,
  BookOpen,
  Play,
  Pause,
  RotateCcw
} from 'lucide-react';
import { useAppStore } from '../../stores/appStore';
import { tradingFundamentalsLessons } from '../../data/lessons/tradingFundamentals';
import { optionsTradingLessons } from '../../data/lessons/optionsTrading';
import InteractiveComponent from '../interactive/InteractiveComponent';
import QuizComponent from '../quizzes/QuizComponent';

const LessonView: React.FC = () => {
  const { lessonId } = useParams<{ lessonId: string }>();
  const navigate = useNavigate();
  const { completeLesson, progress } = useAppStore();
  const [currentContentIndex, setCurrentContentIndex] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  const [startTime, setStartTime] = useState<Date>(new Date());

  // Find the lesson
  const allLessons = [...tradingFundamentalsLessons, ...optionsTradingLessons];
  const lesson = allLessons.find(l => l.id === lessonId);

  useEffect(() => {
    if (lesson) {
      setStartTime(new Date());
      setIsCompleted(progress.completedLessons.includes(lesson.id));
    }
  }, [lesson, progress.completedLessons]);

  if (!lesson) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Lesson Not Found
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          The lesson you're looking for doesn't exist.
        </p>
        <button
          onClick={() => navigate('/')}
          className="btn-primary"
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  const currentContent = lesson.content[currentContentIndex];
  const isLastContent = currentContentIndex === lesson.content.length - 1;
  const isFirstContent = currentContentIndex === 0;

  const handleNext = () => {
    if (isLastContent) {
      // Complete the lesson
      if (!isCompleted) {
        completeLesson(lesson.id);
        setIsCompleted(true);
      }
    } else {
      setCurrentContentIndex(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (!isFirstContent) {
      setCurrentContentIndex(prev => prev - 1);
    }
  };

  const handleRestart = () => {
    setCurrentContentIndex(0);
    setIsCompleted(false);
    setStartTime(new Date());
  };

  const getContentComponent = () => {
    switch (currentContent.type) {
      case 'explanation':
        return (
          <div className="space-y-6">
            {currentContent.title && (
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                {currentContent.title}
              </h2>
            )}
            <div className="prose prose-lg max-w-none">
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                {currentContent.text}
              </p>
            </div>
            {currentContent.analogy && (
              <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
                <div className="flex items-start space-x-3">
                  <div className="text-2xl">💡</div>
                  <div>
                    <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
                      Simple Analogy
                    </h3>
                    <p className="text-blue-800 dark:text-blue-200">
                      {currentContent.analogy}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        );

      case 'interactive':
        return (
          <div className="space-y-6">
            {currentContent.title && (
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                {currentContent.title}
              </h2>
            )}
            <InteractiveComponent 
              component={currentContent.component || ''} 
              params={currentContent.params || {}} 
            />
          </div>
        );

      case 'quiz':
        return (
          <div className="space-y-6">
            {currentContent.title && (
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                {currentContent.title}
              </h2>
            )}
            <QuizComponent 
              questions={currentContent.questions || []}
              onComplete={(score) => {
                completeLesson(lesson.id, score);
                setIsCompleted(true);
              }}
            />
          </div>
        );

      case 'example':
        return (
          <div className="space-y-6">
            {currentContent.title && (
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                {currentContent.title}
              </h2>
            )}
            <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6">
              <div className="flex items-start space-x-3">
                <div className="text-2xl">📝</div>
                <div>
                  <h3 className="font-semibold text-green-900 dark:text-green-100 mb-2">
                    Real Example
                  </h3>
                  <p className="text-green-800 dark:text-green-200">
                    {currentContent.text}
                  </p>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return (
          <div className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">
              Content type not supported yet.
            </p>
          </div>
        );
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate(`/module/${lesson.module.id}`)}
          className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors mb-4"
        >
          <ArrowLeft size={20} />
          <span>Back to {lesson.module.title}</span>
        </button>

        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              {lesson.title}
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              {lesson.description}
            </p>
          </div>
          {isCompleted && (
            <div className="flex items-center space-x-2 text-green-600 dark:text-green-400">
              <CheckCircle size={24} />
              <span className="font-medium">Completed</span>
            </div>
          )}
        </div>

        {/* Progress bar */}
        <div className="flex items-center space-x-4 mb-6">
          <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div 
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentContentIndex + 1) / lesson.content.length) * 100}%` }}
            />
          </div>
          <span className="text-sm text-gray-600 dark:text-gray-400">
            {currentContentIndex + 1} of {lesson.content.length}
          </span>
        </div>

        {/* Lesson info */}
        <div className="flex items-center space-x-6 text-sm text-gray-600 dark:text-gray-400">
          <div className="flex items-center space-x-2">
            <Clock size={16} />
            <span>{lesson.estimatedTime} min</span>
          </div>
          <div className="flex items-center space-x-2">
            <Star size={16} />
            <span>{lesson.xpReward} XP</span>
          </div>
          <div className="flex items-center space-x-2">
            <BookOpen size={16} />
            <span className="capitalize">{lesson.difficulty}</span>
          </div>
        </div>
      </div>

      {/* Content */}
      <motion.div
        key={currentContentIndex}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        transition={{ duration: 0.3 }}
        className="card mb-8"
      >
        <AnimatePresence mode="wait">
          {getContentComponent()}
        </AnimatePresence>
      </motion.div>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {isCompleted && (
            <button
              onClick={handleRestart}
              className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              <RotateCcw size={16} />
              <span>Restart Lesson</span>
            </button>
          )}
        </div>

        <div className="flex items-center space-x-4">
          <button
            onClick={handlePrevious}
            disabled={isFirstContent}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              isFirstContent 
                ? 'text-gray-400 cursor-not-allowed' 
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            <ArrowLeft size={16} />
            <span>Previous</span>
          </button>

          <button
            onClick={handleNext}
            className="btn-primary flex items-center space-x-2"
          >
            <span>
              {isLastContent 
                ? (isCompleted ? 'Lesson Complete!' : 'Complete Lesson') 
                : 'Next'
              }
            </span>
            {!isLastContent && <ArrowRight size={16} />}
            {isLastContent && !isCompleted && <CheckCircle size={16} />}
          </button>
        </div>
      </div>
    </div>
  );
};

export default LessonView;
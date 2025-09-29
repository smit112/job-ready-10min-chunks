import React from 'react';
import { motion } from 'framer-motion';
import { useParams, Link } from 'react-router-dom';
import { 
  BookOpen, 
  Clock, 
  CheckCircle, 
  Lock,
  ArrowRight,
  Play,
  Star,
  Target,
  TrendingUp
} from 'lucide-react';
import { useProgress } from '../../hooks/useStore';
import { tradingFundamentalsLessons } from '../../data/lessons/trading-fundamentals';
import { optionsBasicsLessons } from '../../data/lessons/options-basics';
import { swingTradingBasicsLessons } from '../../data/lessons/swing-trading-basics';

const ModulePage: React.FC = () => {
  const { moduleId } = useParams<{ moduleId: string }>();
  const progress = useProgress();

  const moduleData = {
    fundamentals: {
      title: 'Trading Fundamentals',
      description: 'Learn the basics of trading and investing with simple playground analogies',
      icon: BookOpen,
      color: 'from-warning-400 to-warning-600',
      bgColor: 'bg-warning-50 dark:bg-warning-900/20',
      lessons: tradingFundamentalsLessons,
    },
    options: {
      title: 'Options Trading Mastery',
      description: 'Master options trading from basics to advanced strategies',
      icon: Target,
      color: 'from-danger-400 to-danger-600',
      bgColor: 'bg-danger-50 dark:bg-danger-900/20',
      lessons: optionsBasicsLessons,
    },
    swing: {
      title: 'Swing Trading Mastery',
      description: 'Learn swing trading strategies and technical analysis',
      icon: TrendingUp,
      color: 'from-primary-400 to-primary-600',
      bgColor: 'bg-primary-50 dark:bg-primary-900/20',
      lessons: swingTradingBasicsLessons,
    },
  };

  const module = moduleData[moduleId as keyof typeof moduleData];

  if (!module) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Module not found
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

  const completedLessons = progress.completedLessons.filter(id => 
    module.lessons.some(lesson => lesson.id === id)
  );
  const completionPercentage = module.lessons.length > 0 
    ? (completedLessons.length / module.lessons.length) * 100 
    : 0;

  const isLessonUnlocked = (lesson: any) => {
    if (lesson.prerequisites.length === 0) return true;
    return lesson.prerequisites.every((prereq: string) => 
      progress.completedLessons.includes(prereq)
    );
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Module Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className={`${module.bgColor} rounded-2xl p-8 mb-8`}
      >
        <div className="flex items-center space-x-4 mb-6">
          <div className={`w-16 h-16 bg-gradient-to-br ${module.color} rounded-xl flex items-center justify-center`}>
            <module.icon className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              {module.title}
            </h1>
            <p className="text-gray-600 dark:text-gray-300 mt-2">
              {module.description}
            </p>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Progress
            </span>
            <span className="text-sm font-bold text-gray-900 dark:text-white">
              {completedLessons.length}/{module.lessons.length} lessons
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
            <motion.div
              className="bg-gradient-to-r from-primary-500 to-primary-600 h-3 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${completionPercentage}%` }}
              transition={{ duration: 0.8, delay: 0.2 }}
            />
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {Math.round(completionPercentage)}% complete
          </p>
        </div>
      </motion.div>

      {/* Lessons List */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="space-y-4"
      >
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Lessons
        </h2>
        
        {module.lessons.length === 0 ? (
          <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl">
            <Star className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Coming Soon!
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              This module is under development. Check back soon for new lessons.
            </p>
          </div>
        ) : (
          module.lessons.map((lesson, index) => {
            const isCompleted = progress.completedLessons.includes(lesson.id);
            const isUnlocked = isLessonUnlocked(lesson);
            
            return (
              <motion.div
                key={lesson.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.3 + index * 0.1 }}
                className={`bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border-l-4 ${
                  isCompleted 
                    ? 'border-success-500' 
                    : isUnlocked 
                      ? 'border-primary-500' 
                      : 'border-gray-300 dark:border-gray-600'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                      isCompleted 
                        ? 'bg-success-100 dark:bg-success-900/20' 
                        : isUnlocked 
                          ? 'bg-primary-100 dark:bg-primary-900/20' 
                          : 'bg-gray-100 dark:bg-gray-700'
                    }`}>
                      {isCompleted ? (
                        <CheckCircle className="w-6 h-6 text-success-600 dark:text-success-400" />
                      ) : isUnlocked ? (
                        <Play className="w-6 h-6 text-primary-600 dark:text-primary-400" />
                      ) : (
                        <Lock className="w-6 h-6 text-gray-400" />
                      )}
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                        {lesson.title}
                      </h3>
                      <p className="text-gray-600 dark:text-gray-300 text-sm">
                        {lesson.description}
                      </p>
                      <div className="flex items-center space-x-4 mt-2">
                        <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                          <Clock className="w-4 h-4 mr-1" />
                          {lesson.estimatedTime} min
                        </div>
                        <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                          <Star className="w-4 h-4 mr-1" />
                          {lesson.xpReward} XP
                        </div>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                          lesson.difficulty === 'beginner' 
                            ? 'bg-success-100 text-success-800 dark:bg-success-900/20 dark:text-success-400'
                            : lesson.difficulty === 'intermediate'
                              ? 'bg-warning-100 text-warning-800 dark:bg-warning-900/20 dark:text-warning-400'
                              : 'bg-danger-100 text-danger-800 dark:bg-danger-900/20 dark:text-danger-400'
                        }`}>
                          {lesson.difficulty.charAt(0).toUpperCase() + lesson.difficulty.slice(1)}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    {isCompleted && (
                      <span className="text-sm text-success-600 dark:text-success-400 font-medium">
                        Completed
                      </span>
                    )}
                    {isUnlocked && !isCompleted ? (
                      <Link
                        to={`/lesson/${lesson.id}`}
                        className="inline-flex items-center px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors"
                      >
                        Start Lesson
                        <ArrowRight className="w-4 h-4 ml-2" />
                      </Link>
                    ) : !isUnlocked ? (
                      <span className="text-sm text-gray-400 dark:text-gray-500">
                        Complete prerequisites
                      </span>
                    ) : null}
                  </div>
                </div>
              </motion.div>
            );
          })
        )}
      </motion.div>
    </div>
  );
};

export default ModulePage;
import React from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  ArrowLeft, 
  Play, 
  CheckCircle, 
  Lock, 
  Clock, 
  Star,
  BookOpen,
  Target,
  TrendingUp
} from 'lucide-react';
import { useAppStore } from '../../stores/appStore';
import { tradingFundamentalsModule } from '../../data/lessons/tradingFundamentals';
import { optionsTradingModule } from '../../data/lessons/optionsTrading';

const ModuleView: React.FC = () => {
  const { moduleId } = useParams<{ moduleId: string }>();
  const navigate = useNavigate();
  const { progress } = useAppStore();

  // Find the module
  const modules = [tradingFundamentalsModule, optionsTradingModule];
  const module = modules.find(m => m.id === moduleId);

  if (!module) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Module Not Found
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          The module you're looking for doesn't exist.
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

  const completedLessons = module.lessons.filter(lesson => 
    progress.completedLessons.includes(lesson.id)
  );
  const moduleProgress = (completedLessons.length / module.lessons.length) * 100;
  const isModuleCompleted = moduleProgress === 100;

  const getNextLesson = () => {
    return module.lessons.find(lesson => 
      !progress.completedLessons.includes(lesson.id)
    );
  };

  const getSubModules = () => {
    const subModules = new Map<string, typeof module.lessons>();
    
    module.lessons.forEach(lesson => {
      const subModule = lesson.subModule || 'General';
      if (!subModules.has(subModule)) {
        subModules.set(subModule, []);
      }
      subModules.get(subModule)!.push(lesson);
    });

    return Array.from(subModules.entries()).map(([name, lessons]) => ({
      name,
      lessons,
      completed: lessons.filter(l => progress.completedLessons.includes(l.id)).length,
      total: lessons.length,
      progress: (lessons.filter(l => progress.completedLessons.includes(l.id)).length / lessons.length) * 100
    }));
  };

  const subModules = getSubModules();
  const nextLesson = getNextLesson();

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors mb-4"
        >
          <ArrowLeft size={20} />
          <span>Back to Dashboard</span>
        </button>

        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <div className={`w-16 h-16 ${module.color} rounded-2xl flex items-center justify-center text-3xl`}>
              {module.icon}
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                {module.title}
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                {module.description}
              </p>
            </div>
          </div>
          
          {isModuleCompleted && (
            <div className="flex items-center space-x-2 text-green-600 dark:text-green-400">
              <CheckCircle size={24} />
              <span className="font-medium">Module Complete!</span>
            </div>
          )}
        </div>

        {/* Module Progress */}
        <div className="card mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Module Progress
            </h2>
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {completedLessons.length} of {module.lessons.length} lessons completed
            </span>
          </div>
          
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 mb-4">
            <div 
              className="bg-primary-600 h-3 rounded-full transition-all duration-500"
              style={{ width: `${moduleProgress}%` }}
            />
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                {module.lessons.length}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                Total Lessons
              </div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                {completedLessons.length}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                Completed
              </div>
            </div>
            <div>
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {Math.round(module.lessons.reduce((acc, lesson) => acc + lesson.estimatedTime, 0))}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                Total Minutes
              </div>
            </div>
            <div>
              <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                {module.lessons.reduce((acc, lesson) => acc + lesson.xpReward, 0)}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                Total XP
              </div>
            </div>
          </div>
        </div>

        {/* Quick Action */}
        {nextLesson && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card bg-gradient-to-r from-primary-500 to-primary-700 text-white mb-8"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xl font-semibold mb-2">
                  Continue Your Learning Journey
                </h3>
                <p className="text-primary-100">
                  Next up: {nextLesson.title}
                </p>
              </div>
              <Link
                to={`/lesson/${nextLesson.id}`}
                className="bg-white text-primary-600 hover:bg-primary-50 font-medium py-3 px-6 rounded-lg transition-colors flex items-center space-x-2"
              >
                <Play size={20} />
                <span>Start Lesson</span>
              </Link>
            </div>
          </motion.div>
        )}
      </div>

      {/* Sub-modules */}
      <div className="space-y-8">
        {subModules.map((subModule, index) => (
          <motion.div
            key={subModule.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="card"
          >
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                  {subModule.name}
                </h2>
                <p className="text-gray-600 dark:text-gray-400">
                  {subModule.completed} of {subModule.total} lessons completed
                </p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-primary-600 dark:text-primary-400">
                  {Math.round(subModule.progress)}%
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  Complete
                </div>
              </div>
            </div>

            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-6">
              <div 
                className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${subModule.progress}%` }}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {subModule.lessons.map((lesson, lessonIndex) => {
                const isCompleted = progress.completedLessons.includes(lesson.id);
                const isLocked = lesson.prerequisites.some(prereq => 
                  !progress.completedLessons.includes(prereq)
                );

                return (
                  <motion.div
                    key={lesson.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 + lessonIndex * 0.05 }}
                    className={`lesson-card ${isLocked ? 'opacity-60' : ''}`}
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                          {lesson.title}
                        </h3>
                        <p className="text-gray-600 dark:text-gray-400 text-sm mb-3">
                          {lesson.description}
                        </p>
                      </div>
                      <div className="ml-4">
                        {isCompleted ? (
                          <CheckCircle size={24} className="text-green-500" />
                        ) : isLocked ? (
                          <Lock size={24} className="text-gray-400" />
                        ) : (
                          <Play size={24} className="text-primary-500" />
                        )}
                      </div>
                    </div>

                    <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400 mb-4">
                      <div className="flex items-center space-x-1">
                        <Clock size={14} />
                        <span>{lesson.estimatedTime} min</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Star size={14} />
                        <span>{lesson.xpReward} XP</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Target size={14} />
                        <span className="capitalize">{lesson.difficulty}</span>
                      </div>
                    </div>

                    {isLocked ? (
                      <div className="text-center py-2">
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          Complete prerequisites to unlock
                        </div>
                      </div>
                    ) : (
                      <Link
                        to={`/lesson/${lesson.id}`}
                        className={`w-full text-center inline-block py-2 px-4 rounded-lg font-medium transition-colors ${
                          isCompleted
                            ? 'bg-green-100 text-green-700 hover:bg-green-200 dark:bg-green-900/20 dark:text-green-400'
                            : 'btn-primary'
                        }`}
                      >
                        {isCompleted ? 'Review Lesson' : 'Start Lesson'}
                      </Link>
                    )}
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default ModuleView;
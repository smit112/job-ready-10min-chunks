import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  BookOpen, 
  Target, 
  TrendingUp, 
  Calculator,
  Trophy,
  Zap,
  ArrowRight,
  Play,
  Star
} from 'lucide-react';
import { useProgress } from '../../hooks/useStore';

const HomePage: React.FC = () => {
  const progress = useProgress();

  const modules = [
    {
      id: 'fundamentals',
      title: 'Trading Fundamentals',
      description: 'Learn the basics of trading and investing with simple playground analogies',
      icon: BookOpen,
      color: 'from-warning-400 to-warning-600',
      bgColor: 'bg-warning-50 dark:bg-warning-900/20',
      lessons: 7,
      completed: progress.completedLessons.filter(id => id.startsWith('trading-')).length,
      difficulty: 'Beginner',
    },
    {
      id: 'options',
      title: 'Options Trading Mastery',
      description: 'Master options trading from basics to advanced strategies',
      icon: Target,
      color: 'from-danger-400 to-danger-600',
      bgColor: 'bg-danger-50 dark:bg-danger-900/20',
      lessons: 15,
      completed: progress.completedLessons.filter(id => id.startsWith('options-')).length,
      difficulty: 'Beginner to Advanced',
    },
    {
      id: 'swing',
      title: 'Swing Trading Mastery',
      description: 'Learn swing trading strategies and technical analysis',
      icon: TrendingUp,
      color: 'from-primary-400 to-primary-600',
      bgColor: 'bg-primary-50 dark:bg-primary-900/20',
      lessons: 12,
      completed: progress.completedLessons.filter(id => id.startsWith('swing-')).length,
      difficulty: 'Beginner to Advanced',
    },
  ];

  const features = [
    {
      icon: Calculator,
      title: 'Interactive Calculators',
      description: 'Options P&L, Greeks, Risk calculators and more',
    },
    {
      icon: Trophy,
      title: 'Gamification',
      description: 'Earn XP, unlock achievements, and track your progress',
    },
    {
      icon: Star,
      title: 'Child-Friendly Learning',
      description: 'Complex concepts explained with simple analogies',
    },
  ];

  return (
    <div className="max-w-7xl mx-auto">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center py-12"
      >
        <div className="flex items-center justify-center space-x-2 mb-6">
          <Zap className="w-8 h-8 text-primary-500" />
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white">
            Trading Academy
          </h1>
        </div>
        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
          Learn options trading and swing trading from absolute beginner to advanced practitioner. 
          Complex concepts explained with simple analogies and interactive tools.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/dashboard"
            className="inline-flex items-center px-8 py-4 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-colors"
          >
            <Play className="w-5 h-5 mr-2" />
            Start Learning
          </Link>
          <Link
            to="/tools"
            className="inline-flex items-center px-8 py-4 border-2 border-primary-600 text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20 font-semibold rounded-lg transition-colors"
          >
            <Calculator className="w-5 h-5 mr-2" />
            Try Tools
          </Link>
        </div>
      </motion.div>

      {/* Progress Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 mb-12"
      >
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Your Learning Progress
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-primary-600 dark:text-primary-400 mb-2">
              {progress.totalXP}
            </div>
            <div className="text-gray-600 dark:text-gray-300">Total XP</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-success-600 dark:text-success-400 mb-2">
              {progress.currentStreak}
            </div>
            <div className="text-gray-600 dark:text-gray-300">Day Streak</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-warning-600 dark:text-warning-400 mb-2">
              {progress.completedLessons.length}
            </div>
            <div className="text-gray-600 dark:text-gray-300">Lessons Completed</div>
          </div>
        </div>
      </motion.div>

      {/* Learning Modules */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="mb-12"
      >
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">
          Choose Your Learning Path
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {modules.map((module, index) => (
            <motion.div
              key={module.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
              className="group"
            >
              <Link to={`/module/${module.id}`}>
                <div className={`${module.bgColor} rounded-2xl p-8 h-full transition-all duration-300 group-hover:shadow-xl group-hover:scale-105`}>
                  <div className={`w-16 h-16 bg-gradient-to-br ${module.color} rounded-xl flex items-center justify-center mb-6`}>
                    <module.icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                    {module.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-4">
                    {module.description}
                  </p>
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      {module.completed}/{module.lessons} lessons
                    </span>
                    <span className="text-sm font-medium text-primary-600 dark:text-primary-400">
                      {module.difficulty}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-4">
                    <div 
                      className="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${(module.completed / module.lessons) * 100}%` }}
                    />
                  </div>
                  <div className="flex items-center text-primary-600 dark:text-primary-400 font-medium group-hover:translate-x-2 transition-transform">
                    Start Learning
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Features */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.8 }}
        className="bg-gray-50 dark:bg-gray-800 rounded-2xl p-8"
      >
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">
          Why Choose Our Platform?
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 1.0 + index * 0.1 }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-xl flex items-center justify-center mx-auto mb-4">
                <feature.icon className="w-8 h-8 text-primary-600 dark:text-primary-400" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default HomePage;
import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  BookOpen, 
  Target, 
  TrendingUp, 
  Trophy,
  Zap,
  Clock,
  CheckCircle,
  ArrowRight,
  Calendar,
  BarChart3
} from 'lucide-react';
import { useProgress } from '../../hooks/useStore';

const Dashboard: React.FC = () => {
  const progress = useProgress();

  const recentAchievements = [
    {
      id: 'first-lesson',
      title: 'First Steps',
      description: 'Completed your first lesson',
      icon: CheckCircle,
      color: 'text-success-500',
      unlockedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    },
    {
      id: 'streak-3',
      title: '3-Day Streak',
      description: 'Learned for 3 days in a row',
      icon: Zap,
      color: 'text-warning-500',
      unlockedAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
    },
  ];

  const upcomingLessons = [
    {
      id: 'options-basics-1',
      title: 'What Are Options?',
      module: 'Options Trading',
      estimatedTime: 15,
      difficulty: 'Beginner',
      isUnlocked: true,
    },
    {
      id: 'swing-basics-1',
      title: 'Swing Trading Basics',
      module: 'Swing Trading',
      estimatedTime: 20,
      difficulty: 'Beginner',
      isUnlocked: false,
    },
  ];

  const stats = [
    {
      label: 'Total XP',
      value: progress.totalXP,
      icon: Zap,
      color: 'text-primary-500',
      change: '+150 this week',
    },
    {
      label: 'Current Streak',
      value: `${progress.currentStreak} days`,
      icon: Calendar,
      color: 'text-success-500',
      change: 'Keep it up!',
    },
    {
      label: 'Lessons Completed',
      value: progress.completedLessons.length,
      icon: CheckCircle,
      color: 'text-warning-500',
      change: '+2 this week',
    },
    {
      label: 'Achievements',
      value: progress.achievements.length,
      icon: Trophy,
      color: 'text-danger-500',
      change: '+1 this week',
    },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="flex flex-col md:flex-row md:items-center md:justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome back! 👋
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Continue your trading education journey
          </p>
        </div>
        <div className="mt-4 md:mt-0">
          <Link
            to="/tools"
            className="inline-flex items-center px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-colors"
          >
            <BarChart3 className="w-5 h-5 mr-2" />
            Open Tools
          </Link>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {stats.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 + index * 0.1 }}
            className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 rounded-lg bg-gray-50 dark:bg-gray-700`}>
                <stat.icon className={`w-6 h-6 ${stat.color}`} />
              </div>
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
              {stat.value}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-300 mb-2">
              {stat.label}
            </div>
            <div className="text-xs text-success-600 dark:text-success-400">
              {stat.change}
            </div>
          </motion.div>
        ))}
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Achievements */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg"
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              Recent Achievements
            </h2>
            <Link
              to="/achievements"
              className="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 text-sm font-medium"
            >
              View All
            </Link>
          </div>
          <div className="space-y-4">
            {recentAchievements.map((achievement) => (
              <div key={achievement.id} className="flex items-center space-x-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div className={`p-2 rounded-lg bg-white dark:bg-gray-600`}>
                  <achievement.icon className={`w-5 h-5 ${achievement.color}`} />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    {achievement.title}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    {achievement.description}
                  </p>
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  {achievement.unlockedAt.toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Upcoming Lessons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg"
        >
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
            Continue Learning
          </h2>
          <div className="space-y-4">
            {upcomingLessons.map((lesson) => (
              <div key={lesson.id} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                      {lesson.title}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      {lesson.module}
                    </p>
                  </div>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    lesson.difficulty === 'Beginner' 
                      ? 'bg-success-100 text-success-800 dark:bg-success-900/20 dark:text-success-400'
                      : 'bg-warning-100 text-warning-800 dark:bg-warning-900/20 dark:text-warning-400'
                  }`}>
                    {lesson.difficulty}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                    <Clock className="w-4 h-4 mr-1" />
                    {lesson.estimatedTime} min
                  </div>
                  {lesson.isUnlocked ? (
                    <Link
                      to={`/lesson/${lesson.id}`}
                      className="inline-flex items-center text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 text-sm font-medium"
                    >
                      Start Lesson
                      <ArrowRight className="w-4 h-4 ml-1" />
                    </Link>
                  ) : (
                    <span className="text-sm text-gray-400 dark:text-gray-500">
                      Complete prerequisites
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.5 }}
        className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg"
      >
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
          Quick Actions
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            to="/module/fundamentals"
            className="flex items-center p-4 bg-warning-50 dark:bg-warning-900/20 rounded-lg hover:bg-warning-100 dark:hover:bg-warning-900/30 transition-colors"
          >
            <BookOpen className="w-6 h-6 text-warning-600 dark:text-warning-400 mr-3" />
            <div>
              <div className="font-semibold text-gray-900 dark:text-white">
                Trading Fundamentals
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-300">
                Learn the basics
              </div>
            </div>
          </Link>
          <Link
            to="/module/options"
            className="flex items-center p-4 bg-danger-50 dark:bg-danger-900/20 rounded-lg hover:bg-danger-100 dark:hover:bg-danger-900/30 transition-colors"
          >
            <Target className="w-6 h-6 text-danger-600 dark:text-danger-400 mr-3" />
            <div>
              <div className="font-semibold text-gray-900 dark:text-white">
                Options Trading
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-300">
                Master options
              </div>
            </div>
          </Link>
          <Link
            to="/module/swing"
            className="flex items-center p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/30 transition-colors"
          >
            <TrendingUp className="w-6 h-6 text-primary-600 dark:text-primary-400 mr-3" />
            <div>
              <div className="font-semibold text-gray-900 dark:text-white">
                Swing Trading
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-300">
                Learn swing strategies
              </div>
            </div>
          </Link>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;
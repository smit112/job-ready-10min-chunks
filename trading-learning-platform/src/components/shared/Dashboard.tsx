import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  BookOpen, 
  Target, 
  TrendingUp, 
  Calculator, 
  Trophy, 
  Play,
  Clock,
  Star,
  ArrowRight,
  Zap
} from 'lucide-react';
import { useAppStore } from '../../stores/appStore';
import { tradingFundamentalsModule } from '../../data/lessons/tradingFundamentals';
import { optionsTradingModule } from '../../data/lessons/optionsTrading';

const Dashboard: React.FC = () => {
  const { progress, theme } = useAppStore();

  const modules = [
    {
      ...tradingFundamentalsModule,
      progress: 75, // This would be calculated from actual progress
      lessonsCompleted: 5,
      totalLessons: 7,
      nextLesson: tradingFundamentalsModule.lessons[5], // market-hours lesson
    },
    {
      ...optionsTradingModule,
      progress: 30,
      lessonsCompleted: 3,
      totalLessons: 10,
      nextLesson: optionsTradingModule.lessons[3], // exercise-vs-sell lesson
    },
    {
      id: 'swing-trading',
      title: 'Swing Trading Mastery',
      description: 'Master swing trading strategies and technical analysis',
      icon: '📈',
      color: 'bg-orange-500',
      progress: 0,
      lessonsCompleted: 0,
      totalLessons: 12,
      nextLesson: null,
      unlocked: false,
    }
  ];

  const recentAchievements = [
    {
      id: 'first-steps',
      title: 'First Steps',
      description: 'Completed your first lesson',
      icon: '🎉',
      unlockedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    },
    {
      id: 'options-explorer',
      title: 'Options Explorer',
      description: 'Completed options basics module',
      icon: '🎯',
      unlockedAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
    }
  ];

  const quickActions = [
    {
      title: 'Continue Learning',
      description: 'Pick up where you left off',
      icon: Play,
      color: 'bg-primary-500',
      action: () => {
        // Navigate to next lesson
      }
    },
    {
      title: 'Practice Tools',
      description: 'Use interactive calculators',
      icon: Calculator,
      color: 'bg-green-500',
      action: () => {
        // Navigate to tools
      }
    },
    {
      title: 'Take Quiz',
      description: 'Test your knowledge',
      icon: Target,
      color: 'bg-purple-500',
      action: () => {
        // Navigate to quiz
      }
    }
  ];

  const stats = [
    {
      label: 'Total XP',
      value: progress.totalXP.toLocaleString(),
      icon: Zap,
      color: 'text-yellow-500',
    },
    {
      label: 'Current Streak',
      value: `${progress.currentStreak} days`,
      icon: Clock,
      color: 'text-green-500',
    },
    {
      label: 'Lessons Completed',
      value: progress.completedLessons.length,
      icon: BookOpen,
      color: 'text-blue-500',
    },
    {
      label: 'Achievements',
      value: progress.achievements.length,
      icon: Trophy,
      color: 'text-purple-500',
    }
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-primary-500 to-primary-700 rounded-2xl p-8 text-white"
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">
              Welcome back, Trader! 🚀
            </h1>
            <p className="text-primary-100 text-lg">
              Ready to continue your trading journey? You're doing great!
            </p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold">Level {progress.level}</div>
            <div className="text-primary-200">{progress.totalXP} XP</div>
          </div>
        </div>
        
        {/* Progress bar */}
        <div className="mt-6">
          <div className="flex justify-between text-sm text-primary-200 mb-2">
            <span>Progress to Level {progress.level + 1}</span>
            <span>{progress.totalXP % 1000}/1000 XP</span>
          </div>
          <div className="w-full bg-primary-600 rounded-full h-3">
            <div 
              className="bg-white h-3 rounded-full transition-all duration-500"
              style={{ width: `${(progress.totalXP % 1000) / 10}%` }}
            />
          </div>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {stats.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + index * 0.1 }}
            className="card text-center"
          >
            <stat.icon size={32} className={`mx-auto mb-3 ${stat.color}`} />
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              {stat.value}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              {stat.label}
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6"
      >
        {quickActions.map((action, index) => (
          <motion.button
            key={action.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + index * 0.1 }}
            onClick={action.action}
            className="card hover:shadow-lg transition-all duration-200 text-left group"
          >
            <div className={`w-12 h-12 ${action.color} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
              <action.icon size={24} className="text-white" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {action.title}
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              {action.description}
            </p>
            <ArrowRight size={16} className="text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300 mt-2" />
          </motion.button>
        ))}
      </motion.div>

      {/* Learning Modules */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="space-y-6"
      >
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Learning Modules
          </h2>
          <Link 
            to="/progress" 
            className="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium"
          >
            View All Progress
          </Link>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {modules.map((module, index) => (
            <motion.div
              key={module.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 + index * 0.1 }}
              className={`card ${!module.unlocked ? 'opacity-60' : ''}`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className={`w-12 h-12 ${module.color} rounded-lg flex items-center justify-center text-2xl`}>
                  {module.icon}
                </div>
                {module.unlocked && (
                  <div className="text-right">
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      {module.lessonsCompleted}/{module.totalLessons} lessons
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-500">
                      {module.progress}% complete
                    </div>
                  </div>
                )}
              </div>

              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                {module.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
                {module.description}
              </p>

              {module.unlocked ? (
                <>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-4">
                    <div 
                      className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${module.progress}%` }}
                    />
                  </div>
                  
                  {module.nextLesson ? (
                    <Link
                      to={`/lesson/${module.nextLesson.id}`}
                      className="btn-primary w-full text-center inline-block"
                    >
                      Continue Learning
                    </Link>
                  ) : (
                    <Link
                      to={`/module/${module.id}`}
                      className="btn-primary w-full text-center inline-block"
                    >
                      View Module
                    </Link>
                  )}
                </>
              ) : (
                <div className="text-center py-4">
                  <div className="text-gray-500 dark:text-gray-400 text-sm">
                    Complete previous modules to unlock
                  </div>
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Recent Achievements */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="card"
      >
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
          Recent Achievements
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recentAchievements.map((achievement) => (
            <div key={achievement.id} className="flex items-center space-x-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="text-3xl">{achievement.icon}</div>
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900 dark:text-white">
                  {achievement.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {achievement.description}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                  {achievement.unlockedAt.toLocaleDateString()}
                </p>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;
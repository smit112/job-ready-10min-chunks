import React from 'react';
import { motion } from 'framer-motion';
import { 
  Trophy, 
  Star, 
  Zap, 
  Target, 
  BookOpen,
  TrendingUp,
  CheckCircle,
  Lock
} from 'lucide-react';
import { useProgress } from '../../hooks/useStore';

const Achievements: React.FC = () => {
  const progress = useProgress();

  const achievements = [
    {
      id: 'first-steps',
      title: 'First Steps',
      description: 'Complete your first lesson',
      icon: BookOpen,
      color: 'from-success-400 to-success-600',
      xpReward: 100,
      isUnlocked: progress.completedLessons.length > 0,
      category: 'learning',
    },
    {
      id: 'options-explorer',
      title: 'Options Explorer',
      description: 'Complete 5 options lessons',
      icon: Target,
      color: 'from-danger-400 to-danger-600',
      xpReward: 250,
      isUnlocked: progress.completedLessons.filter(id => id.startsWith('options-')).length >= 5,
      category: 'learning',
    },
    {
      id: 'swing-trader',
      title: 'Swing Trader',
      description: 'Complete 5 swing trading lessons',
      icon: TrendingUp,
      color: 'from-primary-400 to-primary-600',
      xpReward: 250,
      isUnlocked: progress.completedLessons.filter(id => id.startsWith('swing-')).length >= 5,
      category: 'learning',
    },
    {
      id: 'streak-3',
      title: '3-Day Streak',
      description: 'Learn for 3 days in a row',
      icon: Zap,
      color: 'from-warning-400 to-warning-600',
      xpReward: 150,
      isUnlocked: progress.currentStreak >= 3,
      category: 'streak',
    },
    {
      id: 'streak-7',
      title: 'Week Warrior',
      description: 'Learn for 7 days in a row',
      icon: Star,
      color: 'from-purple-400 to-purple-600',
      xpReward: 500,
      isUnlocked: progress.currentStreak >= 7,
      category: 'streak',
    },
    {
      id: 'xp-master',
      title: 'XP Master',
      description: 'Earn 1000 XP points',
      icon: Trophy,
      color: 'from-indigo-400 to-indigo-600',
      xpReward: 1000,
      isUnlocked: progress.totalXP >= 1000,
      category: 'milestone',
    },
  ];

  const unlockedAchievements = achievements.filter(a => a.isUnlocked);
  const lockedAchievements = achievements.filter(a => !a.isUnlocked);

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center py-12"
      >
        <div className="flex items-center justify-center space-x-2 mb-6">
          <Trophy className="w-8 h-8 text-warning-500" />
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
            Achievements
          </h1>
        </div>
        <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
          Track your progress and unlock achievements as you master trading concepts
        </p>
      </motion.div>

      {/* Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
      >
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg text-center">
          <div className="text-3xl font-bold text-warning-600 dark:text-warning-400 mb-2">
            {unlockedAchievements.length}
          </div>
          <div className="text-gray-600 dark:text-gray-300">Achievements Unlocked</div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg text-center">
          <div className="text-3xl font-bold text-primary-600 dark:text-primary-400 mb-2">
            {achievements.length}
          </div>
          <div className="text-gray-600 dark:text-gray-300">Total Achievements</div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg text-center">
          <div className="text-3xl font-bold text-success-600 dark:text-success-400 mb-2">
            {Math.round((unlockedAchievements.length / achievements.length) * 100)}%
          </div>
          <div className="text-gray-600 dark:text-gray-300">Completion Rate</div>
        </div>
      </motion.div>

      {/* Unlocked Achievements */}
      {unlockedAchievements.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mb-12"
        >
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Unlocked Achievements
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {unlockedAchievements.map((achievement, index) => (
              <motion.div
                key={achievement.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.4 + index * 0.1 }}
                className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border-l-4 border-success-500"
              >
                <div className="flex items-center space-x-4 mb-4">
                  <div className={`w-12 h-12 bg-gradient-to-br ${achievement.color} rounded-lg flex items-center justify-center`}>
                    <achievement.icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                      {achievement.title}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      +{achievement.xpReward} XP
                    </p>
                  </div>
                </div>
                <p className="text-gray-700 dark:text-gray-300">
                  {achievement.description}
                </p>
                <div className="flex items-center mt-4">
                  <CheckCircle className="w-4 h-4 text-success-500 mr-2" />
                  <span className="text-sm text-success-600 dark:text-success-400 font-medium">
                    Unlocked
                  </span>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Locked Achievements */}
      {lockedAchievements.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Locked Achievements
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {lockedAchievements.map((achievement, index) => (
              <motion.div
                key={achievement.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
                className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border-l-4 border-gray-300 dark:border-gray-600 opacity-60"
              >
                <div className="flex items-center space-x-4 mb-4">
                  <div className="w-12 h-12 bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center">
                    <Lock className="w-6 h-6 text-gray-400" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-500 dark:text-gray-400">
                      {achievement.title}
                    </h3>
                    <p className="text-sm text-gray-400 dark:text-gray-500">
                      +{achievement.xpReward} XP
                    </p>
                  </div>
                </div>
                <p className="text-gray-500 dark:text-gray-400">
                  {achievement.description}
                </p>
                <div className="flex items-center mt-4">
                  <Lock className="w-4 h-4 text-gray-400 mr-2" />
                  <span className="text-sm text-gray-400 dark:text-gray-500 font-medium">
                    Locked
                  </span>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Achievements;
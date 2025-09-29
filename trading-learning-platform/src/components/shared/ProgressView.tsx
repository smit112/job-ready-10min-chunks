import React from 'react';
import { motion } from 'framer-motion';
import { 
  Trophy, 
  Star, 
  Clock, 
  BookOpen, 
  Target, 
  TrendingUp,
  Award,
  Calendar,
  Zap
} from 'lucide-react';
import { useAppStore } from '../../stores/appStore';

const ProgressView: React.FC = () => {
  const { progress } = useAppStore();

  // Mock achievements data
  const achievements = [
    {
      id: 'first-steps',
      title: 'First Steps',
      description: 'Completed your first lesson',
      icon: '🎉',
      category: 'learning' as const,
      xpReward: 100,
      unlockedAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
      rarity: 'common' as const,
      unlocked: true
    },
    {
      id: 'options-explorer',
      title: 'Options Explorer',
      description: 'Completed options basics module',
      icon: '🎯',
      category: 'trading' as const,
      xpReward: 500,
      unlockedAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
      rarity: 'rare' as const,
      unlocked: true
    },
    {
      id: 'quiz-master',
      title: 'Quiz Master',
      description: 'Scored 90% or higher on 5 quizzes',
      icon: '🧠',
      category: 'mastery' as const,
      xpReward: 300,
      unlockedAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
      rarity: 'rare' as const,
      unlocked: true
    },
    {
      id: 'streak-keeper',
      title: 'Streak Keeper',
      description: 'Maintained a 7-day learning streak',
      icon: '🔥',
      category: 'streak' as const,
      xpReward: 200,
      unlockedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
      rarity: 'common' as const,
      unlocked: true
    },
    {
      id: 'greek-master',
      title: 'Greek Master',
      description: 'Mastered all options Greeks',
      icon: '📊',
      category: 'mastery' as const,
      xpReward: 1000,
      unlockedAt: null,
      rarity: 'epic' as const,
      unlocked: false
    },
    {
      id: 'swing-trader',
      title: 'Swing Trader',
      description: 'Completed swing trading module',
      icon: '📈',
      category: 'trading' as const,
      xpReward: 800,
      unlockedAt: null,
      rarity: 'rare' as const,
      unlocked: false
    }
  ];

  const unlockedAchievements = achievements.filter(a => a.unlocked);
  const lockedAchievements = achievements.filter(a => !a.unlocked);

  const getRarityColor = (rarity: string) => {
    switch (rarity) {
      case 'common': return 'text-gray-600 dark:text-gray-400';
      case 'rare': return 'text-blue-600 dark:text-blue-400';
      case 'epic': return 'text-purple-600 dark:text-purple-400';
      case 'legendary': return 'text-yellow-600 dark:text-yellow-400';
      default: return 'text-gray-600 dark:text-gray-400';
    }
  };

  const getRarityBg = (rarity: string) => {
    switch (rarity) {
      case 'common': return 'bg-gray-100 dark:bg-gray-800';
      case 'rare': return 'bg-blue-100 dark:bg-blue-900/20';
      case 'epic': return 'bg-purple-100 dark:bg-purple-900/20';
      case 'legendary': return 'bg-yellow-100 dark:bg-yellow-900/20';
      default: return 'bg-gray-100 dark:bg-gray-800';
    }
  };

  const stats = [
    {
      label: 'Total XP',
      value: progress.totalXP.toLocaleString(),
      icon: Zap,
      color: 'text-yellow-500',
      bg: 'bg-yellow-100 dark:bg-yellow-900/20'
    },
    {
      label: 'Current Level',
      value: progress.level,
      icon: Star,
      color: 'text-blue-500',
      bg: 'bg-blue-100 dark:bg-blue-900/20'
    },
    {
      label: 'Learning Streak',
      value: `${progress.currentStreak} days`,
      icon: Calendar,
      color: 'text-green-500',
      bg: 'bg-green-100 dark:bg-green-900/20'
    },
    {
      label: 'Lessons Completed',
      value: progress.completedLessons.length,
      icon: BookOpen,
      color: 'text-purple-500',
      bg: 'bg-purple-100 dark:bg-purple-900/20'
    },
    {
      label: 'Achievements',
      value: progress.achievements.length,
      icon: Trophy,
      color: 'text-orange-500',
      bg: 'bg-orange-100 dark:bg-orange-900/20'
    },
    {
      label: 'Time Spent',
      value: `${Math.round(progress.timeSpent / 60)} hours`,
      icon: Clock,
      color: 'text-indigo-500',
      bg: 'bg-indigo-100 dark:bg-indigo-900/20'
    }
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Your Progress
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Track your learning journey and celebrate your achievements
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`${stat.bg} rounded-xl p-4 text-center`}
          >
            <stat.icon size={24} className={`mx-auto mb-2 ${stat.color}`} />
            <div className="text-xl font-bold text-gray-900 dark:text-white">
              {stat.value}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              {stat.label}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Level Progress */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="card"
      >
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Level Progress
        </h2>
        
        <div className="flex items-center space-x-4 mb-4">
          <div className="text-3xl font-bold text-primary-600 dark:text-primary-400">
            Level {progress.level}
          </div>
          <div className="flex-1">
            <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
              <span>Progress to Level {progress.level + 1}</span>
              <span>{progress.totalXP % 1000}/1000 XP</span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
              <div 
                className="bg-primary-600 h-3 rounded-full transition-all duration-500"
                style={{ width: `${(progress.totalXP % 1000) / 10}%` }}
              />
            </div>
          </div>
        </div>

        <div className="text-sm text-gray-600 dark:text-gray-400">
          {1000 - (progress.totalXP % 1000)} XP needed for next level
        </div>
      </motion.div>

      {/* Achievements */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Unlocked Achievements */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Unlocked Achievements
          </h2>
          
          <div className="space-y-4">
            {unlockedAchievements.map((achievement, index) => (
              <motion.div
                key={achievement.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                className={`${getRarityBg(achievement.rarity)} rounded-lg p-4 border border-gray-200 dark:border-gray-700`}
              >
                <div className="flex items-center space-x-4">
                  <div className="text-3xl">{achievement.icon}</div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <h3 className="font-semibold text-gray-900 dark:text-white">
                        {achievement.title}
                      </h3>
                      <span className={`text-xs px-2 py-1 rounded-full ${getRarityBg(achievement.rarity)} ${getRarityColor(achievement.rarity)}`}>
                        {achievement.rarity.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      {achievement.description}
                    </p>
                    <div className="flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-500">
                      <span>+{achievement.xpReward} XP</span>
                      <span>{achievement.unlockedAt?.toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Locked Achievements */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card"
        >
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Upcoming Achievements
          </h2>
          
          <div className="space-y-4">
            {lockedAchievements.map((achievement, index) => (
              <motion.div
                key={achievement.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + index * 0.1 }}
                className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 opacity-60"
              >
                <div className="flex items-center space-x-4">
                  <div className="text-3xl grayscale">{achievement.icon}</div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <h3 className="font-semibold text-gray-600 dark:text-gray-400">
                        {achievement.title}
                      </h3>
                      <span className={`text-xs px-2 py-1 rounded-full ${getRarityBg(achievement.rarity)} ${getRarityColor(achievement.rarity)}`}>
                        {achievement.rarity.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-500 dark:text-gray-500 mb-2">
                      {achievement.description}
                    </p>
                    <div className="text-xs text-gray-500 dark:text-gray-500">
                      +{achievement.xpReward} XP
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Learning Streak */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="card bg-gradient-to-r from-orange-500 to-red-500 text-white"
      >
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold mb-2">
              Learning Streak
            </h2>
            <p className="text-orange-100">
              You've been learning for {progress.currentStreak} days in a row!
            </p>
          </div>
          <div className="text-4xl">🔥</div>
        </div>
        
        <div className="mt-4">
          <div className="text-sm text-orange-100 mb-2">
            Keep it up! Consistency is key to mastering trading.
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default ProgressView;
import React from 'react';
import { motion } from 'framer-motion';
import { NavLink } from 'react-router-dom';
import { 
  Home, 
  BookOpen, 
  Calculator, 
  Trophy, 
  BarChart3,
  Target,
  TrendingUp,
  Settings,
  X
} from 'lucide-react';
import { useStore, useProgress } from '../../hooks/useStore';

const Sidebar: React.FC = () => {
  const { setSidebarOpen, progress } = useStore();

  const navigationItems = [
    {
      name: 'Home',
      href: '/',
      icon: Home,
      color: 'text-primary-500',
    },
    {
      name: 'Dashboard',
      href: '/dashboard',
      icon: BarChart3,
      color: 'text-success-500',
    },
    {
      name: 'Trading Fundamentals',
      href: '/module/fundamentals',
      icon: BookOpen,
      color: 'text-warning-500',
      badge: progress.completedLessons.filter(id => id.startsWith('trading-')).length,
    },
    {
      name: 'Options Trading',
      href: '/module/options',
      icon: Target,
      color: 'text-danger-500',
      badge: progress.completedLessons.filter(id => id.startsWith('options-')).length,
    },
    {
      name: 'Swing Trading',
      href: '/module/swing',
      icon: TrendingUp,
      color: 'text-primary-600',
      badge: progress.completedLessons.filter(id => id.startsWith('swing-')).length,
    },
    {
      name: 'Interactive Tools',
      href: '/tools',
      icon: Calculator,
      color: 'text-success-600',
    },
    {
      name: 'Achievements',
      href: '/achievements',
      icon: Trophy,
      color: 'text-warning-600',
      badge: progress.achievements.length,
    },
  ];

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <span className="text-lg font-bold text-gray-900 dark:text-white">
            Trading Academy
          </span>
        </div>
        <button
          onClick={() => setSidebarOpen(false)}
          className="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors lg:hidden"
        >
          <X className="w-5 h-5 text-gray-600 dark:text-gray-300" />
        </button>
      </div>

      {/* Progress Summary */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Total XP
            </span>
            <span className="text-sm font-bold text-primary-600 dark:text-primary-400">
              {progress.totalXP}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Current Streak
            </span>
            <span className="text-sm font-bold text-success-600 dark:text-success-400">
              {progress.currentStreak} days
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <motion.div
              className="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${Math.min((progress.totalXP / 10000) * 100, 100)}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            {Math.floor(progress.totalXP / 100)}% to next level
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navigationItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              `flex items-center justify-between px-4 py-3 rounded-lg transition-all duration-200 group ${
                isActive
                  ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`
            }
            onClick={() => setSidebarOpen(false)}
          >
            <div className="flex items-center space-x-3">
              <item.icon className={`w-5 h-5 ${item.color}`} />
              <span className="font-medium">{item.name}</span>
            </div>
            {item.badge && item.badge > 0 && (
              <span className="px-2 py-1 text-xs font-bold text-white bg-primary-500 rounded-full">
                {item.badge}
              </span>
            )}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700">
        <NavLink
          to="/settings"
          className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
        >
          <Settings className="w-5 h-5" />
          <span className="font-medium">Settings</span>
        </NavLink>
      </div>
    </div>
  );
};

export default Sidebar;
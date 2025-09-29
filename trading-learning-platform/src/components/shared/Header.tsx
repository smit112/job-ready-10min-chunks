import React from 'react';
import { motion } from 'framer-motion';
import { 
  Menu, 
  Sun, 
  Moon, 
  Bell, 
  User,
  Trophy,
  Zap
} from 'lucide-react';
import { useStore, useProgress, useDarkMode } from '../../hooks/useStore';

const Header: React.FC = () => {
  const { setSidebarOpen, toggleDarkMode, addNotification } = useStore();
  const progress = useProgress();
  const isDarkMode = useDarkMode();

  const handleNotificationClick = () => {
    addNotification({
      type: 'info',
      title: 'New Achievement!',
      message: 'You\'ve completed your first lesson!',
    });
  };

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between px-6 py-4">
        {/* Left side */}
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors lg:hidden"
          >
            <Menu className="w-5 h-5 text-gray-600 dark:text-gray-300" />
          </button>
          
          <div className="hidden sm:flex items-center space-x-2">
            <Zap className="w-5 h-5 text-primary-500" />
            <span className="text-lg font-semibold text-gray-900 dark:text-white">
              Trading Academy
            </span>
          </div>
        </div>

        {/* Center - Progress indicator */}
        <div className="hidden md:flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Trophy className="w-4 h-4 text-warning-500" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {progress.totalXP} XP
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-success-500 rounded-full animate-pulse" />
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {progress.currentStreak} day streak
            </span>
          </div>
        </div>

        {/* Right side */}
        <div className="flex items-center space-x-2">
          {/* Dark mode toggle */}
          <button
            onClick={toggleDarkMode}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            title={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {isDarkMode ? (
              <Sun className="w-5 h-5 text-warning-500" />
            ) : (
              <Moon className="w-5 h-5 text-gray-600 dark:text-gray-300" />
            )}
          </button>

          {/* Notifications */}
          <button
            onClick={handleNotificationClick}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors relative"
            title="Notifications"
          >
            <Bell className="w-5 h-5 text-gray-600 dark:text-gray-300" />
            <span className="absolute -top-1 -right-1 w-3 h-3 bg-danger-500 rounded-full text-xs text-white flex items-center justify-center">
              1
            </span>
          </button>

          {/* User profile */}
          <button className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
            <User className="w-5 h-5 text-gray-600 dark:text-gray-300" />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
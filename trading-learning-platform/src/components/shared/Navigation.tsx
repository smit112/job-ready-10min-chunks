import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Home, 
  BookOpen, 
  Target, 
  TrendingUp, 
  Calculator, 
  Trophy, 
  Settings,
  Menu,
  X,
  Sun,
  Moon,
  ChevronDown
} from 'lucide-react';
import { useAppStore } from '../../stores/appStore';
import { tradingFundamentalsModule } from '../../data/lessons/tradingFundamentals';
import { optionsTradingModule } from '../../data/lessons/optionsTrading';

const Navigation: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [expandedModules, setExpandedModules] = useState<string[]>([]);
  const location = useLocation();
  const { theme, setTheme, progress } = useAppStore();

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      path: '/',
      icon: Home,
      badge: null,
    },
    {
      id: 'modules',
      label: 'Learning Modules',
      path: null,
      icon: BookOpen,
      badge: progress.completedLessons.length,
      children: [
        {
          id: 'trading-fundamentals',
          label: 'Trading Fundamentals',
          path: '/module/trading-fundamentals',
          icon: '📚',
          module: tradingFundamentalsModule,
        },
        {
          id: 'options-trading',
          label: 'Options Trading',
          path: '/module/options-trading',
          icon: '🎯',
          module: optionsTradingModule,
        },
        {
          id: 'swing-trading',
          label: 'Swing Trading',
          path: '/module/swing-trading',
          icon: '📈',
          module: null, // Will be created later
        },
      ],
    },
    {
      id: 'tools',
      label: 'Interactive Tools',
      path: null,
      icon: Calculator,
      badge: null,
      children: [
        {
          id: 'options-calculator',
          label: 'Options Calculator',
          path: '/tool/options-calculator',
          icon: '🧮',
        },
        {
          id: 'greeks-simulator',
          label: 'Greeks Simulator',
          path: '/tool/greeks-simulator',
          icon: '📊',
        },
        {
          id: 'chart-reader',
          label: 'Chart Reader',
          path: '/tool/chart-reader',
          icon: '📈',
        },
        {
          id: 'risk-calculator',
          label: 'Risk Calculator',
          path: '/tool/risk-calculator',
          icon: '⚠️',
        },
      ],
    },
    {
      id: 'progress',
      label: 'Progress',
      path: '/progress',
      icon: Trophy,
      badge: progress.achievements.length,
    },
  ];

  const toggleModule = (moduleId: string) => {
    setExpandedModules(prev => 
      prev.includes(moduleId) 
        ? prev.filter(id => id !== moduleId)
        : [...prev, moduleId]
    );
  };

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  const isActive = (path: string) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-lg bg-white shadow-lg"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Navigation */}
      <motion.nav
        initial={false}
        animate={{ x: isOpen ? 0 : '-100%' }}
        className={`fixed lg:static inset-y-0 left-0 z-40 w-64 bg-white dark:bg-gray-800 shadow-lg lg:shadow-none border-r border-gray-200 dark:border-gray-700 transform lg:transform-none transition-transform duration-300 ease-in-out`}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                Trading Academy
              </h1>
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
              </button>
            </div>
            
            {/* User progress summary */}
            <div className="mt-4 p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
              <div className="flex items-center justify-between text-sm">
                <span className="text-primary-700 dark:text-primary-300">Level {progress.level}</span>
                <span className="text-primary-600 dark:text-primary-400">{progress.totalXP} XP</span>
              </div>
              <div className="mt-2 w-full bg-primary-200 dark:bg-primary-800 rounded-full h-2">
                <div 
                  className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(progress.totalXP % 1000) / 10}%` }}
                />
              </div>
            </div>
          </div>

          {/* Navigation items */}
          <div className="flex-1 overflow-y-auto py-4">
            {navigationItems.map((item) => (
              <div key={item.id}>
                {item.children ? (
                  <div>
                    <button
                      onClick={() => toggleModule(item.id)}
                      className={`w-full flex items-center justify-between px-6 py-3 text-left hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors ${
                        expandedModules.includes(item.id) ? 'bg-gray-50 dark:bg-gray-700' : ''
                      }`}
                    >
                      <div className="flex items-center space-x-3">
                        <item.icon size={20} className="text-gray-600 dark:text-gray-400" />
                        <span className="font-medium text-gray-900 dark:text-white">
                          {item.label}
                        </span>
                        {item.badge && (
                          <span className="bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 text-xs px-2 py-1 rounded-full">
                            {item.badge}
                          </span>
                        )}
                      </div>
                      <ChevronDown 
                        size={16} 
                        className={`text-gray-400 transition-transform ${
                          expandedModules.includes(item.id) ? 'rotate-180' : ''
                        }`}
                      />
                    </button>
                    
                    <AnimatePresence>
                      {expandedModules.includes(item.id) && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.2 }}
                          className="overflow-hidden"
                        >
                          {item.children.map((child) => (
                            <Link
                              key={child.id}
                              to={child.path || '#'}
                              style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '0.75rem',
                                padding: '0.5rem 1.5rem',
                                fontSize: '0.875rem',
                                textDecoration: 'none',
                                color: isActive(child.path || '') ? '#1d4ed8' : '#6b7280',
                                backgroundColor: isActive(child.path || '') ? '#eff6ff' : 'transparent',
                                transition: 'all 0.2s'
                              }}
                            >
                              <span style={{ fontSize: '1.125rem' }}>{child.icon}</span>
                              <span>{child.label}</span>
                              {'module' in child && child.module && (
                                <div style={{ marginLeft: 'auto' }}>
                                  <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#10b981' }} />
                                </div>
                              )}
                            </Link>
                          ))}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                ) : (
                  <Link
                    to={item.path || '#'}
                    className={`flex items-center space-x-3 px-6 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors ${
                      isActive(item.path || '') ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 border-r-2 border-primary-600' : 'text-gray-600 dark:text-gray-400'
                    }`}
                  >
                    <item.icon size={20} />
                    <span className="font-medium">{item.label}</span>
                    {item.badge && (
                      <span className="ml-auto bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 text-xs px-2 py-1 rounded-full">
                        {item.badge}
                      </span>
                    )}
                  </Link>
                )}
              </div>
            ))}
          </div>

          {/* Footer */}
          <div className="p-6 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center space-x-3 text-sm text-gray-500 dark:text-gray-400">
              <Settings size={16} />
              <span>Settings</span>
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Overlay for mobile */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setIsOpen(false)}
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
        />
      )}
    </>
  );
};

export default Navigation;
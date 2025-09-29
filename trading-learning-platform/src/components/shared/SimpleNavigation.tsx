import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Home, 
  BookOpen, 
  Calculator, 
  Trophy, 
  Menu,
  X,
  Sun,
  Moon,
  ChevronDown
} from 'lucide-react';
import { useAppStore } from '../../stores/appStore';

const SimpleNavigation: React.FC = () => {
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
    },
    {
      id: 'modules',
      label: 'Learning Modules',
      path: null,
      icon: BookOpen,
      children: [
        {
          id: 'trading-fundamentals',
          label: 'Trading Fundamentals',
          path: '/module/trading-fundamentals',
          icon: '📚',
        },
        {
          id: 'options-trading',
          label: 'Options Trading',
          path: '/module/options-trading',
          icon: '🎯',
        },
        {
          id: 'swing-trading',
          label: 'Swing Trading',
          path: '/module/swing-trading',
          icon: '📈',
        },
      ],
    },
    {
      id: 'tools',
      label: 'Interactive Tools',
      path: null,
      icon: Calculator,
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
      ],
    },
    {
      id: 'progress',
      label: 'Progress',
      path: '/progress',
      icon: Trophy,
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

  const navStyle = {
    position: 'fixed' as const,
    top: 0,
    left: 0,
    bottom: 0,
    width: '256px',
    backgroundColor: 'white',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    borderRight: '1px solid #e5e7eb',
    zIndex: 40,
    transform: isOpen ? 'translateX(0)' : 'translateX(-100%)',
    transition: 'transform 0.3s ease-in-out'
  };

  const overlayStyle = {
    position: 'fixed' as const,
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    zIndex: 30
  };

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          top: '1rem',
          left: '1rem',
          zIndex: 50,
          padding: '0.5rem',
          borderRadius: '0.5rem',
          backgroundColor: 'white',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
          border: 'none',
          cursor: 'pointer'
        }}
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Navigation */}
      <nav style={navStyle}>
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
          {/* Header */}
          <div style={{ padding: '1.5rem', borderBottom: '1px solid #e5e7eb' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <h1 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#111827', margin: 0 }}>
                Trading Academy
              </h1>
              <button
                onClick={toggleTheme}
                style={{
                  padding: '0.5rem',
                  borderRadius: '0.5rem',
                  border: 'none',
                  backgroundColor: 'transparent',
                  cursor: 'pointer',
                  transition: 'background-color 0.2s'
                }}
              >
                {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
              </button>
            </div>
            
            {/* User progress summary */}
            <div style={{ 
              marginTop: '1rem', 
              padding: '0.75rem', 
              backgroundColor: '#eff6ff', 
              borderRadius: '0.5rem' 
            }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                <span style={{ color: '#1d4ed8' }}>Level {progress.level}</span>
                <span style={{ color: '#2563eb' }}>{progress.totalXP} XP</span>
              </div>
              <div style={{ marginTop: '0.5rem', width: '100%', backgroundColor: '#dbeafe', borderRadius: '9999px', height: '0.5rem' }}>
                <div 
                  style={{ 
                    backgroundColor: '#2563eb', 
                    height: '0.5rem', 
                    borderRadius: '9999px',
                    transition: 'width 0.3s',
                    width: `${(progress.totalXP % 1000) / 10}%` 
                  }}
                />
              </div>
            </div>
          </div>

          {/* Navigation items */}
          <div style={{ flex: 1, overflowY: 'auto', padding: '1rem 0' }}>
            {navigationItems.map((item) => (
              <div key={item.id}>
                {item.children ? (
                  <div>
                    <button
                      onClick={() => toggleModule(item.id)}
                      style={{
                        width: '100%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        padding: '0.75rem 1.5rem',
                        textAlign: 'left',
                        border: 'none',
                        backgroundColor: expandedModules.includes(item.id) ? '#f9fafb' : 'transparent',
                        cursor: 'pointer',
                        transition: 'background-color 0.2s'
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                        <item.icon size={20} style={{ color: '#6b7280' }} />
                        <span style={{ fontWeight: 500, color: '#111827' }}>
                          {item.label}
                        </span>
                      </div>
                      <ChevronDown 
                        size={16} 
                        style={{ 
                          color: '#9ca3af',
                          transform: expandedModules.includes(item.id) ? 'rotate(180deg)' : 'rotate(0deg)',
                          transition: 'transform 0.2s'
                        }}
                      />
                    </button>
                    
                    <AnimatePresence>
                      {expandedModules.includes(item.id) && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.2 }}
                          style={{ overflow: 'hidden' }}
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
                            </Link>
                          ))}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                ) : (
                  <Link
                    to={item.path || '#'}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.75rem',
                      padding: '0.75rem 1.5rem',
                      textDecoration: 'none',
                      color: isActive(item.path || '') ? '#1d4ed8' : '#6b7280',
                      backgroundColor: isActive(item.path || '') ? '#eff6ff' : 'transparent',
                      borderRight: isActive(item.path || '') ? '2px solid #2563eb' : 'none',
                      transition: 'all 0.2s'
                    }}
                  >
                    <item.icon size={20} />
                    <span style={{ fontWeight: 500 }}>{item.label}</span>
                  </Link>
                )}
              </div>
            ))}
          </div>
        </div>
      </nav>

      {/* Overlay for mobile */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setIsOpen(false)}
          style={overlayStyle}
        />
      )}
    </>
  );
};

export default SimpleNavigation;
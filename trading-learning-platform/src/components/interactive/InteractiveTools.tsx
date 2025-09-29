import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Calculator, 
  BarChart3, 
  Target, 
  TrendingUp,
  Zap,
  Shield,
  PieChart
} from 'lucide-react';
import OptionsCalculator from './OptionsCalculator';

const InteractiveTools: React.FC = () => {
  const [activeTool, setActiveTool] = useState<string | null>(null);

  const tools = [
    {
      id: 'options-calculator',
      title: 'Options P&L Calculator',
      description: 'Calculate profit and loss for options trades',
      icon: Calculator,
      color: 'from-primary-400 to-primary-600',
      bgColor: 'bg-primary-50 dark:bg-primary-900/20',
    },
    {
      id: 'greeks-simulator',
      title: 'Greeks Simulator',
      description: 'See how Greeks affect option prices',
      icon: BarChart3,
      color: 'from-success-400 to-success-600',
      bgColor: 'bg-success-50 dark:bg-success-900/20',
    },
    {
      id: 'risk-calculator',
      title: 'Risk Calculator',
      description: 'Calculate position sizing and risk',
      icon: Shield,
      color: 'from-warning-400 to-warning-600',
      bgColor: 'bg-warning-50 dark:bg-warning-900/20',
    },
    {
      id: 'chart-patterns',
      title: 'Chart Pattern Trainer',
      description: 'Practice identifying chart patterns',
      icon: TrendingUp,
      color: 'from-danger-400 to-danger-600',
      bgColor: 'bg-danger-50 dark:bg-danger-900/20',
    },
    {
      id: 'strategy-builder',
      title: 'Strategy Builder',
      description: 'Build and test options strategies',
      icon: Target,
      color: 'from-purple-400 to-purple-600',
      bgColor: 'bg-purple-50 dark:bg-purple-900/20',
    },
    {
      id: 'portfolio-analyzer',
      title: 'Portfolio Analyzer',
      description: 'Analyze your trading portfolio',
      icon: PieChart,
      color: 'from-indigo-400 to-indigo-600',
      bgColor: 'bg-indigo-50 dark:bg-indigo-900/20',
    },
  ];

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center py-12"
      >
        <div className="flex items-center justify-center space-x-2 mb-6">
          <Calculator className="w-8 h-8 text-primary-500" />
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
            Interactive Tools
          </h1>
        </div>
        <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
          Practice with our interactive calculators and simulators to master trading concepts
        </p>
      </motion.div>

      {/* Tools Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
      >
        {tools.map((tool, index) => (
          <motion.div
            key={tool.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 + index * 0.1 }}
            className={`${tool.bgColor} rounded-2xl p-8 hover:shadow-xl transition-all duration-300 cursor-pointer group`}
          >
            <div className={`w-16 h-16 bg-gradient-to-br ${tool.color} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
              <tool.icon className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
              {tool.title}
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              {tool.description}
            </p>
            <button
              onClick={() => setActiveTool(tool.id)}
              className="flex items-center text-primary-600 dark:text-primary-400 font-medium group-hover:translate-x-2 transition-transform"
            >
              {tool.id === 'options-calculator' ? 'Try Now' : 'Coming Soon'}
              <Zap className="w-4 h-4 ml-2" />
            </button>
          </motion.div>
        ))}
      </motion.div>

      {/* Active Tool Display */}
      {activeTool && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mt-12"
        >
          {activeTool === 'options-calculator' && (
            <OptionsCalculator />
          )}
        </motion.div>
      )}

      {/* Coming Soon Notice */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.8 }}
        className="mt-12 bg-gradient-to-r from-primary-50 to-primary-100 dark:from-primary-900/20 dark:to-primary-800/20 rounded-2xl p-8 text-center"
      >
        <Zap className="w-12 h-12 text-primary-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Interactive Tools Coming Soon!
        </h2>
        <p className="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
          We're working hard to bring you powerful interactive tools that will help you master 
          options trading and swing trading. These tools will include calculators, simulators, 
          and practice environments to reinforce your learning.
        </p>
      </motion.div>
    </div>
  );
};

export default InteractiveTools;
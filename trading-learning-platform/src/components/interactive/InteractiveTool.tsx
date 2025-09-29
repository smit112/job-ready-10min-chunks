import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Calculator, TrendingUp, Target, Shield } from 'lucide-react';
import InteractiveComponent from './InteractiveComponent';

const InteractiveTool: React.FC = () => {
  const { toolId } = useParams<{ toolId: string }>();
  const navigate = useNavigate();

  const toolInfo: Record<string, { title: string; description: string; icon: React.ComponentType<any> }> = {
    'options-calculator': {
      title: 'Options Calculator',
      description: 'Calculate profit, loss, and break-even points for your options trades',
      icon: Calculator
    },
    'greeks-simulator': {
      title: 'Greeks Simulator',
      description: 'Interactive tool to understand how Delta, Gamma, Theta, and Vega affect option prices',
      icon: TrendingUp
    },
    'chart-reader': {
      title: 'Chart Reader',
      description: 'Learn to read stock charts and identify patterns with interactive examples',
      icon: TrendingUp
    },
    'risk-calculator': {
      title: 'Risk Calculator',
      description: 'Calculate position sizes and risk management strategies',
      icon: Shield
    }
  };

  const tool = toolInfo[toolId || ''];

  if (!tool) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Tool Not Found
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          The interactive tool you're looking for doesn't exist.
        </p>
        <button
          onClick={() => navigate('/')}
          className="btn-primary"
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  const Icon = tool.icon;

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors mb-4"
        >
          <ArrowLeft size={20} />
          <span>Back to Dashboard</span>
        </button>

        <div className="flex items-center space-x-4 mb-6">
          <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/20 rounded-2xl flex items-center justify-center">
            <Icon size={32} className="text-primary-600 dark:text-primary-400" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              {tool.title}
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              {tool.description}
            </p>
          </div>
        </div>
      </div>

      {/* Tool Component */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <InteractiveComponent 
          component={toolId?.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join('') || ''} 
          params={{}} 
        />
      </motion.div>
    </div>
  );
};

export default InteractiveTool;
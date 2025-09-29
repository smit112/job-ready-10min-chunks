import React from 'react';
import { motion } from 'framer-motion';
import { Construction, Lightbulb, Target, TrendingUp, Calculator, ChartBar, Shield, BookOpen } from 'lucide-react';

// Placeholder component for interactive tools that aren't implemented yet
const PlaceholderComponent: React.FC<{ 
  title: string; 
  description: string; 
  icon: React.ComponentType<any>;
  features: string[];
}> = ({ title, description, icon: Icon, features }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="text-center py-12"
    >
      <div className="mb-8">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
          className="w-24 h-24 mx-auto mb-6 rounded-full bg-primary-100 dark:bg-primary-900/20 flex items-center justify-center"
        >
          <Icon size={48} className="text-primary-600 dark:text-primary-400" />
        </motion.div>
        
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          {title}
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md mx-auto">
          {description}
        </p>
      </div>

      <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6 mb-8">
        <div className="flex items-center justify-center space-x-2 mb-3">
          <Construction size={20} className="text-yellow-600 dark:text-yellow-400" />
          <span className="font-semibold text-yellow-800 dark:text-yellow-200">
            Coming Soon!
          </span>
        </div>
        <p className="text-yellow-700 dark:text-yellow-300 text-sm">
          This interactive tool is currently under development. Check back soon for an amazing learning experience!
        </p>
      </div>

      <div className="max-w-md mx-auto">
        <h3 className="font-semibold text-gray-900 dark:text-white mb-4">
          What you'll be able to do:
        </h3>
        <div className="space-y-2">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 + index * 0.1 }}
              className="flex items-center space-x-3 text-left"
            >
              <div className="w-2 h-2 bg-primary-500 rounded-full" />
              <span className="text-gray-700 dark:text-gray-300 text-sm">
                {feature}
              </span>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
};

// Individual placeholder components
export const GreeksSimulator: React.FC = () => (
  <PlaceholderComponent
    title="Greeks Simulator"
    description="Interactive tool to understand how Delta, Gamma, Theta, and Vega affect option prices"
    icon={TrendingUp}
    features={[
      "Adjust stock price and see how Greeks change",
      "Visual representation of option sensitivity",
      "Real-time calculations with sliders",
      "Educational explanations for each Greek"
    ]}
  />
);

export const ChartReader: React.FC = () => (
  <PlaceholderComponent
    title="Chart Reader"
    description="Learn to read stock charts and identify patterns with interactive examples"
    icon={ChartBar}
    features={[
      "Interactive chart with real stock data",
      "Pattern recognition exercises",
      "Support and resistance identification",
      "Technical indicator explanations"
    ]}
  />
);

export const RiskCalculator: React.FC = () => (
  <PlaceholderComponent
    title="Risk Calculator"
    description="Calculate position sizes and risk management strategies"
    icon={Shield}
    features={[
      "Position sizing based on account size",
      "Risk-reward ratio calculations",
      "Stop-loss and take-profit planning",
      "Portfolio risk assessment"
    ]}
  />
);

export const StockMarketSimulator: React.FC = () => (
  <PlaceholderComponent
    title="Stock Market Simulator"
    description="Practice trading with virtual money in a simulated market environment"
    icon={TrendingUp}
    features={[
      "Virtual trading with $10,000 starting capital",
      "Real-time market data simulation",
      "Portfolio tracking and performance metrics",
      "Risk-free learning environment"
    ]}
  />
);

export const OptionsBasicsSimulator: React.FC = () => (
  <PlaceholderComponent
    title="Options Basics Simulator"
    description="Interactive tool to understand the fundamentals of options trading"
    icon={Lightbulb}
    features={[
      "Movie theater coupon analogy demonstration",
      "Call vs Put option comparisons",
      "Strike price and expiration examples",
      "Step-by-step option buying process"
    ]}
  />
);

export const CallsPutsSimulator: React.FC = () => (
  <PlaceholderComponent
    title="Calls vs Puts Simulator"
    description="Visual comparison of call and put options with real examples"
    icon={Target}
    features={[
      "Side-by-side call and put comparisons",
      "Profit/loss scenarios for both types",
      "When to use calls vs puts",
      "Real stock examples with calculations"
    ]}
  />
);

export const StrikePriceVisualizer: React.FC = () => (
  <PlaceholderComponent
    title="Strike Price Visualizer"
    description="Understand ITM, OTM, and ATM options with visual examples"
    icon={Target}
    features={[
      "Visual representation of strike prices",
      "ITM/OTM/ATM identification",
      "Profit potential at different strikes",
      "Interactive strike price selection"
    ]}
  />
);

export const OptionsPricingCalculator: React.FC = () => (
  <PlaceholderComponent
    title="Options Pricing Calculator"
    description="Deep dive into intrinsic value vs time value with the ice cream analogy"
    icon={Calculator}
    features={[
      "Intrinsic value calculations",
      "Time value decay visualization",
      "Ice cream cone analogy demonstration",
      "Premium breakdown analysis"
    ]}
  />
);

export const DeltaGammaSimulator: React.FC = () => (
  <PlaceholderComponent
    title="Delta & Gamma Simulator"
    description="Car analogies to understand Delta (speedometer) and Gamma (accelerator)"
    icon={TrendingUp}
    features={[
      "Speedometer analogy for Delta",
      "Accelerator analogy for Gamma",
      "Interactive sliders for price changes",
      "Real-time Greek calculations"
    ]}
  />
);

export const ThetaVegaSimulator: React.FC = () => (
  <PlaceholderComponent
    title="Theta & Vega Simulator"
    description="Weather analogies for time decay and volatility sensitivity"
    icon={TrendingUp}
    features={[
      "Leaky bucket analogy for Theta",
      "Weather sensitivity for Vega",
      "Time decay visualization",
      "Volatility impact demonstrations"
    ]}
  />
);

export const BasicPositionsSimulator: React.FC = () => (
  <PlaceholderComponent
    title="Basic Positions Simulator"
    description="Learn the four fundamental options positions with interactive examples"
    icon={Target}
    features={[
      "Four basic positions demonstration",
      "Risk/reward profiles for each",
      "When to use each position",
      "Interactive profit/loss scenarios"
    ]}
  />
);

export const CoveredCallCalculator: React.FC = () => (
  <PlaceholderComponent
    title="Covered Call Calculator"
    description="Car rental analogy for generating income with covered calls"
    icon={Calculator}
    features={[
      "Income generation calculations",
      "Risk scenarios and management",
      "Car rental analogy demonstration",
      "Real stock examples"
    ]}
  />
);

export const ProtectivePutCalculator: React.FC = () => (
  <PlaceholderComponent
    title="Protective Put Calculator"
    description="Car insurance analogy for protecting your stock investments"
    icon={Shield}
    features={[
      "Insurance cost calculations",
      "Protection level analysis",
      "Car insurance analogy",
      "Cost-benefit analysis"
    ]}
  />
);

export const OrderTypeSimulator: React.FC = () => (
  <PlaceholderComponent
    title="Order Type Simulator"
    description="Restaurant analogy for understanding market vs limit orders"
    icon={BookOpen}
    features={[
      "Restaurant ordering analogy",
      "Market vs limit order comparisons",
      "Price impact demonstrations",
      "When to use each order type"
    ]}
  />
);

export const RiskRewardCalculator: React.FC = () => (
  <PlaceholderComponent
    title="Risk Reward Calculator"
    description="Roller coaster analogy for understanding risk vs reward"
    icon={TrendingUp}
    features={[
      "Roller coaster vs carousel analogy",
      "Risk-reward ratio calculations",
      "Conservative vs aggressive strategies",
      "Visual risk assessment"
    ]}
  />
);

export const PaperTradingSimulator: React.FC = () => (
  <PlaceholderComponent
    title="Paper Trading Simulator"
    description="Video game practice mode for learning to trade without risk"
    icon={Target}
    features={[
      "Virtual trading environment",
      "Real market data simulation",
      "Practice mode tutorials",
      "Beginner-friendly scenarios"
    ]}
  />
);
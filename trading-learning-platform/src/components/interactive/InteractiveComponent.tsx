import React from 'react';
import OptionsCalculator from './OptionsCalculator';
import {
  GreeksSimulator,
  ChartReader,
  RiskCalculator,
  StockMarketSimulator,
  OptionsBasicsSimulator,
  CallsPutsSimulator,
  StrikePriceVisualizer,
  OptionsPricingCalculator,
  DeltaGammaSimulator,
  ThetaVegaSimulator,
  BasicPositionsSimulator,
  CoveredCallCalculator,
  ProtectivePutCalculator,
  OrderTypeSimulator,
  RiskRewardCalculator,
  PaperTradingSimulator
} from './PlaceholderComponents';

interface InteractiveComponentProps {
  component: string;
  params: Record<string, any>;
}

const InteractiveComponent: React.FC<InteractiveComponentProps> = ({ 
  component, 
  params 
}) => {
  const components: Record<string, React.ComponentType<any>> = {
    'OptionsCalculator': OptionsCalculator,
    'GreeksSimulator': GreeksSimulator,
    'ChartReader': ChartReader,
    'RiskCalculator': RiskCalculator,
    'StockMarketSimulator': StockMarketSimulator,
    'OptionsBasicsSimulator': OptionsBasicsSimulator,
    'CallsPutsSimulator': CallsPutsSimulator,
    'StrikePriceVisualizer': StrikePriceVisualizer,
    'OptionsPricingCalculator': OptionsPricingCalculator,
    'DeltaGammaSimulator': DeltaGammaSimulator,
    'ThetaVegaSimulator': ThetaVegaSimulator,
    'BasicPositionsSimulator': BasicPositionsSimulator,
    'CoveredCallCalculator': CoveredCallCalculator,
    'ProtectivePutCalculator': ProtectivePutCalculator,
    'OrderTypeSimulator': OrderTypeSimulator,
    'RiskRewardCalculator': RiskRewardCalculator,
    'PaperTradingSimulator': PaperTradingSimulator,
  };

  const Component = components[component];

  if (!Component) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 dark:text-gray-400 mb-4">
          Interactive component "{component}" not found
        </div>
        <div className="text-sm text-gray-400 dark:text-gray-500">
          This feature is coming soon!
        </div>
      </div>
    );
  }

  return <Component {...params} />;
};

export default InteractiveComponent;
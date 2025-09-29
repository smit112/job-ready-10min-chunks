import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Calculator, TrendingUp, TrendingDown } from 'lucide-react';

interface OptionsCalculatorProps {
  initialStockPrice?: number;
  initialStrikePrice?: number;
  initialPremium?: number;
}

const OptionsCalculator: React.FC<OptionsCalculatorProps> = ({
  initialStockPrice = 150,
  initialStrikePrice = 160,
  initialPremium = 5
}) => {
  const [stockPrice, setStockPrice] = useState(initialStockPrice);
  const [strikePrice, setStrikePrice] = useState(initialStrikePrice);
  const [premium, setPremium] = useState(initialPremium);
  const [optionType, setOptionType] = useState<'call' | 'put'>('call');

  // Calculate P&L for different stock prices
  const calculatePnL = (currentStockPrice: number) => {
    if (optionType === 'call') {
      const intrinsicValue = Math.max(0, currentStockPrice - strikePrice);
      const totalValue = intrinsicValue;
      const profitLoss = totalValue - premium;
      return {
        intrinsicValue,
        totalValue,
        profitLoss,
        percentage: (profitLoss / premium) * 100
      };
    } else {
      const intrinsicValue = Math.max(0, strikePrice - currentStockPrice);
      const totalValue = intrinsicValue;
      const profitLoss = totalValue - premium;
      return {
        intrinsicValue,
        totalValue,
        profitLoss,
        percentage: (profitLoss / premium) * 100
      };
    }
  };

  const currentPnL = calculatePnL(stockPrice);
  const isITM = optionType === 'call' ? stockPrice > strikePrice : stockPrice < strikePrice;
  const isOTM = optionType === 'call' ? stockPrice < strikePrice : stockPrice > strikePrice;
  const isATM = stockPrice === strikePrice;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
      <div className="flex items-center space-x-3 mb-6">
        <Calculator className="w-6 h-6 text-primary-600 dark:text-primary-400" />
        <h3 className="text-xl font-bold text-gray-900 dark:text-white">
          Options P&L Calculator
        </h3>
      </div>

      {/* Input Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Option Type
          </label>
          <div className="flex space-x-4">
            <button
              onClick={() => setOptionType('call')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                optionType === 'call'
                  ? 'bg-success-600 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
              }`}
            >
              Call Option
            </button>
            <button
              onClick={() => setOptionType('put')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                optionType === 'put'
                  ? 'bg-danger-600 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
              }`}
            >
              Put Option
            </button>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Current Stock Price
          </label>
          <input
            type="number"
            value={stockPrice}
            onChange={(e) => setStockPrice(Number(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Strike Price
          </label>
          <input
            type="number"
            value={strikePrice}
            onChange={(e) => setStrikePrice(Number(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Premium Paid
          </label>
          <input
            type="number"
            value={premium}
            onChange={(e) => setPremium(Number(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
        </div>
      </div>

      {/* Results */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Intrinsic Value</div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            ${currentPnL.intrinsicValue.toFixed(2)}
          </div>
        </div>
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Value</div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            ${currentPnL.totalValue.toFixed(2)}
          </div>
        </div>
        <div className={`rounded-lg p-4 ${
          currentPnL.profitLoss >= 0 
            ? 'bg-success-50 dark:bg-success-900/20' 
            : 'bg-danger-50 dark:bg-danger-900/20'
        }`}>
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Profit/Loss</div>
          <div className={`text-2xl font-bold ${
            currentPnL.profitLoss >= 0 
              ? 'text-success-600 dark:text-success-400' 
              : 'text-danger-600 dark:text-danger-400'
          }`}>
            ${currentPnL.profitLoss.toFixed(2)}
          </div>
        </div>
      </div>

      {/* Money Status */}
      <div className="mb-6">
        <div className="flex items-center space-x-2 mb-2">
          {isITM && <TrendingUp className="w-5 h-5 text-success-500" />}
          {isOTM && <TrendingDown className="w-5 h-5 text-danger-500" />}
          {isATM && <div className="w-5 h-5 bg-warning-500 rounded-full" />}
          <span className="font-medium text-gray-900 dark:text-white">
            {isITM ? 'In-The-Money (ITM)' : isOTM ? 'Out-of-The-Money (OTM)' : 'At-The-Money (ATM)'}
          </span>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          {isITM 
            ? 'Your option has real value! You can exercise it for a profit.'
            : isOTM 
              ? 'Your option has no intrinsic value. It\'s only worth the time value.'
              : 'Your option is exactly at the strike price. Any movement will make it ITM or OTM.'
          }
        </p>
      </div>

      {/* P&L Chart */}
      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
        <h4 className="font-medium text-gray-900 dark:text-white mb-4">
          Profit/Loss at Different Stock Prices
        </h4>
        <div className="space-y-2">
          {[stockPrice - 20, stockPrice - 10, stockPrice, stockPrice + 10, stockPrice + 20].map((price) => {
            const pnl = calculatePnL(price);
            return (
              <div key={price} className="flex items-center justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-300">
                  ${price.toFixed(0)}
                </span>
                <span className={`text-sm font-medium ${
                  pnl.profitLoss >= 0 
                    ? 'text-success-600 dark:text-success-400' 
                    : 'text-danger-600 dark:text-danger-400'
                }`}>
                  {pnl.profitLoss >= 0 ? '+' : ''}${pnl.profitLoss.toFixed(2)}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default OptionsCalculator;
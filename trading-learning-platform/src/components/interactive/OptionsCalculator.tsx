import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, DollarSign, Target, Clock } from 'lucide-react';

interface OptionsCalculatorProps {
  showIntrinsicTimeValue?: boolean;
  showTimeDecay?: boolean;
  interactiveMode?: boolean;
}

const OptionsCalculator: React.FC<OptionsCalculatorProps> = ({
  showIntrinsicTimeValue = true,
  showTimeDecay = true,
  interactiveMode = true
}) => {
  const [stockPrice, setStockPrice] = useState(150);
  const [strikePrice, setStrikePrice] = useState(155);
  const [premium, setPremium] = useState(3.50);
  const [expirationDays, setExpirationDays] = useState(30);
  const [optionType, setOptionType] = useState<'call' | 'put'>('call');
  const [position, setPosition] = useState<'long' | 'short'>('long');
  const [quantity, setQuantity] = useState(1);

  // Calculate intrinsic value
  const intrinsicValue = optionType === 'call' 
    ? Math.max(0, stockPrice - strikePrice)
    : Math.max(0, strikePrice - stockPrice);

  // Calculate time value (simplified)
  const timeValue = Math.max(0, premium - intrinsicValue);

  // Calculate profit/loss at different stock prices
  const calculatePnL = (currentStockPrice: number) => {
    const currentIntrinsic = optionType === 'call' 
      ? Math.max(0, currentStockPrice - strikePrice)
      : Math.max(0, strikePrice - currentStockPrice);
    
    const currentOptionValue = currentIntrinsic + (timeValue * (expirationDays / 30));
    
    if (position === 'long') {
      return (currentOptionValue - premium) * quantity;
    } else {
      return (premium - currentOptionValue) * quantity;
    }
  };

  // Generate P&L data for chart
  const generatePnLData = () => {
    const data = [];
    const minPrice = Math.min(stockPrice, strikePrice) * 0.8;
    const maxPrice = Math.max(stockPrice, strikePrice) * 1.2;
    
    for (let price = minPrice; price <= maxPrice; price += (maxPrice - minPrice) / 20) {
      data.push({
        stockPrice: price,
        profitLoss: calculatePnL(price),
        intrinsic: optionType === 'call' 
          ? Math.max(0, price - strikePrice)
          : Math.max(0, strikePrice - price)
      });
    }
    
    return data;
  };

  const pnlData = generatePnLData();
  const currentPnL = calculatePnL(stockPrice);
  const maxProfit = position === 'long' ? 'Unlimited' : premium * quantity;
  const maxLoss = position === 'long' ? premium * quantity : 'Unlimited';

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          Options Profit & Loss Calculator
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          See how your option position performs at different stock prices
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Panel */}
        <div className="card">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Option Parameters
          </h4>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Stock Price
              </label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
                <input
                  type="number"
                  value={stockPrice}
                  onChange={(e) => setStockPrice(Number(e.target.value))}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Strike Price
              </label>
              <div className="relative">
                <Target className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
                <input
                  type="number"
                  value={strikePrice}
                  onChange={(e) => setStrikePrice(Number(e.target.value))}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Premium Paid
              </label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
                <input
                  type="number"
                  step="0.01"
                  value={premium}
                  onChange={(e) => setPremium(Number(e.target.value))}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Days to Expiration
              </label>
              <div className="relative">
                <Clock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
                <input
                  type="number"
                  value={expirationDays}
                  onChange={(e) => setExpirationDays(Number(e.target.value))}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Option Type
                </label>
                <select
                  value={optionType}
                  onChange={(e) => setOptionType(e.target.value as 'call' | 'put')}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                >
                  <option value="call">Call</option>
                  <option value="put">Put</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Position
                </label>
                <select
                  value={position}
                  onChange={(e) => setPosition(e.target.value as 'long' | 'short')}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                >
                  <option value="long">Long (Buy)</option>
                  <option value="short">Short (Sell)</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Quantity
              </label>
              <input
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(Number(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>
          </div>
        </div>

        {/* Results Panel */}
        <div className="card">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Current Position Analysis
          </h4>

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-600 dark:text-gray-400">Current P&L</div>
                <div className={`text-xl font-bold ${currentPnL >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                  ${currentPnL.toFixed(2)}
                </div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-600 dark:text-gray-400">Intrinsic Value</div>
                <div className="text-xl font-bold text-gray-900 dark:text-white">
                  ${intrinsicValue.toFixed(2)}
                </div>
              </div>
            </div>

            {showIntrinsicTimeValue && (
              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                <h5 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
                  Premium Breakdown
                </h5>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-blue-800 dark:text-blue-200">Intrinsic Value:</span>
                    <span className="font-medium">${intrinsicValue.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-blue-800 dark:text-blue-200">Time Value:</span>
                    <span className="font-medium">${timeValue.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between border-t border-blue-200 dark:border-blue-800 pt-2">
                    <span className="text-blue-800 dark:text-blue-200 font-semibold">Total Premium:</span>
                    <span className="font-bold">${premium.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            )}

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
                <div className="text-sm text-green-600 dark:text-green-400">Max Profit</div>
                <div className="text-lg font-bold text-green-700 dark:text-green-300">
                  {maxProfit}
                </div>
              </div>
              <div className="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg">
                <div className="text-sm text-red-600 dark:text-red-400">Max Loss</div>
                <div className="text-lg font-bold text-red-700 dark:text-red-300">
                  {maxLoss}
                </div>
              </div>
            </div>

            <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
              <h5 className="font-semibold text-yellow-900 dark:text-yellow-100 mb-2">
                Break-Even Point
              </h5>
              <div className="text-lg font-bold text-yellow-800 dark:text-yellow-200">
                {optionType === 'call' 
                  ? `$${(strikePrice + premium).toFixed(2)}`
                  : `$${(strikePrice - premium).toFixed(2)}`
                }
              </div>
              <div className="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                Stock needs to be at this price to break even
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* P&L Chart */}
      <div className="card">
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Profit & Loss at Different Stock Prices
        </h4>
        
        <div className="h-64 bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
          <div className="h-full flex items-end justify-between space-x-1">
            {pnlData.map((point, index) => (
              <motion.div
                key={index}
                initial={{ height: 0 }}
                animate={{ height: `${Math.abs(point.profitLoss) * 2 + 20}px` }}
                transition={{ delay: index * 0.01 }}
                className={`flex-1 rounded-t ${
                  point.profitLoss >= 0 
                    ? 'bg-green-500' 
                    : 'bg-red-500'
                }`}
                title={`Stock: $${point.stockPrice.toFixed(0)}, P&L: $${point.profitLoss.toFixed(2)}`}
              />
            ))}
          </div>
          
          <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400 mt-2">
            <span>${Math.min(...pnlData.map(p => p.stockPrice)).toFixed(0)}</span>
            <span>Current: ${stockPrice}</span>
            <span>${Math.max(...pnlData.map(p => p.stockPrice)).toFixed(0)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OptionsCalculator;
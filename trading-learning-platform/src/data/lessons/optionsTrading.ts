import { Lesson, Module } from '../../types';

export const optionsTradingModule: Module = {
  id: 'options-trading',
  title: 'Options Trading Mastery',
  description: 'Master options trading from basics to advanced strategies with simple analogies',
  icon: '🎯',
  color: 'bg-green-500',
  lessons: [],
  isCompleted: false,
  progress: 0,
  unlocked: false, // Unlocked after completing trading fundamentals
};

export const optionsTradingLessons: Lesson[] = [
  // Sub-module 2A: Options Basics
  {
    id: 'options-basics-1',
    title: 'What Are Options?',
    description: 'Learn what options are using the movie theater coupon analogy',
    module: optionsTradingModule,
    subModule: 'Options Basics',
    difficulty: 'beginner',
    estimatedTime: 15,
    xpReward: 150,
    prerequisites: ['paper-trading-intro'],
    content: [
      {
        type: 'explanation',
        title: 'Options: Movie Theater Coupons',
        text: 'Options are like movie theater coupons! You pay a small amount (premium) to buy a coupon that gives you the right to buy a movie ticket at a specific price (strike price) before the coupon expires (expiration date).',
        analogy: 'Movie theater coupon system'
      },
      {
        type: 'explanation',
        title: 'Key Terms',
        text: 'Premium: The cost to buy the option (like the cost of the coupon). Strike Price: The guaranteed price you can buy/sell at (like the ticket price on your coupon). Expiration: When the option expires (like the coupon deadline).',
      },
      {
        type: 'interactive',
        component: 'OptionsBasicsSimulator',
        params: { 
          example: 'movie-coupon',
          showVisualization: true,
          interactiveMode: true
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'calls-vs-puts',
    title: 'Calls vs Puts',
    description: 'Understanding the difference between call and put options',
    module: optionsTradingModule,
    subModule: 'Options Basics',
    difficulty: 'beginner',
    estimatedTime: 18,
    xpReward: 180,
    prerequisites: ['options-basics-1'],
    content: [
      {
        type: 'explanation',
        title: 'Calls: Buying Coupons',
        text: 'Call options are like coupons that let you BUY something at a guaranteed price. If Apple stock costs $150 but you have a call option with a $140 strike price, you can buy Apple stock for $140 even if it goes up to $200!',
        analogy: 'Buying coupons for future purchases'
      },
      {
        type: 'explanation',
        title: 'Puts: Insurance Policies',
        text: 'Put options are like insurance policies that let you SELL something at a guaranteed price. If you own Apple stock at $150 but have a put option with a $160 strike price, you can sell it for $160 even if the stock drops to $100!',
        analogy: 'Insurance policy for your investments'
      },
      {
        type: 'interactive',
        component: 'CallsPutsSimulator',
        params: { 
          stock: 'AAPL',
          scenarios: ['bullish-call', 'bearish-put'],
          showProfitLoss: true
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'strike-prices',
    title: 'Strike Prices Explained',
    description: 'Understanding ITM, OTM, and ATM options',
    module: optionsTradingModule,
    subModule: 'Options Basics',
    difficulty: 'beginner',
    estimatedTime: 12,
    xpReward: 120,
    prerequisites: ['calls-vs-puts'],
    content: [
      {
        type: 'explanation',
        title: 'Strike Prices: The Target Zone',
        text: 'Think of strike prices like targets in archery. In-The-Money (ITM) means you hit the bullseye - your option is profitable right now. Out-of-The-Money (OTM) means you missed the target - your option needs the stock to move to be profitable.',
        analogy: 'Archery target practice'
      },
      {
        type: 'explanation',
        title: 'ITM, OTM, ATM',
        text: 'ITM (In-The-Money): Option is profitable right now. OTM (Out-of-The-Money): Option needs stock to move to be profitable. ATM (At-The-Money): Strike price equals current stock price.',
      },
      {
        type: 'interactive',
        component: 'StrikePriceVisualizer',
        params: { 
          stock: 'AAPL',
          currentPrice: 150,
          strikes: [140, 145, 150, 155, 160],
          showITMOTM: true
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'exercise-vs-sell',
    title: 'Exercise vs Selling Options',
    description: 'When to exercise your options vs selling them',
    module: optionsTradingModule,
    subModule: 'Options Basics',
    difficulty: 'beginner',
    estimatedTime: 10,
    xpReward: 100,
    prerequisites: ['strike-prices'],
    content: [
      {
        type: 'explanation',
        title: 'Exercise vs Sell: The Coupon Decision',
        text: 'When you have a valuable coupon, you can either use it (exercise) to get the item, or sell the coupon to someone else for a profit. Most option traders sell their options rather than exercise them!',
        analogy: 'Using vs selling valuable coupons'
      },
      {
        type: 'explanation',
        title: 'When to Exercise',
        text: 'Exercise when: You want to own the stock, the option is deep ITM, or near expiration. Sell when: You want to take profits, avoid assignment risk, or the option has time value left.',
      }
    ],
    isCompleted: false,
    progress: 0,
  },

  // Sub-module 2B: Options Pricing & Greeks
  {
    id: 'options-pricing',
    title: 'Options Pricing: Intrinsic vs Time Value',
    description: 'Understanding how options are priced using the melting ice cream analogy',
    module: optionsTradingModule,
    subModule: 'Options Pricing & Greeks',
    difficulty: 'intermediate',
    estimatedTime: 20,
    xpReward: 200,
    prerequisites: ['exercise-vs-sell'],
    content: [
      {
        type: 'explanation',
        title: 'Options Pricing: The Ice Cream Analogy',
        text: 'Option pricing is like an ice cream cone! The intrinsic value is the actual ice cream (how much the option is worth right now). The time value is like the cone - it melts away as time passes (time decay).',
        analogy: 'Ice cream cone with melting cone'
      },
      {
        type: 'explanation',
        title: 'Intrinsic Value',
        text: 'Intrinsic value is the immediate value if you exercised the option right now. For calls: max(0, stock price - strike price). For puts: max(0, strike price - stock price).',
      },
      {
        type: 'explanation',
        title: 'Time Value',
        text: 'Time value is the extra amount you pay for the possibility that the option becomes more valuable before expiration. This "melts away" as time passes.',
      },
      {
        type: 'interactive',
        component: 'OptionsPricingCalculator',
        params: { 
          showIntrinsicTimeValue: true,
          showTimeDecay: true,
          interactiveMode: true
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'delta-gamma',
    title: 'Delta & Gamma: The Speedometer & Accelerator',
    description: 'Understanding Delta and Gamma using car analogies',
    module: optionsTradingModule,
    subModule: 'Options Pricing & Greeks',
    difficulty: 'intermediate',
    estimatedTime: 18,
    xpReward: 180,
    prerequisites: ['options-pricing'],
    content: [
      {
        type: 'explanation',
        title: 'Delta: The Speedometer',
        text: 'Delta is like a speedometer for your option. It tells you how fast your option price changes when the stock price moves. A delta of 0.5 means your option price moves $0.50 for every $1 the stock moves.',
        analogy: 'Car speedometer showing speed'
      },
      {
        type: 'explanation',
        title: 'Gamma: The Accelerator',
        text: 'Gamma is like the accelerator pedal. It tells you how much your delta changes when the stock moves. High gamma means your delta changes quickly - like pressing the gas pedal hard!',
        analogy: 'Car accelerator pedal'
      },
      {
        type: 'interactive',
        component: 'DeltaGammaSimulator',
        params: { 
          showSpeedometer: true,
          showAccelerator: true,
          stockMovement: 'interactive'
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'theta-vega',
    title: 'Theta & Vega: Time Decay & Volatility',
    description: 'Understanding Theta and Vega using weather analogies',
    module: optionsTradingModule,
    subModule: 'Options Pricing & Greeks',
    difficulty: 'intermediate',
    estimatedTime: 16,
    xpReward: 160,
    prerequisites: ['delta-gamma'],
    content: [
      {
        type: 'explanation',
        title: 'Theta: The Daily Value Loss',
        text: 'Theta is like a leaky bucket - it shows how much value your option loses each day due to time passing. Every day, your option becomes less valuable, just like water leaking out of a bucket.',
        analogy: 'Leaky bucket losing water daily'
      },
      {
        type: 'explanation',
        title: 'Vega: Weather Sensitivity',
        text: 'Vega is like how sensitive you are to weather changes. When market volatility (the "weather") changes, vega tells you how much your option price will change. Stormy markets = higher option prices!',
        analogy: 'Weather sensitivity for outdoor activities'
      },
      {
        type: 'interactive',
        component: 'ThetaVegaSimulator',
        params: { 
          showTimeDecay: true,
          showVolatilityImpact: true,
          scenarios: ['calm-market', 'stormy-market']
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  },

  // Sub-module 2C: Options Strategies
  {
    id: 'basic-positions',
    title: '4 Basic Options Positions',
    description: 'Learn the four fundamental options positions',
    module: optionsTradingModule,
    subModule: 'Options Strategies',
    difficulty: 'intermediate',
    estimatedTime: 15,
    xpReward: 150,
    prerequisites: ['theta-vega'],
    content: [
      {
        type: 'explanation',
        title: 'The Four Basic Positions',
        text: 'There are only four basic things you can do with options: 1) Buy calls (bullish), 2) Sell calls (bearish/neutral), 3) Buy puts (bearish), 4) Sell puts (bullish/neutral). Everything else is a combination of these!',
      },
      {
        type: 'interactive',
        component: 'BasicPositionsSimulator',
        params: { 
          positions: ['buy-call', 'sell-call', 'buy-put', 'sell-put'],
          showRiskReward: true,
          showScenarios: true
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'covered-calls',
    title: 'Covered Calls: Income Strategy',
    description: 'Learn how to generate income with covered calls',
    module: optionsTradingModule,
    subModule: 'Options Strategies',
    difficulty: 'intermediate',
    estimatedTime: 20,
    xpReward: 200,
    prerequisites: ['basic-positions'],
    content: [
      {
        type: 'explanation',
        title: 'Covered Calls: Renting Out Your Car',
        text: 'Covered calls are like renting out your car while you\'re not using it. You own the stock (your car) and sell call options (rent it out) to collect premium (rental income). If the stock goes up too much, you might have to sell it (lose your car), but you keep the rental income!',
        analogy: 'Renting out your car for extra income'
      },
      {
        type: 'explanation',
        title: 'When to Use Covered Calls',
        text: 'Use covered calls when: You own stock you\'re willing to sell, you expect the stock to stay flat or rise slowly, you want to generate income from your holdings.',
      },
      {
        type: 'interactive',
        component: 'CoveredCallCalculator',
        params: { 
          stock: 'AAPL',
          showIncomeGeneration: true,
          showRiskScenarios: true
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'protective-puts',
    title: 'Protective Puts: Insurance Strategy',
    description: 'Learn how to protect your stock with put options',
    module: optionsTradingModule,
    subModule: 'Options Strategies',
    difficulty: 'intermediate',
    estimatedTime: 18,
    xpReward: 180,
    prerequisites: ['covered-calls'],
    content: [
      {
        type: 'explanation',
        title: 'Protective Puts: Car Insurance',
        text: 'Protective puts are like car insurance for your stock. You pay a premium (insurance cost) to protect your stock from big losses. If your stock crashes, your put option pays you the difference, just like insurance covers your car damage!',
        analogy: 'Car insurance for your investments'
      },
      {
        type: 'explanation',
        title: 'When to Use Protective Puts',
        text: 'Use protective puts when: You want to protect against big losses, you\'re holding stock long-term, you\'re worried about market crashes, you want to limit downside risk.',
      },
      {
        type: 'interactive',
        component: 'ProtectivePutCalculator',
        params: { 
          stock: 'AAPL',
          showProtectionLevel: true,
          showCostBenefit: true
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  }
];

// Update the module with lessons
optionsTradingModule.lessons = optionsTradingLessons;
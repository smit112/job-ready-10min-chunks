import { Lesson, Module } from '../../types';

export const tradingFundamentalsModule: Module = {
  id: 'trading-fundamentals',
  title: 'Trading Fundamentals',
  description: 'Learn the basics of trading and investing with simple, child-friendly explanations',
  icon: '📚',
  color: 'bg-blue-500',
  lessons: [],
  isCompleted: false,
  progress: 0,
  unlocked: true,
};

export const tradingFundamentalsLessons: Lesson[] = [
  {
    id: 'what-is-trading',
    title: 'What is Trading vs Investing?',
    description: 'Learn the difference between trading and investing using simple analogies',
    module: tradingFundamentalsModule,
    difficulty: 'beginner',
    estimatedTime: 10,
    xpReward: 100,
    prerequisites: [],
    content: [
      {
        type: 'explanation',
        title: 'Trading vs Investing: The Lemonade Stand Story',
        text: 'Imagine you have a lemonade stand. Trading is like buying and selling lemonade ingredients quickly to make small profits each day. Investing is like planting lemon trees in your backyard - you wait patiently for them to grow and give you lemons for years to come!',
        analogy: 'Lemonade stand vs lemon tree garden'
      },
      {
        type: 'explanation',
        title: 'Key Differences',
        text: 'Trading: Short-term (days to months), active buying/selling, higher risk, potential for quick profits. Investing: Long-term (years), buy and hold, lower risk, steady growth over time.',
      },
      {
        type: 'example',
        title: 'Real World Example',
        text: 'Trading: Buying Apple stock today and selling it next week if it goes up. Investing: Buying Apple stock and holding it for 10 years as the company grows.',
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'stock-market-basics',
    title: 'Stock Market Basics',
    description: 'Understanding how the stock market works like a giant playground',
    module: tradingFundamentalsModule,
    difficulty: 'beginner',
    estimatedTime: 15,
    xpReward: 150,
    prerequisites: ['what-is-trading'],
    content: [
      {
        type: 'explanation',
        title: 'The Stock Market Playground',
        text: 'Think of the stock market like a giant playground where kids trade toys. Some kids have cool toys (stocks) that other kids want. The more kids who want a toy, the more valuable it becomes!',
        analogy: 'Playground toy trading'
      },
      {
        type: 'explanation',
        title: 'What are Stocks?',
        text: 'Stocks are like ownership certificates for companies. If you own 1 stock of Apple, you own a tiny piece of Apple company - like owning 1 brick in a huge castle!',
      },
      {
        type: 'interactive',
        component: 'StockMarketSimulator',
        params: { 
          scenario: 'simple-trading',
          companies: ['Apple', 'Google', 'Tesla'],
          initialMoney: 1000
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'risk-reward',
    title: 'Risk vs Reward',
    description: 'Understanding the balance between potential gains and potential losses',
    module: tradingFundamentalsModule,
    difficulty: 'beginner',
    estimatedTime: 12,
    xpReward: 120,
    prerequisites: ['stock-market-basics'],
    content: [
      {
        type: 'explanation',
        title: 'The Roller Coaster Analogy',
        text: 'Trading is like riding a roller coaster. The higher the hill (potential reward), the scarier the drop (potential risk). Some people love the thrill, others prefer the gentle carousel!',
        analogy: 'Roller coaster vs carousel'
      },
      {
        type: 'explanation',
        title: 'Risk Management Rules',
        text: '1. Never risk more than you can afford to lose (like not betting your lunch money on a game). 2. Diversify your investments (don\'t put all your eggs in one basket). 3. Have a plan before you start.',
      },
      {
        type: 'interactive',
        component: 'RiskRewardCalculator',
        params: { 
          scenarios: ['conservative', 'moderate', 'aggressive'],
          showVisualizations: true
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'market-orders',
    title: 'Market Orders vs Limit Orders',
    description: 'Learn how to buy and sell stocks with different order types',
    module: tradingFundamentalsModule,
    difficulty: 'beginner',
    estimatedTime: 10,
    xpReward: 100,
    prerequisites: ['risk-reward'],
    content: [
      {
        type: 'explanation',
        title: 'Order Types: The Restaurant Analogy',
        text: 'Market orders are like saying "I\'ll take whatever you have ready right now" at a restaurant. Limit orders are like saying "I\'ll only pay $10 for this meal, no more."',
        analogy: 'Restaurant ordering system'
      },
      {
        type: 'explanation',
        title: 'Market Orders',
        text: 'Market orders buy or sell immediately at the current market price. Fast execution but you might pay more than expected if prices move quickly.',
      },
      {
        type: 'explanation',
        title: 'Limit Orders',
        text: 'Limit orders only execute at your specified price or better. You control the price but the order might not fill if the market doesn\'t reach your price.',
      },
      {
        type: 'interactive',
        component: 'OrderTypeSimulator',
        params: { 
          stock: 'AAPL',
          scenarios: ['market-order', 'limit-order'],
          showPriceImpact: true
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'reading-charts',
    title: 'Reading Stock Charts',
    description: 'Learn to read stock charts like reading a story',
    module: tradingFundamentalsModule,
    difficulty: 'beginner',
    estimatedTime: 15,
    xpReward: 150,
    prerequisites: ['market-orders'],
    content: [
      {
        type: 'explanation',
        title: 'Charts Tell a Story',
        text: 'Stock charts are like picture books that tell the story of a stock\'s journey. The line going up means the stock is doing well (like climbing a mountain), and going down means it\'s having a tough time (like sliding down a hill).',
        analogy: 'Picture book storytelling'
      },
      {
        type: 'explanation',
        title: 'Basic Chart Elements',
        text: 'Price (Y-axis): How much the stock costs. Time (X-axis): When the price changed. Volume: How many people are trading (like how many kids are playing at the playground).',
      },
      {
        type: 'interactive',
        component: 'ChartReader',
        params: { 
          stock: 'AAPL',
          timeframe: '1D',
          showAnnotations: true,
          interactiveMode: true
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'market-hours',
    title: 'Market Hours & After-Hours',
    description: 'Understanding when you can trade and what happens after hours',
    module: tradingFundamentalsModule,
    difficulty: 'beginner',
    estimatedTime: 8,
    xpReward: 80,
    prerequisites: ['reading-charts'],
    content: [
      {
        type: 'explanation',
        title: 'Market Hours: School Schedule',
        text: 'The stock market is like school - it has regular hours (9:30 AM - 4:00 PM EST) when most trading happens. After hours is like after-school activities - fewer people participate, and things can be more unpredictable!',
        analogy: 'School schedule vs after-school activities'
      },
      {
        type: 'explanation',
        title: 'Regular Hours vs After-Hours',
        text: 'Regular hours: More people trading, more predictable prices, easier to buy/sell. After-hours: Fewer traders, prices can jump around more, harder to get good prices.',
      }
    ],
    isCompleted: false,
    progress: 0,
  },
  {
    id: 'paper-trading-intro',
    title: 'Introduction to Paper Trading',
    description: 'Practice trading with virtual money before using real money',
    module: tradingFundamentalsModule,
    difficulty: 'beginner',
    estimatedTime: 12,
    xpReward: 120,
    prerequisites: ['market-hours'],
    content: [
      {
        type: 'explanation',
        title: 'Paper Trading: Practice Mode',
        text: 'Paper trading is like playing a video game before the real adventure. You get to practice all the moves, learn the rules, and make mistakes without losing real money - just like practicing soccer in your backyard before the big game!',
        analogy: 'Video game practice mode'
      },
      {
        type: 'explanation',
        title: 'Why Paper Trade First?',
        text: '1. Learn without risk. 2. Practice your strategy. 3. Understand how emotions affect decisions. 4. Build confidence before using real money.',
      },
      {
        type: 'interactive',
        component: 'PaperTradingSimulator',
        params: { 
          initialBalance: 10000,
          realTimeData: false,
          scenarios: ['beginner-friendly'],
          showTutorial: true
        }
      }
    ],
    isCompleted: false,
    progress: 0,
  }
];

// Update the module with lessons
tradingFundamentalsModule.lessons = tradingFundamentalsLessons;
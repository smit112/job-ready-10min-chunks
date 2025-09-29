import { Lesson } from '../../types';

export const tradingFundamentalsLessons: Lesson[] = [
  {
    id: 'trading-vs-investing',
    title: 'Trading vs Investing: What\'s the Difference?',
    description: 'Learn the fundamental differences between trading and investing with simple playground analogies.',
    module: 'fundamentals',
    difficulty: 'beginner',
    estimatedTime: 10,
    xpReward: 100,
    prerequisites: [],
    content: [
      {
        type: 'explanation',
        title: 'The Big Picture',
        text: 'Imagine you have a lemonade stand. You can either run it every day (trading) or invest in it and let it grow over time (investing). Both are ways to make money, but they work differently!'
      },
      {
        type: 'analogy',
        title: 'The Playground Analogy',
        analogy: 'Think of investing like planting a tree - you plant it, water it occasionally, and watch it grow over many years. Trading is like playing catch - you throw the ball (buy), catch it (sell), and try to do it quickly and skillfully to win the game!'
      },
      {
        type: 'explanation',
        title: 'Key Differences',
        text: 'Investing: Long-term (years), lower risk, steady growth, less time needed. Trading: Short-term (days to months), higher risk, potential for quick gains, requires more attention.'
      },
      {
        type: 'example',
        title: 'Real Example',
        text: 'If you buy Apple stock and hold it for 5 years, that\'s investing. If you buy Apple stock today and sell it next week, that\'s trading!'
      }
    ]
  },
  {
    id: 'stock-market-basics',
    title: 'Stock Market Basics: The Big Playground',
    description: 'Understand how the stock market works using playground analogies that make it easy to grasp.',
    module: 'fundamentals',
    difficulty: 'beginner',
    estimatedTime: 15,
    xpReward: 150,
    prerequisites: ['trading-vs-investing'],
    content: [
      {
        type: 'analogy',
        title: 'The School Playground',
        analogy: 'The stock market is like a huge school playground where kids trade their toys. Some kids have cool toys (stocks) that everyone wants, so they can ask for more in return. Other toys aren\'t as popular, so they cost less.'
      },
      {
        type: 'explanation',
        title: 'What Are Stocks?',
        text: 'Stocks are like tiny pieces of a company. When you buy a stock, you own a small part of that company - just like owning a small piece of a pizza!'
      },
      {
        type: 'explanation',
        title: 'How Prices Move',
        text: 'Stock prices go up when more people want to buy than sell (like when everyone wants the cool new toy). Prices go down when more people want to sell than buy (like when a toy becomes boring).'
      },
      {
        type: 'interactive',
        component: 'MarketSimulator',
        params: { example: 'simple-supply-demand' }
      }
    ]
  },
  {
    id: 'risk-vs-reward',
    title: 'Risk vs Reward: The Safety vs Adventure Balance',
    description: 'Learn about the important balance between risk and reward in trading.',
    module: 'fundamentals',
    difficulty: 'beginner',
    estimatedTime: 12,
    xpReward: 120,
    prerequisites: ['stock-market-basics'],
    content: [
      {
        type: 'analogy',
        title: 'The Roller Coaster Analogy',
        analogy: 'Risk vs Reward is like choosing between a gentle merry-go-round (safe, small rewards) and a thrilling roller coaster (risky, big rewards). The higher the risk, the higher the potential reward - but also the higher chance of losing!'
      },
      {
        type: 'explanation',
        title: 'Understanding Risk',
        text: 'Risk means the chance you might lose money. Low risk = small chance of losing, but small chance of big gains. High risk = bigger chance of losing, but also bigger chance of big gains.'
      },
      {
        type: 'example',
        title: 'Real Examples',
        text: 'Low Risk: Government bonds (like a savings account) - safe but small returns. High Risk: New startup stocks - could make you rich or lose everything!'
      },
      {
        type: 'interactive',
        component: 'RiskRewardCalculator',
        params: { scenarios: ['conservative', 'moderate', 'aggressive'] }
      }
    ]
  },
  {
    id: 'market-orders',
    title: 'Market Orders vs Limit Orders: How to Buy and Sell',
    description: 'Learn the difference between market orders and limit orders with simple examples.',
    module: 'fundamentals',
    difficulty: 'beginner',
    estimatedTime: 10,
    xpReward: 100,
    prerequisites: ['risk-vs-reward'],
    content: [
      {
        type: 'analogy',
        title: 'The Toy Store Analogy',
        analogy: 'Market orders are like saying "I want that toy right now, whatever the price!" Limit orders are like saying "I\'ll only buy that toy if it costs $10 or less."'
      },
      {
        type: 'explanation',
        title: 'Market Orders',
        text: 'Market orders buy or sell immediately at whatever price is available. Fast but you might pay more than expected!'
      },
      {
        type: 'explanation',
        title: 'Limit Orders',
        text: 'Limit orders only execute at your specified price or better. Slower but you control the price!'
      },
      {
        type: 'example',
        title: 'When to Use Each',
        text: 'Use market orders when you need to buy/sell quickly. Use limit orders when you want to control the price and can wait.'
      }
    ]
  },
  {
    id: 'reading-charts',
    title: 'Reading Stock Charts: Like Reading a Story',
    description: 'Learn to read stock charts as if they were telling you a story about what happened.',
    module: 'fundamentals',
    difficulty: 'beginner',
    estimatedTime: 15,
    xpReward: 150,
    prerequisites: ['market-orders'],
    content: [
      {
        type: 'analogy',
        title: 'The Story Book Analogy',
        analogy: 'Stock charts are like story books! The line going up means the story is getting exciting (price going up), the line going down means something sad happened (price going down), and the volume bars show how many people were reading the story (how many shares were traded).'
      },
      {
        type: 'explanation',
        title: 'Basic Chart Elements',
        text: 'Price line: Shows if the stock went up or down. Volume bars: Show how many shares were traded. Time: Shows when things happened (days, weeks, months).'
      },
      {
        type: 'interactive',
        component: 'ChartReader',
        params: { example: 'simple-trend' }
      },
      {
        type: 'example',
        title: 'Reading the Story',
        text: 'If you see the price line going up and volume bars getting bigger, it\'s like a story getting more exciting with more readers!'
      }
    ]
  },
  {
    id: 'market-hours',
    title: 'Market Hours: When the Playground is Open',
    description: 'Learn about market hours and when you can trade.',
    module: 'fundamentals',
    difficulty: 'beginner',
    estimatedTime: 8,
    xpReward: 80,
    prerequisites: ['reading-charts'],
    content: [
      {
        type: 'analogy',
        title: 'The School Schedule',
        analogy: 'The stock market is like school - it has specific hours when it\'s open. Regular hours are like school hours (9:30 AM - 4:00 PM), and after-hours trading is like after-school activities!'
      },
      {
        type: 'explanation',
        title: 'Regular Trading Hours',
        text: 'Monday to Friday, 9:30 AM to 4:00 PM Eastern Time. This is when most trading happens and prices are most stable.'
      },
      {
        type: 'explanation',
        title: 'After-Hours Trading',
        text: '4:00 PM to 8:00 PM and 4:00 AM to 9:30 AM. Fewer people trading, so prices can move more dramatically!'
      },
      {
        type: 'example',
        title: 'Why Hours Matter',
        text: 'During regular hours, there are more buyers and sellers, so you get better prices. After hours, fewer people are trading, so prices can jump around more!'
      }
    ]
  },
  {
    id: 'paper-trading-intro',
    title: 'Paper Trading: Practice Before You Play',
    description: 'Learn about paper trading - the safe way to practice without real money.',
    module: 'fundamentals',
    difficulty: 'beginner',
    estimatedTime: 10,
    xpReward: 100,
    prerequisites: ['market-hours'],
    content: [
      {
        type: 'analogy',
        title: 'The Video Game Analogy',
        analogy: 'Paper trading is like playing a racing video game before driving a real car. You learn the rules, practice your skills, and make mistakes safely - all without crashing a real car!'
      },
      {
        type: 'explanation',
        title: 'What is Paper Trading?',
        text: 'Paper trading uses fake money to practice real trading. You make real decisions but with virtual money, so you can learn without risk!'
      },
      {
        type: 'explanation',
        title: 'Why Practice First?',
        text: 'Just like you wouldn\'t play in a real soccer game without practicing first, you shouldn\'t trade with real money until you\'ve practiced with paper trading!'
      },
      {
        type: 'interactive',
        component: 'PaperTradingSimulator',
        params: { startingBalance: 10000, difficulty: 'beginner' }
      }
    ]
  }
];
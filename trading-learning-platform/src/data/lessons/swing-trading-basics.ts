import { Lesson } from '../../types';

export const swingTradingBasicsLessons: Lesson[] = [
  {
    id: 'swing-trading-intro',
    title: 'What is Swing Trading? The Middle Ground',
    description: 'Learn what swing trading is and how it fits between day trading and investing.',
    module: 'swing',
    subModule: 'basics',
    difficulty: 'beginner',
    estimatedTime: 12,
    xpReward: 120,
    prerequisites: ['paper-trading-intro'],
    content: [
      {
        type: 'analogy',
        title: 'The School Day Analogy',
        analogy: 'Think of trading like school activities. Day trading is like playing during recess (quick, short activities). Investing is like a whole school year (long-term, patient). Swing trading is like a school week - you start on Monday, work through the week, and finish on Friday!'
      },
      {
        type: 'explanation',
        title: 'What is Swing Trading?',
        text: 'Swing trading means holding stocks for a few days to several weeks. You "swing" in when you think the price will go up, and "swing" out when you think it will go down. It\'s like catching waves at the beach!'
      },
      {
        type: 'explanation',
        title: 'Why Swing Trading?',
        text: 'Swing trading gives you more time to make decisions than day trading, but faster results than long-term investing. You can work a regular job and still swing trade in your free time!'
      },
      {
        type: 'example',
        title: 'Real Example',
        text: 'You buy Apple stock on Monday for $150 because you think it will go up. On Friday, it reaches $155, so you sell it. You made $5 per share in just one week!'
      }
    ]
  },
  {
    id: 'swing-vs-day-vs-investing',
    title: 'Swing vs Day Trading vs Investing: The Time Spectrum',
    description: 'Understand the differences between different trading timeframes.',
    module: 'swing',
    subModule: 'basics',
    difficulty: 'beginner',
    estimatedTime: 10,
    xpReward: 100,
    prerequisites: ['swing-trading-intro'],
    content: [
      {
        type: 'analogy',
        title: 'The Sports Analogy',
        analogy: 'Day trading is like a sprint race (very fast, over in seconds). Investing is like a marathon (very long, takes hours). Swing trading is like a 100-meter dash - not too fast, not too slow, just right!'
      },
      {
        type: 'explanation',
        title: 'Day Trading',
        text: 'Buy and sell the same day. Like a sprinter - very fast, requires lots of energy and attention. You need to watch the market all day!'
      },
      {
        type: 'explanation',
        title: 'Swing Trading',
        text: 'Hold for days to weeks. Like a middle-distance runner - good balance of speed and endurance. You can check your trades a few times per day.'
      },
      {
        type: 'explanation',
        title: 'Investing',
        text: 'Hold for months to years. Like a marathon runner - very patient, long-term thinking. You check your investments maybe once per month.'
      }
    ]
  },
  {
    id: 'swing-capital-requirements',
    title: 'Capital Requirements: How Much Do You Need?',
    description: 'Learn about the money you need to start swing trading effectively.',
    module: 'swing',
    subModule: 'basics',
    difficulty: 'beginner',
    estimatedTime: 8,
    xpReward: 80,
    prerequisites: ['swing-vs-day-vs-investing'],
    content: [
      {
        type: 'analogy',
        title: 'The Lemonade Stand Analogy',
        analogy: 'Starting swing trading is like opening a lemonade stand. You need enough money to buy lemons, sugar, and cups (your trading capital), plus some extra money in case you spill some lemonade (emergency fund). You don\'t need to be rich, but you need enough to get started!'
      },
      {
        type: 'explanation',
        title: 'Minimum Capital',
        text: 'Most experts recommend at least $2,000-$5,000 to start swing trading. This gives you enough money to buy several different stocks and not put all your eggs in one basket!'
      },
      {
        type: 'explanation',
        title: 'Why You Need Enough Capital',
        text: 'With too little money, you can only buy one or two stocks. If those stocks go down, you lose everything. With more money, you can spread your risk across many stocks.'
      },
      {
        type: 'example',
        title: 'Real Example',
        text: 'With $1,000, you might buy 10 shares of a $100 stock. If it drops 20%, you lose $200. With $5,000, you could buy 5 different stocks, so if one drops 20%, you only lose $200 out of $5,000 total.'
      }
    ]
  },
  {
    id: 'swing-position-sizing',
    title: 'Position Sizing: Don\'t Put All Eggs in One Basket',
    description: 'Learn how to decide how much money to put in each trade.',
    module: 'swing',
    subModule: 'basics',
    difficulty: 'beginner',
    estimatedTime: 10,
    xpReward: 100,
    prerequisites: ['swing-capital-requirements'],
    content: [
      {
        type: 'analogy',
        title: 'The Pizza Analogy',
        analogy: 'Position sizing is like sharing a pizza with friends. You don\'t give one friend the whole pizza (put all your money in one stock). Instead, you cut it into equal slices so everyone gets a fair share!'
      },
      {
        type: 'explanation',
        title: 'What is Position Sizing?',
        text: 'Position sizing means deciding how much of your total money to put in each trade. Most swing traders put 2-5% of their total money in each stock.'
      },
      {
        type: 'explanation',
        title: 'The 2% Rule',
        text: 'A popular rule is to never risk more than 2% of your total money on any single trade. This way, even if you lose, you don\'t lose everything!'
      },
      {
        type: 'example',
        title: 'Real Example',
        text: 'If you have $10,000 total, you should only risk $200 (2%) on any single trade. This means you can afford to lose on 50 trades before you\'re out of money!'
      }
    ]
  },
  {
    id: 'swing-market-scanning',
    title: 'Market Scanning: Finding the Right Stocks',
    description: 'Learn how to find stocks that are good for swing trading.',
    module: 'swing',
    subModule: 'basics',
    difficulty: 'beginner',
    estimatedTime: 12,
    xpReward: 120,
    prerequisites: ['swing-position-sizing'],
    content: [
      {
        type: 'analogy',
        title: 'The Treasure Hunt Analogy',
        analogy: 'Finding good swing trading stocks is like a treasure hunt. You need a map (market scanner) to find where the treasure (good stocks) might be hidden. You look for clues like high volume and price movements!'
      },
      {
        type: 'explanation',
        title: 'What to Look For',
        text: 'Good swing trading stocks have: 1) High volume (lots of people trading), 2) Clear trends (going up or down), 3) Reasonable price (not too expensive), 4) Good news or events.'
      },
      {
        type: 'explanation',
        title: 'Volume is Key',
        text: 'Volume means how many shares are being traded. High volume means lots of interest - like a popular restaurant with a long line. Low volume means few people care - like an empty restaurant.'
      },
      {
        type: 'example',
        title: 'Real Example',
        text: 'Apple stock usually has high volume (millions of shares traded daily), clear trends, and regular news. This makes it good for swing trading. A small company with low volume might be too risky.'
      }
    ]
  }
];
import { Lesson } from '../../types';

export const optionsBasicsLessons: Lesson[] = [
  {
    id: 'what-are-options',
    title: 'What Are Options? The Stock Coupon System',
    description: 'Learn what options are using the simple analogy of movie theater coupons.',
    module: 'options',
    subModule: 'basics',
    difficulty: 'beginner',
    estimatedTime: 15,
    xpReward: 150,
    prerequisites: ['paper-trading-intro'],
    content: [
      {
        type: 'analogy',
        title: 'The Movie Theater Coupon',
        analogy: 'Options are like movie theater coupons! You buy a coupon that says "I can buy a movie ticket for $10" (even if tickets normally cost $15). You don\'t have to use the coupon, but if you want to see the movie, you can use it to save money!'
      },
      {
        type: 'explanation',
        title: 'What Are Options?',
        text: 'Options give you the RIGHT (but not the obligation) to buy or sell a stock at a specific price by a specific date. It\'s like having a special coupon that might become valuable!'
      },
      {
        type: 'explanation',
        title: 'Two Types of Options',
        text: 'Call Options: The right to BUY a stock (like a coupon to buy something). Put Options: The right to SELL a stock (like insurance for your investment).'
      },
      {
        type: 'example',
        title: 'Real Example',
        text: 'Apple stock costs $150. You buy a call option that lets you buy Apple for $160 by next month. If Apple goes to $170, your option is worth $10! If Apple stays at $150, your option expires worthless.'
      }
    ]
  },
  {
    id: 'calls-vs-puts',
    title: 'Calls vs Puts: The Toy Store Example',
    description: 'Understand the difference between call and put options with toy store analogies.',
    module: 'options',
    subModule: 'basics',
    difficulty: 'beginner',
    estimatedTime: 12,
    xpReward: 120,
    prerequisites: ['what-are-options'],
    content: [
      {
        type: 'analogy',
        title: 'The Toy Store Analogy',
        analogy: 'Imagine a toy store with a popular toy that costs $20. A CALL option is like a coupon that says "I can buy this toy for $20 anytime this month." A PUT option is like insurance that says "If I already own this toy and it breaks, I can sell it back to the store for $20."'
      },
      {
        type: 'explanation',
        title: 'Call Options (The Right to Buy)',
        text: 'Call options give you the right to BUY a stock at a specific price. You use calls when you think the stock price will go UP. It\'s like betting the toy will become more popular and expensive!'
      },
      {
        type: 'explanation',
        title: 'Put Options (The Right to Sell)',
        text: 'Put options give you the right to SELL a stock at a specific price. You use puts when you think the stock price will go DOWN. It\'s like insurance in case your toy breaks or becomes less valuable!'
      },
      {
        type: 'interactive',
        component: 'CallsPutsSimulator',
        params: { example: 'toy-store-scenario' }
      }
    ]
  },
  {
    id: 'strike-price-premium',
    title: 'Strike Price & Premium: The Coupon Details',
    description: 'Learn about strike prices and premiums - the key numbers in every option.',
    module: 'options',
    subModule: 'basics',
    difficulty: 'beginner',
    estimatedTime: 15,
    xpReward: 150,
    prerequisites: ['calls-vs-puts'],
    content: [
      {
        type: 'analogy',
        title: 'The Restaurant Coupon',
        analogy: 'Imagine a restaurant coupon that says "Get a $20 meal for only $15." The $15 is the STRIKE PRICE (what you pay), and the $3 you paid for the coupon is the PREMIUM. The meal normally costs $20, so you save $2 total!'
      },
      {
        type: 'explanation',
        title: 'Strike Price',
        text: 'The strike price is the price at which you can buy (call) or sell (put) the stock. It\'s like the guaranteed price on your coupon!'
      },
      {
        type: 'explanation',
        title: 'Premium',
        text: 'The premium is what you pay to buy the option. It\'s like the cost of the coupon itself. You pay this upfront, whether you use the option or not!'
      },
      {
        type: 'example',
        title: 'Real Example',
        text: 'Apple stock is $150. You buy a call option with a $160 strike price for $5 premium. If Apple goes to $170, you can buy it for $160 and sell for $170, making $5 profit (minus the $5 premium = break even).'
      },
      {
        type: 'interactive',
        component: 'StrikePriceCalculator',
        params: { stock: 'AAPL', currentPrice: 150 }
      }
    ]
  },
  {
    id: 'expiration-dates',
    title: 'Expiration Dates: The Coupon Deadline',
    description: 'Learn about expiration dates and why time matters in options.',
    module: 'options',
    subModule: 'basics',
    difficulty: 'beginner',
    estimatedTime: 10,
    xpReward: 100,
    prerequisites: ['strike-price-premium'],
    content: [
      {
        type: 'analogy',
        title: 'The Expiring Coupon',
        analogy: 'Options are like coupons with expiration dates! If you don\'t use your movie coupon by the expiration date, it becomes worthless. The closer you get to expiration, the less valuable the coupon becomes!'
      },
      {
        type: 'explanation',
        title: 'What is Expiration?',
        text: 'Every option has an expiration date - the last day you can use it. After that date, the option becomes worthless and disappears!'
      },
      {
        type: 'explanation',
        title: 'Time Decay',
        text: 'As time passes, options lose value (like a melting ice cream cone). This happens because there\'s less time for the stock to move in your favor!'
      },
      {
        type: 'example',
        title: 'Time Examples',
        text: 'Weekly options expire every Friday. Monthly options expire on the third Friday of each month. The longer the time, the more expensive the option, but also more time for the stock to move!'
      }
    ]
  },
  {
    id: 'itm-otm-atm',
    title: 'ITM, OTM, ATM: Where is Your Option?',
    description: 'Learn about In-The-Money, Out-of-The-Money, and At-The-Money options.',
    module: 'options',
    subModule: 'basics',
    difficulty: 'beginner',
    estimatedTime: 12,
    xpReward: 120,
    prerequisites: ['expiration-dates'],
    content: [
      {
        type: 'analogy',
        title: 'The Target Practice',
        analogy: 'Think of options like target practice! ITM (In-The-Money) is like hitting the bullseye - your option is already profitable. OTM (Out-of-The-Money) is like missing the target - your option needs the stock to move to become profitable. ATM (At-The-Money) is like hitting the edge of the target - right on the line!'
      },
      {
        type: 'explanation',
        title: 'In-The-Money (ITM)',
        text: 'For calls: Stock price > Strike price (you can buy below market price). For puts: Stock price < Strike price (you can sell above market price). These options have real value!'
      },
      {
        type: 'explanation',
        title: 'Out-of-The-Money (OTM)',
        text: 'For calls: Stock price < Strike price (strike is too high). For puts: Stock price > Strike price (strike is too low). These options are cheaper but need the stock to move!'
      },
      {
        type: 'explanation',
        title: 'At-The-Money (ATM)',
        text: 'Stock price = Strike price (exactly at the target). These options are in the middle - not too expensive, not too cheap!'
      },
      {
        type: 'interactive',
        component: 'ITMOTMCalculator',
        params: { stock: 'AAPL', currentPrice: 150 }
      }
    ]
  },
  {
    id: 'exercise-vs-selling',
    title: 'Exercise vs Selling: Using Your Coupon',
    description: 'Learn when to exercise your option vs selling it for profit.',
    module: 'options',
    subModule: 'basics',
    difficulty: 'beginner',
    estimatedTime: 10,
    xpReward: 100,
    prerequisites: ['itm-otm-atm'],
    content: [
      {
        type: 'analogy',
        title: 'The Restaurant Choice',
        analogy: 'You have a restaurant coupon worth $10 off a meal. You can either USE the coupon (exercise) to get the discount, or SELL the coupon to someone else for $8. Most people sell the coupon because it\'s easier and you get cash right away!'
      },
      {
        type: 'explanation',
        title: 'Exercising an Option',
        text: 'Exercising means actually buying (call) or selling (put) the stock at the strike price. You get the stock, but you need the money to buy it!'
      },
      {
        type: 'explanation',
        title: 'Selling an Option',
        text: 'Selling means selling your option to someone else for cash. Most traders do this because it\'s easier and you get money immediately!'
      },
      {
        type: 'example',
        title: 'When to Do What',
        text: 'Exercise: When you actually want to own the stock. Sell: When you just want to make money from the option price going up. Most people sell!'
      }
    ]
  }
];
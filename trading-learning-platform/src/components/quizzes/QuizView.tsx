import React from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Clock, Star, Target } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import QuizComponent from './QuizComponent';

const QuizView: React.FC = () => {
  const { quizId } = useParams<{ quizId: string }>();
  const navigate = useNavigate();

  // Mock quiz data - in a real app, this would come from an API
  const mockQuiz = {
    id: 'options-basics-quiz',
    title: 'Options Basics Quiz',
    description: 'Test your knowledge of options fundamentals',
    questions: [
      {
        id: 'q1',
        question: 'What is a call option?',
        type: 'multiple-choice' as const,
        options: [
          'The right to buy a stock at a specific price',
          'The right to sell a stock at a specific price',
          'An obligation to buy a stock',
          'An insurance policy for your portfolio'
        ],
        correctAnswer: 'The right to buy a stock at a specific price',
        explanation: 'A call option gives you the right (but not the obligation) to buy a stock at a specific price (strike price) before the expiration date.',
        difficulty: 'easy' as const,
        xpReward: 50
      },
      {
        id: 'q2',
        question: 'What happens to the time value of an option as it approaches expiration?',
        type: 'multiple-choice' as const,
        options: [
          'It increases',
          'It decreases',
          'It stays the same',
          'It becomes negative'
        ],
        correctAnswer: 'It decreases',
        explanation: 'Time value decreases as the option approaches expiration, just like ice cream melting away. This is called time decay or theta decay.',
        difficulty: 'medium' as const,
        xpReward: 75
      },
      {
        id: 'q3',
        question: 'If you buy a call option with a strike price of $100 and the stock is currently trading at $105, is this option in-the-money?',
        type: 'multiple-choice' as const,
        options: [
          'Yes, because the stock price is above the strike price',
          'No, because you paid a premium',
          'It depends on the expiration date',
          'Only if the stock price is exactly $100'
        ],
        correctAnswer: 'Yes, because the stock price is above the strike price',
        explanation: 'A call option is in-the-money when the stock price is above the strike price. In this case, $105 > $100, so the option has intrinsic value.',
        difficulty: 'medium' as const,
        xpReward: 75
      },
      {
        id: 'q4',
        question: 'What is the maximum loss for someone who buys a call option?',
        type: 'multiple-choice' as const,
        options: [
          'Unlimited',
          'The premium paid',
          'The strike price',
          'The stock price'
        ],
        correctAnswer: 'The premium paid',
        explanation: 'When you buy a call option, your maximum loss is limited to the premium you paid. You can never lose more than what you invested.',
        difficulty: 'easy' as const,
        xpReward: 50
      },
      {
        id: 'q5',
        question: 'What does Delta represent in options trading?',
        type: 'multiple-choice' as const,
        options: [
          'The time decay of an option',
          'How much the option price changes when the stock price changes',
          'The volatility of the underlying stock',
          'The interest rate effect on options'
        ],
        correctAnswer: 'How much the option price changes when the stock price changes',
        explanation: 'Delta is like a speedometer - it shows how fast your option price changes when the stock price moves. A delta of 0.5 means your option moves $0.50 for every $1 the stock moves.',
        difficulty: 'hard' as const,
        xpReward: 100
      }
    ]
  };

  const handleQuizComplete = (score: number) => {
    console.log(`Quiz completed with score: ${score}%`);
    // In a real app, this would save the score and award XP
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors mb-4"
        >
          <ArrowLeft size={20} />
          <span>Back to Dashboard</span>
        </button>

        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            {mockQuiz.title}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            {mockQuiz.description}
          </p>
        </div>

        {/* Quiz Info */}
        <div className="flex items-center justify-center space-x-6 text-sm text-gray-600 dark:text-gray-400 mb-8">
          <div className="flex items-center space-x-2">
            <Target size={16} />
            <span>{mockQuiz.questions.length} Questions</span>
          </div>
          <div className="flex items-center space-x-2">
            <Clock size={16} />
            <span>~10 minutes</span>
          </div>
          <div className="flex items-center space-x-2">
            <Star size={16} />
            <span>{mockQuiz.questions.reduce((acc, q) => acc + q.xpReward, 0)} XP</span>
          </div>
        </div>
      </div>

      {/* Quiz Component */}
      <QuizComponent 
        questions={mockQuiz.questions}
        onComplete={handleQuizComplete}
      />
    </div>
  );
};

export default QuizView;
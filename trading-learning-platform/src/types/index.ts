// Core types for the trading learning platform

export interface User {
  id: string;
  name: string;
  email?: string;
  avatar?: string;
  totalXP: number;
  currentStreak: number;
  level: number;
  achievements: Achievement[];
  preferences: UserPreferences;
  createdAt: Date;
  lastActive: Date;
}

export interface UserPreferences {
  theme: 'light' | 'dark';
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  learningPath: 'options' | 'swing' | 'both';
  notifications: boolean;
}

export interface Lesson {
  id: string;
  title: string;
  description: string;
  module: Module;
  subModule?: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimatedTime: number; // in minutes
  xpReward: number;
  prerequisites: string[];
  content: LessonContent[];
  isCompleted: boolean;
  completedAt?: Date;
  progress: number; // 0-100
}

export interface LessonContent {
  type: 'explanation' | 'interactive' | 'quiz' | 'video' | 'analogy' | 'example';
  title?: string;
  text?: string;
  analogy?: string;
  component?: string;
  params?: Record<string, any>;
  questions?: QuizQuestion[];
  examples?: Example[];
}

export interface QuizQuestion {
  id: string;
  question: string;
  type: 'multiple-choice' | 'true-false' | 'calculation' | 'scenario';
  options?: string[];
  correctAnswer: string | number;
  explanation: string;
  difficulty: 'easy' | 'medium' | 'hard';
  xpReward: number;
}

export interface Example {
  id: string;
  title: string;
  description: string;
  scenario: string;
  solution: string;
  keyTakeaways: string[];
}

export interface Module {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  lessons: Lesson[];
  isCompleted: boolean;
  progress: number;
  unlocked: boolean;
}

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  category: 'learning' | 'trading' | 'streak' | 'mastery';
  xpReward: number;
  unlockedAt: Date;
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
}

export interface Progress {
  totalXP: number;
  level: number;
  currentStreak: number;
  completedLessons: string[];
  completedModules: string[];
  achievements: string[];
  quizScores: Record<string, number>;
  timeSpent: number; // in minutes
  lastActive: Date;
}

// Interactive tool types
export interface OptionsCalculator {
  stockPrice: number;
  strikePrice: number;
  premium: number;
  expirationDays: number;
  optionType: 'call' | 'put';
  position: 'long' | 'short';
  quantity: number;
}

export interface GreeksData {
  delta: number;
  gamma: number;
  theta: number;
  vega: number;
  rho: number;
}

export interface PnLData {
  stockPrice: number;
  profitLoss: number;
  percentage: number;
}

export interface TechnicalIndicator {
  name: string;
  value: number;
  signal: 'bullish' | 'bearish' | 'neutral';
  description: string;
}

export interface ChartPattern {
  name: string;
  type: 'reversal' | 'continuation';
  description: string;
  example: string;
  successRate: number;
}

export interface TradingStrategy {
  id: string;
  name: string;
  type: 'options' | 'swing' | 'combined';
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  description: string;
  whenToUse: string[];
  riskLevel: 'low' | 'medium' | 'high';
  expectedReturn: string;
  maxLoss: string;
  steps: string[];
  examples: Example[];
}

// Navigation types
export interface NavigationItem {
  id: string;
  label: string;
  path: string;
  icon: string;
  badge?: string | number;
  children?: NavigationItem[];
}

// Store types
export interface AppState {
  user: User | null;
  progress: Progress;
  currentLesson: Lesson | null;
  currentModule: Module | null;
  theme: 'light' | 'dark';
  isLoading: boolean;
  error: string | null;
}

export interface AppActions {
  setUser: (user: User) => void;
  updateProgress: (progress: Partial<Progress>) => void;
  completeLesson: (lessonId: string, score?: number) => void;
  unlockAchievement: (achievementId: string) => void;
  setTheme: (theme: 'light' | 'dark') => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}
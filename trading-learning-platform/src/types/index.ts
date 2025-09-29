// Core types for the trading learning platform

export interface User {
  id: string;
  name: string;
  email?: string;
  avatar?: string;
  createdAt: Date;
  lastActive: Date;
}

export interface UserProgress {
  totalXP: number;
  currentStreak: number;
  completedLessons: string[];
  achievements: string[];
  quizScores: Record<string, number>;
  lastActive: Date;
  preferredLearningPath: 'options' | 'swing' | 'both';
  currentModule: string;
  currentLesson: string;
}

export interface Lesson {
  id: string;
  title: string;
  description: string;
  module: string;
  subModule?: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimatedTime: number; // in minutes
  xpReward: number;
  prerequisites: string[];
  content: LessonContent[];
  quiz?: Quiz;
  isCompleted?: boolean;
  isUnlocked?: boolean;
}

export interface LessonContent {
  type: 'explanation' | 'interactive' | 'analogy' | 'example' | 'video' | 'image';
  title?: string;
  text?: string;
  analogy?: string;
  component?: string;
  params?: Record<string, any>;
  imageUrl?: string;
  videoUrl?: string;
}

export interface Quiz {
  id: string;
  title: string;
  questions: QuizQuestion[];
  passingScore: number;
  xpReward: number;
  timeLimit?: number; // in minutes
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

export interface Module {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  lessons: string[];
  prerequisites: string[];
  isUnlocked: boolean;
  completionPercentage: number;
}

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  xpReward: number;
  category: 'learning' | 'quiz' | 'streak' | 'milestone' | 'special';
  isUnlocked: boolean;
  unlockedAt?: Date;
}

// Interactive tool types
export interface OptionsCalculatorParams {
  optionType: 'call' | 'put';
  stockPrice: number;
  strikePrice: number;
  premium: number;
  expirationDays: number;
  volatility?: number;
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
  type: 'trend' | 'momentum' | 'volatility' | 'volume';
  description: string;
  calculation: string;
  interpretation: string;
}

export interface ChartPattern {
  name: string;
  type: 'reversal' | 'continuation';
  description: string;
  recognition: string[];
  implications: string;
  reliability: number; // 0-100
}

// State management types
export interface AppState {
  user: User | null;
  progress: UserProgress;
  currentLesson: Lesson | null;
  isDarkMode: boolean;
  sidebarOpen: boolean;
  notifications: Notification[];
}

export interface Notification {
  id: string;
  type: 'success' | 'warning' | 'error' | 'info';
  title: string;
  message: string;
  timestamp: Date;
  isRead: boolean;
}

// Navigation types
export interface NavItem {
  id: string;
  label: string;
  icon: string;
  path: string;
  badge?: string | number;
  children?: NavItem[];
}

// Learning path types
export interface LearningPath {
  id: string;
  name: string;
  description: string;
  modules: string[];
  estimatedDuration: number; // in hours
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  prerequisites: string[];
}

// Analytics types
export interface LearningAnalytics {
  totalTimeSpent: number; // in minutes
  averageQuizScore: number;
  lessonsCompleted: number;
  streakRecord: number;
  favoriteModule: string;
  improvementAreas: string[];
  strengths: string[];
}
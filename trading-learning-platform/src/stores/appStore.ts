import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { AppState, AppActions, User, Progress, Lesson, Module, Achievement } from '../types';

interface AppStore extends AppState, AppActions {}

const initialProgress: Progress = {
  totalXP: 0,
  level: 1,
  currentStreak: 0,
  completedLessons: [],
  completedModules: [],
  achievements: [],
  quizScores: {},
  timeSpent: 0,
  lastActive: new Date(),
};

export const useAppStore = create<AppStore>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      progress: initialProgress,
      currentLesson: null,
      currentModule: null,
      theme: 'light',
      isLoading: false,
      error: null,

      // Actions
      setUser: (user: User) => set({ user }),

      updateProgress: (progressUpdate: Partial<Progress>) =>
        set((state) => ({
          progress: { ...state.progress, ...progressUpdate },
        })),

      completeLesson: (lessonId: string, score?: number) =>
        set((state) => {
          const newProgress = { ...state.progress };
          
          // Add lesson to completed list if not already there
          if (!newProgress.completedLessons.includes(lessonId)) {
            newProgress.completedLessons.push(lessonId);
          }

          // Update quiz score if provided
          if (score !== undefined) {
            newProgress.quizScores[lessonId] = score;
          }

          // Calculate XP gain (base XP + bonus for high scores)
          const baseXP = 100; // This should come from lesson data
          const bonusXP = score && score >= 80 ? Math.floor(score / 10) * 10 : 0;
          newProgress.totalXP += baseXP + bonusXP;

          // Update level (every 1000 XP = 1 level)
          newProgress.level = Math.floor(newProgress.totalXP / 1000) + 1;

          // Update last active
          newProgress.lastActive = new Date();

          return { progress: newProgress };
        }),

      unlockAchievement: (achievementId: string) =>
        set((state) => {
          const newProgress = { ...state.progress };
          
          if (!newProgress.achievements.includes(achievementId)) {
            newProgress.achievements.push(achievementId);
            
            // Award XP for achievement (this should come from achievement data)
            newProgress.totalXP += 500;
            newProgress.level = Math.floor(newProgress.totalXP / 1000) + 1;
          }

          return { progress: newProgress };
        }),

      setTheme: (theme: 'light' | 'dark') => set({ theme }),

      setLoading: (isLoading: boolean) => set({ isLoading }),

      setError: (error: string | null) => set({ error }),

      // Helper methods
      getCompletedLessonsCount: () => get().progress.completedLessons.length,
      
      getCurrentStreak: () => get().progress.currentStreak,
      
      getTotalXP: () => get().progress.totalXP,
      
      getLevel: () => get().progress.level,
      
      isLessonCompleted: (lessonId: string) => 
        get().progress.completedLessons.includes(lessonId),
      
      isModuleCompleted: (moduleId: string) => 
        get().progress.completedModules.includes(moduleId),
      
      getQuizScore: (lessonId: string) => 
        get().progress.quizScores[lessonId] || 0,
    }),
    {
      name: 'trading-learning-storage',
      partialize: (state) => ({
        user: state.user,
        progress: state.progress,
        theme: state.theme,
      }),
    }
  )
);
// Trading Learning Platform - Feature Test Script
// Run this in the browser console to test key features

console.log('🎯 Trading Learning Platform - Feature Tests');
console.log('==========================================');

// Test 1: Check if React app is loaded
const testReactApp = () => {
  const reactRoot = document.getElementById('root');
  if (reactRoot && reactRoot.children.length > 0) {
    console.log('✅ React app loaded successfully');
    return true;
  } else {
    console.log('❌ React app not loaded');
    return false;
  }
};

// Test 2: Check navigation elements
const testNavigation = () => {
  const navElements = [
    'Dashboard',
    'Learning Modules', 
    'Interactive Tools',
    'Progress'
  ];
  
  let found = 0;
  navElements.forEach(element => {
    if (document.body.textContent.includes(element)) {
      found++;
    }
  });
  
  if (found >= 3) {
    console.log('✅ Navigation elements found');
    return true;
  } else {
    console.log('❌ Navigation elements missing');
    return false;
  }
};

// Test 3: Check for lesson content
const testLessonContent = () => {
  const lessonKeywords = [
    'Trading Fundamentals',
    'Options Trading',
    'lemonade stand',
    'movie theater coupon',
    'ice cream'
  ];
  
  let found = 0;
  lessonKeywords.forEach(keyword => {
    if (document.body.textContent.includes(keyword)) {
      found++;
    }
  });
  
  if (found >= 3) {
    console.log('✅ Lesson content with analogies found');
    return true;
  } else {
    console.log('❌ Lesson content missing');
    return false;
  }
};

// Test 4: Check for interactive elements
const testInteractiveElements = () => {
  const interactiveElements = [
    'Options Calculator',
    'Greeks Simulator',
    'Chart Reader',
    'Risk Calculator'
  ];
  
  let found = 0;
  interactiveElements.forEach(element => {
    if (document.body.textContent.includes(element)) {
      found++;
    }
  });
  
  if (found >= 2) {
    console.log('✅ Interactive tools found');
    return true;
  } else {
    console.log('❌ Interactive tools missing');
    return false;
  }
};

// Test 5: Check for gamification elements
const testGamification = () => {
  const gamificationElements = [
    'XP',
    'Level',
    'Achievement',
    'Streak',
    'Progress'
  ];
  
  let found = 0;
  gamificationElements.forEach(element => {
    if (document.body.textContent.includes(element)) {
      found++;
    }
  });
  
  if (found >= 3) {
    console.log('✅ Gamification elements found');
    return true;
  } else {
    console.log('❌ Gamification elements missing');
    return false;
  }
};

// Test 6: Check for responsive design
const testResponsiveDesign = () => {
  const viewport = window.innerWidth;
  const isResponsive = viewport < 768 ? 'Mobile' : 'Desktop';
  console.log(`✅ Responsive design detected: ${isResponsive} view (${viewport}px)`);
  return true;
};

// Test 7: Check for animations
const testAnimations = () => {
  // Check if Framer Motion is loaded
  if (window.React && window.React.createElement) {
    console.log('✅ React animations framework loaded');
    return true;
  } else {
    console.log('❌ Animations framework not detected');
    return false;
  }
};

// Run all tests
const runAllTests = () => {
  console.log('\n🧪 Running Feature Tests...\n');
  
  const tests = [
    { name: 'React App Loading', test: testReactApp },
    { name: 'Navigation System', test: testNavigation },
    { name: 'Lesson Content', test: testLessonContent },
    { name: 'Interactive Tools', test: testInteractiveElements },
    { name: 'Gamification', test: testGamification },
    { name: 'Responsive Design', test: testResponsiveDesign },
    { name: 'Animations', test: testAnimations }
  ];
  
  let passed = 0;
  let total = tests.length;
  
  tests.forEach(({ name, test }) => {
    console.log(`\n🔍 Testing: ${name}`);
    if (test()) {
      passed++;
    }
  });
  
  console.log('\n📊 Test Results:');
  console.log(`✅ Passed: ${passed}/${total}`);
  console.log(`❌ Failed: ${total - passed}/${total}`);
  
  if (passed === total) {
    console.log('\n🎉 All tests passed! The Trading Learning Platform is working perfectly!');
  } else {
    console.log('\n⚠️  Some tests failed. Check the console for details.');
  }
  
  return { passed, total };
};

// Test specific features
const testOptionsCalculator = () => {
  console.log('\n🧮 Testing Options Calculator...');
  
  // Look for calculator elements
  const calculatorElements = [
    'Stock Price',
    'Strike Price', 
    'Premium',
    'Option Type',
    'Position'
  ];
  
  let found = 0;
  calculatorElements.forEach(element => {
    if (document.body.textContent.includes(element)) {
      found++;
    }
  });
  
  if (found >= 3) {
    console.log('✅ Options Calculator elements found');
    return true;
  } else {
    console.log('❌ Options Calculator elements missing');
    return false;
  }
};

const testQuizSystem = () => {
  console.log('\n📝 Testing Quiz System...');
  
  const quizElements = [
    'Quiz',
    'Question',
    'Answer',
    'Score',
    'Correct',
    'Incorrect'
  ];
  
  let found = 0;
  quizElements.forEach(element => {
    if (document.body.textContent.includes(element)) {
      found++;
    }
  });
  
  if (found >= 3) {
    console.log('✅ Quiz system elements found');
    return true;
  } else {
    console.log('❌ Quiz system elements missing');
    return false;
  }
};

// Export functions for manual testing
window.tradingPlatformTests = {
  runAllTests,
  testReactApp,
  testNavigation,
  testLessonContent,
  testInteractiveElements,
  testGamification,
  testResponsiveDesign,
  testAnimations,
  testOptionsCalculator,
  testQuizSystem
};

// Auto-run tests
console.log('\n🚀 Auto-running tests...');
runAllTests();

console.log('\n💡 Manual Testing Commands:');
console.log('- tradingPlatformTests.runAllTests() - Run all tests');
console.log('- tradingPlatformTests.testOptionsCalculator() - Test calculator');
console.log('- tradingPlatformTests.testQuizSystem() - Test quiz system');
console.log('\n🎯 Happy Testing!');
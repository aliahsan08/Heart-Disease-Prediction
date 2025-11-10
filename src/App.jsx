import { useState } from 'react'
import HomePage from './components/HomePage'
import QuestionPage from './components/QuestionPage'
import ResultPage from './components/ResultPage'

const QUESTIONS = [
  {
    id: 'age',
    label: 'What is your current age?',
    description: 'Please enter your age in years. This helps us understand your risk profile.',
    type: 'number',
    min: 1,
    max: 120,
    placeholder: 'Enter your age'
  },
  {
    id: 'sex',
    label: 'What is your biological sex?',
    description: 'This information helps in assessing heart disease risk factors.',
    type: 'select',
    options: [
      { value: 1, label: 'Male' },
      { value: 0, label: 'Female' }
    ]
  },
  {
    id: 'cp',
    label: 'What type of chest pain do you experience?',
    description: 'Chest pain type can be an important indicator. Please select the option that best describes your experience.',
    type: 'select',
    options: [
      { value: 0, label: 'Typical Angina - Chest pain related to the heart' },
      { value: 1, label: 'Atypical Angina - Chest pain that may not be heart-related' },
      { value: 2, label: 'Non-anginal Pain - Pain not related to angina' },
      { value: 3, label: 'Asymptomatic - No chest pain experienced' }
    ]
  },
  {
    id: 'oldpeak',
    label: 'ST Depression Value',
    description: 'ST depression is measured during exercise stress tests. It indicates how much the ST segment of your ECG is depressed during exercise compared to rest. If you don\'t know this value, please consult your doctor or enter 0 if you haven\'t had this test.',
    type: 'number',
    min: 0,
    max: 10,
    step: 0.1,
    placeholder: 'Enter value (e.g., 0.5)'
  },
  {
    id: 'thalach',
    label: 'Maximum Heart Rate Achieved',
    description: 'This is the highest heart rate you reached during physical activity or exercise. It\'s typically measured in beats per minute (BPM). A rough estimate: 220 minus your age gives an approximate maximum heart rate.',
    type: 'number',
    min: 60,
    max: 220,
    placeholder: 'Enter heart rate (BPM)'
  },
  {
    id: 'chol',
    label: 'Serum Cholesterol Level',
    description: 'This is your total cholesterol level measured in milligrams per deciliter (mg/dL). Normal levels are typically below 200 mg/dL. You can find this on your recent blood test results.',
    type: 'number',
    min: 100,
    max: 600,
    placeholder: 'Enter cholesterol (mg/dL)'
  }
]

function App() {
  const [currentStep, setCurrentStep] = useState('home')
  const [answers, setAnswers] = useState({})
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleStart = () => {
    setCurrentStep('questions')
    setCurrentQuestionIndex(0)
    setAnswers({})
  }

  const handleAnswer = (value) => {
    const question = QUESTIONS[currentQuestionIndex]
    const newAnswers = { ...answers, [question.id]: value }
    setAnswers(newAnswers)

    if (currentQuestionIndex < QUESTIONS.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    } else {
      // All questions answered, make prediction
      makePrediction(newAnswers)
    }
  }

  const makePrediction = async (allAnswers) => {
    setLoading(true)
    setCurrentStep('result')

    try {
      // Prepare the input data in the correct order
      // Based on typical heart disease datasets: age, sex, cp, oldpeak, thalach, chol
      const features = [
        parseFloat(allAnswers.age),
        parseFloat(allAnswers.sex),
        parseFloat(allAnswers.cp),
        parseFloat(allAnswers.oldpeak),
        parseFloat(allAnswers.thalach),
        parseFloat(allAnswers.chol)
      ]

      // Call local Python serverless function API
      // Works both in development (with Vercel CLI) and production
      const apiUrl = '/api/predict'
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          features: features
        })
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || 'Prediction failed')
      }

      const result = await response.json()
      
      // Extract prediction (0 or 1)
      const finalPrediction = result.prediction !== undefined 
        ? result.prediction 
        : (result.has_risk ? 1 : 0)

      setPrediction(finalPrediction)
    } catch (error) {
      console.error('Prediction error:', error)
      alert(`Unable to get prediction: ${error.message}. Please try again later.`)
      setCurrentStep('questions')
      setCurrentQuestionIndex(QUESTIONS.length - 1)
    } finally {
      setLoading(false)
    }
  }

  const handleBack = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  const handleReset = () => {
    setCurrentStep('home')
    setCurrentQuestionIndex(0)
    setAnswers({})
    setPrediction(null)
  }

  return (
    <div className="app">
      {currentStep === 'home' && <HomePage onStart={handleStart} />}
      {currentStep === 'questions' && (
        <QuestionPage
          question={QUESTIONS[currentQuestionIndex]}
          questionNumber={currentQuestionIndex + 1}
          totalQuestions={QUESTIONS.length}
          onAnswer={handleAnswer}
          onBack={currentQuestionIndex > 0 ? handleBack : null}
          currentAnswer={answers[QUESTIONS[currentQuestionIndex].id]}
        />
      )}
      {currentStep === 'result' && (
        <ResultPage
          prediction={prediction}
          loading={loading}
          onReset={handleReset}
        />
      )}
    </div>
  )
}

export default App


import { useState, useEffect } from 'react'

function QuestionPage({ question, questionNumber, totalQuestions, onAnswer, onBack, currentAnswer }) {
  const [inputValue, setInputValue] = useState(currentAnswer || '')

  useEffect(() => {
    setInputValue(currentAnswer || '')
  }, [question.id, currentAnswer])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (inputValue !== '' && inputValue !== null && inputValue !== undefined) {
      onAnswer(parseFloat(inputValue) || inputValue)
    }
  }

  const handleNext = () => {
    if (inputValue !== '' && inputValue !== null && inputValue !== undefined) {
      onAnswer(parseFloat(inputValue) || inputValue)
    }
  }

  return (
    <div className="question-page">
      <div className="question-container">
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${(questionNumber / totalQuestions) * 100}%` }}
          ></div>
        </div>
        <div className="question-number">
          Question {questionNumber} of {totalQuestions}
        </div>
        
        <h2 className="question-label">{question.label}</h2>
        <p className="question-description">{question.description}</p>

        <form onSubmit={handleSubmit} className="question-form">
          {question.type === 'number' && (
            <input
              type="number"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              min={question.min}
              max={question.max}
              step={question.step || 1}
              placeholder={question.placeholder}
              className="question-input"
              required
              autoFocus
            />
          )}

          {question.type === 'select' && (
            <div className="select-options">
              {question.options.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  className={`select-option ${inputValue == option.value ? 'selected' : ''}`}
                  onClick={() => {
                    setInputValue(option.value)
                    setTimeout(() => onAnswer(option.value), 300)
                  }}
                >
                  {option.label}
                </button>
              ))}
            </div>
          )}

          {question.type === 'number' && (
            <div className="question-actions">
              {onBack && (
                <button type="button" className="back-button" onClick={onBack}>
                  ← Back
                </button>
              )}
              <button type="submit" className="next-button" disabled={!inputValue}>
                {questionNumber === totalQuestions ? 'Get Results' : 'Next →'}
              </button>
            </div>
          )}
        </form>
      </div>
    </div>
  )
}

export default QuestionPage


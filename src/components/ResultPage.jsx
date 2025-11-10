function ResultPage({ prediction, loading, onReset }) {
  if (loading) {
    return (
      <div className="result-page">
        <div className="result-container">
          <div className="loading-spinner"></div>
          <p className="loading-text">Analyzing your results...</p>
        </div>
      </div>
    )
  }

  const hasRisk = prediction === 1

  return (
    <div className="result-page">
      <div className="result-container">
        <div className={`result-icon ${hasRisk ? 'risk' : 'no-risk'}`}>
          {hasRisk ? '⚠️' : '✅'}
        </div>
        <h2 className="result-title">
          {hasRisk ? 'Heart Disease Risk Detected' : 'Low Risk of Heart Disease'}
        </h2>
        <div className="result-message">
          {hasRisk ? (
            <>
              <p className="result-text">
                Based on the information you provided, our assessment indicates a 
                potential risk for heart disease.
              </p>
              <p className="result-advice">
                <strong>Please consult with a healthcare professional</strong> for a 
                comprehensive evaluation. Early detection and proper medical guidance 
                are crucial for maintaining heart health.
              </p>
            </>
          ) : (
            <>
              <p className="result-text">
                Based on the information you provided, our assessment indicates a 
                low risk of heart disease.
              </p>
              <p className="result-advice">
                However, it's still important to maintain regular check-ups with your 
                healthcare provider and follow a heart-healthy lifestyle.
              </p>
            </>
          )}
        </div>
        <div className="result-disclaimer">
          <p>
            <strong>Disclaimer:</strong> This assessment is for informational purposes 
            only and is not a substitute for professional medical advice, diagnosis, 
            or treatment. Always seek the advice of qualified health providers with 
            any questions you may have regarding a medical condition.
          </p>
        </div>
        <button className="reset-button" onClick={onReset}>
          Start New Assessment
        </button>
      </div>
    </div>
  )
}

export default ResultPage


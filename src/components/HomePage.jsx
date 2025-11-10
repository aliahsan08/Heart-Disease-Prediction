function HomePage({ onStart }) {
  return (
    <div className="home-page">
      <div className="home-content">
        <h1 className="home-title">Heart Disease Predictor</h1>
        <div className="home-info">
          <p className="info-text">
            Welcome to our Heart Disease Risk Assessment tool. This application uses 
            advanced machine learning to help you understand your potential risk for 
            heart disease based on key health indicators.
          </p>
          <p className="info-text">
            We'll ask you a few simple questions about your health metrics. 
            The assessment takes just a few minutes and provides valuable insights 
            about your cardiovascular health.
          </p>
          <p className="info-note">
            <strong>Important:</strong> This tool is for informational purposes only 
            and should not replace professional medical advice. Always consult with a 
            healthcare provider for medical concerns.
          </p>
        </div>
        <button className="start-button" onClick={onStart}>
          Let's Begin
        </button>
      </div>
    </div>
  )
}

export default HomePage


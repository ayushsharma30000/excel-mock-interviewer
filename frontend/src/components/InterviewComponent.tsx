import React, { useState } from 'react';
import axios from 'axios';
import './InterviewComponent.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface InterviewState {
  stage: 'start' | 'interview' | 'feedback' | 'complete';
  sessionId: string;
  userName: string;
  currentQuestion: string;
  questionNumber: number;
  totalQuestions: number;
  questionType: 'mcq' | 'general';
  options: string[];
  answer: string;
  currentFeedback: any;
  currentScore: number;
  correctAnswer: string;
  suggestions: string[];
  nextQuestion: string;
  report: any;
}

const InterviewComponent: React.FC = () => {
  const [state, setState] = useState<InterviewState>({
    stage: 'start',
    sessionId: '',
    userName: '',
    currentQuestion: '',
    questionNumber: 0,
    totalQuestions: 0,
    questionType: 'general',
    options: [],
    answer: '',
    currentFeedback: null,
    currentScore: 0,
    correctAnswer: '',
    suggestions: [],
    nextQuestion: '',
    report: null,
  });
  const [loading, setLoading] = useState(false);

  const startInterview = async () => {
    if (!state.userName.trim()) {
      alert('Please enter your name');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/interview/start`, {
        user_name: userInfo.userName,
      });

      setState({
        ...state,
        stage: 'interview',
        sessionId: response.data.session_id,
        currentQuestion: response.data.current_question,
        questionNumber: response.data.question_number,
        totalQuestions: response.data.total_questions,
        questionType: response.data.question_type,
        options: response.data.options || [],
        answer: '',
        currentFeedback: null,
      });
    } catch (error) {
      console.error('Error starting interview:', error);
      alert('Failed to start interview. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!state.answer.trim()) {
      alert('Please provide an answer');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/interview/submit-answer`, {
        session_id: state.sessionId,
        answer: state.answer,
      });

      if (response.data.status === 'completed') {
        setState({
          ...state,
          stage: 'complete',
          report: response.data.report,
        });
      } else {
        setState({
          ...state,
          stage: 'feedback',
          currentFeedback: response.data.feedback,
          currentScore: response.data.score || 5,
          correctAnswer: response.data.correct_answer || '',
          suggestions: response.data.suggestions || [],
          nextQuestion: response.data.next_question,
          questionNumber: response.data.question_number,
          questionType: response.data.question_type,
          options: response.data.options || [],
        });
      }
    } catch (error) {
      console.error('Error submitting answer:', error);
      alert('Failed to submit answer');
    } finally {
      setLoading(false);
    }
  };

  const moveToNextQuestion = () => {
    setState({
      ...state,
      stage: 'interview',
      currentQuestion: state.nextQuestion,
      answer: '',
      currentFeedback: null,
      correctAnswer: '',
      suggestions: [],
    });
  };

  const resetInterview = () => {
    setState({
      stage: 'start',
      sessionId: '',
      userName: '',
      currentQuestion: '',
      questionNumber: 0,
      totalQuestions: 0,
      questionType: 'general',
      options: [],
      answer: '',
      currentFeedback: null,
      currentScore: 0,
      correctAnswer: '',
      suggestions: [],
      nextQuestion: '',
      report: null,
    });
  };

  return (
    <div className="interview-container">
      <h1>Excel Mock Interview</h1>

      {state.stage === 'start' && (
        <div className="start-container">
          <h2>Welcome to the Excel Skills Assessment</h2>
          <p>This interview will test your Excel knowledge through 10 questions:</p>
          <ul className="interview-info">
            <li>5 Multiple Choice Questions</li>
            <li>5 Open-ended Questions</li>
          </ul>
          <input
            type="text"
            placeholder="Enter your name"
            value={state.userName}
            onChange={(e) => setState({ ...state, userName: e.target.value })}
            className="name-input"
            onKeyPress={(e) => e.key === 'Enter' && startInterview()}
          />
          <button onClick={startInterview} disabled={loading} className="start-button">
            {loading ? 'Starting...' : 'Start Interview'}
          </button>
        </div>
      )}

      {state.stage === 'interview' && (
        <div className="interview-container-active">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${((state.questionNumber - 1) / state.totalQuestions) * 100}%` }}
            />
          </div>
          <p className="question-counter">
            Question {state.questionNumber} of {state.totalQuestions}
            <span className="question-type-badge">
              {state.questionType === 'mcq' ? 'Multiple Choice' : 'Open Answer'}
            </span>
          </p>

          <div className="question-box">
            <h3>Question:</h3>
            <p>{state.currentQuestion}</p>
          </div>

          {state.questionType === 'mcq' ? (
            <div className="mcq-options">
              {state.options.map((option, index) => (
                <div key={index} className="option-item">
                  <input
                    type="radio"
                    id={`option-${index}`}
                    name="mcq-option"
                    value={option.charAt(0)}
                    checked={state.answer === option.charAt(0)}
                    onChange={(e) => setState({ ...state, answer: e.target.value })}
                  />
                  <label htmlFor={`option-${index}`}>{option}</label>
                </div>
              ))}
            </div>
          ) : (
            <textarea
              placeholder="Type your answer here..."
              value={state.answer}
              onChange={(e) => setState({ ...state, answer: e.target.value })}
              className="answer-input"
              rows={6}
            />
          )}

          <button onClick={submitAnswer} disabled={loading} className="submit-button">
            {loading ? 'Submitting...' : 'Submit Answer'}
          </button>
        </div>
      )}

      {state.stage === 'feedback' && (
        <div className="feedback-container">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${((state.questionNumber - 1) / state.totalQuestions) * 100}%` }}
            />
          </div>
          <p className="question-counter">
            Completed Question {state.questionNumber - 1} of {state.totalQuestions}
          </p>

          <div className="feedback-section">
            <h3>Your Answer:</h3>
            <div className="user-answer-box">
              <p>{state.answer}</p>
            </div>

            <h3>Feedback:</h3>
            <div className={`feedback-detail-box ${state.currentScore >= 7 ? 'feedback-good' : state.currentScore < 5 ? 'feedback-poor' : 'feedback-neutral'}`}>
              <p>{state.currentFeedback}</p>
            </div>

            {state.correctAnswer && (
              <>
                <h3>Correct Answer:</h3>
                <div className="correct-answer-box">
                  <p>{state.correctAnswer}</p>
                </div>
              </>
            )}

            {state.suggestions && state.suggestions.length > 0 && (
              <>
                <h3>Suggestions for Improvement:</h3>
                <div className="suggestions-box">
                  <ul>
                    {state.suggestions.map((suggestion: string, index: number) => (
                      <li key={index}>{suggestion}</li>
                    ))}
                  </ul>
                </div>
              </>
            )}

            <button onClick={moveToNextQuestion} className="next-button">
              Next Question →
            </button>
          </div>
        </div>
      )}

      {state.stage === 'complete' && state.report && (
        <div className="report-container">
          <h2>Interview Complete!</h2>
          <div className="report-card">
            <h3>{state.report.candidate_name}</h3>
            <div className="score-summary">
              <p className="score">Overall Score: {state.report.overall_score}/10</p>
              <p className="score-detail">MCQ Score: {state.report.mcq_score}/10</p>
              <p className="score-detail">General Questions Score: {state.report.general_score}/10</p>
            </div>
            <p className="level">Level: {state.report.performance_level}</p>
            <p>Duration: {state.report.duration_minutes} minutes</p>

            {state.report.summary && (
              <>
                {state.report.summary.strengths && state.report.summary.strengths.length > 0 && (
                  <div className="strengths-section">
                    <h4>Strengths:</h4>
                    <ul>
                      {state.report.summary.strengths.map((strength: string, index: number) => (
                        <li key={index}>{strength}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {state.report.summary.areas_for_improvement && state.report.summary.areas_for_improvement.length > 0 && (
                  <div className="improvement-section">
                    <h4>Areas for Improvement:</h4>
                    <ul>
                      {state.report.summary.areas_for_improvement.map((area: string, index: number) => (
                        <li key={index}>{area}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            )}

            <h4>Recommendations:</h4>
            <ul>
              {state.report.recommendations.map((rec: string, index: number) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>

            <h4>Detailed Feedback:</h4>
            {state.report.detailed_feedback.map((item: any, index: number) => (
              <div key={index} className="feedback-item">
                <h5>
                  Question {index + 1} 
                  <span className="question-type-label">
                    ({item.question_type === 'mcq' ? 'MCQ' : 'General'})
                  </span>
                </h5>
                <p className="question-text">{item.question}</p>
                <p><strong>Your Answer:</strong> {item.answer}</p>
                <p><strong>Score:</strong> {item.evaluation.score}/10</p>
                <p><strong>Feedback:</strong> {item.evaluation.feedback}</p>
                
                {item.question_type === 'general' && (
                  <>
                    {item.evaluation.strengths && item.evaluation.strengths.length > 0 && (
                      <div>
                        <strong>Strengths:</strong>
                        <ul>
                          {item.evaluation.strengths.map((strength: string, idx: number) => (
                            <li key={idx}>{strength}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {item.evaluation.missing_concepts && item.evaluation.missing_concepts.length > 0 && (
                      <div>
                        <strong>Areas for Improvement:</strong>
                        <ul>
                          {item.evaluation.missing_concepts.map((concept: string, idx: number) => (
                            <li key={idx}>{concept}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </>
                )}
              </div>
            ))}

            <button onClick={resetInterview} className="reset-button">
              Start New Interview
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default InterviewComponent;
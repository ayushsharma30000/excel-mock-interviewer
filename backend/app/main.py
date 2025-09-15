from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
from datetime import datetime
from .llm_service import llm_service

app = FastAPI(title="Excel Mock Interviewer API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class InterviewSession(BaseModel):
    session_id: str
    user_name: str
    current_question_index: int = 0
    responses: List[Dict] = []
    start_time: datetime
    end_time: Optional[datetime] = None
    
class UserResponse(BaseModel):
    session_id: str
    answer: str

class StartInterviewRequest(BaseModel):
    user_name: str

# Interview questions bank
EXCEL_QUESTIONS = [
    {
        "id": 1,
        "question": "What is the difference between VLOOKUP and XLOOKUP? When would you use each?",
        "difficulty": "intermediate",
        "category": "lookup_functions",
        "evaluation_criteria": ["accuracy", "practical_examples", "limitations_understanding"]
    },
    {
        "id": 2,
        "question": "How would you create a dynamic dashboard in Excel that updates automatically when new data is added?",
        "difficulty": "advanced",
        "category": "data_visualization",
        "evaluation_criteria": ["pivot_tables", "dynamic_ranges", "charts", "data_connections"]
    },
    {
        "id": 3,
        "question": "Explain how you would clean and prepare a dataset with 10,000 rows containing duplicates, missing values, and inconsistent formatting.",
        "difficulty": "intermediate",
        "category": "data_cleaning",
        "evaluation_criteria": ["remove_duplicates", "handling_nulls", "text_functions", "efficiency"]
    },
    {
        "id": 4,
        "question": "What are the most common Excel functions you use for financial analysis and why?",
        "difficulty": "intermediate",
        "category": "financial_analysis",
        "evaluation_criteria": ["function_knowledge", "practical_application", "financial_understanding"]
    },
    {
        "id": 5,
        "question": "Describe a complex Excel problem you've solved and walk me through your approach.",
        "difficulty": "advanced",
        "category": "problem_solving",
        "evaluation_criteria": ["problem_complexity", "solution_approach", "technical_skills", "communication"]
    }
]

# In-memory session storage (replace with Redis in production)
sessions = {}

@app.get("/")
async def root():
    return {"message": "Excel Mock Interviewer API is running"}

@app.post("/api/interview/start")
async def start_interview(request: StartInterviewRequest):
    session_id = str(uuid.uuid4())
    session = {
        "session_id": session_id,
        "user_name": request.user_name,
        "current_question_index": 0,
        "responses": [],
        "start_time": datetime.now(),
        "end_time": None
    }
    sessions[session_id] = session
    
    # Get first question
    first_question = EXCEL_QUESTIONS[0]
    
    return {
        "session_id": session_id,
        "message": f"Hello {request.user_name}! Welcome to the Excel Mock Interview. I'll ask you 5 questions to assess your Excel skills. Let's begin!",
        "current_question": first_question["question"],
        "question_number": 1,
        "total_questions": len(EXCEL_QUESTIONS)
    }

@app.post("/api/interview/submit-answer")
async def submit_answer(response: UserResponse):
    session = sessions.get(response.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    current_q = EXCEL_QUESTIONS[session["current_question_index"]]
    
    # Evaluate answer using Gemini
    evaluation = llm_service.evaluate_answer(
        question=current_q["question"],
        answer=response.answer,
        criteria=current_q["evaluation_criteria"]
    )
    
    # Store response
    session["responses"].append({
        "question": current_q["question"],
        "answer": response.answer,
        "evaluation": evaluation,
        "timestamp": datetime.now()
    })
    
    # Move to next question
    session["current_question_index"] += 1
    
    if session["current_question_index"] >= len(EXCEL_QUESTIONS):
        # Interview complete
        session["end_time"] = datetime.now()
        report = generate_final_report(session)
        return {
            "status": "completed",
            "report": report
        }
    else:
        # Get next question
        next_question = EXCEL_QUESTIONS[session["current_question_index"]]
        return {
            "status": "continue",
            "feedback": evaluation["feedback"],
            "next_question": next_question["question"],
            "question_number": session["current_question_index"] + 1,
            "total_questions": len(EXCEL_QUESTIONS)
        }

def generate_final_report(session: Dict) -> Dict:
    total_score = sum(r["evaluation"]["score"] for r in session["responses"])
    avg_score = total_score / len(session["responses"])
    
    return {
        "candidate_name": session["user_name"],
        "interview_date": session["start_time"].isoformat(),
        "duration_minutes": int((session["end_time"] - session["start_time"]).total_seconds() / 60),
        "overall_score": round(avg_score, 1),
        "performance_level": get_performance_level(avg_score),
        "detailed_feedback": session["responses"],
        "recommendations": generate_recommendations(session["responses"])
    }

def get_performance_level(score: float) -> str:
    if score >= 8.5:
        return "Expert"
    elif score >= 7:
        return "Advanced"
    elif score >= 5:
        return "Intermediate"
    else:
        return "Beginner"

def generate_recommendations(responses: List[Dict]) -> List[str]:
    recommendations = []
    avg_score = sum(r["evaluation"]["score"] for r in responses) / len(responses)
    
    if avg_score < 6:
        recommendations.append("Consider taking advanced Excel courses to strengthen foundational skills")
    
    # Add specific recommendations based on weak areas
    for response in responses:
        if response["evaluation"]["score"] < 5:
            recommendations.append(f"Focus on improving: {response['question'][:50]}...")
    
    return recommendations[:3]  # Limit to top 3 recommendations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
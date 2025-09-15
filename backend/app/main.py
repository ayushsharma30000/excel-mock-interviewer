from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
from datetime import datetime
import random

app = FastAPI(title="Excel Mock Interviewer API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
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
    selected_questions: List[Dict] = []
    
class UserResponse(BaseModel):
    session_id: str
    answer: str

class StartInterviewRequest(BaseModel):
    user_name: str

# MCQ Questions Bank
MCQ_QUESTIONS = [
    {
        "id": "mcq_1",
        "question": "Which function would you use to find the position of a specific character in a text string?",
        "options": ["A) FIND()", "B) VLOOKUP()", "C) MATCH()", "D) INDEX()"],
        "correct_answer": "A",
        "difficulty": "easy",
        "category": "text_functions",
        "question_type": "mcq"
    },
    {
        "id": "mcq_2",
        "question": "What is the keyboard shortcut to create an absolute reference in Excel?",
        "options": ["A) Ctrl + $", "B) F4", "C) Alt + $", "D) Shift + F4"],
        "correct_answer": "B",
        "difficulty": "easy",
        "category": "shortcuts",
        "question_type": "mcq"
    },
    {
        "id": "mcq_3",
        "question": "Which of the following is NOT a valid Excel chart type?",
        "options": ["A) Waterfall", "B) Sunburst", "C) Pyramid", "D) Treemap"],
        "correct_answer": "C",
        "difficulty": "intermediate",
        "category": "charts",
        "question_type": "mcq"
    },
    {
        "id": "mcq_4",
        "question": "What does the IFERROR function do?",
        "options": [
            "A) Checks if a cell contains an error",
            "B) Returns a specified value if a formula results in an error",
            "C) Removes all errors from a worksheet",
            "D) Counts the number of errors in a range"
        ],
        "correct_answer": "B",
        "difficulty": "easy",
        "category": "error_handling",
        "question_type": "mcq"
    },
    {
        "id": "mcq_5",
        "question": "Which function would you use to return the nth largest value in a dataset?",
        "options": ["A) MAX()", "B) LARGE()", "C) RANK()", "D) TOP()"],
        "correct_answer": "B",
        "difficulty": "intermediate",
        "category": "statistical_functions",
        "question_type": "mcq"
    },
    {
        "id": "mcq_6",
        "question": "What is the maximum number of rows in Excel 365?",
        "options": ["A) 65,536", "B) 1,048,576", "C) 2,097,152", "D) Unlimited"],
        "correct_answer": "B",
        "difficulty": "easy",
        "category": "excel_basics",
        "question_type": "mcq"
    },
    {
        "id": "mcq_7",
        "question": "Which of these is a dynamic array function introduced in Excel 365?",
        "options": ["A) VLOOKUP()", "B) SUMIF()", "C) FILTER()", "D) COUNTIF()"],
        "correct_answer": "C",
        "difficulty": "intermediate",
        "category": "dynamic_arrays",
        "question_type": "mcq"
    },
    {
        "id": "mcq_8",
        "question": "What does pressing Ctrl+Shift+L do in Excel?",
        "options": [
            "A) Lock cells",
            "B) Toggle AutoFilter",
            "C) Create a list",
            "D) Insert a hyperlink"
        ],
        "correct_answer": "B",
        "difficulty": "easy",
        "category": "shortcuts",
        "question_type": "mcq"
    },
    {
        "id": "mcq_9",
        "question": "Which function combines text from multiple cells into one cell?",
        "options": ["A) JOIN()", "B) COMBINE()", "C) CONCATENATE()", "D) MERGE()"],
        "correct_answer": "C",
        "difficulty": "easy",
        "category": "text_functions",
        "question_type": "mcq"
    },
    {
        "id": "mcq_10",
        "question": "What is the purpose of the INDIRECT function?",
        "options": [
            "A) To create indirect cell references",
            "B) To convert text strings into cell references",
            "C) To create circular references",
            "D) To reference cells in closed workbooks"
        ],
        "correct_answer": "B",
        "difficulty": "intermediate",
        "category": "reference_functions",
        "question_type": "mcq"
    }
]

# General Questions Bank (expanded)
GENERAL_QUESTIONS = [
    {
        "id": "gen_1",
        "question": "What is the difference between VLOOKUP and XLOOKUP? When would you use each?",
        "difficulty": "intermediate",
        "category": "lookup_functions",
        "evaluation_criteria": ["accuracy", "practical_examples", "limitations_understanding"],
        "question_type": "general"
    },
    {
        "id": "gen_2",
        "question": "How would you create a dynamic dashboard in Excel that updates automatically when new data is added?",
        "difficulty": "advanced",
        "category": "data_visualization",
        "evaluation_criteria": ["pivot_tables", "dynamic_ranges", "charts", "data_connections"],
        "question_type": "general"
    },
    {
        "id": "gen_3",
        "question": "Explain how you would clean and prepare a dataset with 10,000 rows containing duplicates, missing values, and inconsistent formatting.",
        "difficulty": "intermediate",
        "category": "data_cleaning",
        "evaluation_criteria": ["remove_duplicates", "handling_nulls", "text_functions", "efficiency"],
        "question_type": "general"
    },
    {
        "id": "gen_4",
        "question": "What are the most common Excel functions you use for financial analysis and why?",
        "difficulty": "intermediate",
        "category": "financial_analysis",
        "evaluation_criteria": ["function_knowledge", "practical_application", "financial_understanding"],
        "question_type": "general"
    },
    {
        "id": "gen_5",
        "question": "Describe a complex Excel problem you've solved and walk me through your approach.",
        "difficulty": "advanced",
        "category": "problem_solving",
        "evaluation_criteria": ["problem_complexity", "solution_approach", "technical_skills", "communication"],
        "question_type": "general"
    },
    {
        "id": "gen_6",
        "question": "How would you use Power Query to combine data from multiple sources and transform it for analysis?",
        "difficulty": "advanced",
        "category": "power_query",
        "evaluation_criteria": ["data_sources", "transformation_steps", "m_language", "best_practices"],
        "question_type": "general"
    },
    {
        "id": "gen_7",
        "question": "Explain the concept of array formulas and provide an example of when they would be more efficient than regular formulas.",
        "difficulty": "intermediate",
        "category": "array_formulas",
        "evaluation_criteria": ["concept_understanding", "practical_examples", "performance_benefits"],
        "question_type": "general"
    },
    {
        "id": "gen_8",
        "question": "How would you set up a spreadsheet to track project budgets with automatic variance analysis and conditional formatting alerts?",
        "difficulty": "intermediate",
        "category": "project_management",
        "evaluation_criteria": ["structure", "formulas", "conditional_formatting", "reporting"],
        "question_type": "general"
    },
    {
        "id": "gen_9",
        "question": "What are your strategies for optimizing large Excel files that are running slowly?",
        "difficulty": "advanced",
        "category": "performance_optimization",
        "evaluation_criteria": ["file_size_reduction", "formula_optimization", "data_model", "best_practices"],
        "question_type": "general"
    },
    {
        "id": "gen_10",
        "question": "How would you create a data validation system to ensure data quality in a shared Excel workbook?",
        "difficulty": "intermediate",
        "category": "data_validation",
        "evaluation_criteria": ["validation_rules", "error_messages", "dropdown_lists", "custom_formulas"],
        "question_type": "general"
    }
]

# In-memory session storage (replace with Redis in production)
sessions = {}

def select_interview_questions():
    """Randomly select 5 MCQ and 5 general questions for the interview"""
    selected_mcq = random.sample(MCQ_QUESTIONS, 5)
    selected_general = random.sample(GENERAL_QUESTIONS, 5)
    
    # Combine questions: MCQs first, then general questions
    return selected_mcq + selected_general

@app.get("/")
async def root():
    return {"message": "Excel Mock Interviewer API is running"}

@app.post("/api/interview/start")
async def start_interview(request: StartInterviewRequest):
    session_id = str(uuid.uuid4())
    selected_questions = select_interview_questions()
    
    session = {
        "session_id": session_id,
        "user_name": request.user_name,
        "current_question_index": 0,
        "responses": [],
        "start_time": datetime.now(),
        "end_time": None,
        "selected_questions": selected_questions
    }
    sessions[session_id] = session
    
    # Get first question
    first_question = selected_questions[0]
    
    response = {
        "session_id": session_id,
        "message": f"Hello {request.user_name}! Welcome to the Excel Mock Interview. I'll ask you 10 questions (5 multiple choice and 5 open-ended) to assess your Excel skills. Let's begin!",
        "current_question": first_question["question"],
        "question_number": 1,
        "total_questions": 10,
        "question_type": first_question["question_type"]
    }
    
    # Add options if it's an MCQ
    if first_question["question_type"] == "mcq":
        response["options"] = first_question["options"]
    
    return response

@app.post("/api/interview/submit-answer")
async def submit_answer(response: UserResponse):
    session = sessions.get(response.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    current_q = session["selected_questions"][session["current_question_index"]]
    
    # Handle MCQ vs General question evaluation differently
    if current_q["question_type"] == "mcq":
        # Simple evaluation for MCQ
        is_correct = response.answer.upper().strip() == current_q["correct_answer"]
        evaluation = {
            "score": 10 if is_correct else 0,
            "feedback": f"{'Correct!' if is_correct else f'Incorrect. The correct answer is {current_q['correct_answer']}'}",
            "correct_answer": current_q["correct_answer"],
            "is_correct": is_correct
        }
    else:
        # Use LLM for general questions
        try:
            from app.llm_service import llm_service
            
            evaluation = llm_service.evaluate_answer(
                question=current_q["question"],
                answer=response.answer,
                criteria=current_q["evaluation_criteria"]
            )
        except Exception as e:
            print(f"Error with LLM service: {e}")
            evaluation = {
                "score": 5,
                "feedback": "Thank you for your answer. The system is currently unable to provide detailed feedback.",
                "strengths": ["Provided an answer"],
                "improvements": ["Unable to assess at this time"],
                "correct_concepts": [],
                "missing_concepts": []
            }
    
    # Store response
    session["responses"].append({
        "question": current_q["question"],
        "question_type": current_q["question_type"],
        "answer": response.answer,
        "evaluation": evaluation,
        "timestamp": datetime.now()
    })
    
    # Move to next question
    session["current_question_index"] += 1
    
    if session["current_question_index"] >= len(session["selected_questions"]):
        # Interview complete
        session["end_time"] = datetime.now()
        report = generate_final_report(session)
        return {
            "status": "completed",
            "report": report
        }
    else:
        # Get next question
        next_question = session["selected_questions"][session["current_question_index"]]
        response_data = {
            "status": "continue",
            "feedback": evaluation.get("feedback", "Thank you for your answer."),
            "score": evaluation.get("score", 5),
            "next_question": next_question["question"],
            "question_number": session["current_question_index"] + 1,
            "total_questions": 10,
            "question_type": next_question["question_type"]
        }
        
        # Add options if next question is MCQ
        if next_question["question_type"] == "mcq":
            response_data["options"] = next_question["options"]
        
        # Add additional feedback for general questions
        if current_q["question_type"] == "general":
            response_data["suggestions"] = evaluation.get("suggestions", [])
            response_data["correct_answer"] = evaluation.get("correct_answer", "")
        
        return response_data

def generate_final_report(session: Dict) -> Dict:
    responses = session["responses"]
    
    # Separate MCQ and general question scores
    mcq_responses = [r for r in responses if r["question_type"] == "mcq"]
    general_responses = [r for r in responses if r["question_type"] == "general"]
    
    # Calculate scores
    mcq_score = sum(r["evaluation"].get("score", 0) for r in mcq_responses) / len(mcq_responses) if mcq_responses else 0
    general_score = sum(r["evaluation"].get("score", 0) for r in general_responses) / len(general_responses) if general_responses else 0
    
    # Overall score (weighted average)
    overall_score = (mcq_score + general_score) / 2 if responses else 0
    
    return {
        "candidate_name": session["user_name"],
        "interview_date": session["start_time"].isoformat(),
        "duration_minutes": int((session["end_time"] - session["start_time"]).total_seconds() / 60) if session["end_time"] else 0,
        "overall_score": round(overall_score, 1),
        "mcq_score": round(mcq_score, 1),
        "general_score": round(general_score, 1),
        "performance_level": get_performance_level(overall_score),
        "detailed_feedback": responses,
        "recommendations": generate_recommendations(responses),
        "summary": {
            "total_questions": len(responses),
            "mcq_questions": len(mcq_responses),
            "general_questions": len(general_responses),
            "strengths": get_strengths(responses),
            "areas_for_improvement": get_improvement_areas(responses)
        }
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

def get_strengths(responses: List[Dict]) -> List[str]:
    strengths = []
    high_score_categories = {}
    
    for response in responses:
        if response["evaluation"].get("score", 0) >= 7:
            category = response.get("category", "general")
            if category not in high_score_categories:
                high_score_categories[category] = 0
            high_score_categories[category] += 1
    
    for category, count in high_score_categories.items():
        if count >= 1:
            strengths.append(f"Strong performance in {category.replace('_', ' ').title()}")
    
    return strengths[:3]  # Return top 3 strengths

def get_improvement_areas(responses: List[Dict]) -> List[str]:
    areas = []
    low_score_categories = {}
    
    for response in responses:
        if response["evaluation"].get("score", 0) < 5:
            category = response.get("category", "general")
            if category not in low_score_categories:
                low_score_categories[category] = 0
            low_score_categories[category] += 1
    
    for category, count in low_score_categories.items():
        if count >= 1:
            areas.append(f"Needs improvement in {category.replace('_', ' ').title()}")
    
    return areas[:3]  # Return top 3 areas for improvement

def generate_recommendations(responses: List[Dict]) -> List[str]:
    recommendations = []
    
    if not responses:
        return ["Complete the interview to receive recommendations"]
    
    # Separate MCQ and general responses
    mcq_responses = [r for r in responses if r["question_type"] == "mcq"]
    general_responses = [r for r in responses if r["question_type"] == "general"]
    
    # Calculate average scores
    mcq_avg = sum(r["evaluation"].get("score", 0) for r in mcq_responses) / len(mcq_responses) if mcq_responses else 0
    general_avg = sum(r["evaluation"].get("score", 0) for r in general_responses) / len(general_responses) if general_responses else 0
    overall_avg = (mcq_avg + general_avg) / 2
    
    # General recommendations based on overall performance
    if overall_avg < 5:
        recommendations.append("Consider taking a comprehensive Excel fundamentals course to strengthen your foundation")
    elif overall_avg < 7:
        recommendations.append("Focus on advanced Excel features like Power Query, Power Pivot, and complex formulas")
    else:
        recommendations.append("Excellent Excel skills! Consider pursuing Excel expert certification or teaching others")
    
    # MCQ-specific recommendations
    if mcq_avg < 6:
        recommendations.append("Review Excel terminology and basic function syntax through practice tests")
    
    # General question-specific recommendations
    if general_avg < 6:
        recommendations.append("Practice explaining Excel concepts and solutions in real-world scenarios")
    
    # Category-specific recommendations
    weak_categories = {}
    for response in responses:
        if response["evaluation"].get("score", 0) < 5:
            category = response.get("category", "general")
            if category not in weak_categories:
                weak_categories[category] = 0
            weak_categories[category] += 1
    
    for category, count in weak_categories.items():
        if count >= 2:
            readable_category = category.replace('_', ' ').title()
            recommendations.append(f"Dedicate extra study time to {readable_category}")
    
    return list(set(recommendations))[:5]  # Remove duplicates and limit to 5 recommendations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
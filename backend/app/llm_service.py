import os
from typing import Dict, List, Optional
import google.generativeai as genai
from dotenv import load_dotenv
import json
import time

load_dotenv()

class GeminiService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def evaluate_answer(self, question: str, answer: str, criteria: List[str]) -> Dict:
        """Evaluate a candidate's answer using Gemini"""
        
        prompt = f"""
        You are an expert Excel interviewer. Evaluate this answer and provide helpful feedback.
        
        Question: {question}
        Candidate's Answer: {answer}
        
        Evaluation criteria: {', '.join(criteria)}
        
        Provide a JSON response with this exact format:
        {{
            "score": <number 0-10>,
            "feedback": "<2-3 sentences of specific feedback WITHOUT mentioning the score>",
            "correct_answer": "<Provide a comprehensive correct answer to the question>",
            "suggestions": ["<specific suggestion 1>", "<specific suggestion 2>"],
            "strengths": ["<what they got right>"],
            "missing_concepts": ["<what they missed>"]
        }}
        
        Important:
        - Do NOT mention the score in the feedback
        - Focus on what they did well and what to improve
        - Provide the actual correct answer
        - Give actionable suggestions
        
        Return ONLY the JSON, no other text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean the response to get JSON
            json_str = response.text.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0]
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0]
            
            return json.loads(json_str.strip())
        except Exception as e:
            print(f"Error evaluating answer: {e}")
            # Return default evaluation on error
            return {
                "score": 5,
                "feedback": "Thank you for your answer. Let me provide some guidance on this topic.",
                "correct_answer": "Please refer to Excel documentation for detailed information on this topic.",
                "suggestions": ["Review the core concepts", "Practice with real examples"],
                "strengths": ["You provided an answer"],
                "missing_concepts": ["Unable to assess at this time"]
            }

# Initialize service
llm_service = GeminiService()
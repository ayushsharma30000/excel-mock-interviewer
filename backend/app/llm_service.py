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
        You are an expert Excel interviewer. Evaluate this answer based on technical accuracy.
        
        Question: {question}
        Candidate's Answer: {answer}
        
        Evaluation criteria: {', '.join(criteria)}
        
        Provide a JSON response with this exact format:
        {{
            "score": <number 0-10>,
            "feedback": "<2-3 sentences of specific feedback>",
            "strengths": ["<strength1>", "<strength2>"],
            "improvements": ["<area1>", "<area2>"],
            "correct_concepts": ["<concept1>", "<concept2>"],
            "missing_concepts": ["<concept1>", "<concept2>"]
        }}
        
        Be fair but thorough. Score breakdown:
        - 9-10: Expert level, comprehensive answer
        - 7-8: Strong understanding with minor gaps
        - 5-6: Basic understanding, some errors
        - 3-4: Limited understanding
        - 0-2: Incorrect or very limited
        
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
                "feedback": "Unable to fully evaluate the response. Please try again.",
                "strengths": ["Attempted to answer"],
                "improvements": ["Could not fully assess"],
                "correct_concepts": [],
                "missing_concepts": []
            }
    
    def generate_follow_up_question(self, topic: str, difficulty: str) -> str:
        """Generate a follow-up question based on topic and difficulty"""
        
        prompt = f"""
        Generate one Excel interview question about {topic} at {difficulty} level.
        The question should be practical and test real-world Excel skills.
        Keep it concise (2-3 sentences max).
        Do not include the answer.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating question: {e}")
            return "How do you handle errors in Excel formulas?"

# Initialize service
llm_service = GeminiService()
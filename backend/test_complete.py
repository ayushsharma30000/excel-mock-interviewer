from app.llm_service import llm_service

print("Testing LLM Service...")

# Test evaluation
result = llm_service.evaluate_answer(
    question="What is VLOOKUP used for?",
    answer="VLOOKUP is used to search for a value in the leftmost column of a table and return a value from the same row in a specified column.",
    criteria=["accuracy", "completeness", "practical understanding"]
)

print("\nEvaluation Result:")
print(f"Score: {result.get('score', 'N/A')}/10")
print(f"Feedback: {result.get('feedback', 'N/A')}")
print(f"Strengths: {result.get('strengths', [])}")
print(f"Areas for improvement: {result.get('improvements', [])}")

# Test question generation
print("\n" + "="*50 + "\n")
new_question = llm_service.generate_follow_up_question("pivot tables", "intermediate")
print(f"Generated Question: {new_question}")
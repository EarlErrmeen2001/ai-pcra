
from analyzer_of_code import AnalyzerOfCode
import openai
import json

class ReviewerOfAI:
    def __init__(self, api_key):
        openai.api_key = api_key

    def explain_issue(self, code_snippet, issue):
        """This use GPT-4 to explain a code issue"""
        prompt = f"""
        Explain this coding issue in simple terms and suggest a fix:
        Code: {code_snippet}
        Issue: {issue}
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def review_code(self, code_file):
        """This Automatically review a file"""
        analyzer = AnalyzerOfCode()
        report = analyzer.analyze(code_file)
        
        feedback_of_ai = []
        for issue in report["pylint"]:
            explanation = self.explain_issue(issue["code"], issue["message"])
            feedback_of_ai.append({
                "line": issue["line"],
                "issue": issue["message"],
                "ai_explanation": explanation
            })
        
        return feedback_of_ai
    
reviewer = ReviewerOfAI("your-openai-key")
print(reviewer.review_code("my_first_test_file.py"))

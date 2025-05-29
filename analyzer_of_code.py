import ast
import json
import subprocess
import fire

class AnalyzerOfCode:
    @staticmethod
    def run_pylint(code_file):
        """Run Pylint which is general python code for quality and return JSON report"""
        result = subprocess.run(
            ["pylint", "--output-format=json", code_file],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)

    @staticmethod
    def run_bandit(code_file):
        """Run Bandit which is security audits for python apps (security scanner)"""
        result = subprocess.run(
            ["bandit", "-f", "json", "-q", "-r", code_file],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)
    @staticmethod
    def parse_ast(code_file):
        """Parse code using AST to detect anti-patterns (let's you inspect\modify code programmatically)"""
        with open(code_file, "r") as f:
            tree = ast.parse(f.read())
        
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                issues.append({
                    "line": node.lineno,
                    "issue": "Consider using list comprehensions for simplicity"
                })
        return issues

    def analyze(self, code_file):
        """Run all checks;pylint, bandit, ast_issues and generate a report"""

        report = {
            "pylint": self.run_pylint(code_file),
            "bandit": self.run_bandit(code_file),
            "ast_issues": self.parse_ast(code_file)
        }
        return report
    
if __name__ == "__main__":
    fire.Fire(AnalyzerOfCode)

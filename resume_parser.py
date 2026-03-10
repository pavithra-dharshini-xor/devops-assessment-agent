"""
Resume Parser Module
Extracts text from PDF resumes and parses key information
"""

import re
from typing import Dict, List, Optional
import PyPDF2
from io import BytesIO


class ResumeParser:
    """Parse and extract information from candidate resumes"""
    
    def __init__(self):
        self.devops_keywords = [
            'kubernetes', 'docker', 'jenkins', 'terraform', 'ansible',
            'aws', 'azure', 'gcp', 'cloud', 'ci/cd', 'gitlab', 'github actions',
            'helm', 'prometheus', 'grafana', 'elk', 'datadog', 'newrelic',
            'python', 'bash', 'shell', 'scripting', 'linux', 'monitoring',
            'observability', 'sre', 'devops', 'infrastructure', 'automation',
            'argocd', 'flux', 'gitops', 'vault', 'consul', 'istio',
            'nginx', 'apache', 'load balancer', 'cdn', 'api gateway'
        ]
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF resume"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def extract_text_from_bytes(self, pdf_bytes: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF bytes: {str(e)}")
    
    def extract_experience_years(self, text: str) -> Optional[float]:
        """Extract total years of experience from resume text"""
        patterns = [
            r'(\d+\.?\d*)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+\.?\d*)\+?\s*years?',
            r'(\d+\.?\d*)\s*years?\s+in\s+(?:devops|sre|cloud|infrastructure)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        
        # Try to infer from date ranges
        date_pattern = r'(20\d{2})\s*[-–—]\s*(20\d{2}|present|current)'
        dates = re.findall(date_pattern, text, re.IGNORECASE)
        if dates:
            total_years = 0
            for start, end in dates:
                end_year = 2026 if end.lower() in ['present', 'current'] else int(end)
                total_years += end_year - int(start)
            return total_years if total_years > 0 else None
        
        return None
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from resume"""
        text_lower = text.lower()
        found_skills = []
        
        for keyword in self.devops_keywords:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(keyword.title())
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in found_skills:
            if skill.lower() not in seen:
                seen.add(skill.lower())
                unique_skills.append(skill)
        
        return sorted(unique_skills)  # Return sorted for consistency
    
    def extract_projects(self, text: str) -> List[str]:
        """Extract project descriptions from resume"""
        projects = []
        
        # Look for project sections
        project_section_patterns = [
            r'(?:projects?|experience|work\s+experience)[:\s]*\n(.*?)(?:\n\n|\Z)',
        ]
        
        # Split by common delimiters and extract meaningful bullet points
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ['project', 'developed', 'implemented', 'deployed', 'managed', 'automated']):
                if len(line.strip()) > 30:  # Filter out short lines
                    projects.append(line.strip())
        
        return projects[:10]  # Return top 10 projects
    
    def extract_responsibilities(self, text: str) -> List[str]:
        """Extract key responsibilities from resume"""
        responsibilities = []
        
        responsibility_keywords = [
            'responsible for', 'managed', 'led', 'architected', 'designed',
            'implemented', 'automated', 'deployed', 'maintained', 'monitored',
            'troubleshot', 'optimized', 'scaled', 'configured', 'integrated'
        ]
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in responsibility_keywords):
                if len(line.strip()) > 30 and len(line.strip()) < 300:
                    responsibilities.append(line.strip())
        
        return responsibilities[:15]  # Return top 15 responsibilities
    
    def determine_seniority(self, years: Optional[float]) -> str:
        """Determine seniority level based on experience years"""
        if years is None:
            return "Entry"
        elif years < 2:
            return "Entry"
        elif years < 5:
            return "Mid"
        elif years < 8:
            return "Senior"
        else:
            return "Staff/Principal"
    
    def parse_resume(self, pdf_path: str) -> Dict:
        """Main method to parse resume and extract all information"""
        text = self.extract_text_from_pdf(pdf_path)
        
        experience_years = self.extract_experience_years(text)
        skills = self.extract_skills(text)
        projects = self.extract_projects(text)
        responsibilities = self.extract_responsibilities(text)
        seniority = self.determine_seniority(experience_years)
        
        return {
            'raw_text': text,
            'experience_years': experience_years,
            'seniority': seniority,
            'skills': skills,
            'projects': projects,
            'responsibilities': responsibilities,
            'skill_count': len(skills)
        }
    
    def parse_resume_from_text(self, text: str) -> Dict:
        """Parse resume from already extracted text"""
        experience_years = self.extract_experience_years(text)
        skills = self.extract_skills(text)
        projects = self.extract_projects(text)
        responsibilities = self.extract_responsibilities(text)
        seniority = self.determine_seniority(experience_years)
        
        return {
            'raw_text': text,
            'experience_years': experience_years,
            'seniority': seniority,
            'skills': skills,
            'projects': projects,
            'responsibilities': responsibilities,
            'skill_count': len(skills)
        }


if __name__ == "__main__":
    # Test the parser
    parser = ResumeParser()
    
    # Example test with a sample resume
    sample_text = """
    John Doe
    DevOps Engineer
    
    Professional Summary:
    DevOps Engineer with 5 years of experience in cloud infrastructure and automation.
    
    Skills:
    Kubernetes, Docker, Terraform, AWS, Jenkins, Python, Bash, Prometheus, Grafana
    
    Experience:
    Senior DevOps Engineer | Tech Corp | 2021 - Present
    - Managed Kubernetes clusters serving 1M+ users
    - Automated CI/CD pipelines using Jenkins and GitLab CI
    - Implemented infrastructure as code using Terraform
    - Deployed monitoring solutions with Prometheus and Grafana
    
    Projects:
    - Migrated legacy infrastructure to AWS cloud
    - Implemented GitOps workflow using ArgoCD
    - Developed Python automation scripts for deployment
    """
    
    result = parser.parse_resume_from_text(sample_text)
    print("Parsed Resume Information:")
    print(f"Experience Years: {result['experience_years']}")
    print(f"Seniority: {result['seniority']}")
    print(f"Skills Found: {result['skills']}")
    print(f"Projects Count: {len(result['projects'])}")
    print(f"Responsibilities Count: {len(result['responsibilities'])}")

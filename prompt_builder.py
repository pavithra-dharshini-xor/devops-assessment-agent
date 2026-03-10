"""
Prompt Builder Module
Builds prompts using agent instructions and candidate profile
"""

from typing import Dict


class PromptBuilder:
    """Build structured prompts for LLM to generate interview assessments"""
    
    def __init__(self, agent_instructions_path: str = "agent.md"):
        self.agent_instructions = self._load_agent_instructions(agent_instructions_path)
    
    def _load_agent_instructions(self, path: str) -> str:
        """Load agent instructions from agent.md file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise Exception(f"Agent instructions file not found: {path}")
    
    def build_assessment_prompt(
        self,
        candidate_profile: Dict,
        position: str,
        interview_round: str,
        complexity_level: str
    ) -> str:
        """
        Build a comprehensive prompt for generating interview assessment
        
        Args:
            candidate_profile: Parsed resume data
            position: DevOps / SRE / Observability
            interview_round: L1 / L2
            complexity_level: Basic / Intermediate / Advanced
        
        Returns:
            Formatted prompt string
        """
        
        prompt = f"""# Interview Assessment Generation Task

You are an expert technical interviewer for DevOps, SRE, and Observability roles.

Your task is to generate a comprehensive interview assessment sheet based on the following information.

---

## Agent Instructions

{self.agent_instructions}

---

## Candidate Profile Analysis

**Experience Level:** {candidate_profile.get('experience_years', 'Not specified')} years
**Seniority:** {candidate_profile.get('seniority', 'Not specified')}
**Technical Skills Detected:** {', '.join(candidate_profile.get('skills', [])[:20])}
**Number of Skills:** {candidate_profile.get('skill_count', 0)}

### Key Projects & Responsibilities:
{self._format_list(candidate_profile.get('projects', [])[:5])}
{self._format_list(candidate_profile.get('responsibilities', [])[:5])}

---

## Interview Configuration

**Position:** {position}
**Interview Round:** {interview_round}
**Complexity Level:** {complexity_level}

---

## Generation Requirements

Based on the candidate profile and interview configuration above, generate a complete interview assessment sheet with:

### Question Distribution for {interview_round} Round:

"""
        
        # Add round-specific instructions
        if interview_round == "L1":
            prompt += """
**L1 Round Focus:**
- 5 Multiple Choice Questions (MCQ) - Test fundamentals
- 4 Scenario-Based Questions - Real-world problem solving
- 2 Coding/Scripting Questions - Automation capability
- 3 Technology/Skill Based Questions - Tool expertise
- 2 Responsibility-Based Questions - Verify actual experience

Total: 16 questions
"""
        else:  # L2
            prompt += """
**L2 Round Focus:**
- 3 Multiple Choice Questions (MCQ) - Advanced concepts
- 6 Scenario-Based Questions - Complex production scenarios
- 3 Coding/Scripting Questions - Advanced automation
- 3 Technology/Skill Based Questions - Deep technical knowledge
- 3 Responsibility-Based Questions - Leadership & ownership

Total: 18 questions
"""
        
        prompt += f"""
---

## Critical Instructions

1. **Personalize to Candidate:** Generate questions specifically tailored to the skills and technologies mentioned in the candidate's profile ({', '.join(candidate_profile.get('skills', [])[:10])})

2. **Align with Experience:** Adjust question difficulty to match {candidate_profile.get('seniority', 'Not specified')} level ({candidate_profile.get('experience_years', 'N/A')} years)

3. **Real-World Focus:** Prioritize scenario-based questions that reflect actual DevOps/SRE work

4. **Responsibility Validation:** Include questions that verify whether the candidate has actually performed the responsibilities listed in their resume

5. **Provide Complete Answers:** For each question, provide:
   - Clear question text
   - Expected answer/solution
   - Evaluation criteria
   - Weightage percentage

---

## Output Format

Generate the assessment in the following structured format:

```
# Interview Assessment Sheet

**Role:** {position}
**Round:** {interview_round}
**Candidate Experience:** {candidate_profile.get('experience_years', 'N/A')} years ({candidate_profile.get('seniority', 'N/A')})
**Complexity Level:** {complexity_level}
**Generated:** [Current Date]

---

## Section 1: Multiple Choice Questions (MCQ) - 20%

### Question 1
**Question:** [Question text]

**Options:**
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

**Correct Answer:** [A/B/C/D]

**Explanation:** [Why this answer is correct and what it tests]

**Weightage:** [X%]

---

## Section 2: Scenario-Based Questions - 40%

### Scenario 1
**Scenario:** [Detailed production scenario description]

**Question:** [What should the candidate do?]

**Expected Answer:**
- [Key point 1]
- [Key point 2]
- [Commands/steps to take]
- [Reasoning]

**Evaluation Criteria:**
- [What to look for in answer]
- [Bonus points]

**Weightage:** [X%]

---

## Section 3: Coding/Scripting Questions - 20%

### Problem 1
**Problem:** [Automation task description]

**Expected Approach:**
- [Solution strategy]
- [Key concepts to use]

**Sample Solution:**
```[language]
[Code solution]
```

**Evaluation Criteria:**
- [Code quality]
- [Error handling]
- [Best practices]

**Weightage:** [X%]

---

## Section 4: Technology/Skill Based Questions - 10%

### Question 1
**Technology:** [Specific tech from candidate profile]

**Question:** [Technical question]

**Expected Answer:**
- [Key concepts]
- [Real-world application]

**Weightage:** [X%]

---

## Section 5: Responsibility-Based Questions - 10%

### Question 1
**Responsibility:** [From candidate's resume]

**Question:** [Verify they actually did this]

**Expected Answer:**
- [Specific details they should know]
- [Tools/processes used]
- [Outcomes achieved]

**Red Flags:**
- [Vague answers]
- [Lack of technical depth]

**Weightage:** [X%]

---

## Scoring Summary

| Section | Weightage | Points |
|---------|-----------|--------|
| MCQ | 20% | /20 |
| Scenario-Based | 40% | /40 |
| Coding/Scripting | 20% | /20 |
| Technology/Skills | 10% | /10 |
| Responsibility | 10% | /10 |
| **Total** | **100%** | **/100** |

---

## Evaluation Guidelines

**90-100:** Exceptional candidate - Strong hire
**75-89:** Good candidate - Hire
**60-74:** Average candidate - Maybe hire with training
**Below 60:** Not recommended

---

## Interviewer Notes

[Space for interviewer to add observations during the interview]
```

---

Now generate the complete interview assessment sheet following the format above.
"""
        
        return prompt
    
    def _format_list(self, items: list) -> str:
        """Format a list of items as bullet points"""
        if not items:
            return "- None specified"
        return '\n'.join([f"- {item}" for item in items])
    
    def build_quick_analysis_prompt(self, candidate_profile: Dict) -> str:
        """Build a prompt for quick candidate analysis"""
        prompt = f"""Analyze this candidate profile and provide a brief assessment:

**Experience:** {candidate_profile.get('experience_years', 'Not specified')} years
**Seniority:** {candidate_profile.get('seniority', 'Not specified')}
**Skills:** {', '.join(candidate_profile.get('skills', []))}
**Key Responsibilities:** {len(candidate_profile.get('responsibilities', []))} items found

Provide:
1. Recommended interview round (L1 or L2)
2. Suggested complexity level (Basic/Intermediate/Advanced)
3. Key areas to focus on during interview
4. Potential red flags to watch for
"""
        return prompt


if __name__ == "__main__":
    # Test the prompt builder
    builder = PromptBuilder()
    
    # Sample candidate profile
    sample_profile = {
        'experience_years': 5.0,
        'seniority': 'Senior',
        'skills': ['Kubernetes', 'Docker', 'Terraform', 'Aws', 'Jenkins', 'Python'],
        'projects': [
            'Managed Kubernetes clusters serving 1M+ users',
            'Automated CI/CD pipelines using Jenkins',
        ],
        'responsibilities': [
            'Led infrastructure automation initiatives',
            'Implemented monitoring solutions',
        ],
        'skill_count': 6
    }
    
    prompt = builder.build_assessment_prompt(
        candidate_profile=sample_profile,
        position="DevOps",
        interview_round="L2",
        complexity_level="Intermediate"
    )
    
    print("Generated Prompt Length:", len(prompt))
    print("\n--- Prompt Preview (first 500 chars) ---")
    print(prompt[:500])

"""
Enhanced Prompt Builder Module (v2)
Builds prompts using structured profile analysis with stricter formatting
"""

from typing import Dict, List
from datetime import datetime


class PromptBuilderV2:
    """Build optimized prompts with smaller context and tech prioritization"""
    
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
        profile_analysis: Dict,
        prioritized_tech: List[Dict],
        position: str,
        interview_round: str,
        complexity_level: str
    ) -> str:
        """
        Build optimized prompt with structured analysis and tech prioritization
        
        Args:
            profile_analysis: Structured output from ProfileAnalyzer
            prioritized_tech: Prioritized technology list
            position: DevOps / SRE / Observability
            interview_round: L1 / L2
            complexity_level: Basic / Intermediate / Advanced
        
        Returns:
            Optimized prompt string with smaller context
        """
        
        # Use concise summary instead of full resume data
        concise_summary = profile_analysis['concise_summary']
        
        # Get top 3 prioritized technologies
        top_3_tech = prioritized_tech[:3] if prioritized_tech else []
        
        # Build tech focus string
        tech_focus = self._build_tech_focus_string(top_3_tech)
        
        # Determine question counts based on round and profile
        question_counts = self._get_question_counts(interview_round, profile_analysis)
        
        prompt = f"""# Interview Assessment Generation Task

You are an expert technical interviewer for {position} roles.

## Candidate Summary (Concise)

{concise_summary}

## Technology Focus (Prioritized)

{tech_focus}

## Interview Configuration

- **Position:** {position}
- **Round:** {interview_round} 
- **Complexity:** {complexity_level}
- **Recommended Focus:** {', '.join(profile_analysis['focus_recommendations'])}

---

## STRICT OUTPUT FORMAT REQUIREMENTS

Generate EXACTLY {question_counts['total']} questions following this distribution:

### 1. MCQ Section ({question_counts['mcq']} questions - 20% weight)
Focus on: {self._get_mcq_focus(profile_analysis, interview_round)}

**Format per question:**
```
### MCQ {interview_round}-[number]

**Question:** [Clear, specific technical question]

**Options:**
A) [Option]
B) [Option]  
C) [Option]
D) [Option]

**Correct Answer:** [Letter]

**Explanation:** [2-3 sentences explaining why + what it tests]

**Weight:** [X]%
```

### 2. Scenario-Based Section ({question_counts['scenario']} questions - 40% weight)
Focus on: Production situations involving {tech_focus.split(':')[0] if ':' in tech_focus else 'their key technologies'}

**IMPORTANT:** Include follow-up questions for complex scenarios to test depth of understanding.

**Format per scenario:**
```
### Scenario {interview_round}-[number]

**Situation:** [Specific production problem - 2-3 sentences max]

**Question 1:** [Initial question - what action should they take?]

**Expected Answer:**
1. [Key step/concept]
2. [Key step/concept]
3. [Commands/approach if relevant]

**Follow-up Question 2 (Optional but recommended for complex scenarios):** [What if that doesn't work? or Dig deeper into root cause]

**Expected Answer:**
- [Alternative approach]
- [Deeper analysis]

**Follow-up Question 3 (Optional):** [How would you prevent this?]

**Expected Answer:**
- [Prevention/monitoring strategy]
- [Long-term solution]

**Evaluation:**
- ✓ [Must mention this]
- ✓ [Must mention this]
- + [Bonus point]

**Weight:** [X]%
```

**Note:** Not every scenario needs 3 questions - simple scenarios can have just 1-2 questions, complex scenarios should have 2-3 follow-ups.

### 3. Coding/Scripting Section ({question_counts['coding']} questions - 20% weight)
Focus on: {self._get_coding_focus(top_3_tech)}

**Format per problem:**
```
### Coding {interview_round}-[number]

**Task:** [Specific automation problem - 1-2 sentences]

**Expected Solution:**
```{{language}}
[Clean, working code sample]
```

**Key Points:**
- [Must have feature 1]
- [Must have feature 2]

**Weight:** [X]%
```

### 4. Tech-Specific Section ({question_counts['tech_deep_dives']} Deep-Dives with Follow-ups - 10% weight)
**CRITICAL:** MUST include follow-up questions for each technology. Each deep-dive = 1 main question + 2-3 follow-ups.

**Must use these exact technologies:** {', '.join([t['skills'][0] for t in top_3_tech if t['skills']])}

**Strategy:** Instead of asking different questions about different tools, pick ONE technology and ask 2-3 follow-up questions that go progressively deeper.

**Example Format:**
```
### Tech {interview_round}-1 (Kubernetes Deep Dive)

**Technology:** Kubernetes

**Question 1:** How would you debug a service that's intermittently failing with 503 errors?

**Expected Answer:**
- Check endpoints, pod health, resource constraints
- kubectl get endpoints, describe service
- Review ingress/service mesh config

**Follow-up Question 2:** The pods are healthy but you notice high latency. What would you investigate?

**Expected Answer:**  
- Network policies, CNI issues
- Service mesh observability
- Pod placement, node affinity
- Resource contention

**Follow-up Question 3:** After fixing, how would you prevent this in future?

**Expected Answer:**
- SLOs/SLIs, proper monitoring
- Circuit breakers, retry policies
- Load testing in staging
- Capacity planning

**Weight:** [X]%
```

**Format per technology:**
```
### Tech {interview_round}-[number] ([Technology] Deep Dive)

**Technology:** [Specific tool]

**Question 1:** [Initial question]
**Expected Answer:** [Key points]

**Follow-up 2:** [Dig deeper based on Q1]
**Expected Answer:** [More advanced points]

**Follow-up 3 (Optional):** [Even deeper or prevention/optimization]
**Expected Answer:** [Expert-level insights]

**Weight:** [X]%
```

### 5. Responsibility Validation Section ({question_counts['responsibility']} questions - 10% weight)
Focus on: Verify claimed experience is genuine

**Format per question:**
```
### Responsibility {interview_round}-[number]

**Claimed Experience:** [From their background]

**Validation Question:** [Ask for specific details]

**Red Flags:**
- ❌ [Vague answer indicates]
- ❌ [Missing detail indicates]

**Good Signs:**
- ✓ [Specific detail shows]
- ✓ [Practical knowledge shows]

**Weight:** [X]%
```

---

## CRITICAL RULES

1. **EXACT COUNTS:** Generate EXACTLY the number of questions specified above
2. **WEIGHT DISTRIBUTION:** Ensure weights add up to 100%
3. **TECH ALIGNMENT:** Questions MUST use technologies from their actual resume
4. **DIFFICULTY CALIBRATION:** {self._get_difficulty_guidelines(profile_analysis, complexity_level)}
5. **PRACTICAL FOCUS:** Prefer "what would you do" over "what is the definition of"
6. **NO FLUFF:** Keep questions and answers concise and actionable
7. **DEPTH OVER BREADTH:** Ask about edge cases, failure scenarios, optimization, not basics

---

## Additional Context (Core DevOps Principles)

{self._get_core_principles_snippet()}

---

## OUTPUT STRUCTURE

```markdown
# {position} Interview Assessment - Round {interview_round}

**Candidate Level:** {profile_analysis['seniority']} ({profile_analysis['experience_years']} years)
**Complexity:** {complexity_level}
**Generated:** {datetime.now().strftime('%B %d, %Y')}

---

## Section 1: Multiple Choice Questions (20%)

[Generate {question_counts['mcq']} MCQs here following format above]

---

## Section 2: Scenario-Based Questions (40%)

[Generate {question_counts['scenario']} scenarios here following format above]

---

## Section 3: Coding/Scripting Questions (20%)

[Generate {question_counts['coding']} problems here following format above]

---

## Section 4: Technology-Specific Questions (10%)

[Generate {question_counts['tech_deep_dives']} Tech Deep-Dives here, each with 3 sub-questions following format above]

---

## Section 5: Responsibility Validation (10%)

[Generate {question_counts['responsibility']} questions here following format above]

---

## Scoring Matrix

| Section | Weight | Score |
|---------|--------|-------|
| MCQ | 20% | /20 |
| Scenarios | 40% | /40 |
| Coding | 20% | /20 |
| Tech-Specific | 10% | /10 |
| Responsibility | 10% | /10 |
| **Total** | **100%** | **/100** |

**Evaluation Guide:**
- 90-100: Strong Hire
- 75-89: Hire
- 60-74: Maybe
- <60: No Hire
```

NOW GENERATE THE COMPLETE ASSESSMENT FOLLOWING THE EXACT FORMAT ABOVE.
"""
        
        return prompt
    
    def _build_tech_focus_string(self, top_3_tech: List[Dict]) -> str:
        """Build concise tech focus string"""
        if not top_3_tech:
            return "General DevOps practices"
        
        lines = []
        for i, tech in enumerate(top_3_tech, 1):
            skills_str = ', '.join(tech['skills'][:2])  # Max 2 skills per category
            lines.append(f"{i}. **{tech['category']}** ({tech['level']}): {skills_str}")
        
        return '\n'.join(lines)
    
    def _get_question_counts(self, interview_round: str, profile_analysis: Dict = None) -> Dict:
        """Get question distribution for 1-hour interview, with follow-ups"""
        
        # Calculate tech deep-dive count based on skill diversity
        # Each deep-dive = 1 main + 2-3 follow-ups
        tech_deep_dives = 2  # default (2 deep-dives = 6-8 questions total)
        if profile_analysis:
            skill_count = profile_analysis.get('total_skills', 0)
            if skill_count >= 20:
                tech_deep_dives = 4  # 4 deep-dives = 12-16 questions
            elif skill_count >= 15:
                tech_deep_dives = 3  # 3 deep-dives = 9-12 questions
            elif skill_count >= 10:
                tech_deep_dives = 3
        
        if interview_round == "L1":
            # L1 Round for 1-hour interview (45-50 minutes actual questions)
            # Focus on practical skills, minimize MCQs
            return {
                'mcq': 2,  # Just 2 MCQs for quick fundamentals check
                'scenario': 8,  # 8 scenarios (more valuable than MCQs)
                'coding': 4,  # 4 coding problems
                'tech_deep_dives': tech_deep_dives,  # Each with 3 follow-ups
                'responsibility': 4,  # 4 responsibility validations
                'total': f"2 MCQs + 8 Scenarios + 4 Coding + {tech_deep_dives} Tech Deep-Dives (each with 3 sub-questions) + 4 Responsibility = ~35-40 questions"
            }
        else:  # L2
            # L2 Round for 1-hour interview (deep technical assessment)
            # Minimal MCQs, focus on complex scenarios and coding
            return {
                'mcq': 2,  # Just 2 advanced MCQs
                'scenario': 10,  # 10 complex scenarios (most important)
                'coding': 5,  # 5 advanced coding problems
                'tech_deep_dives': tech_deep_dives,  # Each with 3 follow-ups
                'responsibility': 4,  # 4 responsibility validations
                'total': f"2 MCQs + 10 Scenarios + 5 Coding + {tech_deep_dives} Tech Deep-Dives (each with 3 sub-questions) + 4 Responsibility = ~40-45 questions"
            }
    
    def _get_mcq_focus(self, profile_analysis: Dict, interview_round: str) -> str:
        """Determine MCQ focus based on profile"""
        if interview_round == "L1":
            return "Fundamentals, tool basics, best practices"
        else:
            return "Advanced concepts, architecture, troubleshooting patterns"
    
    def _get_coding_focus(self, top_3_tech: List[Dict]) -> str:
        """Determine coding focus"""
        # Check if scripting is in top tech
        has_scripting = any('Script' in t['category'] for t in top_3_tech)
        
        if has_scripting:
            return "Python/Bash automation for their specific tech stack"
        else:
            return "General automation, API interaction, data processing"
    
    def _get_difficulty_guidelines(self, profile_analysis: Dict, complexity_level: str) -> str:
        """Generate difficulty calibration guidelines based on experience"""
        years = profile_analysis.get('experience_years', 0) or 0
        seniority = profile_analysis.get('seniority', 'Entry')
        
        guidelines = f"""
**For {seniority} level ({years} years) with {complexity_level} complexity:**

**MCQs - MUST be challenging:**
- ❌ DON'T ASK: "What is Kubernetes?" or "What does CI/CD stand for?"
- ✅ DO ASK: Edge cases, performance implications, architecture decisions
- Example: "When would you choose StatefulSet over Deployment in K8s and why?"

**Scenarios - MUST test deep knowledge:**
- ❌ DON'T ASK: Basic troubleshooting steps everyone knows
- ✅ DO ASK: Complex production issues requiring multi-step analysis
- Example: "50% of pods failing with OOMKilled, but memory limits seem correct. Investigate."

**Coding - MUST require expertise:**
- ❌ DON'T ASK: Write a hello world script
- ✅ DO ASK: Error handling, optimization, real automation problems
- Example: "Write a script to safely drain nodes with PDBs, handling timeouts"

**Difficulty Bar:** Questions should challenge someone with {years} years experience, not test dictionary definitions."""
        
        return guidelines.strip()
    
    def _get_core_principles_snippet(self) -> str:
        """Get core DevOps principles for context"""
        return """Remember these core DevOps/SRE principles when generating questions:
- **Automation First:** Reduce manual toil
- **Observability:** Metrics, logs, traces
- **Reliability:** SLIs, SLOs, error budgets
- **Infrastructure as Code:** Version controlled, testable
- **Continuous Delivery:** Fast, safe deployments
- **Incident Management:** On-call, postmortems, learning"""


if __name__ == "__main__":
    # Test
    print("PromptBuilderV2 loaded successfully")
    print("Use with ProfileAnalyzer for best results")

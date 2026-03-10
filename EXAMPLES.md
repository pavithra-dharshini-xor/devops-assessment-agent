# Usage Examples

This document provides practical examples for using the DevOps/SRE/Observability Interview Assessment Generator.

## Prerequisites

Before running the examples, ensure you have:
1. Installed dependencies: `pip install -r requirements.txt`
2. Set your OpenAI API key: `export OPENAI_API_KEY='your-key-here'`

## Basic Usage

### Example 1: Generate L1 Assessment for DevOps Position

```bash
python app.py sample_resume.pdf --position DevOps --round L1 --complexity Intermediate
```

**Output:**
```
======================================================================
DevOps/SRE/Observability Interview Assessment Generator
======================================================================

[Step 1/4] Parsing resume...
✓ Resume parsed successfully
  - Experience: 6.0 years
  - Seniority: Senior
  - Skills found: 30
  - Top skills: Kubernetes, Docker, Terraform, Aws, Jenkins

[Step 2/4] Building assessment prompt...
✓ Prompt built successfully (5234 characters)

[Step 3/4] Generating assessment with AI...
  - Position: DevOps
  - Round: L1
  - Complexity: Intermediate
  - Model: gpt-4o
  - This may take 30-60 seconds...
✓ Assessment generated successfully (12456 characters)

[Step 4/4] Saving assessment...
✓ Assessment saved to: assessment_DevOps_L1_20260309_213045.md

======================================================================
Assessment generation complete!
======================================================================
```

### Example 2: Generate L2 Assessment for SRE Position

```bash
python app.py sample_resume.pdf \
  --position SRE \
  --round L2 \
  --complexity Advanced \
  --output senior_sre_assessment.md
```

This generates an advanced L2 round assessment tailored for a Senior SRE position.

### Example 3: Generate Observability Engineer Assessment

```bash
python app.py sample_resume.pdf \
  --position Observability \
  --round L1 \
  --complexity Intermediate
```

### Example 4: Quick Analysis Only

Get a quick overview of the candidate without generating full assessment:

```bash
python app.py sample_resume.pdf --analyze
```

**Output:**
```
[Quick Analysis] Analyzing candidate profile...

--- Candidate Profile Summary ---
Experience: 6.0 years
Seniority: Senior
Skills: Kubernetes, Docker, Terraform, Aws, Jenkins, Python, Bash, Prometheus, Grafana, Argocd
Total skills found: 30

--- Recommendations ---
Suggested Round: L2
Suggested Complexity: Advanced
Focus Areas: Container Orchestration, Infrastructure as Code, CI/CD, Observability, Cloud Platforms
```

## Advanced Usage

### Example 5: Using Different AI Models

For faster/cheaper results, use GPT-4o-mini:

```bash
python app.py sample_resume.pdf \
  --model gpt-4o-mini \
  --position DevOps \
  --round L1
```

For highest quality, use GPT-4o (default):

```bash
python app.py sample_resume.pdf \
  --model gpt-4o \
  --position SRE \
  --round L2 \
  --complexity Advanced
```

### Example 6: Entry-Level DevOps Position

```bash
python app.py junior_candidate_resume.pdf \
  --position DevOps \
  --round L1 \
  --complexity Basic \
  --output junior_devops_assessment.md
```

### Example 7: Principal/Staff SRE Position

```bash
python app.py principal_resume.pdf \
  --position SRE \
  --round L2 \
  --complexity Advanced \
  --output principal_sre_assessment.md
```

## Python API Usage

You can also use the agent programmatically in your Python scripts:

### Example 8: Programmatic Usage

```python
from app import AssessmentGenerator
import os

# Set API key
os.environ['OPENAI_API_KEY'] = 'your-api-key-here'

# Initialize generator
generator = AssessmentGenerator()

# Generate assessment
assessment = generator.generate_assessment(
    resume_path='sample_resume.pdf',
    position='DevOps',
    interview_round='L2',
    complexity_level='Intermediate',
    output_path='my_assessment.md'
)

print("Assessment generated successfully!")
```

### Example 9: Quick Analysis in Python

```python
from app import AssessmentGenerator

generator = AssessmentGenerator()

# Quick analysis
analysis = generator.quick_analysis('sample_resume.pdf')

print(f"Experience: {analysis['profile']['experience_years']} years")
print(f"Seniority: {analysis['profile']['seniority']}")
print(f"Skills: {', '.join(analysis['profile']['skills'][:10])}")
print(f"Recommended Round: {analysis['recommendations']['round']}")
print(f"Recommended Complexity: {analysis['recommendations']['complexity']}")
```

### Example 10: Batch Processing Multiple Resumes

```python
from app import AssessmentGenerator
import os
from pathlib import Path

generator = AssessmentGenerator()

# Process all resumes in a directory
resume_dir = Path('resumes')
output_dir = Path('assessments')
output_dir.mkdir(exist_ok=True)

for resume_file in resume_dir.glob('*.pdf'):
    print(f"\nProcessing: {resume_file.name}")
    
    output_path = output_dir / f"{resume_file.stem}_assessment.md"
    
    try:
        generator.generate_assessment(
            resume_path=str(resume_file),
            position='DevOps',
            interview_round='L1',
            complexity_level='Intermediate',
            output_path=str(output_path)
        )
        print(f"✓ Generated: {output_path}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
```

## Testing with Sample Resume

### Step 1: Create Sample Resume

```bash
python create_sample_resume.py
```

This creates `sample_resume.pdf` with realistic DevOps engineer experience.

### Step 2: Test Resume Parser

```bash
python resume_parser.py
```

### Step 3: Generate Test Assessment

```bash
python app.py sample_resume.pdf --position DevOps --round L2
```

## Common Scenarios

### Scenario 1: Junior DevOps Engineer (0-2 years)

```bash
python app.py junior_resume.pdf \
  --position DevOps \
  --round L1 \
  --complexity Basic
```

**Expected Assessment:**
- Focus on fundamentals
- Basic troubleshooting questions
- Simple scripting tasks
- Tool familiarity verification

### Scenario 2: Mid-Level DevOps Engineer (3-5 years)

```bash
python app.py mid_level_resume.pdf \
  --position DevOps \
  --round L1 \
  --complexity Intermediate
```

**Expected Assessment:**
- Moderate complexity scenarios
- Infrastructure automation questions
- CI/CD pipeline design
- Cloud platform knowledge

### Scenario 3: Senior SRE (6-8 years)

```bash
python app.py senior_resume.pdf \
  --position SRE \
  --round L2 \
  --complexity Advanced
```

**Expected Assessment:**
- Complex production scenarios
- System design questions
- Incident management
- Architecture decisions
- Leadership responsibilities

### Scenario 4: Staff/Principal SRE (8+ years)

```bash
python app.py staff_resume.pdf \
  --position SRE \
  --round L2 \
  --complexity Advanced
```

**Expected Assessment:**
- Strategic architecture questions
- Scalability challenges
- Team leadership scenarios
- Cross-functional collaboration
- Technical strategy

## Tips for Best Results

1. **Resume Quality**: Ensure resumes are well-structured PDFs with extractable text
2. **Appropriate Complexity**: Match complexity to candidate's experience level
3. **Round Selection**: Use L1 for screening, L2 for in-depth evaluation
4. **Review Output**: Always review and customize generated questions
5. **Multiple Runs**: Generate multiple assessments and pick the best questions

## Environment Variables

```bash
# Required
export OPENAI_API_KEY='sk-...'

# Optional (for .env file support)
# Create a .env file in the project root:
echo "OPENAI_API_KEY=sk-..." > .env
```

## Troubleshooting

### Issue: API Key Error

```bash
# Solution:
export OPENAI_API_KEY='your-actual-key'
python app.py sample_resume.pdf
```

### Issue: PDF Parsing Fails

```bash
# Check if PDF is readable:
python -c "from resume_parser import ResumeParser; p = ResumeParser(); print(p.parse_resume('your_resume.pdf'))"
```

### Issue: Low Quality Questions

```bash
# Use better model:
python app.py resume.pdf --model gpt-4o --complexity Advanced
```

## Next Steps

After generating an assessment:

1. **Review the Questions**: Ensure they align with your needs
2. **Customize as Needed**: Add or modify questions
3. **Print for Interview**: Use as reference during the interview
4. **Take Notes**: Use the "Interviewer Notes" section
5. **Score the Candidate**: Fill in the scoring matrix

## Support

For issues or questions, please refer to:
- README.md for general documentation
- agent.md for detailed agent instructions
- GitHub issues for bug reports and feature requests

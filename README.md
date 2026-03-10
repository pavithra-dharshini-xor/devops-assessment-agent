# DevOps/SRE/Observability Interview Assessment Generator

AI agent that generates comprehensive, challenging interview assessment sheets for DevOps, SRE, and Observability roles from candidate resumes using an advanced 2-step agentic workflow.

## 🎯 Overview

This agent automatically generates **depth-focused interview assessment sheets** optimized for 1-hour technical interviews. It helps interview panelists evaluate candidates based on their technical skills, experience, project exposure, and real-world responsibilities.

The generated assessment acts as a **reference handbook for interview panelists**, containing:
- Multiple choice questions (MCQ) - Minimal, only challenging concepts
- Scenario-based questions with follow-ups (production situations)
- Coding/scripting questions (real automation problems)
- Technology deep-dives with progressive follow-ups
- Responsibility validation questions
- Expected answers and evaluation criteria
- Scoring weightage

## ✨ Key Features (V2)

### 🏗️ **2-Step Architecture**
```
Resume → ProfileAnalyzer → PromptBuilderV2 → LLM → Assessment
         (Structured      (Optimized prompts
          Analysis)        with follow-ups)
```

### 🎯 **Optimized for Quality**
- **Depth Over Breadth**: Follow-up questions test true understanding
- **60% Smaller Context**: Efficient prompts for better AI responses
- **Dynamic Scaling**: Tech questions adapt to candidate's skill breadth
- **Difficulty Calibrated**: Questions match experience level
- **Consistent Results**: Sorted skills, no randomization

### 🚀 **1-Hour Interview Format**
- **40-45 total questions** for comprehensive 60-minute assessment
- **Minimal MCQs** (just 2) - Focus on practical skills
- **Follow-up questions** for tech and scenarios - Progressive depth testing
- **Real production scenarios** - Not textbook definitions

## 🏗️ Architecture

```
devops-assessment-agent/
│
├── agent.md                    # Agent instructions and requirements
├── app.py                      # Main agent workflow (5-step process)
├── resume_parser.py            # Resume text extraction and parsing
├── profile_analyzer.py         # Structured profile analysis
├── prompt_builder_v2.py        # Enhanced prompt builder with follow-ups
├── requirements.txt            # Python dependencies
├── create_sample_resume.py     # Generate sample resume for testing
└── README.md                   # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup

1. **Clone the repository**:
```bash
git clone https://github.com/pavithra-dharshini-xor/devops-assessment-agent.git
cd devops-assessment-agent
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up OpenAI API key**:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

## 📖 Usage

### Basic Usage

Generate an assessment from a resume:

```bash
python app.py path/to/resume.pdf
```

### Advanced Options

```bash
python app.py path/to/resume.pdf \
  --position DevOps \
  --round L2 \
  --complexity Intermediate \
  --output assessment.md
```

### Command Line Arguments

| Argument | Options | Default | Description |
|----------|---------|---------|-------------|
| `resume_path` | Path to PDF | Required | Candidate's resume file |
| `--position` | DevOps, SRE, Observability | DevOps | Technical position |
| `--round` | L1, L2 | L1 | Interview round |
| `--complexity` | Basic, Intermediate, Advanced | Intermediate | Question difficulty |
| `--output` | File path | Auto-generated | Output file path |
| `--analyze` | Flag | False | Quick analysis only |
| `--model` | OpenAI model | gpt-4o | Model to use |

### Quick Analysis

Analyze a candidate profile without generating full assessment:

```bash
python app.py path/to/resume.pdf --analyze
```

### Examples

**L1 Round for Entry-Level DevOps**:
```bash
python app.py resume.pdf --position DevOps --round L1 --complexity Basic
```

**L2 Round for Mid-Level DevOps (4+ years)**:
```bash
python app.py resume.pdf --position SRE --round L2 --complexity Intermediate
```

**Advanced Observability Engineer**:
```bash
python app.py resume.pdf --position Observability --round L2 --complexity Advanced
```

## 🧪 Testing

### Create Sample Resume

Generate a sample DevOps resume for testing:

```bash
python create_sample_resume.py
```

This creates `sample_resume.pdf` with realistic DevOps experience.

### Test the Agent

```bash
python app.py sample_resume.pdf --position DevOps --round L2 --complexity Intermediate
```

## 📊 Assessment Structure (V2)

Generated assessments are optimized for **1-hour interviews** with progressive questioning:

### Section 1: Multiple Choice Questions (20% weight)
- **Just 2 MCQs** - Quick challenging fundamentals only
- No basic "what is X" questions
- Focus on edge cases and architecture decisions

### Section 2: Scenario-Based Questions (40% weight)
- **8-10 complex production scenarios**
- **Follow-up questions included** for depth testing
- Real production issues requiring multi-step analysis
- Format: Initial problem → Deeper investigation → Prevention/optimization

### Section 3: Coding/Scripting Questions (20% weight)
- **4-5 automation problems**
- Error handling, optimization required
- Based on candidate's actual tech stack
- Sample solutions with evaluation criteria

### Section 4: Technology Deep-Dives (10% weight)
- **2-4 deep-dives** (scales with skill count)
- **Each deep-dive = 3 progressive follow-up questions**
- Tests depth, not breadth
- Example: K8s debugging → Performance → Prevention

### Section 5: Responsibility Validation (10% weight)
- **3-4 validation questions**
- Verify claimed experience is genuine
- Red flags and good signs listed

## 🎓 Question Distribution

### L1 Round (Initial Technical Screening - 1 Hour)
- **2 MCQs** - Quick fundamentals check
- **8 Scenarios** (with optional follow-ups) - Real-world problem solving
- **4 Coding** - Automation capability
- **2-4 Tech Deep-Dives** (each with 3 sub-questions) - Based on skill count
- **4 Responsibility** - Verify experience
- **Total: ~35-40 questions**

### L2 Round (Advanced Technical - 1 Hour)
- **2 MCQs** - Advanced challenging concepts only
- **10 Scenarios** (with follow-ups) - Complex production situations
- **5 Coding** - Advanced automation with error handling
- **2-4 Tech Deep-Dives** (each with 3 sub-questions) - Progressive depth
- **4 Responsibility** - Leadership & ownership validation
- **Total: ~40-45 questions**

### Dynamic Tech Deep-Dives

Tech questions **automatically scale** based on candidate's skill breadth:
- **27+ skills** → 4 deep-dives (12-16 tech questions)
- **15-19 skills** → 3 deep-dives (9-12 tech questions)
- **10-14 skills** → 3 deep-dives (9-12 tech questions)
- **<10 skills** → 2 deep-dives (6-8 tech questions)

## 🔍 How It Works (V2 Workflow)

1. **Resume Parsing**: Extracts text from PDF, identifies skills, experience, projects
2. **Profile Analysis** ⭐ NEW: 
   - Categorizes technologies into 10 groups
   - Identifies top 3 primary expertise areas
   - Determines skill diversity score
   - Creates concise summary (60% smaller context)
3. **Prompt Building**: Constructs optimized prompt with:
   - Smaller context for efficiency
   - Tech prioritization
   - Strict formatting rules
   - Difficulty calibration
   - Follow-up question mandates
4. **AI Generation**: Uses OpenAI GPT model with structured prompts
5. **Output Formatting**: Saves markdown assessment with actual date

## 💡 What Makes V2 Better

### Before (V1)
❌ Generic questions not aligned with candidate  
❌ Large unstructured prompts  
❌ No follow-up questions  
❌ Too many shallow MCQs  
❌ No tech prioritization  

### After (V2)
✅ **Personalized** to candidate's top 3 tech areas  
✅ **60% smaller context** = better AI responses  
✅ **Follow-up questions** test depth  
✅ **Just 2 MCQs** focus on practical skills  
✅ **Dynamic scaling** based on skill count  
✅ **Difficulty calibrated** for experience level  

## 🔧 Configuration

### Customizing Agent Behavior

Edit `agent.md` to modify:
- Question types and distribution
- Evaluation criteria
- Scoring guidelines
- Output format requirements

### Using Different AI Models

```bash
# Use GPT-4o (default - most capable)
python app.py resume.pdf --model gpt-4o

# Use GPT-4o-mini (faster, cheaper)
python app.py resume.pdf --model gpt-4o-mini

# Use GPT-4 Turbo
python app.py resume.pdf --model gpt-4-turbo-preview
```

## 📝 Output Format

The generated assessment includes:

1. **Candidate Overview**: Experience level, seniority, skill diversity score
2. **Interview Configuration**: Position, round, complexity level
3. **Primary Focus Areas**: Top 3 tech categories from profile analysis
4. **Question Sections**: All 5 categories with progressive questions
5. **Follow-up Questions**: For tech and complex scenarios
6. **Expected Answers**: Detailed with evaluation criteria
7. **Scoring Matrix**: Evaluation weightage by section
8. **Guidelines**: Scoring thresholds and recommendations

## 🎯 Best Practices

1. **Resume Quality**: Better structured resumes yield more accurate assessments
2. **Experience Alignment**: Match complexity level with candidate's years of experience
3. **Round Selection**: Use L1 for initial screening, L2 for deep technical evaluation
4. **Review Generated Content**: Always review questions - they're challenging by design
5. **Use Follow-ups**: The follow-up questions are key to testing real expertise
6. **Skill Count Matters**: More skills = more tech deep-dives automatically

## 📈 Profile Analysis Features

The ProfileAnalyzer categorizes skills into:

1. **Container Orchestration** (Kubernetes, Docker, etc.)
2. **Infrastructure as Code** (Terraform, Ansible, etc.)
3. **CI/CD** (Jenkins, GitLab, ArgoCD, etc.)
4. **Cloud Platforms** (AWS, Azure, GCP)
5. **Monitoring/Observability** (Prometheus, Grafana, ELK)
6. **Scripting** (Python, Bash, Shell)
7. **Networking** (Nginx, Load Balancers, API Gateway)
8. **Databases** (MySQL, PostgreSQL, Redis)
9. **Version Control** (Git, GitHub, GitLab)
10. **Security** (Vault, Secrets, SSL/TLS)

## 🛠️ Development

### Code Structure

- `ResumeParser`: Handles PDF parsing and information extraction
- `ProfileAnalyzer` ⭐ NEW: Structured profile analysis with tech categorization
- `PromptBuilderV2` ⭐ NEW: Optimized prompts with follow-ups and strict formatting
- `AssessmentGenerator`: Main workflow orchestration (5-step process)

## 🐛 Troubleshooting

**Issue**: OpenAI API key error
```bash
export OPENAI_API_KEY='your-key'
```

**Issue**: PDF parsing fails
- Ensure resume is a valid PDF with extractable text
- Scanned images may not work without OCR

**Issue**: Questions still too easy
- The system is calibrated for experience level
- Try using `--complexity Advanced`
- Ensure resume clearly states years of experience

**Issue**: Not enough tech questions
- Tech deep-dives scale with skill count
- Add more skills to resume for more coverage
- Each deep-dive includes 3 follow-up questions

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests or open issues.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This tool uses AI to generate challenging assessments optimized for 1-hour interviews. Questions are designed to test depth of knowledge through follow-ups. Always review and customize the output before using in actual interviews.

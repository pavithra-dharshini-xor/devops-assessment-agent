# DevOps/SRE/Observability Interview Assessment Generator

AI agent that generates comprehensive interview assessment sheets for DevOps, SRE, and Observability roles from candidate resumes using an agentic workflow.

## 🎯 Overview

This agent automatically generates structured interview assessment sheets that help interview panelists evaluate candidates based on their technical skills, experience, project exposure, and real-world responsibilities.

The generated assessment acts as a **reference handbook for interview panelists**, containing:
- Multiple choice questions (MCQ)
- Scenario-based questions (production situations)
- Coding/scripting questions
- Technology/skill-based questions
- Responsibility validation questions
- Expected answers and evaluation criteria
- Scoring weightage

## 📋 Features

- **Automated Resume Parsing**: Extracts skills, experience, projects, and responsibilities from PDF resumes
- **Personalized Questions**: Generates questions tailored to the candidate's specific skills and experience level
- **Multiple Interview Rounds**: Supports L1 (screening) and L2 (advanced) rounds
- **Complexity Levels**: Adjustable difficulty (Basic, Intermediate, Advanced)
- **Role-Specific**: Customized for DevOps, SRE, or Observability positions
- **Real-World Focus**: Prioritizes practical scenarios over theoretical questions
- **Comprehensive Scoring**: Includes evaluation criteria and weightage for each section

## 🏗️ Architecture

```
devops-assessment-agent/
│
├── agent.md                    # Agent instructions and requirements
├── app.py                      # Main agent workflow
├── resume_parser.py            # Resume text extraction and parsing
├── prompt_builder.py           # Prompt construction from agent instructions
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
  --round L1 \
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

**L2 Round for Senior SRE**:
```bash
python app.py resume.pdf --position SRE --round L2 --complexity Advanced
```

**Observability Engineer Assessment**:
```bash
python app.py resume.pdf --position Observability --round L1 --complexity Intermediate
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

## 📊 Assessment Structure

Generated assessments follow this structure:

### Section 1: Multiple Choice Questions (20%)
- Tests foundational technical knowledge
- 3-5 questions with answers and explanations

### Section 2: Scenario-Based Questions (40%)
- Real production situations
- 4-6 questions with expected solutions and evaluation criteria

### Section 3: Coding/Scripting Questions (20%)
- Automation and scripting capability
- 2-3 problems with sample solutions

### Section 4: Technology/Skill Based Questions (10%)
- Deep-dive into specific technologies from resume
- 2-3 questions aligned with candidate's skills

### Section 5: Responsibility-Based Questions (10%)
- Validates actual experience claimed in resume
- 2-3 questions with red flags to watch for

## 🎓 Question Distribution

### L1 Round (Initial Technical Screening)
- 5 MCQs - Test fundamentals
- 4 Scenario-based - Real-world problem solving
- 2 Coding/Scripting - Automation capability
- 3 Technology/Skills - Tool expertise
- 2 Responsibility-based - Verify experience
- **Total: 16 questions**

### L2 Round (Advanced Technical)
- 3 MCQs - Advanced concepts
- 6 Scenario-based - Complex production scenarios
- 3 Coding/Scripting - Advanced automation
- 3 Technology/Skills - Deep technical knowledge
- 3 Responsibility-based - Leadership & ownership
- **Total: 18 questions**

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

1. **Candidate Overview**: Experience level, seniority, detected skills
2. **Interview Configuration**: Position, round, complexity level
3. **Question Sections**: All 5 categories with questions and answers
4. **Scoring Matrix**: Evaluation weightage by section
5. **Guidelines**: Scoring thresholds and recommendations
6. **Interviewer Notes**: Space for observations

## 🔍 How It Works

1. **Resume Parsing**: Extracts text from PDF, identifies skills, experience, projects, and responsibilities
2. **Profile Analysis**: Determines seniority level and technical focus areas
3. **Prompt Building**: Constructs comprehensive prompt using agent instructions and candidate profile
4. **AI Generation**: Uses OpenAI's GPT model to generate personalized questions and answers
5. **Output Formatting**: Saves structured markdown assessment for panelists

## 💡 Best Practices

1. **Resume Quality**: Better structured resumes yield more accurate assessments
2. **Experience Alignment**: Match complexity level with candidate's years of experience
3. **Round Selection**: Use L1 for initial screening, L2 for deep technical evaluation
4. **Review Generated Content**: Always review and customize questions before interviews
5. **Use as Guide**: Generated assessments are starting points - adapt to your needs

## 🛠️ Development

### Running Tests

```bash
pytest
```

### Code Structure

- `ResumeParser`: Handles PDF parsing and information extraction
- `PromptBuilder`: Constructs prompts from agent instructions
- `AssessmentGenerator`: Main workflow orchestration and AI interaction

## 🐛 Troubleshooting

**Issue**: OpenAI API key error
```bash
export OPENAI_API_KEY='your-key'
```

**Issue**: PDF parsing fails
- Ensure resume is a valid PDF with extractable text
- Scanned images may not work without OCR

**Issue**: Low-quality questions
- Try using `--model gpt-4o` instead of mini versions
- Ensure resume has clear skills and experience sections
- Adjust complexity level appropriately

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests or open issues.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This tool uses AI to generate assessments. Always review and customize the output before using in actual interviews.

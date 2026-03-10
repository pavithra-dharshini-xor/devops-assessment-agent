# Quick Start Guide

## Where Are Assessment Files Generated?

When you run:
```bash
python app.py 1534144_BasavrajMangale.pdf --position DevOps --round L2 --complexity Intermediate
```

The assessment file is generated in the **current directory** with an auto-generated filename:
```
assessment_DevOps_L2_YYYYMMDD_HHMMSS.md
```

Example: `assessment_DevOps_L2_20260309_221505.md`

## Custom Output Location

To specify a custom output path:
```bash
python app.py resume.pdf --position DevOps --round L2 --output my_assessment.md
```

## Most Common Issue: Missing OpenAI API Key

If no file was generated, the most likely reason is a **missing OpenAI API key**.

### Solution: Set Your API Key

**Option 1: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY='sk-your-actual-api-key-here'
```

Then run the command again:
```bash
python app.py 1534144_BasavrajMangale.pdf --position DevOps --round L2 --complexity Intermediate
```

**Option 2: Create .env File**
```bash
echo "OPENAI_API_KEY=sk-your-actual-api-key-here" > .env
```

Then run your command.

**Option 3: Set in Shell Profile (Permanent)**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export OPENAI_API_KEY="sk-your-actual-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## Check for Errors

If the command ran but you're not sure what happened:

```bash
# Run with full output visible
python app.py 1534144_BasavrajMangale.pdf --position DevOps --round L2 --complexity Intermediate
```

You should see output like:
```
======================================================================
DevOps/SRE/Observability Interview Assessment Generator
======================================================================

[Step 1/4] Parsing resume...
✓ Resume parsed successfully
  - Experience: X years
  - Seniority: Level
  - Skills found: N

[Step 2/4] Building assessment prompt...
✓ Prompt built successfully

[Step 3/4] Generating assessment with AI...
  - This may take 30-60 seconds...
✓ Assessment generated successfully

[Step 4/4] Saving assessment...
✓ Assessment saved to: assessment_DevOps_L2_20260309_221505.md

======================================================================
Assessment generation complete!
======================================================================
```

## List Generated Assessments

To see all assessment files:
```bash
ls -lh assessment_*.md
```

## Full Working Example

```bash
# 1. Set API key
export OPENAI_API_KEY='sk-your-key'

# 2. Run assessment generation
python app.py 1534144_BasavrajMangale.pdf \
  --position DevOps \
  --round L2 \
  --complexity Intermediate

# 3. Check the generated file
ls -lh assessment_*.md

# 4. View the assessment
cat assessment_DevOps_L2_*.md
```

## Get OpenAI API Key

If you don't have an OpenAI API key:

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy it and set it as shown above

**Note:** You need to have credits in your OpenAI account to use the API.

## Quick Test

Test the system without generating a full assessment:

```bash
# Quick analysis only (doesn't use API)
python app.py 1534144_BasavrajMangale.pdf --analyze
```

This will show candidate profile without generating questions (no API key needed).

## Troubleshooting

### Error: "OpenAI API key not found"
**Solution:** Set the OPENAI_API_KEY environment variable as shown above.

### Error: "Resume file not found"
**Solution:** Make sure the PDF file exists:
```bash
ls -l 1534144_BasavrajMangale.pdf
```

### No Output at All
**Solution:** Check if Python dependencies are installed:
```bash
pip install -r requirements.txt
```

### Assessment Takes Too Long
**Solution:** Use a faster model:
```bash
python app.py resume.pdf --model gpt-4o-mini --position DevOps --round L1
```

## Need Help?

Check the documentation:
- **README.md** - Full documentation
- **EXAMPLES.md** - Usage examples
- **agent.md** - Agent instructions

## Contact

For issues, open a GitHub issue in the repository.

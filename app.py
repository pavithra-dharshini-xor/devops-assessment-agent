"""
DevOps/SRE/Observability Interview Assessment Generator
Main application workflow
"""

import os
import sys
from datetime import datetime
from typing import Optional
import json
import openai
from resume_parser import ResumeParser
from profile_analyzer import ProfileAnalyzer
from prompt_builder_v2 import PromptBuilderV2
from openai import OpenAI
import httpx

# Check if required packages are available
try:
    OPENAI_VERSION = openai.__version__
    print(f"OpenAI version: {OPENAI_VERSION}")
except ImportError:
    print("Error: openai package not installed. Run: pip install -r requirements.txt")
    sys.exit(1)


class AssessmentGenerator:
    """Main agent workflow for generating interview assessments"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the assessment generator
        
        Args:
            api_key: OpenAI API key (if not provided, will use OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass api_key parameter.")

        # Determine API version
        version_major = int(OPENAI_VERSION.split('.')[0])

        if version_major >= 1:
            # New API (v1.0+)

            # Create a custom HTTP client without proxies to avoid compatibility issues
            http_client = httpx.Client(
                timeout=60.0,
                limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
            )

            try:
                self.client = OpenAI(api_key=self.api_key, http_client=http_client)
                self.use_new_api = True
                print("Using OpenAI API v1.0+")
            except TypeError:
                # If http_client parameter doesn't work, try without it
                print("Note: Using simplified client initialization")
                os.environ['OPENAI_API_KEY'] = self.api_key
                self.client = OpenAI()
                self.use_new_api = True
                print("Using OpenAI API v1.0+")
        else:
            # Legacy API (v0.x)
            openai.api_key = self.api_key
            self.client = None
            self.use_new_api = False
            print("Using OpenAI legacy API (v0.x)")

        self.parser = ResumeParser()
        self.analyzer = ProfileAnalyzer()
        self.prompt_builder = PromptBuilderV2()
        self.model = "gpt-4o"  # or "gpt-4o-mini" for faster/cheaper results

    def generate_assessment(
        self,
        resume_path: str,
        position: str = "DevOps",
        interview_round: str = "L1",
        complexity_level: str = "Intermediate",
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate complete interview assessment from resume
        
        Args:
            resume_path: Path to candidate's resume (PDF)
            position: DevOps / SRE / Observability
            interview_round: L1 / L2
            complexity_level: Basic / Intermediate / Advanced
            output_path: Optional path to save the assessment
        
        Returns:
            Generated assessment content
        """
        print("=" * 70)
        print("DevOps/SRE/Observability Interview Assessment Generator")
        print("=" * 70)

        # Step 1: Parse Resume
        print("\n[Step 1/5] Parsing resume...")
        try:
            candidate_profile = self.parser.parse_resume(resume_path)
            print(f"✓ Resume parsed successfully")
            print(f"  - Experience: {candidate_profile.get('experience_years', 'N/A')} years")
            print(f"  - Seniority: {candidate_profile.get('seniority', 'N/A')}")
            print(f"  - Skills found: {candidate_profile.get('skill_count', 0)}")
            print(f"  - Top skills: {', '.join(candidate_profile.get('skills', [])[:5])}")
        except Exception as e:
            print(f"✗ Error parsing resume: {str(e)}")
            return None

        # Step 2: Analyze Profile (NEW - structured analysis)
        print("\n[Step 2/5] Analyzing candidate profile...")
        try:
            profile_analysis = self.analyzer.analyze(candidate_profile)
            prioritized_tech = self.analyzer.get_prioritized_tech_list(profile_analysis)
            
            print(f"✓ Profile analyzed successfully")
            print(f"  - Primary Focus: {', '.join([c.replace('_', ' ').title() for c, _ in profile_analysis['primary_focus']][:2])}")
            print(f"  - Skill Diversity: {profile_analysis['skill_diversity_score']}/10")
            print(f"  - Top Tech: {prioritized_tech[0]['category'] if prioritized_tech else 'N/A'}")
        except Exception as e:
            print(f"✗ Error analyzing profile: {str(e)}")
            return None

        # Step 3: Build Optimized Prompt (with smaller context)
        print("\n[Step 3/5] Building optimized assessment prompt...")
        try:
            prompt = self.prompt_builder.build_assessment_prompt(
                profile_analysis=profile_analysis,
                prioritized_tech=prioritized_tech,
                position=position,
                interview_round=interview_round,
                complexity_level=complexity_level
            )
            print(f"✓ Prompt built successfully ({len(prompt)} characters)")
            print(f"  - Context size reduced by using structured analysis")
        except Exception as e:
            print(f"✗ Error building prompt: {str(e)}")
            return None

        # Step 4: Generate Assessment using LLM
        print("\n[Step 4/5] Generating assessment with AI...")
        print(f"  - Position: {position}")
        print(f"  - Round: {interview_round}")
        print(f"  - Complexity: {complexity_level}")
        print(f"  - Model: {self.model}")
        print("  - This may take 30-60 seconds...")

        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert technical interviewer specializing in DevOps, SRE, and Observability roles. Generate comprehensive, practical interview assessments based on candidate profiles."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            if self.use_new_api:
                # New API (v1.0+)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=4000
                )
                assessment = response.choices[0].message.content
            else:
                # Legacy API (v0.x)
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=4000
                )
                assessment = response.choices[0].message['content']

            print(f"✓ Assessment generated successfully ({len(assessment)} characters)")

        except Exception as e:
            print(f"✗ Error generating assessment: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

        # Step 5: Save Assessment
        print("\n[Step 5/5] Saving assessment...")
        if output_path is None:
            # Generate default filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"assessment_{position}_{interview_round}_{timestamp}.md"

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(assessment)
            print(f"Assessment saved to: {output_path}")
        except Exception as e:
            print(f"Error saving assessment: {str(e)}")
            return assessment  # Still return the content even if saving fails

        print("\n" + "=" * 70)
        print("Assessment generation complete!")
        print("=" * 70)

        return assessment

    def quick_analysis(self, resume_path: str) -> dict:
        """
        Quick analysis of candidate profile
        
        Args:
            resume_path: Path to candidate's resume
        
        Returns:
            Analysis results
        """
        print("\n[Quick Analysis] Analyzing candidate profile...")

        candidate_profile = self.parser.parse_resume(resume_path)

        print("\n--- Candidate Profile Summary ---")
        print(f"Experience: {candidate_profile.get('experience_years', 'Not specified')} years")
        print(f"Seniority: {candidate_profile.get('seniority', 'Not specified')}")
        print(f"Skills: {', '.join(candidate_profile.get('skills', [])[:10])}")
        print(f"Total skills found: {candidate_profile.get('skill_count', 0)}")

        # Generate recommendations
        recommendations = self._generate_recommendations(candidate_profile)

        print("\n--- Recommendations ---")
        print(f"Suggested Round: {recommendations['round']}")
        print(f"Suggested Complexity: {recommendations['complexity']}")
        print(f"Focus Areas: {', '.join(recommendations['focus_areas'])}")

        return {
            'profile': candidate_profile,
            'recommendations': recommendations
        }

    def _generate_recommendations(self, profile: dict) -> dict:
        """Generate interview recommendations based on profile"""
        years = profile.get('experience_years', 0) or 0
        skill_count = profile.get('skill_count', 0)

        # Determine round
        if years < 3:
            round_rec = "L1"
        else:
            round_rec = "L2"

        # Determine complexity
        if years < 2 or skill_count < 5:
            complexity = "Basic"
        elif years < 5 or skill_count < 10:
            complexity = "Intermediate"
        else:
            complexity = "Advanced"

        # Focus areas based on skills
        skills = profile.get('skills', [])
        focus_areas = []

        if any(s in str(skills).lower() for s in ['kubernetes', 'docker']):
            focus_areas.append("Container Orchestration")
        if any(s in str(skills).lower() for s in ['terraform', 'ansible']):
            focus_areas.append("Infrastructure as Code")
        if any(s in str(skills).lower() for s in ['jenkins', 'gitlab', 'github']):
            focus_areas.append("CI/CD")
        if any(s in str(skills).lower() for s in ['prometheus', 'grafana', 'elk']):
            focus_areas.append("Observability")
        if any(s in str(skills).lower() for s in ['aws', 'azure', 'gcp']):
            focus_areas.append("Cloud Platforms")

        if not focus_areas:
            focus_areas = ["General DevOps", "Problem Solving"]

        return {
            'round': round_rec,
            'complexity': complexity,
            'focus_areas': focus_areas
        }


def main():
    """Main entry point with CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate DevOps/SRE/Observability interview assessments from resumes"
    )

    parser.add_argument(
        'resume_path',
        help="Path to candidate's resume (PDF)"
    )

    parser.add_argument(
        '--position',
        choices=['DevOps', 'SRE', 'Observability'],
        default='DevOps',
        help="Technical position (default: DevOps)"
    )

    parser.add_argument(
        '--round',
        choices=['L1', 'L2'],
        default='L1',
        help="Interview round (default: L1)"
    )

    parser.add_argument(
        '--complexity',
        choices=['Basic', 'Intermediate', 'Advanced'],
        default='Intermediate',
        help="Complexity level (default: Intermediate)"
    )

    parser.add_argument(
        '--output',
        '-o',
        help="Output file path (default: auto-generated)"
    )

    parser.add_argument(
        '--analyze',
        action='store_true',
        help="Quick analysis only (no assessment generation)"
    )

    parser.add_argument(
        '--model',
        default='gpt-4o',
        help="OpenAI model to use (default: gpt-4o)"
    )

    args = parser.parse_args()

    # Validate resume file
    if not os.path.exists(args.resume_path):
        print(f"Error: Resume file not found: {args.resume_path}")
        sys.exit(1)

    try:
        generator = AssessmentGenerator()
        generator.model = args.model

        if args.analyze:
            # Quick analysis only
            generator.quick_analysis(args.resume_path)
        else:
            # Full assessment generation
            generator.generate_assessment(
                resume_path=args.resume_path,
                position=args.position,
                interview_round=args.round,
                complexity_level=args.complexity,
                output_path=args.output
            )

    except ValueError as e:
        print(f"Error: {str(e)}")
        print("\nTo use this tool, you need to set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

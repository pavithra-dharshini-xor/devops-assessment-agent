"""
Profile Analyzer Module
Analyzes parsed resume data and extracts structured information for assessment generation
"""

from typing import Dict, List, Tuple
from collections import Counter


class ProfileAnalyzer:
    """Analyzes candidate profile and prepares structured data for question generation"""
    
    def __init__(self):
        self.tech_categories = {
            'container_orchestration': ['kubernetes', 'docker', 'containerd', 'podman', 'helm', 'rancher'],
            'infrastructure_as_code': ['terraform', 'ansible', 'cloudformation', 'pulumi', 'chef', 'puppet'],
            'ci_cd': ['jenkins', 'gitlab', 'github actions', 'circleci', 'travis', 'argocd', 'flux', 'gitops'],
            'cloud_platforms': ['aws', 'azure', 'gcp', 'cloud'],
            'monitoring_observability': ['prometheus', 'grafana', 'elk', 'datadog', 'newrelic', 'splunk', 'nagios'],
            'scripting': ['python', 'bash', 'shell', 'go', 'ruby', 'perl'],
            'networking': ['nginx', 'haproxy', 'load balancer', 'cdn', 'api gateway', 'istio', 'envoy'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'elasticsearch'],
            'version_control': ['git', 'github', 'gitlab', 'bitbucket'],
            'security': ['vault', 'secrets', 'ssl', 'tls', 'security', 'compliance']
        }
    
    def analyze(self, parsed_resume: Dict) -> Dict:
        """
        Perform deep analysis of parsed resume
        
        Args:
            parsed_resume: Output from ResumeParser
        
        Returns:
            Structured profile analysis
        """
        skills = parsed_resume.get('skills', [])
        experience_years = parsed_resume.get('experience_years', 0)
        seniority = parsed_resume.get('seniority', 'Entry')
        
        # Categorize technologies
        tech_stack = self._categorize_technologies(skills)
        
        # Determine primary focus areas (top 3)
        primary_focus = self._identify_primary_focus(tech_stack)
        
        # Extract expertise level per category
        expertise_levels = self._determine_expertise_levels(tech_stack, experience_years)
        
        # Identify gaps/weak areas
        coverage_gaps = self._identify_gaps(tech_stack)
        
        # Generate focus recommendations
        focus_recommendations = self._generate_focus_areas(
            primary_focus, experience_years, seniority
        )
        
        # Create concise summary for prompt (smaller context)
        concise_summary = self._create_concise_summary(
            experience_years, seniority, primary_focus, tech_stack
        )
        
        return {
            'experience_years': experience_years,
            'seniority': seniority,
            'tech_stack': tech_stack,
            'primary_focus': primary_focus,
            'expertise_levels': expertise_levels,
            'coverage_gaps': coverage_gaps,
            'focus_recommendations': focus_recommendations,
            'concise_summary': concise_summary,
            'total_skills': len(skills),
            'skill_diversity_score': self._calculate_diversity_score(tech_stack)
        }
    
    def _categorize_technologies(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize skills into technology categories"""
        categorized = {category: [] for category in self.tech_categories.keys()}
        skills_lower = [s.lower() for s in skills]
        
        for category, keywords in self.tech_categories.items():
            for skill in skills:
                skill_lower = skill.lower()
                if any(keyword in skill_lower for keyword in keywords):
                    if skill not in categorized[category]:
                        categorized[category].append(skill)
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}
    
    def _identify_primary_focus(self, tech_stack: Dict) -> List[Tuple[str, int]]:
        """Identify top 3 primary focus areas based on skill count"""
        focus_scores = [(category, len(skills)) for category, skills in tech_stack.items()]
        focus_scores.sort(key=lambda x: x[1], reverse=True)
        return focus_scores[:3]  # Top 3
    
    def _determine_expertise_levels(self, tech_stack: Dict, experience_years: float) -> Dict:
        """Determine expertise level for each category"""
        expertise = {}
        
        for category, skills in tech_stack.items():
            skill_count = len(skills)
            
            # Simple heuristic based on experience and skill count
            if experience_years >= 5 and skill_count >= 3:
                level = "Expert"
            elif experience_years >= 3 and skill_count >= 2:
                level = "Advanced"
            elif skill_count >= 2:
                level = "Intermediate"
            else:
                level = "Basic"
            
            expertise[category] = {
                'level': level,
                'skills': skills,
                'count': skill_count
            }
        
        return expertise
    
    def _identify_gaps(self, tech_stack: Dict) -> List[str]:
        """Identify missing or weak technology areas"""
        gaps = []
        present_categories = set(tech_stack.keys())
        
        # Core DevOps areas that should ideally be present
        core_areas = {
            'container_orchestration',
            'infrastructure_as_code',
            'ci_cd',
            'monitoring_observability'
        }
        
        missing = core_areas - present_categories
        
        for area in missing:
            gaps.append(area.replace('_', ' ').title())
        
        # Check for thin coverage (only 1 skill in important category)
        for category, skills in tech_stack.items():
            if category in core_areas and len(skills) == 1:
                gaps.append(f"Limited {category.replace('_', ' ')} exposure")
        
        return gaps
    
    def _generate_focus_areas(self, primary_focus: List, experience_years: float, seniority: str) -> List[str]:
        """Generate recommended focus areas for interview"""
        recommendations = []
        
        # Add primary technology areas
        for category, count in primary_focus:
            recommendations.append(category.replace('_', ' ').title())
        
        # Add experience-based focus
        if experience_years >= 5:
            recommendations.extend([
                "Architecture & Design",
                "Team Leadership",
                "Production Incident Management"
            ])
        elif experience_years >= 3:
            recommendations.extend([
                "System Reliability",
                "Performance Optimization"
            ])
        else:
            recommendations.extend([
                "Fundamentals",
                "Best Practices"
            ])
        
        return recommendations[:5]  # Top 5 only
    
    def _create_concise_summary(self, experience_years: float, seniority: str, 
                                primary_focus: List, tech_stack: Dict) -> str:
        """Create a concise, formatted summary for LLM prompt (smaller context)"""
        
        # Get top skills from each primary focus area
        top_skills = []
        for category, _ in primary_focus:
            if category in tech_stack:
                top_skills.extend(tech_stack[category][:3])  # Max 3 per category
        
        # Limit to top 10 skills total
        top_skills = top_skills[:10]
        
        summary = f"""**Candidate Profile Summary**
- Experience: {experience_years} years ({seniority} level)
- Primary Expertise: {', '.join([cat.replace('_', ' ').title() for cat, _ in primary_focus])}
- Key Technologies: {', '.join(top_skills)}
- Skill Breadth: {len(tech_stack)} technology categories
"""
        return summary
    
    def _calculate_diversity_score(self, tech_stack: Dict) -> float:
        """Calculate skill diversity score (0-10)"""
        # Based on number of categories covered
        category_count = len(tech_stack)
        max_categories = len(self.tech_categories)
        
        # Normalize to 0-10 scale
        score = (category_count / max_categories) * 10
        return round(score, 1)
    
    def get_prioritized_tech_list(self, profile_analysis: Dict) -> List[Dict]:
        """Get prioritized list of technologies for question generation"""
        prioritized = []
        
        for category, skills_data in profile_analysis['expertise_levels'].items():
            prioritized.append({
                'category': category.replace('_', ' ').title(),
                'level': skills_data['level'],
                'skills': skills_data['skills'],
                'priority': self._calculate_priority(
                    category,
                    skills_data['count'],
                    profile_analysis['primary_focus']
                )
            })
        
        # Sort by priority (descending)
        prioritized.sort(key=lambda x: x['priority'], reverse=True)
        return prioritized
    
    def _calculate_priority(self, category: str, skill_count: int, primary_focus: List) -> int:
        """Calculate priority score for a technology category"""
        priority = skill_count * 10  # Base score
        
        # Boost if in primary focus
        focus_categories = [cat for cat, _ in primary_focus]
        if category in focus_categories:
            focus_rank = focus_categories.index(category)
            priority += (3 - focus_rank) * 20  # 60, 40, 20 bonus
        
        return priority


if __name__ == "__main__":
    # Test the analyzer
    from resume_parser import ResumeParser
    
    parser = ResumeParser()
    parsed = parser.parse_resume('sample_resume.pdf')
    
    analyzer = ProfileAnalyzer()
    analysis = analyzer.analyze(parsed)
    
    print("=" * 70)
    print("PROFILE ANALYSIS RESULTS")
    print("=" * 70)
    print(f"\nExperience: {analysis['experience_years']} years")
    print(f"Seniority: {analysis['seniority']}")
    print(f"Skill Diversity Score: {analysis['skill_diversity_score']}/10")
    
    print("\n--- Primary Focus Areas ---")
    for category, count in analysis['primary_focus']:
        print(f"  {category.replace('_', ' ').title()}: {count} skills")
    
    print("\n--- Coverage Gaps ---")
    for gap in analysis['coverage_gaps']:
        print(f"  - {gap}")
    
    print("\n--- Concise Summary ---")
    print(analysis['concise_summary'])
    
    print("\n--- Prioritized Tech List ---")
    prioritized = analyzer.get_prioritized_tech_list(analysis)
    for item in prioritized[:5]:
        print(f"  {item['category']} ({item['level']}): {', '.join(item['skills'][:3])}")

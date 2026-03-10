"""
Script to create a sample DevOps resume PDF for testing
"""

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
except ImportError:
    print("reportlab not installed. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
    from reportlab.lib.enums import TA_LEFT, TA_CENTER


def create_sample_resume():
    """Create a sample DevOps engineer resume"""
    
    filename = "sample_resume.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2C3E50',
        spaceAfter=6,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#34495E',
        spaceAfter=6,
        spaceBefore=12,
    )
    
    # Name and Title
    story.append(Paragraph("JOHN DOE", title_style))
    story.append(Paragraph("Senior DevOps Engineer", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Contact Info
    contact = "Email: john.doe@example.com | Phone: +1-555-0123 | LinkedIn: linkedin.com/in/johndoe"
    story.append(Paragraph(contact, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    summary = """
    Senior DevOps Engineer with 6 years of experience in cloud infrastructure automation, 
    container orchestration, and CI/CD pipeline development. Proven expertise in managing 
    large-scale Kubernetes clusters, implementing Infrastructure as Code, and building 
    robust monitoring solutions. Strong background in AWS cloud services and Python automation.
    """
    story.append(Paragraph(summary, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Technical Skills
    story.append(Paragraph("TECHNICAL SKILLS", heading_style))
    skills = """
    <b>Cloud Platforms:</b> AWS (EC2, ECS, EKS, S3, Lambda, CloudFormation), Azure, GCP<br/>
    <b>Container & Orchestration:</b> Kubernetes, Docker, Helm, ArgoCD, Rancher<br/>
    <b>Infrastructure as Code:</b> Terraform, Ansible, CloudFormation, Pulumi<br/>
    <b>CI/CD Tools:</b> Jenkins, GitLab CI, GitHub Actions, CircleCI<br/>
    <b>Monitoring & Observability:</b> Prometheus, Grafana, ELK Stack, Datadog, New Relic<br/>
    <b>Scripting & Programming:</b> Python, Bash, Shell scripting, Go<br/>
    <b>Version Control:</b> Git, GitHub, GitLab, Bitbucket<br/>
    <b>Service Mesh:</b> Istio, Linkerd<br/>
    <b>Secrets Management:</b> HashiCorp Vault, AWS Secrets Manager
    """
    story.append(Paragraph(skills, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Work Experience
    story.append(Paragraph("WORK EXPERIENCE", heading_style))
    
    # Job 1
    job1_title = "<b>Senior DevOps Engineer</b> | TechCorp Inc. | Jan 2021 - Present"
    story.append(Paragraph(job1_title, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    job1_resp = """
    • Managed production Kubernetes clusters serving 2M+ daily active users across multiple regions<br/>
    • Implemented GitOps workflow using ArgoCD, reducing deployment time by 60%<br/>
    • Automated infrastructure provisioning using Terraform, managing 500+ AWS resources<br/>
    • Developed Python automation scripts for incident response and routine maintenance tasks<br/>
    • Led migration from monolithic to microservices architecture on EKS<br/>
    • Implemented comprehensive monitoring solution with Prometheus and Grafana dashboards<br/>
    • Reduced production incidents by 40% through proactive alerting and automated remediation<br/>
    • Conducted on-call rotations and performed root cause analysis for critical incidents
    """
    story.append(Paragraph(job1_resp, styles['Normal']))
    story.append(Spacer(1, 0.15*inch))
    
    # Job 2
    job2_title = "<b>DevOps Engineer</b> | StartupXYZ | Jun 2018 - Dec 2020"
    story.append(Paragraph(job2_title, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    job2_resp = """
    • Built and maintained CI/CD pipelines using Jenkins and GitLab CI for 20+ microservices<br/>
    • Deployed and managed Docker containers in production environments<br/>
    • Automated server provisioning and configuration management using Ansible<br/>
    • Implemented infrastructure monitoring using ELK stack and custom Python scripts<br/>
    • Optimized AWS costs by 35% through resource rightsizing and reserved instances<br/>
    • Collaborated with development teams to implement DevOps best practices<br/>
    • Maintained 99.9% uptime SLA for critical production services
    """
    story.append(Paragraph(job2_resp, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Key Projects
    story.append(Paragraph("KEY PROJECTS", heading_style))
    
    projects = """
    <b>Cloud Migration Project:</b> Led migration of legacy on-premise infrastructure to AWS cloud, 
    involving 50+ applications and services. Implemented blue-green deployment strategy and 
    reduced infrastructure costs by 40%.<br/><br/>
    
    <b>Kubernetes Platform:</b> Designed and deployed enterprise Kubernetes platform using EKS, 
    implementing multi-tenancy, RBAC, network policies, and automated scaling. Served 15+ 
    development teams.<br/><br/>
    
    <b>Observability Initiative:</b> Built comprehensive observability solution integrating 
    Prometheus, Grafana, and distributed tracing. Created 50+ dashboards and 100+ alerts 
    for proactive monitoring.
    """
    story.append(Paragraph(projects, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Education
    story.append(Paragraph("EDUCATION", heading_style))
    education = """
    <b>Bachelor of Science in Computer Science</b><br/>
    University of Technology | 2014 - 2018
    """
    story.append(Paragraph(education, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Certifications
    story.append(Paragraph("CERTIFICATIONS", heading_style))
    certs = """
    • AWS Certified Solutions Architect - Professional<br/>
    • Certified Kubernetes Administrator (CKA)<br/>
    • HashiCorp Certified: Terraform Associate<br/>
    • AWS Certified DevOps Engineer - Professional
    """
    story.append(Paragraph(certs, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"✓ Sample resume created: {filename}")
    return filename


if __name__ == "__main__":
    create_sample_resume()

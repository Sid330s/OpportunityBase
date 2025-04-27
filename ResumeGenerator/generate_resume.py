import yaml
from jinja2 import Environment, FileSystemLoader
from pdflatex import PDFLaTeX
import os
import sys
import shutil


# Load YAML Data
def load_yaml(file_path):
    """Load YAML data from a given file path."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Generate LaTeX file using Jinja2
def generate_latex(yaml_data, template_path, output_path, pref_template_path):
    """Generate LaTeX file from a Jinja2 template and YAML data, prepending pref_template.tex."""
    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)

    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)

    rendered_content = template.render(yaml_data)
    
    # Read pref_template.tex
    with open(pref_template_path, 'r') as pref_file:
        pref_content = pref_file.read()
    
    # Combine pref_template.tex with rendered LaTeX
    final_content = pref_content + "\n" + rendered_content
    
    with open(output_path, "w") as file:
        file.write(final_content)

# Compile LaTeX file
def compile_latex(tex_file, output_dir):
    """Compile LaTeX file and store output in a specific directory."""
    try:
        pdfl = PDFLaTeX.from_texfile(tex_file)
        pdfl.set_output_directory(output_dir)
        pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
    except Exception as e:
        print(f"Error compiling LaTeX file {tex_file}: {e}")

if __name__ == "__main__":
    
    jobs_file = "jobs.yml"

    if not os.path.exists(jobs_file):
        print(f"Error: {jobs_file} not found!")
        sys.exit(1)

    jobs_data = load_yaml(jobs_file)

    for job in jobs_data.get("job_ids", []):
        job_id = job.get("job_id")
        company = job.get("company")
        generate = job.get("generate",False)

        if not generate:
            continue
        
        yaml_file = f"ResumeYAMLs/Siddharth_{company}_{version}.yml"
        template_file = "ResumeGenerator/resume_template.tex"
        pref_template_file = "ResumeGenerator/pref_template.tex"
        std_resume_file = "ResumeGenerator/resume-std.yml"
        output_tex = f"ResumeYAMLs/latex/Siddharth_{company}_{version}.tex"
        output_dir = "ResumeGenerator/output"

        if not os.path.exists(yaml_file):
            shutil.copy(std_resume_file, yaml_file)

        yaml_data = load_yaml(yaml_file)
        print(f"Starting Resume Generate: {yaml_file}")
        generate_latex(yaml_data, template_file, output_tex, pref_template_file)
        compile_latex(output_tex, output_dir)

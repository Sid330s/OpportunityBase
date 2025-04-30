import os
import sys
import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr, make_msgid

SENDER_EMAIL = os.environ['SENDER_EMAIL']
SENDER_NAME = os.environ['SENDER_NAME']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

smtp_server = "smtp.gmail.com"
smtp_port = 587

input_file = "ResumeGenerator/input.yml"

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found!")
    sys.exit(1)


def load_yaml(file_path):
    """Load YAML data from a given file path."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


jobs_file = "jobs.yml"
input_file = "EmailSender/input.yml"

if not os.path.exists(jobs_file):
    print(f"Error: {jobs_file} not found!")
    sys.exit(1)

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found!")
    sys.exit(1)

jobs_data = load_yaml(jobs_file)
input_data = load_yaml(input_file)

recipients = []


# Helper to find a person (recruiter/employee) by email
def find_recipients(input_data):
    recipients = []
    for jobs in jobs_data['job_ids']:
        company_name = jobs['company']
        job_id = jobs['job_id']
        jd_link = jobs['jd_link']
        if job_id not in input_data['job_ids']:
            continue
        for role_type in ['recruiters', 'employees']:
            for person in jobs.get(role_type, []):
                if person['email'].lower() == person['email']:
                    recipients.append(
                        (person['email'], person['name'], company_name, job_id,
                         jd_link, role_type))
    return recipients


# Start SMTP session
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(SENDER_EMAIL, EMAIL_PASSWORD)

    recipients = find_recipients(input_data)

    for recipient in recipients:

        recipient_email, recipient_name, company_name, job_id, jd_link, role_type = recipient

        # Prepare resume path
        resume_filename = f"Siddharth_{company_name}_{job_id}.pdf"
        resume_path = os.path.join("Resumes", resume_filename)

        if not os.path.exists(resume_path):
            print(
                f"❌ Resume file {resume_path} not found. Skipping {recipient_email}."
            )
            continue

        # Python code to construct the email content

        subject = f"Exploring Opportunities at {company_name} – Siddharth Kale"
        body = f"""
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
          <p>Hi {recipient_name},</p>

          <p>I'm <strong>Siddharth Kale</strong>, a software engineer passionate about building scalable distributed systems and cloud-native services.</p>

          <p>Here's a quick snapshot of my experience:</p>
          <ul>
            <li><strong>Distributed systems:</strong> Delivered resilient and performant backend services using Python and C++, focusing on concurrency and scalability.</li>
            <li><strong>Cloud-native services & orchestration engines:</strong> Hands-on with AWS, Kubernetes, Docker, and Terraform, building and automating production-grade services and infrastructure.</li>
            <li><strong>Core CS fundamentals:</strong> Achieved a CGPA of 9.49/10 with strong grasp over Operating Systems concepts including multi-threading, concurrency, memory management.</li>
            <li><strong>Data Structures & Algorithms:</strong> Solved 370+ problems on LeetCode, developing strong skills in designing efficient and scalable systems.</li>
          </ul>

          <p>I strongly value <strong>empathy, collaboration, and humility</strong>. With solid technical chops and a team-first mindset, I aim to build not just good code, but better culture. I thrive in environments where engineers support one another, communicate openly, and ship meaningful software together—just like <strong>{company_name}</strong>'s mission demands.</p>

          <p>I'm excited about the opportunity and would love to explore how I can contribute to your team.</p>

          <p>Thanks for your time and consideration. Looking forward to connecting!</p>

          <p>Best regards,<br>
          Siddharth Kale<br>
          <a href="mailto:siddharth.kale918@gmail.com">siddharth.kale918@gmail.com</a><br>
          <a href="https://www.linkedin.com/in/siddharth-kale-936922174/" target="_blank">LinkedIn</a> | 
          <a href="https://github.com/Sid330s" target="_blank">GitHub</a>
          </p>
        </body>
        """



        try:
            msg = MIMEMultipart()
            msg["From"] = formataddr((SENDER_NAME, SENDER_EMAIL))
            msg["To"] = recipient_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "html"))

            # Attach resume
            with open(resume_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition",
                                f"attachment; filename={resume_filename}")
                msg.attach(part)

            # Create custom Message-ID
            custom_message_id = make_msgid(domain="gmail.com")

            # Send email
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
            print(f"✅ Email sent to {recipient_email} ({company_name})")

        except Exception as e:
            print(f"❌ Failed to send to {recipient_email}: {e}")

    server.quit()

    print("\n📩 All emails processed and jobs.yml updated.")

except Exception as e:
    print(f"🚨 Error connecting to SMTP server: {e}")

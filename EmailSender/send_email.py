import os
import argparse
import smtplib
import yaml
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr, make_msgid

# Load environment variables
load_dotenv()
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_NAME = os.getenv('SENDER_NAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

smtp_server = "smtp.gmail.com"
smtp_port = 587

# Argument parsing
parser = argparse.ArgumentParser(description="Send customized emails.")
parser.add_argument('--emails', type=str, required=True, help="Comma separated list of emails.")
args = parser.parse_args()
input_emails = [email.strip() for email in args.emails.split(',')]

# Read jobs.yml
with open('jobs.yml', 'r') as f:
    jobs_data = yaml.safe_load(f)

# Helper to find a person (recruiter/employee) by email
def find_person(email):
    for company in jobs_data['companies']:
        for role_type in ['recruiters', 'employees']:
            for person in company.get(role_type, []):
                if person['email'].lower() == email.lower():
                    return company, person, role_type
    return None, None, None

# Start SMTP session
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(SENDER_EMAIL, EMAIL_PASSWORD)

    for recipient_email in input_emails:
        company, person, role_type = find_person(recipient_email)

        if not company or not person:
            print(f"⚠️ Email {recipient_email} not found in jobs.yml. Skipping.")
            continue

        company_name = company['name']
        recipient_name = person['name']

        # Use the first JD link (customize if needed)
        jd_link = company['job_descriptions'][-1]['jd_link']

        # Assume latest version is v1 (you can enhance by checking folder)
        version = len(company['job_descriptions'])

        # Prepare resume path
        resume_filename = f"SiddharthKale{company_name}V{version}.pdf"
        resume_path = os.path.join("Resumes", resume_filename)

        if not os.path.exists(resume_path):
            print(f"❌ Resume file {resume_path} not found. Skipping {recipient_email}.")
            continue

        # Compose email
        subject = f"Exploring Opportunities at {company_name} – Siddharth Kale"
        body = f"""
<body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
  <p>Hi {recipient_name},</p>

  <p>I'm <b>Siddharth Kale</b>, passionate about distributed systems, cloud infrastructure, and AI-based solutions.</p>

  <ul>
    <li><b>Strong engineering:</b> Built scalable cloud services, led initiatives in AI, blockchain, and optimized multithreaded C++/Python backends.</li>
    <li><b>Cloud ready:</b> Hands-on with AWS, Kubernetes, Terraform, Datadog, GCP, Azure.</li>
    <li><b>Impactful projects:</b> Blockchain for COVID-era medical equipment trust, Teamcenter AI Chat, scalable CAD storage services.</li>
  </ul>

  <p>I'm excited about the job <b>{jd_link}</b> at <b>{company_name}</b> and would love to connect further!</p>

  <p>Thank you for your time and consideration!</p>
  
  <p>Best,<br>
  Siddharth Kale<br>
  <a href="https://your-portfolio-link.com" target="_blank">Portfolio</a></p>
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
                part.add_header("Content-Disposition", f"attachment; filename={resume_filename}")
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

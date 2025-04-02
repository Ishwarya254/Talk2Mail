import whisper
import os
from google.colab import userdata
from langchain_groq import ChatGroq

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.colab import userdata
from email.message import EmailMessage

model = whisper.load_model("turbo")

result1 = model.transcribe("your_audio_file")
transcribed_text = result1["text"]

print(transcribed_text)

api_key = userdata.get('GROQ_web1')

os.environ["GROQ_API_KEY"] = "your api key"

llm = ChatGroq(model_name="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

prompt = f"""
Convert the following text into a professional email:

"{transcribed_text}"

Ensure the email includes:
- A clear and professional subject line.
- A polite greeting.
- A structured body that conveys the message concisely.
- A polite closing statement.

The email **must end with**:
**"Best regards,"**
[Your Name]

Do **not** include any additional text, explanations, or notes after "Best regards,". Ensure the output is strictly formatted as a professional email.


"""

# Pass to LLM for email generation
response = llm.invoke(input= prompt)

response

email_body = response.content.strip()

sender_email = "sender_email_ID"
receiver_email = "receiver_email_ID"
app_password = "your app_password"

email_text = response.content.strip()  # Get email text from LLM
lines = email_text.split("\n")  # Split into lines

# Extract Subject (first line should be 'Subject: ...')
subject_line = lines[0].replace("Subject:", "").strip()

# Ensure subject does not have newlines
subject_line = subject_line.replace("\n", " ")

# Reconstruct email body (skip the subject line)
email_body = "\n".join(lines[1:]).strip()

# Set up the email
msg = EmailMessage()
msg.set_content(email_body)
msg["Subject"] = subject_line  # Use cleaned subject
msg["From"] = sender_email
msg["To"] = receiver_email

# Send via SMTP
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "sender_email_ID"
smtp_password = app_password

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Error sending email: {e}")

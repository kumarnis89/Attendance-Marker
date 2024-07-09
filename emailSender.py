import smtplib
import configParser as cp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


cm = cp.ConfigManager()

# Accessing properties
from_email = cm.get_from_email()
from_password = cm.get_from_password()
to_email = cm.get_to_email()

def send_html_email(subject, html_content):

    # Create the email content
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Failed to send email: {e}')

def load_html_template(template_path):
    with open(template_path, 'r') as file:
        template = file.read()
    return template

# Example usage
def send_attendance_notification(success, date,action):
    template_path = 'attendance_template.html'

    if action == 1:
        action_text = "CLOCK IN"
    else:
        action_text = "CLOCK OUT"
    
    if success:
        message = f'{action_text} marked successfully for {date}.'
    else:
        message = f'{action_text} failed for {date}. Please mark it manually.'

    html_content = load_html_template(template_path)
    html_content = html_content.replace('{{ message }}',message)
    color = 'green'
    if success == False:
        color = 'red'

    html_content = html_content.replace('bg_result_based', color)
    send_html_email('Attendance Notification', html_content)

# Example call
# send_attendance_notification(False, '2024-07-07',1)
# send_attendance_notification(True, '2024-07-07',2)


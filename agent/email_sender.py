"""Email sender for phishing campaign simulation using SMTP."""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from core.logger import Logger


class EmailSender:
    """Handles email sending via SMTP (real or test services like Mailtrap)."""
    
    def __init__(self):
        self.logger = Logger.get_logger("EmailSender")
        
        # SMTP Configuration from environment variables
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.mailtrap.io")
        self.smtp_port = int(os.getenv("SMTP_PORT", "2525"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        
        # Sender configuration
        self.sender_domain = os.getenv("SENDER_DOMAIN", "securemail.test")
        self.sender_name = os.getenv("SENDER_NAME", "IT Security")
        
        # Email sending mode
        self.email_mode = os.getenv("EMAIL_MODE", "simulation")  # "simulation" or "smtp"
        
        if self.email_mode == "smtp":
            if not self.smtp_username or not self.smtp_password:
                self.logger.warning("SMTP credentials not configured. Set SMTP_USERNAME and SMTP_PASSWORD.")
                self.logger.info("Falling back to simulation mode.")
                self.email_mode = "simulation"
            else:
                self.logger.info(f"SMTP configured: {self.smtp_host}:{self.smtp_port} (TLS: {self.smtp_use_tls})")
                self.logger.info(f"Sender domain: {self.sender_domain}")
        else:
            self.logger.info("Running in SIMULATION mode (no emails will be sent)")
    
    def send(self, to: str, subject: str, body: str, sender_persona: str) -> bool:
        """Send email via SMTP or simulate sending."""
        
        if self.email_mode == "simulation":
            return self._simulate_send(to, subject, body, sender_persona)
        else:
            return self._send_smtp(to, subject, body, sender_persona)
    
    def _simulate_send(self, to: str, subject: str, body: str, sender_persona: str) -> bool:
        """Simulate email sending (log only)."""
        self.logger.info(f"[SIMULATION] Email prepared for {to}")
        self.logger.info(f"From: {sender_persona} <{sender_persona.lower().replace(' ', '.')}@{self.sender_domain}>")
        self.logger.info(f"Subject: {subject}")
        self.logger.info(f"Body preview: {body[:100]}...")
        return True
    
    def _send_smtp(self, to: str, subject: str, body: str, sender_persona: str) -> bool:
        """Actually send email via SMTP."""
        try:
            # Create sender email address
            sender_email = f"{sender_persona.lower().replace(' ', '.')}@{self.sender_domain}"
            
            # Create message
            message = MIMEMultipart("alternative")
            message["From"] = f"{sender_persona} <{sender_email}>"
            message["To"] = to
            message["Subject"] = subject
            
            # Add body as HTML (phishing emails often use HTML)
            html_body = self._convert_to_html(body)
            part = MIMEText(html_body, "html")
            message.attach(part)
            
            # Connect to SMTP server
            self.logger.info(f"Connecting to SMTP server: {self.smtp_host}:{self.smtp_port}")
            
            if self.smtp_use_tls:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            
            # Login
            self.logger.info(f"Authenticating as {self.smtp_username}")
            server.login(self.smtp_username, self.smtp_password)
            
            # Send email
            self.logger.info(f"Sending email to {to}")
            server.sendmail(sender_email, to, message.as_string())
            
            # Disconnect
            server.quit()
            
            self.logger.info(f"Email successfully sent to {to}")
            self.logger.info(f"From: {sender_persona} <{sender_email}>")
            self.logger.info(f"Subject: {subject}")
            
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            self.logger.error(f"SMTP Authentication failed: {str(e)}")
            self.logger.error("Check SMTP_USERNAME and SMTP_PASSWORD environment variables")
            return False
            
        except smtplib.SMTPException as e:
            self.logger.error(f"SMTP error: {str(e)}")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def _convert_to_html(self, text_body: str) -> str:
        """Convert plain text body to HTML with basic formatting."""
        # Replace newlines with <br> and wrap in basic HTML
        html_body = text_body.replace("\n", "<br>\n")
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .email-content {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="email-content">
        {html_body}
    </div>
</body>
</html>
"""
        return html
    
    def test_connection(self) -> bool:
        """Test SMTP connection and authentication."""
        if self.email_mode == "simulation":
            self.logger.info("Running in simulation mode - no SMTP to test")
            return True
        
        try:
            self.logger.info(f"Testing SMTP connection to {self.smtp_host}:{self.smtp_port}")
            
            if self.smtp_use_tls:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            
            server.login(self.smtp_username, self.smtp_password)
            server.quit()
            
            self.logger.info("SMTP connection successful")
            return True
            
        except Exception as e:
            self.logger.error(f"SMTP connection failed: {str(e)}")
            return False


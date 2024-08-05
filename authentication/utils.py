# from django.core.mail import EmailMessage
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

class Util:
    @staticmethod
    def send_email(subject, template_path, context, to_email):
        """
        Sends an email with the specified subject, template, context, and recipient.
        """
        # Load email template
        html_content = render_to_string(template_path, context)

        # Create email message with alternative content (HTML)
        email = EmailMultiAlternatives(
            subject=subject,
            body=html_content,
            from_email=os.environ.get('EMAIL_FROM', settings.DEFAULT_FROM_EMAIL),  # Use default email if not provided
            to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")


        # Send email
        email.send()

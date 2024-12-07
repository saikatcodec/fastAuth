def get_reset_password_email_template(reset_link: str) -> str:
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reset Your Password</title>
    </head>
    <body>
        <h2>Password Reset Request</h2>
        <p>We received a request to reset your password. Click the link below to choose a new password:</p>
        <a href="{ reset_link }">Reset Password</a>
        <p>If you did not request a password reset, please ignore this email or contact support if you have questions.</p>
        <p>Thanks,<br>The Support Team</p>
    </body>
    </html>
    """
    
    return html_content


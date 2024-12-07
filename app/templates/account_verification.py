def get_account_verification_template(verification_link):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Account Verification</title>
    </head>
    <body>
        <h1>Account Verification</h1>
        <p>Thank you for registering. Please verify your account by clicking the link below:</p>
        <a href="{verification_link}">Verify Account</a>
    </body>
    </html>
    """
    
    
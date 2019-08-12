class EmailConstant:
    EMAIL_HEADER = """
    <br><img width='350px' src={logo} / ><br><br>
    Dear <b>{user_name}</b>,<br><br>
    Greetings from Compliance 1Source.<br><br>
    """

    EMAIL_FOOTER = "<br><br>This is a system generated email. Do not reply." \
                   "<br><br>Thanks,<br>" \
                   "<b>Compliance 1Source</b>"

    CREATE_USER_SUBJECT = "Invitation - Thank you for signing up with Compliance 1Source!"

    CREATE_USER_BODY = """
                        <p>You have been set up as a user on the Compliance 1Source platform.</p>
                        <p>Click on the link below in order to complete the Registration. Alternately, copy and paste the link below in your browser and proceed.</p>
                        <p>{link}</p>
                        <p>We're excited to have you onboard.</p>
                        """

    FORGOT_PASSWORD_SUBJECT = "Forgotten your password?"

    FORGOT_PASSWORD_BODY = """<p>It looks like you need to change your password.</p>
                              <p>Not to worry, just use the link below and we'll help you reset your password to
                               something more memorable.</p>
                               <p>{link} </p>"""


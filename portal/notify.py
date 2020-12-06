import smtplib
from email.message import EmailMessage


def send_mail(send_to, name, title, skills):
        EMAIL_ADDRESS = 'Thepaceyogi@gmail.com'
        EMAIL_PASSWORD = 'vpselpeqcxoskzzh'

        jobapplied ='Chef required'

        msg = EmailMessage()
        msg['Subject']='Congratulations. You have been shortlisted.'
        msg['From']=EMAIL_ADDRESS
        msg['To']= send_to
        msg.set_content("""\
        Dear """ +name+""",

        You have been shortlisted for the below job you had applied for.
         -Title:"""+ title +"""
         -Required Skills:"""+ skills +"""

        Regards,
        Jobseeker.

        """)

        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:

            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

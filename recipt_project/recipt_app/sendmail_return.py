import smtplib
from email.mime.text import MIMEText
from datetime import datetime

class EmailSupportAgent:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def create_return_receipt_body(self, email_data):
        body = f"""
        <html>
        <body>
        <h1>WORKING ON IT</h1>
        <h2>E-RETURN RECEIPT</h2>
        <p>Receipt code (Return): {email_data['recipt_code']}</p>
        <p>Original Receipt code (Purchase): {email_data['recipt_code_buy']}</p>
        <h3>Customer Details:</h3>
        <p>Name: {email_data['customer_name']}</p>
        <p>Email: {email_data['customer_email']}</p>
        <h3>Returned Products:</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>Product Code</th>
                <th>Product Description</th>
                <th>Quantity Bought</th>
                <th>Quantity Returned</th>
                <th>Quantity Remaining</th>
                <th>Price per Unit</th>
                <th>Refund Amount</th>
            </tr>
        """
        
        for product in email_data['products']:
            product_code, quantity_bought, quantity_returned, price, product_description = product
            quantity_remaining = quantity_bought - quantity_returned
            refund_amount = quantity_returned * price
            
            body += f"""
            <tr>
                <td>{product_code}</td>
                <td>{product_description}</td>
                <td>{quantity_bought}</td>
                <td>{quantity_returned}</td>
                <td>{quantity_remaining}</td>
                <td>${price:.2f}</td>
                <td>${refund_amount:.2f}</td>
            </tr>
            """
        
        body += f"""
        </table>
        <h3>Total Refund: ${email_data['total_price']:.2f}</h3>
        <h3>User Information:</h3>
        <p>First Name: {email_data['first_name']}</p>
        <p>Last Name: {email_data['last_name']}</p>
        <p>Username: {email_data['username']}</p>
        <p>Date of Return: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        <p>Thank you for your return. We hope to serve you again!</p>
        </body>
        </html>
        """
        return body

    def send_email(self, subject, body, to_email):
        msg = MIMEText(body, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = self.smtp_user
        msg['To'] = to_email

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            return "Success"
        except smtplib.SMTPAuthenticationError as e:
            return f"Authentication Error: {str(e)}"
        except smtplib.SMTPConnectError as e:
            return f"Connection Error: {str(e)}"
        except smtplib.SMTPDataError as e:
            return f"Data Error: {str(e)}"
        except smtplib.SMTPException as e:
            return f"SMTP Error: {str(e)}"
        except Exception as e:
            return f"Unexpected Error: {str(e)}"

    def handle_return_email(self, email_data):
        subject = f"{email_data['customer_name']}'s Return Receipt from BUGS at {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        body = self.create_return_receipt_body(email_data)
        return self.send_email(subject, body, email_data['customer_email'])

# Global initialization of support_agent
support_agent = EmailSupportAgent(
    'smtp.gmail.com', 587,
    'saqlainfawad@gmail.com', 'jtpqvszrodmcarlt'  # Replace with your actual app password
)

def sendmail_return_py(email_data):
    return support_agent.handle_return_email(email_data)

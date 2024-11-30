import smtplib
from email.mime.text import MIMEText
from datetime import datetime

class EmailSupportAgent:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def create_receipt_body(self, email_data):
        body = f"""
        <html>
        <body>
        <h2>E-RECEIPT</h2>
        <p>Receipt code: {email_data['recipt_code']}</p>
        <h3>Customer Details:</h3>
        <p>Name: {email_data['customer_name']}</p>
        <p>Email: {email_data['customer_email']}</p>
        <h3>Products Purchased:</h3>
        <table border="1">
            <tr>
                <th>Product code</th>
                <th>Product Discreption</th>
                <th>Quantity</th>
                <th>Price per Unit</th>
                <th>Total</th>
            </tr>
        """
        
        for product in email_data['products']:
            print(f"line 33 product :: {product}")
            product_code, quantity, price, quantity_price,product_discreption = product
            body += f"""
            <tr>
                <td>{product_code}</td>
                <td>${product_discreption}</td>
                <td>{quantity}</td>
                <td>${price:.2f}</td>
                <td>${quantity_price:.2f}</td>
            </tr>
            """
        
        body += f"""
        </table>
        <h3>Total Price: ${email_data['total_price']:.2f}</h3>
        <h3>User Information:</h3>
        <p>First Name: {email_data['first_name']}</p>
        <p>Last Name: {email_data['last_name']}</p>
        <p>Username: {email_data['username']}</p>
        <p>Date of Purchase: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        <p>Thank you for shopping with us!</p>
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

    def handle_incoming_email(self, email_data):
        subject = f"{email_data['customer_name']}'s Purchase Receipt from Easy Mart at {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        body = self.create_receipt_body(email_data)
        return self.send_email(subject, body, email_data['customer_email'])

# Global initialization of support_agent
support_agent = EmailSupportAgent(
    'smtp.gmail.com', 587,
    'saqlainfawad@gmail.com', 'jtpqvszrodmcarlt'  # Replace with your actual app password
)

def sendmail_py(email_data):
    return support_agent.handle_incoming_email(email_data)

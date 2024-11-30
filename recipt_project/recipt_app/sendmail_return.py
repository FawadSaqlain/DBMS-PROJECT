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
        <h1>E-RETURN RECEIPT</h1>
        <p><strong>Receipt Code (Return):</strong> {email_data['recipt_code']}</p>
        <p><strong>Original Receipt Code (Purchase):</strong> {email_data['recipt_code_buy']}</p>
        
        <h2>Customer Details</h2>
        <p><strong>Name:</strong> {email_data['customer_name']}</p>
        <p><strong>Email:</strong> {email_data['customer_email']}</p>
        
        <h2>Returned Products</h2>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse:collapse;">
            <tr>
                <th>Product Code</th>
                <th>Product Description</th>
                <th>Quantity now in Bought recipt</th>
                <th>Quantity Returned</th>
                <th>Price per Unit</th>
                <th>Refund Amount</th>
            </tr>
        """

        total_refund = 0.0  # Initialize total refund

        # Loop over bought products and match with returned products
        for product_bought in email_data['bought_product']:
            prod_id_bought, prod_code_bought, prod_description_bought, quantity_bought, price_bought, price_quantity_bought = product_bought

            # Convert price_bought to float if necessary
            try:
                price_bought = float(price_bought)
            except ValueError:
                price_bought = 0.0  # Handle invalid price conversion

            # Find matching returned product
            matching_returned_product = next((p for p in email_data['products'] if p[0] == prod_code_bought), None)

            if matching_returned_product:
                # Unpacking returned product details
                product_code_return, quantity_return, price_returned, quantity_price_return, product_description_return = matching_returned_product
                quantity_was_bought = quantity_bought + quantity_return
                refund_amount = quantity_return * price_bought  # Calculate refund amount
                total_refund += refund_amount  # Accumulate total refund
            else:
                quantity_return = 0
                refund_amount = 0
                quantity_was_bought = quantity_bought

            body += f"""
            <tr>
                <td>{prod_code_bought}</td>
                <td>{prod_description_bought}</td>
                <td>{quantity_bought}</td>
                <td>{quantity_return}</td>
                <td>${price_bought:.2f}</td>
                <td>${refund_amount:.2f}</td>
            </tr>
            """

        body += f"""
        </table>
        <h3>Total Refund: ${total_refund:.2f}</h3>

        <h2>User Information</h2>
        {"<p><strong>First Name:</strong> " + email_data['first_name'] + "</p>" if email_data.get('first_name') else ""}
        {"<p><strong>Last Name:</strong> " + email_data['last_name'] + "</p>" if email_data.get('last_name') else ""}
        <p><strong>Username:</strong> {email_data['username']}</p>
        <p><strong>Date of Return:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>

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
        subject = f"{email_data['customer_name']}'s Return Receipt from Easy Mart at {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        body = self.create_return_receipt_body(email_data)
        return self.send_email(subject, body, email_data['customer_email'])

# Global initialization of support_agent
support_agent = EmailSupportAgent(
    'smtp.gmail.com', 587,
    'saqlainfawad@gmail.com', 'jtpqvszrodmcarlt'  # Replace with your actual app password
)

def sendmail_return_py(email_data):
    return support_agent.handle_return_email(email_data)

from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/envoyer', methods=['POST'])
def envoyer():
    destinataire = request.form['user_mail']
    message_user = request.form['user_message']

    # Configuration de ton e-mail (à adapter)
    sender_email = "mathis.vende7@gmail.com"
    sender_password = "xrmo tjgh eehj tdnb"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Créer le message
    msg = MIMEText(message_user)
    msg['Subject'] = "Message de ton site"
    msg['From'] = sender_email
    msg['To'] = destinataire

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return "E-mail envoyé avec succès !"
    except Exception as e:
        return f"Erreur : {e}"

if __name__ == '__main__':
    app.run(debug=True)

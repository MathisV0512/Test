from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Charger les variables d’environnement si en local
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/envoyer', methods=['POST'])
def envoyer():
    destinataire = request.form['email']
    message_user = request.form['message']

    # Récupération des infos de connexion Gmail via variables d’environnement
    sender_email = os.environ.get('EMAIL_USER')
    sender_password = os.environ.get('EMAIL_PASS')
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    msg = MIMEText(message_user)
    msg['Subject'] = "Message depuis le formulaire Flask"
    msg['From'] = sender_email
    msg['To'] = destinataire

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return f"E-mail envoyé à {destinataire} !"
    except Exception as e:
        return f"Erreur lors de l'envoi de l'e-mail : {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Port auto-assigné par Render
    app.run(host='0.0.0.0', port=port, debug=True)

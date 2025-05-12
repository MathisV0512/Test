from flask import Flask, request, redirect, url_for, render_template
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

@app.route('/boutique')
def boutique():
    return render_template('boutique.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def contact():
    return render_template('about.html')

@app.route('/commentaire')
def contact():
    return render_template('commentaire.html')

@app.route('/envoyer', methods=['POST'])
def envoyer():
    sender_email = request.form['user_mail']
    message_user = request.form['user_message']

    destinataire = os.environ.get('EMAIL_USER')
    sender_password = os.environ.get('EMAIL_PASS')
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Corps du message avec adresse de l'utilisateur
    body = f"Message de : {sender_email}\n\n{message_user}"
    msg = MIMEText(body)
    msg['Subject'] = "Message depuis le formulaire Flask"
    msg['From'] = destinataire
    msg['To'] = destinataire
    msg['Reply-To'] = sender_email  # Pour pouvoir répondre à l'utilisateur

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(destinataire, sender_password)
            server.send_message(msg)
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erreur lors de l'envoi de l'e-mail : {str(e)}"
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Port auto-assigné par Render
    app.run(host='0.0.0.0', port=port, debug=True)

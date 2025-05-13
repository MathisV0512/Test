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
    # Récupération du numéro de page (1 par défaut)
    page = int(request.args.get('page', 1))
    per_page = 9

    # Liste simulée de 12 produits
    photos = [
        {"filename": "photo1.jpg", "title": "Chapeau de paille", "price": "25€", "desc": "Un chapeau idéal pour l'été."},
        {"filename": "photo2.jpg", "title": "Lunettes de soleil", "price": "15€", "desc": "Protection UV garantie."},
        {"filename": "photo4.jpg", "title": "Montre élégante", "price": "120€", "desc": "Élégance et précision."},
        {"filename": "photo5.jpg", "title": "Bracelet en argent", "price": "45€", "desc": "Un bijou intemporel."},
        {"filename": "photo6.jpg", "title": "Boucles d'oreilles", "price": "30€", "desc": "Pour un look chic."},
        {"filename": "photo7.jpg", "title": "Écharpe en laine", "price": "35€", "desc": "Chaleur et confort."},
        {"filename": "photo8.jpg", "title": "Portefeuille en cuir", "price": "50€", "desc": "Pratique et élégant."},
        {"filename": "photo9.jpg", "title": "Tote bag en coton", "price": "20€", "desc": "Pour vos courses."},
        {"filename": "photo10.jpg", "title": "Bottines en cuir", "price": "80€", "desc": "Confort et style."},
        {"filename": "photo11.jpg", "title": "Ceinture en cuir", "price": "40€", "desc": "Accessoire indispensable."},
        {"filename": "photo12.jpg", "title": "Gant en cuir", "price": "25€", "desc": ""}  
    ]

    # Découpage des photos selon la page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_photos = photos[start:end]

    # Nombre total de pages
    total_pages = ((len(photos) // per_page) + (1 if len(photos) % per_page > 0 else 0))

    return render_template(
        'boutique.html',
        photos=paginated_photos,
        page=page,
        total_pages=total_pages
    )

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/commentaire')
def commentaire():
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
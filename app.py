from flask import Flask, request, redirect, url_for, render_template, abort
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

photos = [
    {"id": 1, "filename": "photo1.jpg", "title": "Chapeau de paille", "price": "15.99$", "description": "Un chapeau de paille léger et élégant pour l'été.", "event_id": 1},
    {"id": 2, "filename": "photo2.jpg", "title": "Lunettes de soleil", "price": "25.99$", "description": "Des lunettes de soleil tendance pour protéger vos yeux.", "event_id": 1},
    {"id": 3, "filename": "photo3.jpg", "title": "Montre élégante", "price": "99.99$", "description": "Une montre élégante pour toutes les occasions.", "event_id": 2},
    {"id": 4, "filename": "photo4.jpg", "title": "Bracelet en argent", "price": "45.00$", "description": "Un bracelet en argent massif pour un look chic.", "event_id": 2},
    {"id": 5, "filename": "photo5.jpg", "title": "Boucles d'oreilles", "price": "30.00$", "description": "Des boucles d'oreilles en or pour briller.", "event_id": 3},
    {"id": 6, "filename": "photo6.jpg", "title": "Écharpe en laine", "price": "20.00$", "description": "Une écharpe en laine douce pour l'hiver.", "event_id": 3},
    {"id": 7, "filename": "photo7.jpg", "title": "Portefeuille en cuir", "price": "50.00$", "description": "Un portefeuille en cuir de haute qualité.", "event_id": 4},
    {"id": 8, "filename": "photo8.jpg", "title": "Tote bag en coton", "price": "15.00$", "description": "Un tote bag en coton bio pour vos courses.", "event_id": 4},
    {"id": 9, "filename": "photo9.jpg", "title": "Bottines en cuir", "price": "$120.00",  "description": 'Des bottines en cuir confortables et stylées.', "event_id": 5},
    {"id": 10, "filename": 'photo10.jpg', "title": 'Ceinture en cuir', "price": '$35.00', "description": 'Une ceinture en cuir robuste et élégante.', "event_id": 5},
    {"id": 11, "filename": 'photo11.jpg', "title": 'Gant en cuir', "price": '$40.00', "description": 'Des gants en cuir doux et chauds.', "event_id": 5},
]

# Liste simulée de 12 produits
events = [
    {"id": 1, "filename": "photo1.jpg", "title": "Chapeau de paille"},
    {"id": 2, "filename": "photo2.jpg", "title": "Lunettes de soleil"},
    {"id": 3, "filename": "photo4.jpg", "title": "Montre élégante"},
    {"id": 4, "filename": "photo5.jpg", "title": "Bracelet en argent"},
    {"id": 5, "filename": "photo6.jpg", "title": "Boucles d'oreilles"},
    {"id": 6, "filename": "photo7.jpg", "title": "Écharpe en laine"},
    {"id": 7, "filename": "photo8.jpg", "title": "Portefeuille en cuir"},
    {"id": 8, "filename": "photo9.jpg", "title": "Tote bag en coton"},
    {"id": 9, "filename": "photo10.jpg", "title": "Bottines en cuir"},
    {"id": 10, "filename": "photo11.jpg", "title": "Ceinture en cuir"},
    {"id": 11, "filename": "photo12.jpg", "title": "Gant en cuir"}  
]

cart_items= []

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

    # Découpage des events selon la page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_events = events[start:end]

    # Nombre total de pages
    total_pages = ((len(events) // per_page) + (1 if len(events) % per_page > 0 else 0))

    return render_template(
        'boutique.html',
        events=paginated_events,
        page=page,
        total_pages=total_pages
    )

@app.route('/event/<int:id>')
def event(id):
    event_data = next((e for e in events if e['id'] == id), None)
    if event_data is None:
        abort(404)

    page = int(request.args.get('page', 1))
    per_page = 9

    # Filtrer les photos appartenant à cet événement
    photos_for_event = [p for p in photos if p['event_id'] == id]

    start = (page - 1) * per_page
    end = start + per_page
    paginated_photos = photos_for_event[start:end]

    total_pages = (len(photos_for_event) + per_page - 1) // per_page

    return render_template(
        'event.html',
        photos=paginated_photos,
        page=page,
        total_pages=total_pages,
        event_data=event_data  
    )

@app.route('/produit/<int:id>')
def produit(id):
    produit = next((p for p in photos if p['id'] == id), None)
    if produit is None:
        abort(404)
    return render_template('produit.html', produit=produit)

@app.route('/panier')
def panier():
    item_id = request.args.get('item')
    if item_id:
        try:
            item_id = int(item_id)
            produit = next((p for p in photos if p['id'] == item_id), None)
            if produit and produit not in cart_items:
                cart_items.append(produit)
        except ValueError:
            pass  # En cas d'ID invalide
    return render_template('panier.html', cart_items=cart_items)



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
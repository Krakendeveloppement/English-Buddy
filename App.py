import streamlit as st
import random
from datetime import date, datetime
import time
import hashlib
import json
import os
from pathlib import Path

# -------------------------------
# CONFIGURATION DE LA PAGE
# -------------------------------
st.set_page_config(
    page_title="English Buddy by Krakendeveloppement",
    page_icon="🇬🇧",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------
# GESTION DES UTILISATEURS (fichier JSON simple)
# -------------------------------
# Dans une vraie app, tu utiliserais une base de données
# Mais pour commencer, on utilise un fichier local
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"
PROGRESS_FILE = DATA_DIR / "progress.json"

def hash_password(password):
    """Hash simple (à remplacer par bcrypt en production)"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)

# Initialisation de la session utilisateur
if "user" not in st.session_state:
    st.session_state.user = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"  # login ou register

# -------------------------------
# SYSTÈME D'ABONNEMENT (simulé)
# -------------------------------
# Idée: tu peux intégrer Stripe via https://nevermined.io [citation:4]
# Pour l'instant, on simule avec un fichier
SUBSCRIPTIONS_FILE = DATA_DIR / "subscriptions.json"

def load_subscriptions():
    if SUBSCRIPTIONS_FILE.exists():
        with open(SUBSCRIPTIONS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_subscriptions(subs):
    with open(SUBSCRIPTIONS_FILE, "w") as f:
        json.dump(subs, f)

def check_subscription(email):
    """Vérifie si l'utilisateur a un abonnement actif"""
    subs = load_subscriptions()
    if email in subs:
        expiry = datetime.fromisoformat(subs[email])
        if expiry > datetime.now():
            return True
    return False

def activate_subscription(email, duration_days=365):
    """Active un abonnement pour 1 an"""
    subs = load_subscriptions()
    expiry = datetime.now() + timedelta(days=duration_days)
    subs[email] = expiry.isoformat()
    save_subscriptions(subs)

# -------------------------------
# CSS PERSONNALISÉ (avec fond mots qui fonctionne)
# -------------------------------
st.markdown("""
<style>
    /* Variables pour les deux thèmes - adaptatif */
    :root {
        --bg-primary: #f0f2f6;
        --bg-secondary: #ffffff;
        --text-primary: #000000;
        --text-secondary: #333333;
        --accent-color: #4CAF50;
        --accent-hover: #45a049;
        --border-color: #ddd;
        --bot-message-bg: rgba(200, 200, 200, 0.9);
        --user-message-bg: rgba(173, 216, 230, 0.9);
        --overlay-bg: rgba(255, 255, 255, 0.9);
    }

    /* Mode sombre détecté automatiquement */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #1e1e1e;
            --bg-secondary: #2d2d2d;
            --text-primary: #ffffff;
            --text-secondary: #e0e0e0;
            --accent-color: #6bb86b;
            --accent-hover: #5ca65c;
            --border-color: #555;
            --bot-message-bg: rgba(60, 60, 60, 0.95);
            --user-message-bg: rgba(0, 100, 148, 0.9);
            --overlay-bg: rgba(30, 30, 30, 0.9);
        }
    }

    /* Fond avec mots - visible mais discret */
    .word-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
        opacity: 0.15;
        pointer-events: none;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-around;
        padding: 20px;
    }
    
    .word-background span {
        font-size: 1.2rem;
        color: var(--text-primary);
        margin: 10px;
        transform: rotate(calc(var(--rotation) * 1deg));
        white-space: nowrap;
        font-weight: bold;
        animation: float 20s infinite alternate;
    }
    
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        100% { transform: translateY(-20px) rotate(5deg); }
    }

    /* Style du conteneur principal - semi-transparent */
    .main-content {
        background-color: var(--overlay-bg);
        border-radius: 20px;
        padding: 25px;
        margin: 10px 0;
        backdrop-filter: blur(3px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Boutons */
    .stButton button {
        width: 100%;
        height: 3.5em;
        font-size: 1.1em;
        margin: 5px 0;
        background-color: var(--accent-color);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: var(--accent-hover);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }

    /* Messages */
    .bot-message {
        background-color: var(--bot-message-bg);
        color: var(--text-primary);
        border-radius: 20px 20px 20px 5px;
        padding: 15px;
        margin: 10px 0;
        font-size: 1.1em;
        border: 1px solid var(--border-color);
    }

    .user-message {
        background-color: var(--user-message-bg);
        color: var(--text-primary);
        border-radius: 20px 20px 5px 20px;
        padding: 12px 18px;
        margin: 5px 0;
        text-align: right;
        border: 1px solid var(--border-color);
    }

    /* Titre */
    .title {
        text-align: center;
        font-size: 2.5em;
        color: var(--accent-color);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 1.1em;
        color: var(--text-secondary);
        margin-top: 0;
        margin-bottom: 20px;
    }

    /* Cartes */
    .level-card, .stats-card {
        background-color: var(--bg-secondary);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 15px;
        font-size: 0.9em;
        color: var(--text-secondary);
        border-top: 1px solid var(--border-color);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# FOND AVEC MOTS (génération)
# -------------------------------
word_pairs = [
    ("bonjour", "hello"), ("merci", "thank you"), ("maison", "house"), ("voiture", "car"),
    ("chat", "cat"), ("chien", "dog"), ("manger", "eat"), ("boire", "drink"),
    ("soleil", "sun"), ("lune", "moon"), ("étoile", "star"), ("ciel", "sky"),
    ("grand", "big"), ("petit", "small"), ("content", "happy"), ("triste", "sad"),
    ("livre", "book"), ("ordinateur", "computer"), ("école", "school"), ("travail", "work"),
    ("rouge", "red"), ("bleu", "blue"), ("vert", "green"), ("jaune", "yellow"),
    ("pomme", "apple"), ("pain", "bread"), ("eau", "water"), ("feu", "fire")
]

# Créer le fond avec rotation aléatoire
background_html = '<div class="word-background">'
for i, (fr, en) in enumerate(word_pairs):
    rotation = random.randint(-10, 10)
    background_html += f'<span style="--rotation:{rotation}">{fr} → {en}</span>'
background_html += '</div>'

st.markdown(background_html, unsafe_allow_html=True)

# -------------------------------
# DONNÉES DE L'APPLICATION
# -------------------------------

# Vocabulaire par niveau
vocabulaire_debutant = {
    "bonjour": "hello", "merci": "thank you", "au revoir": "goodbye", "maison": "house",
    "voiture": "car", "chien": "dog", "chat": "cat", "manger": "eat", "boire": "drink",
    "dormir": "sleep", "aimer": "love", "parler": "speak", "travail": "work", "école": "school",
    "livre": "book", "stylo": "pen", "table": "table", "chaise": "chair", "porte": "door",
    "soleil": "sun", "lune": "moon", "eau": "water", "feu": "fire", "grand": "big",
    "petit": "small", "content": "happy", "triste": "sad", "jour": "day", "nuit": "night"
}

vocabulaire_intermediaire = {
    "ordinateur": "computer", "téléphone": "phone", "avion": "plane", "train": "train",
    "animal": "animal", "oiseau": "bird", "poisson": "fish", "cheval": "horse",
    "fleur": "flower", "arbre": "tree", "pomme": "apple", "banane": "banana",
    "pain": "bread", "fromage": "cheese", "lait": "milk", "œuf": "egg",
    "vêtement": "clothes", "chemise": "shirt", "chaussure": "shoe", "chapeau": "hat",
    "couleur": "color", "rouge": "red", "bleu": "blue", "vert": "green", "jaune": "yellow"
}

vocabulaire_professionnel = {
    "réunion": "meeting", "contrat": "contract", "client": "client", "marché": "market",
    "vente": "sale", "achat": "purchase", "négociation": "negotiation", "stratégie": "strategy",
    "objectif": "goal", "performance": "performance", "bénéfice": "profit", "budget": "budget",
    "analyse": "analysis", "rapport": "report", "présentation": "presentation", "projet": "project",
    "équipe": "team", "management": "management", "compétence": "skill", "formation": "training",
    "salaire": "salary", "contrat": "contract", "télétravail": "remote work", "bureau": "office"
}

vocabulaire_par_niveau = {
    "Débutant": vocabulaire_debutant,
    "Intermédiaire": vocabulaire_intermediaire,
    "Professionnel": vocabulaire_professionnel
}

# Autres données (verbes, phrases, etc.)
verbes_irreguliers = [
    {"base": "be", "preterit": "was/were", "participe": "been", "francais": "être"},
    {"base": "have", "preterit": "had", "participe": "had", "francais": "avoir"},
    {"base": "do", "preterit": "did", "participe": "done", "francais": "faire"},
    {"base": "go", "preterit": "went", "participe": "gone", "francais": "aller"},
    {"base": "eat", "preterit": "ate", "participe": "eaten", "francais": "manger"},
    {"base": "drink", "preterit": "drank", "participe": "drunk", "francais": "boire"}
]

phrases_du_jour = [
    {"francais": "Quel temps fait-il ?", "anglais": "What's the weather like?"},
    {"francais": "Je voudrais un café", "anglais": "I would like a coffee"},
    {"francais": "Où est la gare ?", "anglais": "Where is the station?"}
]

lecons_journalieres = {
    "lundi": "📘 **Present Simple** – I eat, you eat...",
    "mardi": "📙 **Past Simple** – I ate, you ate...",
    "mercredi": "📕 **Future** – I will eat...",
    "jeudi": "📗 **Prepositions** – in, on, at",
    "vendredi": "📓 **Modal verbs** – can, must, should",
    "samedi": "📔 **Adjectives** – big, small",
    "dimanche": "📒 **Adverbs** – quickly, slowly"
}

reponses_bot = {
    "salutation": ["Hello!", "Hi there!", "Hey!"],
    "forme": ["I'm fine!", "Doing great!", "All good!"],
    "remerciement": ["You're welcome!", "My pleasure!"],
    "au_revoir": ["Goodbye!", "See you later!"],
    "inconnu": ["I don't understand", "Can you rephrase?"],
    "encouragement": ["Great!", "Excellent!", "Well done!"]
}

# -------------------------------
# SESSION STATE (données temporaires)
# -------------------------------
if "etape" not in st.session_state:
    st.session_state.etape = "menu"
if "score" not in st.session_state:
    st.session_state.score = 0
if "niveau_app" not in st.session_state:
    st.session_state.niveau_app = 1
if "historique" not in st.session_state:
    st.session_state.historique = []
if "question_quiz" not in st.session_state:
    st.session_state.question_quiz = None
if "reponse_quiz" not in st.session_state:
    st.session_state.reponse_quiz = None
if "nb_quiz" not in st.session_state:
    st.session_state.nb_quiz = 0
if "niveau_utilisateur" not in st.session_state:
    st.session_state.niveau_utilisateur = "Débutant"

# -------------------------------
# FONCTIONS
# -------------------------------
def get_bot_reponse(msg):
    msg = msg.lower()
    if any(g in msg for g in ["hello", "hi", "bonjour"]):
        return random.choice(reponses_bot["salutation"])
    elif any(f in msg for f in ["how are you", "ça va"]):
        return random.choice(reponses_bot["forme"])
    elif any(t in msg for t in ["merci", "thanks"]):
        return random.choice(reponses_bot["remerciement"])
    elif any(b in msg for b in ["bye", "au revoir"]):
        return random.choice(reponses_bot["au_revoir"])
    else:
        return random.choice(reponses_bot["inconnu"])

def ajouter_point():
    st.session_state.score += 1
    if st.session_state.score % 5 == 0:
        st.session_state.niveau_app += 1
        st.balloons()
    
    # Sauvegarder la progression si utilisateur connecté
    if st.session_state.user:
        progress = load_progress()
        email = st.session_state.user["email"]
        if email not in progress:
            progress[email] = {"score": 0, "niveau": 1, "historique": []}
        progress[email]["score"] = st.session_state.score
        progress[email]["niveau"] = st.session_state.niveau_app
        save_progress(progress)

def nouvelle_question_quiz():
    vocab = vocabulaire_par_niveau[st.session_state.niveau_utilisateur]
    return random.choice(list(vocab.items()))

# -------------------------------
# PAGE D'AUTHENTIFICATION
# -------------------------------
def auth_page():
    st.markdown('<h1 class="title">🇬🇧 English Buddy ++</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Created by <strong>Krakendeveloppement</strong></p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔐 Connexion", use_container_width=True):
                st.session_state.auth_mode = "login"
        with col2:
            if st.button("📝 Inscription", use_container_width=True):
                st.session_state.auth_mode = "register"
        
        st.markdown("---")
        
        if st.session_state.auth_mode == "login":
            st.subheader("Connexion")
            email = st.text_input("Email")
            password = st.text_input("Mot de passe", type="password")
            
            if st.button("Se connecter", use_container_width=True):
                users = load_users()
                if email in users and users[email] == hash_password(password):
                    st.session_state.user = {"email": email}
                    
                    # Charger la progression
                    progress = load_progress()
                    if email in progress:
                        st.session_state.score = progress[email]["score"]
                        st.session_state.niveau_app = progress[email]["niveau"]
                    
                    st.success("Connexion réussie !")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Email ou mot de passe incorrect")
        
        else:  # register
            st.subheader("Inscription")
            email = st.text_input("Email")
            password = st.text_input("Mot de passe", type="password")
            confirm = st.text_input("Confirmer mot de passe", type="password")
            
            if st.button("S'inscrire", use_container_width=True):
                if password != confirm:
                    st.error("Les mots de passe ne correspondent pas")
                elif len(password) < 6:
                    st.error("Mot de passe trop court (min 6 caractères)")
                else:
                    users = load_users()
                    if email in users:
                        st.error("Cet email est déjà utilisé")
                    else:
                        users[email] = hash_password(password)
                        save_users(users)
                        st.session_state.user = {"email": email}
                        st.success("Inscription réussie !")
                        time.sleep(1)
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# PAGE PRINCIPALE (après connexion)
# -------------------------------
def main_app():
    # En-tête
    st.markdown('<h1 class="title">🇬🇧 English Buddy ++</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Created by <strong>Krakendeveloppement</strong></p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header(f"👤 {st.session_state.user['email']}")
        st.metric("Score", st.session_state.score)
        st.metric("Niveau", st.session_state.niveau_app)
        
        # Vérification abonnement
        if check_subscription(st.session_state.user["email"]):
            st.success("✅ Abonnement actif")
        else:
            st.warning("⏳ Abonnement requis")
            if st.button("💳 S'abonner (20€/an)", use_container_width=True):
                # Rediriger vers Stripe (à implémenter)
                st.info("Redirection vers Stripe...")
                # activate_subscription(st.session_state.user["email"])  # À décommenter après paiement
        
        st.markdown("---")
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    # Contenu principal
    with st.container():
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
        # Sélecteur de niveau visible sur la page d'accueil
        st.markdown('<div class="level-card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔰 Débutant", use_container_width=True,
                        type="primary" if st.session_state.niveau_utilisateur == "Débutant" else "secondary"):
                st.session_state.niveau_utilisateur = "Débutant"
                st.rerun()
        with col2:
            if st.button("📚 Intermédiaire", use_container_width=True,
                        type="primary" if st.session_state.niveau_utilisateur == "Intermédiaire" else "secondary"):
                st.session_state.niveau_utilisateur = "Intermédiaire"
                st.rerun()
        with col3:
            if st.button("💼 Professionnel", use_container_width=True,
                        type="primary" if st.session_state.niveau_utilisateur == "Professionnel" else "secondary"):
                st.session_state.niveau_utilisateur = "Professionnel"
                st.rerun()
        st.markdown(f"**Niveau actuel : {st.session_state.niveau_utilisateur}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Menu principal selon l'étape
        if st.session_state.etape == "menu":
            st.markdown("---")
            st.markdown("### Choisis une activité :")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💬 Conversation", use_container_width=True):
                    st.session_state.etape = "conversation"
                    st.rerun()
            with col2:
                if st.button("📚 Vocabulaire", use_container_width=True):
                    st.session_state.etape = "vocabulaire"
                    st.session_state.nb_quiz = 0
                    st.session_state.question_quiz = None
                    st.rerun()
            with col3:
                if st.button("📖 Leçon", use_container_width=True):
                    st.session_state.etape = "lecon"
                    st.rerun()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔤 Verbes", use_container_width=True):
                    st.session_state.etape = "verbes"
                    st.session_state.verbe_quiz = None
                    st.rerun()
            with col2:
                if st.button("💬 Phrase", use_container_width=True):
                    st.session_state.etape = "phrase"
                    st.rerun()
        
        elif st.session_state.etape == "conversation":
            st.markdown("## 💬 Conversation")
            for msg in st.session_state.historique[-10:]:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-message">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
            
            with st.form(key="chat", clear_on_submit=True):
                user_input = st.text_input("Ton message :")
                if st.form_submit_button("Envoyer") and user_input:
                    st.session_state.historique.append({"role": "user", "content": user_input})
                    st.session_state.historique.append({"role": "bot", "content": get_bot_reponse(user_input)})
                    ajouter_point()
                    st.rerun()
            
            if st.button("🔙 Retour"):
                st.session_state.etape = "menu"
                st.rerun()
        
        elif st.session_state.etape == "vocabulaire":
            st.markdown(f"## 📚 Vocabulaire ({st.session_state.niveau_utilisateur})")
            
            if st.session_state.question_quiz is None:
                fr, en = nouvelle_question_quiz()
                st.session_state.question_quiz = fr
                st.session_state.reponse_quiz = en
                st.session_state.nb_quiz += 1
            
            st.markdown(f"**Question {st.session_state.nb_quiz} :** Comment dit-on **'{st.session_state.question_quiz}'** ?")
            
            with st.form(key="quiz", clear_on_submit=True):
                reponse = st.text_input("Ta réponse :")
                if st.form_submit_button("Vérifier") and reponse:
                    if reponse.lower().strip() == st.session_state.reponse_quiz.lower():
                        st.success("✅ Correct !")
                        ajouter_point()
                    else:
                        st.error(f"❌ Réponse : {st.session_state.reponse_quiz}")
                    st.session_state.question_quiz = None
                    time.sleep(1.5)
                    st.rerun()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔁 Suivant", use_container_width=True):
                    st.session_state.question_quiz = None
                    st.rerun()
            with col2:
                if st.button("🔙 Retour", use_container_width=True):
                    st.session_state.etape = "menu"
                    st.rerun()
        
        elif st.session_state.etape == "lecon":
            st.markdown("## 📖 Leçon du jour")
            jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
            today = jours[date.today().weekday()]
            st.info(lecons_journalieres[today])
            
            if st.button("🔙 Retour"):
                st.session_state.etape = "menu"
                st.rerun()
        
        elif st.session_state.etape == "verbes":
            st.markdown("## 🔤 Verbes irréguliers")
            if "verbe_quiz" not in st.session_state or st.session_state.verbe_quiz is None:
                v = random.choice(verbes_irreguliers)
                mode = random.choice(["base", "preterit", "participe"])
                if mode == "base":
                    st.session_state.verbe_quiz = (f"Base de '{v['francais']}' ?", v['base'])
                elif mode == "preterit":
                    st.session_state.verbe_quiz = (f"Prétérit de '{v['base']}' ?", v['preterit'])
                else:
                    st.session_state.verbe_quiz = (f"Participe de '{v['base']}' ?", v['participe'])
            
            question, reponse = st.session_state.verbe_quiz
            st.markdown(f"**{question}**")
            
            with st.form(key="verbe", clear_on_submit=True):
                user = st.text_input("Ta réponse :")
                if st.form_submit_button("Vérifier") and user:
                    if user.lower().strip() == reponse.lower():
                        st.success("✅ Correct !")
                        ajouter_point()
                    else:
                        st.error(f"❌ Réponse : {reponse}")
                    st.session_state.verbe_quiz = None
                    time.sleep(1.5)
                    st.rerun()
            
            if st.button("🔙 Retour"):
                st.session_state.etape = "menu"
                st.rerun()
        
        elif st.session_state.etape == "phrase":
            st.markdown("## 💬 Phrase du jour")
            phrase = random.choice(phrases_du_jour)
            st.info(f"**Français :** {phrase['francais']}")
            st.markdown(f"**Anglais :** {phrase['anglais']}")
            
            if st.button("🔙 Retour"):
                st.session_state.etape = "menu"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown('<div class="footer">✨ English Buddy ++ – Created by <strong>Krakendeveloppement</strong> – 20€/an</div>', 
                unsafe_allow_html=True)

# -------------------------------
# POINT D'ENTRÉE PRINCIPAL
# -------------------------------
if st.session_state.user is None:
    auth_page()
else:
    main_app()

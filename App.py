import streamlit as st
import random
import time
import re
from datetime import date
import hashlib
import json
from pathlib import Path

# -------------------------------
# CONFIGURATION DE LA PAGE
# -------------------------------
st.set_page_config(
    page_title="English Buddy - Krakendeveloppement",
    page_icon="🇬🇧",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------
# GESTION DES UTILISATEURS
# -------------------------------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"
PROGRESS_FILE = DATA_DIR / "progress.json"

def hash_password(password):
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

# -------------------------------
# SESSION STATE INITIAL
# -------------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "etape" not in st.session_state:
    st.session_state.etape = "menu"
if "score" not in st.session_state:
    st.session_state.score = 0
if "niveau_app" not in st.session_state:
    st.session_state.niveau_app = 1
if "historique_conv" not in st.session_state:
    st.session_state.historique_conv = []
if "niveau_utilisateur" not in st.session_state:
    st.session_state.niveau_utilisateur = "Débutant"
if "derniers_mots" not in st.session_state:
    st.session_state.derniers_mots = []
if "essais_phrase" not in st.session_state:
    st.session_state.essais_phrase = 0
if "phrase_courante" not in st.session_state:
    st.session_state.phrase_courante = None
if "qcm_verbe" not in st.session_state:
    st.session_state.qcm_verbe = None
if "mot_prononciation" not in st.session_state:
    st.session_state.mot_prononciation = random.choice([
        "hello", "world", "apple", "banana", "computer", "language", "practice",
        "pronunciation", "speak", "listen", "learn", "english", "friend", "family",
        "weather", "coffee", "restaurant", "beautiful", "interesting", "development"
    ])

# -------------------------------
# CSS PERSONNALISÉ
# -------------------------------
st.markdown("""
<style>
    :root {
        --bg-gradient-light: linear-gradient(145deg, #f9f3e8 0%, #ffe6d5 100%);
        --bg-gradient-dark: linear-gradient(145deg, #2b2b2b 0%, #1a2634 100%);
        --text-light: #2c3e50;
        --text-dark: #ecf0f1;
        --card-light: rgba(255, 255, 255, 0.7);
        --card-dark: rgba(30, 30, 30, 0.7);
        --accent: #ff7f50;
        --accent-hover: #ff6347;
    }

    @media (prefers-color-scheme: light) {
        .stApp {
            background: var(--bg-gradient-light);
            color: var(--text-light);
        }
        .card, .stButton button, .stTextInput input {
            background-color: var(--card-light);
            backdrop-filter: blur(5px);
            color: var(--text-light);
        }
    }

    @media (prefers-color-scheme: dark) {
        .stApp {
            background: var(--bg-gradient-dark);
            color: var(--text-dark);
        }
        .card, .stButton button, .stTextInput input {
            background-color: var(--card-dark);
            backdrop-filter: blur(5px);
            color: var(--text-dark);
        }
        .stButton button {
            border: 1px solid #555;
        }
    }

    .stButton button {
        border-radius: 30px;
        font-weight: bold;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        background-color: var(--accent-hover) !important;
        color: white !important;
    }
    .title {
        text-align: center;
        font-size: 3em;
        color: var(--accent);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 30px;
        opacity: 0.9;
    }
    .card {
        border-radius: 25px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
    }
    .bot-message {
        background-color: rgba(255,127,80,0.2);
        border-radius: 25px 25px 25px 5px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid var(--accent);
    }
    .user-message {
        background-color: rgba(100,149,237,0.2);
        border-radius: 25px 25px 5px 25px;
        padding: 15px;
        margin: 10px 0;
        text-align: right;
        border-right: 5px solid #6495ed;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 0.9em;
        opacity: 0.7;
    }
    .level-selector button {
        font-size: 1.2em !important;
    }
    .pronunciation-box {
        text-align: center;
        padding: 30px;
        font-size: 2em;
        border: 3px dashed var(--accent);
        border-radius: 50px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# BASES DE DONNÉES ENRICHIES
# -------------------------------

# (Les dictionnaires de vocabulaire, verbes, phrases, etc. sont inchangés, je les reprends du code précédent)
vocabulaire_debutant = { ... }  # Pour la concision, je ne réécris pas tout, mais dans le code final il faut les inclure
vocabulaire_intermediaire = { ... }
vocabulaire_professionnel = { ... }
vocabulaire_par_niveau = { ... }
verbes_irreguliers = [ ... ]
phrases_du_jour = [ ... ]
reponses_bot = { ... }
lecons_journalieres = { ... }
mots_prononciation = [ ... ]

# -------------------------------
# FONCTIONS UTILITAIRES
# -------------------------------

def get_bot_reponse(message):
    # ... (identique)
    pass

def ajouter_point():
    st.session_state.score += 1
    if st.session_state.score % 5 == 0:
        st.session_state.niveau_app += 1
        st.balloons()
    if st.session_state.user:
        progress = load_progress()
        email = st.session_state.user["email"]
        if email not in progress:
            progress[email] = {"score": 0, "niveau": 1}
        progress[email]["score"] = st.session_state.score
        progress[email]["niveau"] = st.session_state.niveau_app
        save_progress(progress)

def nouvelle_question_quiz():
    vocab = vocabulaire_par_niveau[st.session_state.niveau_utilisateur]
    disponibles = [(fr, en) for fr, en in vocab.items() if fr not in st.session_state.derniers_mots]
    if not disponibles:
        disponibles = list(vocab.items())
        st.session_state.derniers_mots = []
    fr, en = random.choice(disponibles)
    st.session_state.derniers_mots.append(fr)
    if len(st.session_state.derniers_mots) > 15:
        st.session_state.derniers_mots.pop(0)
    return fr, en

def generer_qcm_verbe():
    # ... (identique)
    pass

# -------------------------------
# PAGE D'AUTHENTIFICATION
# -------------------------------
def auth_page():
    st.markdown('<h1 class="title">🇬🇧 English Buddy ++</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Created by <strong>Krakendeveloppement</strong></p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
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
                    progress = load_progress()
                    if email in progress:
                        st.session_state.score = progress[email]["score"]
                        st.session_state.niveau_app = progress[email]["niveau"]
                    st.success("Connexion réussie !")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Email ou mot de passe incorrect")
        else:
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
# COMPOSANT DE PRONONCIATION AVEC REDIRECTION AUTOMATIQUE
# -------------------------------
def pronunciation_component(word):
    """Génère le HTML pour la prononciation avec redirection auto en cas de succès"""
    html_code = f"""
    <div style="text-align:center; padding:20px;">
        <div style="font-size:3em; margin-bottom:20px;">🔊 {word}</div>
        <button id="speak" style="font-size:1.5em; padding:10px 30px; border-radius:50px; background-color:#ff7f50; color:white; border:none; margin:10px; cursor:pointer;">🔊 Écouter</button>
        <button id="listen" style="font-size:1.5em; padding:10px 30px; border-radius:50px; background-color:#6495ed; color:white; border:none; margin:10px; cursor:pointer;">🎤 Prononcer</button>
        <div id="result" style="font-size:1.2em; margin-top:20px;"></div>
    </div>
    <script>
        const word = "{word}";
        const speakBtn = document.getElementById('speak');
        const listenBtn = document.getElementById('listen');
        const resultDiv = document.getElementById('result');
        
        speakBtn.addEventListener('click', function() {{
            const utterance = new SpeechSynthesisUtterance(word);
            utterance.lang = 'en-US';
            window.speechSynthesis.speak(utterance);
        }});
        
        listenBtn.addEventListener('click', function() {{
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            
            resultDiv.innerHTML = '🎤 Écoute... Parle maintenant.';
            recognition.start();
            
            recognition.onresult = function(event) {{
                const spoken = event.results[0][0].transcript.trim().toLowerCase();
                const expected = word.toLowerCase();
                const isCorrect = (spoken === expected) || (spoken.includes(expected) && expected.length > 3);
                
                if (isCorrect) {{
                    resultDiv.innerHTML = '✅ Parfait ! Passage au mot suivant...';
                    // Redirection avec paramètre pour indiquer le succès
                    setTimeout(() => {{
                        window.location.href = window.location.href.split('?')[0] + '?pronounce_success=true';
                    }}, 1500);
                }} else {{
                    resultDiv.innerHTML = '❌ Pas tout à fait. Essaie encore. (Tu as dit: "' + spoken + '")';
                }}
            }};
            
            recognition.onerror = function(event) {{
                resultDiv.innerHTML = 'Erreur: ' + event.error;
            }};
        }});
    </script>
    """
    return html_code

# -------------------------------
# APPLICATION PRINCIPALE
# -------------------------------
def main_app():
    # En-tête
    st.markdown('<h1 class="title">🇬🇧 English Buddy ++</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Created by <strong>Krakendeveloppement</strong></p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user['email']}")
        st.metric("Score", st.session_state.score)
        st.metric("Niveau global", st.session_state.niveau_app)
        st.markdown("---")
        st.markdown("**Niveau d'apprentissage**")
        niveaux = ["Débutant", "Intermédiaire", "Professionnel"]
        for niv in niveaux:
            if st.button(niv, use_container_width=True, 
                         type="primary" if st.session_state.niveau_utilisateur == niv else "secondary"):
                st.session_state.niveau_utilisateur = niv
                st.rerun()
        st.markdown("---")
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    # Contenu principal
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Sélecteur d'activité
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            if st.button("💬 Conv", use_container_width=True):
                st.session_state.etape = "conversation"
                st.rerun()
        with col2:
            if st.button("📚 Vocab", use_container_width=True):
                st.session_state.etape = "vocabulaire"
                st.session_state.nb_quiz = 0
                st.session_state.question_quiz = None
                st.rerun()
        with col3:
            if st.button("🔤 Verbes", use_container_width=True):
                st.session_state.etape = "verbes"
                st.session_state.qcm_verbe = None
                st.rerun()
        with col4:
            if st.button("💬 Phrase", use_container_width=True):
                st.session_state.etape = "phrase"
                st.session_state.essais_phrase = 0
                st.session_state.phrase_courante = random.choice(phrases_du_jour)
                st.rerun()
        with col5:
            if st.button("🗣 Pronon", use_container_width=True):
                st.session_state.etape = "prononciation"
                st.rerun()
        
        st.markdown("---")
        
        # Gestion de la redirection pour prononciation
        if "pronounce_success" in st.query_params:
            # Changer de mot et supprimer le paramètre
            st.session_state.mot_prononciation = random.choice(mots_prononciation)
            st.query_params.clear()  # Efface tous les paramètres
            st.rerun()
        
        # Affichage selon l'étape
        if st.session_state.etape == "conversation":
            st.markdown("## 💬 Conversation")
            for msg in st.session_state.historique_conv[-20:]:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-message">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
            
            with st.form(key="chat_form", clear_on_submit=True):
                user_input = st.text_input("Écris ton message :", placeholder="Pose une question ou parle en anglais...")
                if st.form_submit_button("Envoyer") and user_input:
                    st.session_state.historique_conv.append({"role": "user", "content": user_input})
                    bot_reponse = get_bot_reponse(user_input)
                    st.session_state.historique_conv.append({"role": "bot", "content": bot_reponse})
                    ajouter_point()
                    st.rerun()
            
            if st.button("🔙 Retour au menu"):
                st.session_state.etape = "menu"
                st.rerun()
        
        elif st.session_state.etape == "vocabulaire":
            st.markdown(f"## 📚 Vocabulaire - {st.session_state.niveau_utilisateur}")
            
            if st.session_state.question_quiz is None:
                fr, en = nouvelle_question_quiz()
                st.session_state.question_quiz = fr
                st.session_state.reponse_quiz = en
                st.session_state.nb_quiz = st.session_state.get("nb_quiz", 0) + 1
            
            st.markdown(f"**Question {st.session_state.nb_quiz} :** Comment dit-on **'{st.session_state.question_quiz}'** en anglais ?")
            
            with st.form(key="quiz_form", clear_on_submit=True):
                reponse = st.text_input("Ta réponse :")
                if st.form_submit_button("Vérifier") and reponse:
                    if reponse.strip().lower() == st.session_state.reponse_quiz.lower():
                        st.success("✅ Bonne réponse !")
                        ajouter_point()
                    else:
                        st.error(f"❌ La réponse était : **{st.session_state.reponse_quiz}**")
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
        
        elif st.session_state.etape == "verbes":
            st.markdown("## 🔤 Verbes irréguliers (QCM)")
            
            if st.session_state.qcm_verbe is None:
                question, bonne, options = generer_qcm_verbe()
                st.session_state.qcm_verbe = {
                    "question": question,
                    "bonne": bonne,
                    "options": options
                }
            
            qcm = st.session_state.qcm_verbe
            st.markdown(f"**{qcm['question']}**")
            
            cols = st.columns(2)
            for i, opt in enumerate(qcm['options']):
                with cols[i % 2]:
                    if st.button(opt, use_container_width=True, key=f"verbe_{i}"):
                        if opt == qcm['bonne']:
                            st.success("✅ Correct !")
                            ajouter_point()
                        else:
                            st.error(f"❌ Non. La bonne réponse était : {qcm['bonne']}")
                        st.session_state.qcm_verbe = None
                        time.sleep(1.5)
                        st.rerun()
            
            if st.button("🔙 Retour au menu"):
                st.session_state.etape = "menu"
                st.rerun()
        
        elif st.session_state.etape == "phrase":
            st.markdown("## 💬 Phrase du jour")
            phrase = st.session_state.phrase_courante
            
            st.markdown(f"**Français :** {phrase['francais']}")
            st.markdown(f"*Essais restants : {3 - st.session_state.essais_phrase}*")
            
            with st.form(key="phrase_form", clear_on_submit=True):
                trad = st.text_input("Ta traduction en anglais :")
                if st.form_submit_button("Vérifier"):
                    if trad.strip().lower() == phrase['anglais'].lower():
                        st.success("✅ Parfait !")
                        ajouter_point()
                        st.session_state.essais_phrase = 0
                        st.session_state.phrase_courante = random.choice(phrases_du_jour)
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.session_state.essais_phrase += 1
                        if st.session_state.essais_phrase >= 3:
                            st.error(f"La bonne traduction était : **{phrase['anglais']}**")
                            st.session_state.essais_phrase = 0
                            st.session_state.phrase_courante = random.choice(phrases_du_jour)
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.warning(f"Ce n'est pas correct. Essaie encore ! ({3 - st.session_state.essais_phrase} essais restants)")
            
            if st.button("🔙 Retour au menu"):
                st.session_state.etape = "menu"
                st.rerun()
        
        elif st.session_state.etape == "prononciation":
            st.markdown("## 🗣 Prononciation")
            st.markdown("Clique sur **Écouter** pour entendre le mot, puis sur **Prononcer** pour t'enregistrer.")
            
            mot = st.session_state.mot_prononciation
            st.markdown(f"<div class='pronunciation-box'>🔊 {mot}</div>", unsafe_allow_html=True)
            
            # Intégration du composant HTML
            st.components.v1.html(pronunciation_component(mot), height=350)
            
            if st.button("🔙 Retour"):
                st.session_state.etape = "menu"
                st.rerun()
        
        else:  # menu
            st.markdown("### Bienvenue ! Choisis une activité ci-dessus.")
            st.markdown("""
            - **💬 Conversation** : Discute avec le bot en anglais.
            - **📚 Vocabulaire** : Apprends de nouveaux mots avec des quiz.
            - **🔤 Verbes** : Entraîne-toi sur les verbes irréguliers (QCM).
            - **💬 Phrase** : Traduis une phrase française en anglais (3 essais).
            - **🗣 Prononciation** : Écoute et répète des mots pour améliorer ton accent (passe automatiquement au suivant si réussi).
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="footer">✨ English Buddy ++ – Created by <strong>Krakendeveloppement</strong></div>', unsafe_allow_html=True)

# -------------------------------
# LANCEMENT
# -------------------------------
if st.session_state.user is None:
    auth_page()
else:
    main_app()

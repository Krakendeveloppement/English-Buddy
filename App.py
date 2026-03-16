import streamlit as st
import random
from datetime import date
import time

# -------------------------------
# CONFIGURATION DE LA PAGE
# -------------------------------
st.set_page_config(
    page_title="English Buddy by Krakendeveloppement",
    page_icon="🇬🇧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# CSS PERSONNALISÉ (adaptatif clair/sombre)
# -------------------------------
st.markdown("""
<style>
    /* Variables pour les deux thèmes */
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
    }

    /* Adaptation au mode sombre */
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
        }
    }

    /* Style global */
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
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

    /* Zone de texte */
    .stTextInput input {
        font-size: 1.1em;
        padding: 12px;
        border-radius: 12px;
        border: 2px solid var(--accent-color);
        background-color: var(--bg-secondary);
        color: var(--text-primary);
    }

    /* Messages du bot */
    .bot-message {
        background-color: var(--bot-message-bg);
        color: var(--text-primary);
        border-radius: 20px 20px 20px 5px;
        padding: 15px;
        margin: 10px 0;
        font-size: 1.1em;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(5px);
    }

    /* Messages de l'utilisateur */
    .user-message {
        background-color: var(--user-message-bg);
        color: var(--text-primary);
        border-radius: 20px 20px 5px 20px;
        padding: 12px 18px;
        margin: 5px 0;
        text-align: right;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(5px);
    }

    /* Titre principal */
    .title {
        text-align: center;
        font-size: 2.5em;
        color: var(--accent-color);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 5px;
    }

    /* Sous-titre (created by) */
    .subtitle {
        text-align: center;
        font-size: 1.1em;
        color: var(--text-secondary);
        margin-top: 0;
        margin-bottom: 20px;
    }

    /* Pied de page */
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 15px;
        font-size: 0.95em;
        color: var(--text-secondary);
        border-top: 1px solid var(--border-color);
    }

    /* Cartes de menu */
    .menu-card {
        background-color: var(--bg-secondary);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Grille des boutons du menu principal */
    .menu-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin: 20px 0;
    }

    /* Style des métriques (score) */
    .stMetric {
        background-color: var(--bg-secondary);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid var(--border-color);
    }
    .stMetric label {
        color: var(--text-secondary) !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: var(--accent-color) !important;
        font-size: 2em !important;
    }

    /* Sidebar */
    .css-1d391kg, .css-12oz5g7 {
        background-color: var(--bg-secondary);
    }

    /* Messages d'info/success/error */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid var(--accent-color);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# DONNÉES ÉLARGIES
# -------------------------------

# Vocabulaire français -> anglais (200+ mots)
vocabulaire = {
    "bonjour": "hello", "merci": "thank you", "au revoir": "goodbye", "maison": "house",
    "voiture": "car", "chien": "dog", "chat": "cat", "manger": "eat", "boire": "drink",
    "dormir": "sleep", "aimer": "love", "parler": "speak", "travail": "work", "école": "school",
    "livre": "book", "stylo": "pen", "table": "table", "chaise": "chair", "porte": "door",
    "fenêtre": "window", "soleil": "sun", "lune": "moon", "étoile": "star", "ciel": "sky",
    "eau": "water", "feu": "fire", "terre": "earth", "air": "air", "grand": "big",
    "petit": "small", "chaud": "hot", "froid": "cold", "content": "happy", "triste": "sad",
    "vite": "fast", "lent": "slow", "maintenant": "now", "plus tard": "later", "jour": "day",
    "nuit": "night", "semaine": "week", "mois": "month", "année": "year", "aujourd'hui": "today",
    "demain": "tomorrow", "hier": "yesterday", "homme": "man", "femme": "woman", "enfant": "child",
    "père": "father", "mère": "mother", "frère": "brother", "sœur": "sister", "ami": "friend",
    "école": "school", "université": "university", "professeur": "teacher", "étudiant": "student",
    "livre": "book", "cahier": "notebook", "ordinateur": "computer", "téléphone": "phone",
    "voiture": "car", "bus": "bus", "train": "train", "avion": "plane", "bateau": "boat",
    "ville": "city", "campagne": "countryside", "mer": "sea", "montagne": "mountain", "forêt": "forest",
    "animal": "animal", "oiseau": "bird", "poisson": "fish", "cheval": "horse", "vache": "cow",
    "cochon": "pig", "poulet": "chicken", "mouton": "sheep", "lion": "lion", "tigre": "tiger",
    "éléphant": "elephant", "girafe": "giraffe", "singe": "monkey", "serpent": "snake",
    "fleur": "flower", "arbre": "tree", "herbe": "grass", "feuille": "leaf", "pomme": "apple",
    "banane": "banana", "orange": "orange", "fraise": "strawberry", "raisin": "grape",
    "pain": "bread", "fromage": "cheese", "lait": "milk", "œuf": "egg", "viande": "meat",
    "poisson": "fish", "riz": "rice", "pâtes": "pasta", "soupe": "soup", "salade": "salad",
    "café": "coffee", "thé": "tea", "jus": "juice", "bière": "beer", "vin": "wine",
    "vêtement": "clothes", "chemise": "shirt", "pantalon": "pants", "chaussure": "shoe",
    "chaussette": "sock", "chapeau": "hat", "manteau": "coat", "robe": "dress", "jupe": "skirt",
    "couleur": "color", "rouge": "red", "bleu": "blue", "vert": "green", "jaune": "yellow",
    "noir": "black", "blanc": "white", "gris": "gray", "marron": "brown", "rose": "pink",
    "orange": "orange", "violet": "purple"
}

# Verbes irréguliers (base, prétérit, participe passé)
verbes_irreguliers = [
    {"base": "be", "preterit": "was/were", "participe": "been", "francais": "être"},
    {"base": "have", "preterit": "had", "participe": "had", "francais": "avoir"},
    {"base": "do", "preterit": "did", "participe": "done", "francais": "faire"},
    {"base": "say", "preterit": "said", "participe": "said", "francais": "dire"},
    {"base": "go", "preterit": "went", "participe": "gone", "francais": "aller"},
    {"base": "get", "preterit": "got", "participe": "gotten", "francais": "obtenir"},
    {"base": "make", "preterit": "made", "participe": "made", "francais": "fabriquer"},
    {"base": "know", "preterit": "knew", "participe": "known", "francais": "savoir"},
    {"base": "think", "preterit": "thought", "participe": "thought", "francais": "penser"},
    {"base": "take", "preterit": "took", "participe": "taken", "francais": "prendre"},
    {"base": "see", "preterit": "saw", "participe": "seen", "francais": "voir"},
    {"base": "come", "preterit": "came", "participe": "come", "francais": "venir"},
    {"base": "want", "preterit": "wanted", "participe": "wanted", "francais": "vouloir"},
    {"base": "give", "preterit": "gave", "participe": "given", "francais": "donner"},
    {"base": "find", "preterit": "found", "participe": "found", "francais": "trouver"},
    {"base": "eat", "preterit": "ate", "participe": "eaten", "francais": "manger"},
    {"base": "drink", "preterit": "drank", "participe": "drunk", "francais": "boire"},
    {"base": "sleep", "preterit": "slept", "participe": "slept", "francais": "dormir"},
    {"base": "run", "preterit": "ran", "participe": "run", "francais": "courir"},
    {"base": "swim", "preterit": "swam", "participe": "swum", "francais": "nager"}
]

# Phrases du jour (thèmes variés)
phrases_du_jour = [
    {"francais": "Quel temps fait-il aujourd'hui ?", "anglais": "What's the weather like today?"},
    {"francais": "Je voudrais un café, s'il vous plaît.", "anglais": "I would like a coffee, please."},
    {"francais": "Où se trouve la gare ?", "anglais": "Where is the train station?"},
    {"francais": "Combien ça coûte ?", "anglais": "How much does it cost?"},
    {"francais": "Pouvez-vous m'aider ?", "anglais": "Can you help me?"},
    {"francais": "Je suis perdu.", "anglais": "I am lost."},
    {"francais": "Parlez-vous anglais ?", "anglais": "Do you speak English?"},
    {"francais": "Je m'appelle...", "anglais": "My name is..."},
    {"francais": "Enchanté.", "anglais": "Nice to meet you."},
    {"francais": "À plus tard.", "anglais": "See you later."}
]

# Réponses du bot (conversation)
reponses_bot = {
    "salutation": [
        "Hello! How are you today?",
        "Hi there! Nice to see you.",
        "Hey! Ready to practice English?"
    ],
    "forme": [
        "I'm doing great, thanks!",
        "I'm fine, just a bot but happy to help.",
        "All systems operational! 😊"
    ],
    "remerciement": [
        "You're welcome!",
        "My pleasure!",
        "Anytime!"
    ],
    "au_revoir": [
        "Goodbye! Come back soon!",
        "See you later! Keep practicing.",
        "Bye! Have a great day!"
    ],
    "inconnu": [
        "I didn't understand. Can you rephrase?",
        "Hmm, I'm not sure. Try something simpler!",
        "I'm still learning. Could you ask differently?"
    ],
    "encouragement": [
        "Great job!",
        "Excellent!",
        "Well done!",
        "Perfect!",
        "You're making progress!"
    ]
}

# Leçons du jour (grammaire)
lecons_journalieres = {
    "lundi": "📘 **Present Simple** – I eat, you eat, he eats.",
    "mardi": "📙 **Past Simple** – I ate, you ate, he ate.",
    "mercredi": "📕 **Future with 'will'** – I will eat, you will eat.",
    "jeudi": "📗 **Prepositions** – in, on, at.",
    "vendredi": "📓 **Modal verbs** – can, must, should.",
    "samedi": "📔 **Adjectives** – big, small, happy, sad.",
    "dimanche": "📒 **Adverbs** – quickly, slowly, well."
}

# Mots pour le jeu du pendu
mots_pendu = ["hello", "world", "python", "english", "learn", "computer", "mobile", "language", "practice", "friend"]

# -------------------------------
# SESSION STATE
# -------------------------------
if "etape" not in st.session_state:
    st.session_state.etape = "menu"
if "score" not in st.session_state:
    st.session_state.score = 0
if "niveau" not in st.session_state:
    st.session_state.niveau = 1
if "historique" not in st.session_state:
    st.session_state.historique = []
if "question_quiz" not in st.session_state:
    st.session_state.question_quiz = None
if "reponse_quiz" not in st.session_state:
    st.session_state.reponse_quiz = None
if "nb_quiz" not in st.session_state:
    st.session_state.nb_quiz = 0
if "verbe_quiz" not in st.session_state:
    st.session_state.verbe_quiz = None
if "phrase_jour" not in st.session_state:
    st.session_state.phrase_jour = None
if "pendu_mot" not in st.session_state:
    st.session_state.pendu_mot = ""
if "pendu_lettres_trouvees" not in st.session_state:
    st.session_state.pendu_lettres_trouvees = []
if "pendu_essais" not in st.session_state:
    st.session_state.pendu_essais = 0
if "pendu_max_essais" not in st.session_state:
    st.session_state.pendu_max_essais = 6

# -------------------------------
# FONCTIONS UTILITAIRES
# -------------------------------

def get_bot_reponse(message_user):
    msg = message_user.lower()
    if any(greeting in msg for greeting in ["hello", "hi", "hey", "bonjour", "salut"]):
        return random.choice(reponses_bot["salutation"])
    elif any(feeling in msg for feeling in ["how are you", "ça va", "comment"]):
        return random.choice(reponses_bot["forme"])
    elif any(thanks in msg for thanks in ["merci", "thanks", "thank you"]):
        return random.choice(reponses_bot["remerciement"])
    elif any(bye in msg for bye in ["bye", "au revoir", "à bientôt", "goodbye"]):
        return random.choice(reponses_bot["au_revoir"])
    else:
        if random.random() < 0.3:
            return random.choice(reponses_bot["encouragement"]) + " " + random.choice(reponses_bot["inconnu"])
        return random.choice(reponses_bot["inconnu"])

def ajouter_point():
    st.session_state.score += 1
    if st.session_state.score % 5 == 0:
        st.session_state.niveau += 1
        st.balloons()

def nouvelle_question_quiz():
    mot_fr, mot_en = random.choice(list(vocabulaire.items()))
    return mot_fr, mot_en

def nouveau_verbe_quiz():
    verbe = random.choice(verbes_irreguliers)
    mode = random.choice(["base", "preterit", "participe"])
    question = ""
    reponse = ""
    if mode == "base":
        question = f"Quel est le verbe de base pour '{verbe['francais']}' ?"
        reponse = verbe['base']
    elif mode == "preterit":
        question = f"Quel est le prétérit de '{verbe['base']}' ({verbe['francais']}) ?"
        reponse = verbe['preterit']
    else:
        question = f"Quel est le participe passé de '{verbe['base']}' ({verbe['francais']}) ?"
        reponse = verbe['participe']
    return question, reponse

def nouvelle_phrase():
    return random.choice(phrases_du_jour)

def nouveau_pendu():
    mot = random.choice(mots_pendu)
    return mot.lower(), [], 0

# -------------------------------
# INTERFACE PRINCIPALE
# -------------------------------

st.markdown('<h1 class="title">🇬🇧 English Buddy ++</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Created by <strong>Krakendeveloppement</strong></p>', unsafe_allow_html=True)

# Sidebar avec progression et menu
with st.sidebar:
    st.header("📊 Ta progression")
    st.metric("Score", st.session_state.score)
    st.metric("Niveau", st.session_state.niveau)
    st.markdown("---")
    st.markdown("**Menu principal**")
    if st.button("🏠 Accueil", use_container_width=True):
        st.session_state.etape = "menu"
    if st.button("💬 Conversation", use_container_width=True):
        st.session_state.etape = "conversation"
    if st.button("📚 Vocabulaire", use_container_width=True):
        st.session_state.etape = "vocabulaire"
        st.session_state.nb_quiz = 0
        st.session_state.question_quiz = None
    if st.button("🔤 Verbes irréguliers", use_container_width=True):
        st.session_state.etape = "verbes"
        st.session_state.verbe_quiz = None
    if st.button("💬 Phrase du jour", use_container_width=True):
        st.session_state.etape = "phrase"
        st.session_state.phrase_jour = nouvelle_phrase()
    if st.button("🎮 Jeu du pendu", use_container_width=True):
        st.session_state.etape = "pendu"
        mot, lettres, essais = nouveau_pendu()
        st.session_state.pendu_mot = mot
        st.session_state.pendu_lettres_trouvees = lettres
        st.session_state.pendu_essais = essais
    if st.button("📖 Leçon du jour", use_container_width=True):
        st.session_state.etape = "lecon"
    st.markdown("---")
    st.markdown("Partage cette app avec tes amis ! 📲")

# -------------------------------
# ÉCRAN MENU (amélioré)
# -------------------------------
if st.session_state.etape == "menu":
    st.markdown("""
    <div class="menu-card">
        <h3 style="text-align:center; margin-top:0;">Bienvenue sur English Buddy ++</h3>
        <p style="text-align:center;">Choisis une activité pour commencer :</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grille de boutons 3x2
    st.markdown('<div class="menu-grid">', unsafe_allow_html=True)
    
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
    
    # Deuxième ligne
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔤 Verbes", use_container_width=True):
            st.session_state.etape = "verbes"
            st.session_state.verbe_quiz = None
            st.rerun()
    with col2:
        if st.button("💬 Phrase", use_container_width=True):
            st.session_state.etape = "phrase"
            st.session_state.phrase_jour = nouvelle_phrase()
            st.rerun()
    with col3:
        if st.button("🎮 Pendu", use_container_width=True):
            st.session_state.etape = "pendu"
            mot, lettres, essais = nouveau_pendu()
            st.session_state.pendu_mot = mot
            st.session_state.pendu_lettres_trouvees = lettres
            st.session_state.pendu_essais = essais
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Message d'encouragement
    st.markdown("""
    <div style="text-align:center; margin-top:20px; padding:15px; background-color:var(--bg-secondary); border-radius:15px; border:1px solid var(--border-color);">
        Plus tu pratiques, plus ton score augmente ! 🚀<br>
        <span style="font-size:0.9em;">Partage cette app avec tes amis ! 📲</span>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# MODE CONVERSATION
# -------------------------------
elif st.session_state.etape == "conversation":
    st.markdown("## 💬 Mode Conversation")
    st.markdown("Pose-moi des questions ou parle-moi en anglais. Je te répondrai !")
    
    # Afficher l'historique
    for msg in st.session_state.historique[-10:]:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message">🧑 <strong>Toi :</strong> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">🤖 <strong>Bot :</strong> {msg["content"]}</div>', unsafe_allow_html=True)
    
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Écris ton message :", placeholder="Ex: Hello, how are you?")
        submitted = st.form_submit_button("Envoyer")
        if submitted and user_input:
            st.session_state.historique.append({"role": "user", "content": user_input})
            bot_reponse = get_bot_reponse(user_input)
            st.session_state.historique.append({"role": "bot", "content": bot_reponse})
            ajouter_point()
            st.rerun()
    
    if st.button("🔙 Retour au menu"):
        st.session_state.etape = "menu"
        st.rerun()

# -------------------------------
# MODE VOCABULAIRE
# -------------------------------
elif st.session_state.etape == "vocabulaire":
    st.markdown("## 📚 Mode Vocabulaire")
    st.markdown("Traduis les mots du français à l'anglais.")
    
    if st.session_state.question_quiz is None:
        fr, en = nouvelle_question_quiz()
        st.session_state.question_quiz = fr
        st.session_state.reponse_quiz = en
        st.session_state.nb_quiz += 1
    
    st.markdown(f"**Question {st.session_state.nb_quiz} :** Comment dit-on **'{st.session_state.question_quiz}'** en anglais ?")
    
    with st.form(key="quiz_form", clear_on_submit=True):
        reponse_user = st.text_input("Ta réponse :")
        submitted = st.form_submit_button("Vérifier")
        if submitted and reponse_user:
            if reponse_user.strip().lower() == st.session_state.reponse_quiz.lower():
                st.success("✅ Bonne réponse !")
                ajouter_point()
            else:
                st.error(f"❌ La réponse était : **{st.session_state.reponse_quiz}**")
            st.session_state.question_quiz = None
            time.sleep(1.5)
            st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Nouvelle question", use_container_width=True):
            st.session_state.question_quiz = None
            st.rerun()
    with col2:
        if st.button("🔙 Retour", use_container_width=True):
            st.session_state.etape = "menu"
            st.session_state.question_quiz = None
            st.rerun()

# -------------------------------
# MODE VERBES IRREGULIERS
# -------------------------------
elif st.session_state.etape == "verbes":
    st.markdown("## 🔤 Verbes irréguliers")
    st.markdown("Teste tes connaissances sur les verbes irréguliers.")
    
    if st.session_state.verbe_quiz is None:
        question, reponse = nouveau_verbe_quiz()
        st.session_state.verbe_quiz = (question, reponse)
    
    question, reponse = st.session_state.verbe_quiz
    st.markdown(f"**Question :** {question}")
    
    with st.form(key="verbe_form", clear_on_submit=True):
        user_reponse = st.text_input("Ta réponse :")
        submitted = st.form_submit_button("Vérifier")
        if submitted and user_reponse:
            if user_reponse.strip().lower() == reponse.lower():
                st.success("✅ Exact !")
                ajouter_point()
            else:
                st.error(f"❌ La bonne réponse est : {reponse}")
            st.session_state.verbe_quiz = None
            time.sleep(1.5)
            st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Nouveau verbe", use_container_width=True):
            st.session_state.verbe_quiz = None
            st.rerun()
    with col2:
        if st.button("🔙 Retour", use_container_width=True):
            st.session_state.etape = "menu"
            st.rerun()

# -------------------------------
# MODE PHRASE DU JOUR
# -------------------------------
elif st.session_state.etape == "phrase":
    st.markdown("## 💬 Phrase du jour")
    phrase = st.session_state.phrase_jour
    st.info(f"**Français :** {phrase['francais']}")
    st.markdown(f"**Anglais :** {phrase['anglais']}")
    
    # Petit exercice : traduire dans l'autre sens
    st.markdown("---")
    st.markdown("**Exercice :** Traduis cette phrase en anglais.")
    with st.form(key="phrase_form"):
        user_trad = st.text_input("Ta traduction :")
        submitted = st.form_submit_button("Vérifier")
        if submitted and user_trad:
            if user_trad.strip().lower() == phrase['anglais'].lower():
                st.success("✅ Parfait !")
                ajouter_point()
            else:
                st.error(f"❌ La bonne traduction est : {phrase['anglais']}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Nouvelle phrase", use_container_width=True):
            st.session_state.phrase_jour = nouvelle_phrase()
            st.rerun()
    with col2:
        if st.button("🔙 Retour", use_container_width=True):
            st.session_state.etape = "menu"
            st.rerun()

# -------------------------------
# MODE JEU DU PENDU
# -------------------------------
elif st.session_state.etape == "pendu":
    st.markdown("## 🎮 Jeu du pendu")
    st.markdown("Devine le mot anglais lettre par lettre.")
    
    mot = st.session_state.pendu_mot
    lettres_trouvees = st.session_state.pendu_lettres_trouvees
    essais = st.session_state.pendu_essais
    max_essais = st.session_state.pendu_max_essais
    
    # Affichage du mot masqué
    affichage = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            affichage += lettre + " "
        else:
            affichage += "_ "
    st.markdown(f"### {affichage}")
    st.markdown(f"Essais restants : {max_essais - essais}/{max_essais}")
    
    if "_" not in affichage:
        st.success("🎉 Bravo ! Tu as trouvé le mot !")
        ajouter_point()
        if st.button("🔁 Nouveau mot"):
            mot, lettres, essais = nouveau_pendu()
            st.session_state.pendu_mot = mot
            st.session_state.pendu_lettres_trouvees = lettres
            st.session_state.pendu_essais = essais
            st.rerun()
    elif essais >= max_essais:
        st.error(f"💀 Perdu ! Le mot était : {mot}")
        if st.button("🔁 Rejouer"):
            mot, lettres, essais = nouveau_pendu()
            st.session_state.pendu_mot = mot
            st.session_state.pendu_lettres_trouvees = lettres
            st.session_state.pendu_essais = essais
            st.rerun()
    else:
        # Saisie d'une lettre
        with st.form(key="pendu_form"):
            lettre = st.text_input("Propose une lettre :", max_chars=1).lower()
            submitted = st.form_submit_button("Essayer")
            if submitted and lettre:
                if lettre in lettres_trouvees:
                    st.warning("Lettre déjà proposée.")
                elif lettre in mot:
                    st.success("Bonne lettre !")
                    lettres_trouvees.append(lettre)
                else:
                    st.error("Mauvaise lettre.")
                    st.session_state.pendu_essais += 1
                st.rerun()
    
    if st.button("🔙 Retour au menu"):
        st.session_state.etape = "menu"
        st.rerun()

# -------------------------------
# MODE LEÇON DU JOUR
# -------------------------------
elif st.session_state.etape == "lecon":
    st.markdown("## 📖 Leçon du jour")
    jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    aujourdhui = jours[date.today().weekday()]
    lecon = lecons_journalieres[aujourdhui]
    st.markdown(f"### Aujourd'hui c'est {aujourdhui.capitalize()} !")
    st.info(lecon)
    
    # Petit exercice selon le jour
    st.markdown("---")
    st.markdown("**Petit exercice :**")
    
    if aujourdhui == "lundi":
        st.markdown("Complète : I ___ (to eat) apples every day.")
        reponse = st.text_input("Ta réponse :")
        if reponse:
            if reponse.lower() == "eat":
                st.success("✅ Bravo ! 'I eat apples' est correct.")
                ajouter_point()
            else:
                st.error("❌ La bonne réponse est 'eat'.")
    elif aujourdhui == "mardi":
        st.markdown("Complète : Yesterday, I ___ (to go) to the park.")
        reponse = st.text_input("Ta réponse :")
        if reponse:
            if reponse.lower() == "went":
                st.success("✅ Bien joué ! 'I went' est correct.")
                ajouter_point()
            else:
                st.error("❌ La bonne réponse est 'went'.")
    elif aujourdhui == "mercredi":
        st.markdown("Complète : Tomorrow, I ___ (to see) the doctor.")
        reponse = st.text_input("Ta réponse :")
        if reponse:
            if reponse.lower() == "will see":
                st.success("✅ Parfait ! 'I will see' est correct.")
                ajouter_point()
            else:
                st.error("❌ La bonne réponse est 'will see'.")
    else:
        st.markdown("Pas d'exercice aujourd'hui, mais n'oublie pas de réviser !")
    
    if st.button("🔙 Retour au menu"):
        st.session_state.etape = "menu"
        st.rerun()

# -------------------------------
# PIED DE PAGE
# -------------------------------
st.markdown("---")
st.markdown('<div class="footer">✨ <strong>English Buddy ++</strong> – Created by <strong>Krakendeveloppement</strong> – Avec ❤️ et Python</div>', unsafe_allow_html=True)

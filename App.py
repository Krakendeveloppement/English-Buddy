import streamlit as st
import random
import json
from datetime import date
import time

# Configuration de la page
st.set_page_config(
    page_title="English Buddy",
    page_icon="🇬🇧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        height: 3em;
        font-size: 1.2em;
        margin: 5px 0;
    }
    .stTextInput input {
        font-size: 1.1em;
        padding: 10px;
    }
    .bot-message {
        background-color: #f0f2f6;
        border-radius: 20px;
        padding: 15px;
        margin: 10px 0;
        font-size: 1.1em;
    }
    .user-message {
        background-color: #e1f5fe;
        border-radius: 20px;
        padding: 10px 15px;
        margin: 5px 0;
        text-align: right;
    }
    .title {
        text-align: center;
        font-size: 2.5em;
        color: #1e88e5;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# DONNÉES DE L'APPLICATION
# -------------------------------

vocabulaire = {
    "bonjour": "hello",
    "merci": "thank you",
    "au revoir": "goodbye",
    "maison": "house",
    "voiture": "car",
    "chien": "dog",
    "chat": "cat",
    "manger": "eat",
    "boire": "drink",
    "dormir": "sleep",
    "aimer": "love",
    "parler": "speak",
    "travail": "work",
    "école": "school",
    "livre": "book"
}

reponses_bot = {
    "salutation": [
        "Hello ! How are you today?",
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

lecons_journalieres = {
    "lundi": "Today's lesson: **Present Simple** – I eat, you eat, he eats.",
    "mardi": "Today's lesson: **Past Simple** – I ate, you ate, he ate.",
    "mercredi": "Today's lesson: **Future with 'will'** – I will eat, you will eat.",
    "jeudi": "Today's lesson: **Prepositions** – in, on, at.",
    "vendredi": "Today's lesson: **Modal verbs** – can, must, should.",
    "samedi": "Weekend fun: Learn 5 new animal names!",
    "dimanche": "Rest day, but here's a proverb: 'Practice makes perfect.'"
}

# Session state
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

# Fonctions
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

def nouvelle_question_quiz():
    mot_fr, mot_en = random.choice(list(vocabulaire.items()))
    return mot_fr, mot_en

def ajouter_point():
    st.session_state.score += 1
    if st.session_state.score % 5 == 0:
        st.session_state.niveau += 1
        st.balloons()

# Interface
st.markdown('<h1 class="title">🇬🇧 English Buddy</h1>', unsafe_allow_html=True)

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
    if st.button("📖 Leçon du jour", use_container_width=True):
        st.session_state.etape = "lecon"
    st.markdown("---")
    st.markdown("Partage cette app avec tes amis ! 📲")

if st.session_state.etape == "menu":
    st.markdown("## Bienvenue sur English Buddy !")
    st.markdown("""
    Choisis une activité pour commencer :
    
    - **💬 Conversation** : Parle avec moi en anglais, je te répondrai.
    - **📚 Vocabulaire** : Apprends de nouveaux mots avec des quiz.
    - **📖 Leçon du jour** : Découvre une leçon rapide chaque jour.
    
    Plus tu pratiques, plus ton score augmente ! 🚀
    """)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💬 Conversation", use_container_width=True):
            st.session_state.etape = "conversation"
            st.rerun()
    with col2:
        if st.button("📚 Vocabulaire", use_container_width=True):
            st.session_state.etape = "vocabulaire"
            st.session_state.nb_quiz = 0
            st.rerun()
    with col3:
        if st.button("📖 Leçon du jour", use_container_width=True):
            st.session_state.etape = "lecon"
            st.rerun()

elif st.session_state.etape == "conversation":
    st.markdown("## 💬 Mode Conversation")
    st.markdown("Pose-moi des questions ou parle-moi en anglais. Je te répondrai !")
    
    for msg in st.session_state.historique[-10:]:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
    
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Toi :", placeholder="Écris ton message ici...")
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
        reponse_user = st.text_input("Ta réponse :", key="quiz_input")
        submitted = st.form_submit_button("Vérifier")
        if submitted and reponse_user:
            if reponse_user.strip().lower() == st.session_state.reponse_quiz.lower():
                st.success("✅ Bonne réponse !")
                ajouter_point()
            else:
                st.error(f"❌ Pas tout à fait. La réponse était : **{st.session_state.reponse_quiz}**")
            st.session_state.question_quiz = None
            time.sleep(1.5)
            st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Nouvelle question", use_container_width=True):
            st.session_state.question_quiz = None
            st.rerun()
    with col2:
        if st.button("🔙 Retour au menu", use_container_width=True):
            st.session_state.etape = "menu"
            st.session_state.question_quiz = None
            st.rerun()

elif st.session_state.etape == "lecon":
    st.markdown("## 📖 Leçon du jour")
    jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    aujourdhui = jours[date.today().weekday()]
    lecon = lecons_journalieres[aujourdhui]
    st.markdown(f"### Aujourd'hui c'est {aujourdhui.capitalize()} !")
    st.info(lecon)
    
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
    else:
        st.markdown("Pas d'exercice aujourd'hui, mais n'oublie pas de réviser !")
    
    if st.button("🔙 Retour au menu"):
        st.session_state.etape = "menu"
        st.rerun()

st.markdown("---")
st.markdown("✨ *English Buddy – Créé avec ❤️ et Python*")

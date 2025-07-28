import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Essilor Instruments", layout="wide")

# --- LOGO ---
st.image("logo_essilor_instruments.png", width=150)
st.title("Application Essilor Instruments")
st.write("Gestion des réclamations, réparations et qualité")

# --- MENU ---
menu = ["Accueil", "Service TBS", "Service Réparation SC", "Instruments & Quality", "Dashboards"]
choice = st.sidebar.radio("Navigation", menu)

# --- ACCUEIL ---
if choice == "Accueil":
    st.header("Présentation de l'entreprise")
    st.write("""
    Bienvenue dans l'application Essilor Instruments.  
    Cette application permet de gérer les réclamations clients, les réparations et le suivi qualité.
    """)
    st.subheader("Produits standards")
    col1, col2 = st.columns(2)
    with col1:
        st.success("Produit VR - Virtual Refraction")
    with col2:
        st.success("Produit VS - Vision Screening")

# --- SERVICE TBS ---
elif choice == "Service TBS":
    st.header("Tableau des réclamations clients (TBS)")
    data_tbs = pd.DataFrame({
        "Id_réclamation": [1, 2],
        "Modèle": ["VR", "VS"],
        "Numéro de série": ["12345", "67890"],
        "Client": ["Opticien A", "Opticien B"],
        "Date réclamation": ["2025-07-01", "2025-07-10"],
        "Description défaut client": ["Problème d'écran", "Erreur calibration"],
        "Analyse TBS": ["En cours", "Complète"],
        "Date d'analyse": ["2025-07-05", "2025-07-12"],
        "Date envoi SC": ["2025-07-07", "2025-07-15"]
    })
    st.dataframe(data_tbs)

    st.info("⚙️ Options : Ajouter | Supprimer | Modifier (à implémenter)")

# --- SERVICE RÉPARATION SC ---
elif choice == "Service Réparation SC":
    st.header("Tableau des réclamations clients (SC)")
    data_sc = pd.DataFrame({
        "Id_réclamation": [1],
        "Modèle": ["VR"],
        "Numéro de série": ["12345"],
        "Client": ["Opticien A"],
        "Date réclamation": ["2025-07-01"],
        "Description défaut client": ["Problème d'écran"],
        "Analyse TBS": ["En cours"],
        "Analyse SC": ["Pièce défectueuse"],
        "Défauts constatés": ["Écran HS"],
        "Réparations effectuées": ["Changement écran"],
        "Date envoi client": ["2025-07-20"]
    })
    st.dataframe(data_sc)

    st.info("⚙️ Options : Ajouter | Supprimer | Modifier (à implémenter)")

# --- INSTRUMENTS & QUALITY ---
elif choice == "Instruments & Quality":
    st.header("Tableau des CAPA")
    data_capa = pd.DataFrame({
        "Id_CAPA": [101],
        "Type de remontée": ["Réclamation client"],
        "Instrument": ["VR"],
        "Date ouverture": ["2025-06-15"],
        "Date analyse": ["2025-06-20"],
        "Date clôture": ["2025-07-10"],
        "Analyse": ["Défaut design"],
        "Status": ["Clôturé"],
        "Cause racine": ["Conception"],
        "Demande changement": ["Oui"],
        "Indice IPR": [12],
        "Priorité": ["Haute"],
        "Urgency": ["Élevée"]
    })
    st.dataframe(data_capa)

    st.info("⚙️ Options : Ajouter | Supprimer | Modifier (à implémenter)")

# --- DASHBOARDS ---
elif choice == "Dashboards":
    st.header("Tableaux de bord")
    st.write("📊 Nombre de réclamations et indicateurs clés")

    # Exemple KPI
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Réclamations TBS", 25)
    with col2:
        st.metric("Réclamations SC", 15)
    with col3:
        st.metric("CAPA Qualité", 8)

    st.info("🔧 Ici, vous pourrez ajouter des graphiques et KPI détaillés.")

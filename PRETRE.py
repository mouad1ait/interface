import pandas as pd
import streamlit as st
from datetime import datetime

# --------------------------
# Fonctions utilitaires
# --------------------------

def convertir_dates(df, colonnes_dates):
    """Convertit les colonnes de dates sous forme texte en datetime"""
    for col in colonnes_dates:
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        except:
            st.warning(f"Impossible de convertir la colonne {col}")
    return df

def extraire_date_fabrication(numero):
    """Extrait la date de fabrication à partir du numéro de série (format mmaaxxx)."""
    try:
        mois = int(numero[:2])
        annee = int("20" + numero[2:4])  # exemple : 25 -> 2025
        return datetime(annee, mois, 1)
    except:
        return None

def ajouter_cle_primaire(df, col_modele, col_numero):
    """Crée une clé primaire modèle/numéro de série"""
    df["clé_produit"] = df[col_modele].astype(str) + "/" + df[col_numero].astype(str)
    return df

def premiere_installation(df, col_cle, col_installation):
    """Récupère la première date d’installation pour chaque produit"""
    return df.groupby(col_cle)[col_installation].min().reset_index()

# --------------------------
# Interface Streamlit
# --------------------------

st.title("🧹 Nettoyage des données - Extraction SIS")

uploaded_file = st.file_uploader("Importer un fichier Excel", type=["xlsx", "csv"])

if uploaded_file:
    # Lecture du fichier
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, dtype=str)
    else:
        df = pd.read_excel(uploaded_file, dtype=str)
    
    st.write("Aperçu des données importées :", df.head())

    # Sélection des colonnes de dates
    colonnes_dates = st.multiselect("Sélectionnez les colonnes de dates à convertir :", df.columns)
    if st.button("Convertir les dates"):
        df = convertir_dates(df, colonnes_dates)
        st.success("✅ Dates converties avec succès")
        st.write(df.head())

    # Génération de la date de fabrication
    if "numéro_de_série" in df.columns:
        df["date_fabrication"] = df["numéro_de_série"].apply(extraire_date_fabrication)
        st.success("✅ Date de fabrication extraite")
        st.write(df[["numéro_de_série", "date_fabrication"]].head())

    # Création de la clé produit
    if "modèle" in df.columns and "numéro_de_série" in df.columns:
        df = ajouter_cle_primaire(df, "modèle", "numéro_de_série")
        st.success("✅ Clé produit générée")
        st.write(df[["modèle", "numéro_de_série", "clé_produit"]].head())

    # Première installation
    if "clé_produit" in df.columns and "date_installation" in df.columns:
        df_install = premiere_installation(df, "clé_produit", "date_installation")
        st.success("✅ Première date d’installation extraite")
        st.write(df_install.head())

    # Téléchargement du fichier nettoyé
    st.download_button(
        "📥 Télécharger le fichier nettoyé",
        df.to_csv(index=False).encode("utf-8"),
        "donnees_nettoyees.csv",
        "text/csv"
    )

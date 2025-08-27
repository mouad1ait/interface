import pandas as pd
import streamlit as st
from datetime import datetime
from io import BytesIO

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
        annee = int("20" + numero[2:4])  # ex : '25' -> 2025
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

def to_excel(df):
    """Convertit un DataFrame en fichier Excel (mémoire)"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Données_nettoyées")
    processed_data = output.getvalue()
    return processed_data

# --------------------------
# Interface Streamlit
# --------------------------

st.title("🧹 Nettoyage des données - Extraction SIS")

uploaded_file = st.file_uploader("Importer un fichier Excel ou CSV", type=["xlsx", "csv"])

if uploaded_file:
    # Lecture du fichier
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, dtype=str)
    else:
        df = pd.read_excel(uploaded_file, dtype=str)
    
    st.write("### 📊 Aperçu des données importées")
    st.dataframe(df.head())

    # Sélection des colonnes pour modèle et numéro de série
    col_modele = st.selectbox("👉 Sélectionnez la colonne du modèle :", df.columns)
    col_numero = st.selectbox("👉 Sélectionnez la colonne du numéro de série :", df.columns)

    # Sélection des colonnes de dates
    colonnes_dates = st.multiselect("👉 Sélectionnez les colonnes de dates à convertir :", df.columns)

    # Conversion des dates
    if st.button("🔄 Convertir les dates sélectionnées"):
        df = convertir_dates(df, colonnes_dates)
        st.success("✅ Dates converties avec succès")
        st.write(df[colonnes_dates].head())

    # Génération de la date de fabrication
    if col_numero:
        df["date_fabrication"] = df[col_numero].apply(extraire_date_fabrication)
        st.success("✅ Date de fabrication extraite à partir du numéro de série")
        st.write(df[[col_numero, "date_fabrication"]].head())

    # Création de la clé produit
    if col_modele and col_numero:
        df = ajouter_cle_primaire(df, col_modele, col_numero)
        st.success("✅ Clé produit générée")
        st.write(df[[col_modele, col_numero, "clé_produit"]].head())

    # Première installation (si date sélectionnée)
    col_install = st.selectbox("👉 Sélectionnez la colonne de date d’installation (facultatif) :", [""] + list(df.columns))
    if col_install and col_install != "":
        df_install = premiere_installation(df, "clé_produit", col_install)
        st.success("✅ Première date d’installation extraite")
        st.write(df_install.head())

    # Téléchargement du fichier nettoyé en Excel
    excel_file = to_excel(df)
    st.download_button(
        label="📥 Télécharger le fichier nettoyé (Excel)",
        data=excel_file,
        file_name="donnees_nettoyees.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

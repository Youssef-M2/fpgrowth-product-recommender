"""
data_preprocessing.py
--------------------
Chargement, nettoyage et transformation des transactions en format binaire.
Utilise TransactionEncoder de mlxtend.
"""

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder


def load_data(filepath: str) -> pd.DataFrame:
    """
    Charge le fichier Excel (online_retail_II.xlsx).
    """
    df = pd.read_excel(filepath)
    print(f"[INFO] Données chargées : {df.shape[0]:,} lignes, {df.shape[1]} colonnes")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie le DataFrame selon les règles du notebook :
    - Supprime les Customer ID manquants
    - Garde les quantités > 0
    - Supprime les factures annulées (Invoice ne commençant pas par 'C')
    - Convertit Customer ID en string
    """
    initial = len(df)

    df = df.dropna(subset=['Customer ID'])
    print(f"[CLEAN] Après suppression Customer ID nuls : {len(df):,} lignes (-{initial - len(df):,})")

    df = df[df['Quantity'] > 0]
    print(f"[CLEAN] Après suppression quantités ≤ 0 : {len(df):,} lignes")

    # Garder seulement les factures non annulées (ne commencent pas par 'C')
    df = df[~df['Invoice'].astype(str).str.startswith('C')]
    print(f"[CLEAN] Après suppression factures annulées : {len(df):,} lignes")

    df['Customer ID'] = df['Customer ID'].astype(str)

    print(f"[INFO] Nettoyage terminé : {len(df):,} lignes conservées ({len(df)/initial*100:.1f}% du total)")
    return df.reset_index(drop=True)


def create_transactions(df: pd.DataFrame) -> list:
    """
    Crée une liste de paniers (chaque panier = liste des descriptions produits).
    Regroupe par numéro de facture.
    """
    transactions = df.groupby('Invoice')['Description'].apply(list).tolist()
    print(f"[INFO] {len(transactions):,} transactions (factures) créées")
    return transactions


def encode_transactions(transactions: list) -> pd.DataFrame:
    """
    Encode les transactions en matrice binaire (True/False) avec TransactionEncoder.
    """
    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_array, columns=te.columns_)
    print(f"[INFO] Matrice encodée : {df_encoded.shape[0]:,} lignes × {df_encoded.shape[1]:,} produits")
    return df_encoded
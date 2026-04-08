"""
model.py
--------
FP-Growth, extraction des itemsets fréquents, génération des règles,
sauvegarde/chargement des modèles.
"""

import pandas as pd
import pickle
from pathlib import Path
from mlxtend.frequent_patterns import fpgrowth, association_rules


def run_fpgrowth(df_encoded: pd.DataFrame, min_support: float = 0.01) -> pd.DataFrame:
    """
    Applique FP-Growth sur la matrice binaire.
    Retourne les itemsets fréquents avec leur support.
    """
    print(f"[FPGrowth] Calcul des itemsets fréquents (min_support = {min_support})...")
    frequent_itemsets = fpgrowth(df_encoded, min_support=min_support, use_colnames=True)
    frequent_itemsets = frequent_itemsets.sort_values('support', ascending=False).reset_index(drop=True)
    print(f"[FPGrowth] {len(frequent_itemsets):,} itemsets fréquents trouvés")
    return frequent_itemsets


def generate_rules(frequent_itemsets: pd.DataFrame, min_lift: float = 1.0) -> pd.DataFrame:
    """
    Génère les règles d'association à partir des itemsets fréquents.
    Filtre par lift >= min_lift et trie par lift décroissant.
    """
    print(f"[Rules] Génération des règles (lift >= {min_lift})...")
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)
    rules = rules.sort_values('lift', ascending=False).reset_index(drop=True)
    # Ajout de colonnes lisibles
    rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(sorted(x)))
    rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(sorted(x)))
    print(f"[Rules] {len(rules):,} règles générées")
    return rules


def save_model(obj, filepath: str) -> None:
    """Sauvegarde un objet Python (itemsets ou règles) avec pickle."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)
    print(f"[SAVE] Modèle sauvegardé → {filepath}")


def load_model(filepath: str):
    """Charge un objet depuis un fichier pickle."""
    with open(filepath, 'rb') as f:
        obj = pickle.load(f)
    print(f"[LOAD] Modèle chargé ← {filepath}")
    return obj


def evaluate_rules(rules: pd.DataFrame) -> dict:
    """Retourne des statistiques descriptives sur les règles."""
    if rules.empty:
        return {"nb_rules": 0}
    stats = {
        "nb_rules": len(rules),
        "support_mean": rules['support'].mean(),
        "support_max": rules['support'].max(),
        "confidence_mean": rules['confidence'].mean(),
        "confidence_max": rules['confidence'].max(),
        "lift_mean": rules['lift'].mean(),
        "lift_max": rules['lift'].max(),
        "lift_min": rules['lift'].min(),
    }
    return stats
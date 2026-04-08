"""
recommender.py
--------------
Système de recommandation basé sur les règles d'association.
Fonction principale : recommend_products()
"""

import pandas as pd
from typing import List, Dict, Set


def recommend_products(
    cart_items: List[str],
    rules: pd.DataFrame,
    top_n: int = 5,
    min_confidence: float = 0.0,
    min_lift: float = 1.0
) -> List[Dict]:
    """
    Recommande des produits complémentaires à partir d'un panier.

    Args:
        cart_items: Liste des produits déjà dans le panier (noms exacts)
        rules: DataFrame des règles d'association (avec colonnes antecedents, consequents, confidence, lift, support)
        top_n: Nombre maximum de recommandations
        min_confidence: Confiance minimale (optionnel)
        min_lift: Lift minimal (optionnel)

    Returns:
        Liste de dictionnaires contenant 'product', 'confidence', 'lift', 'support'
    """
    if not cart_items or rules.empty:
        return []

    cart_set = set(item.strip().upper() for item in cart_items)

    # Filtrer les règles selon les seuils
    filtered_rules = rules[(rules['confidence'] >= min_confidence) & (rules['lift'] >= min_lift)]

    recommendations = {}

    for _, row in filtered_rules.iterrows():
        antecedents = set(row['antecedents'])
        # Vérifier si tous les antécédents sont dans le panier
        if antecedents.issubset(cart_set):
            consequents = set(row['consequents'])
            new_products = consequents - cart_set
            for prod in new_products:
                if prod not in recommendations:
                    recommendations[prod] = {
                        'product': prod,
                        'confidence': row['confidence'],
                        'lift': row['lift'],
                        'support': row['support']
                    }
                else:
                    # Garder la meilleure confiance/lift
                    if row['lift'] > recommendations[prod]['lift']:
                        recommendations[prod] = {
                            'product': prod,
                            'confidence': row['confidence'],
                            'lift': row['lift'],
                            'support': row['support']
                        }

    # Trier par lift décroissant puis confiance
    sorted_recs = sorted(
        recommendations.values(),
        key=lambda x: (x['lift'], x['confidence']),
        reverse=True
    )
    return sorted_recs[:top_n]


def format_recommendations(recommendations: List[Dict]) -> pd.DataFrame:
    """Convertit la liste de recommandations en DataFrame lisible."""
    if not recommendations:
        return pd.DataFrame(columns=['Produit recommandé', 'Confiance', 'Lift', 'Support'])

    df = pd.DataFrame(recommendations)
    df = df.rename(columns={
        'product': 'Produit recommandé',
        'confidence': 'Confiance',
        'lift': 'Lift',
        'support': 'Support'
    })
    df['Confiance'] = df['Confiance'].map('{:.1%}'.format)
    df['Lift'] = df['Lift'].map('{:.2f}'.format)
    df['Support'] = df['Support'].map('{:.4f}'.format)
    return df.reset_index(drop=True)


def get_available_products(rules: pd.DataFrame) -> List[str]:
    """Retourne tous les produits apparaissant dans les règles (antécédents ou conséquents)."""
    products = set()
    for _, row in rules.iterrows():
        products.update(row['antecedents'])
        products.update(row['consequents'])
    return sorted(products)
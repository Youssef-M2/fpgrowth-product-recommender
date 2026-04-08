#!/usr/bin/env python3
"""
main.py
-------
Pipeline complet :
- Chargement et nettoyage des données
- Encodage des transactions
- FP-Growth et extraction des règles
- Sauvegarde des modèles
- Mode interactif ou démo
"""

import argparse
import sys
from pathlib import Path

from data_preprocessing import load_data, clean_data, create_transactions, encode_transactions
from model import run_fpgrowth, generate_rules, save_model, load_model, evaluate_rules
from recommender import recommend_products, format_recommendations, get_available_products


def parse_args():
    parser = argparse.ArgumentParser(description="FP-Growth Recommender System")
    parser.add_argument('--data', type=str, default='data/online_retail_II.xlsx',
                        help='Chemin vers le fichier Excel')
    parser.add_argument('--min_support', type=float, default=0.01,
                        help='Support minimal pour FP-Growth (défaut: 0.01)')
    parser.add_argument('--min_lift', type=float, default=1.0,
                        help='Lift minimal pour les règles (défaut: 1.0)')
    parser.add_argument('--save_models', action='store_true', default=True,
                        help='Sauvegarder les modèles (itemsets et règles)')
    parser.add_argument('--load_rules', type=str, default=None,
                        help='Charger des règles préexistantes (chemin .pkl)')
    parser.add_argument('--interactive', action='store_true',
                        help='Mode interactif pour tester des paniers')
    return parser.parse_args()


def main():
    args = parse_args()

    # ---------- Chargement ou entraînement ----------
    if args.load_rules and Path(args.load_rules).exists():
        print(f"[MAIN] Chargement des règles depuis {args.load_rules}")
        rules = load_model(args.load_rules)
        frequent_itemsets = None  # non utilisé
    else:
        if not Path(args.data).exists():
            print(f"Erreur : fichier {args.data} introuvable.")
            sys.exit(1)

        print(f"[MAIN] Chargement des données depuis {args.data}")
        df_raw = load_data(args.data)

        print("[MAIN] Nettoyage des données")
        df_clean = clean_data(df_raw)

        print("[MAIN] Création des transactions (paniers)")
        transactions = create_transactions(df_clean)

        print("[MAIN] Encodage des transactions en matrice binaire")
        df_encoded = encode_transactions(transactions)

        print("[MAIN] Extraction des itemsets fréquents (FP-Growth)")
        frequent_itemsets = run_fpgrowth(df_encoded, min_support=args.min_support)

        if frequent_itemsets.empty:
            print("Aucun itemset fréquent trouvé. Essayez un support plus faible.")
            sys.exit(1)

        print("[MAIN] Génération des règles d'association")
        rules = generate_rules(frequent_itemsets, min_lift=args.min_lift)

        if rules.empty:
            print("Aucune règle générée. Essayez de baisser le lift minimal.")
            sys.exit(1)

        if args.save_models:
            save_model(frequent_itemsets, "models/fpgrowth.pkl")
            save_model(rules, "models/rules.pkl")

    # ---------- Statistiques ----------
    stats = evaluate_rules(rules)
    print("\n[STATS] Résumé des règles :")
    for k, v in stats.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.4f}")
        else:
            print(f"  {k}: {v}")

    available_products = get_available_products(rules)
    print(f"\n[INFO] {len(available_products)} produits disponibles dans les règles.")

    # ---------- Mode interactif ou démo ----------
    if args.interactive:
        print("\n" + "=" * 60)
        print("MODE INTERACTIF - Entrez les produits de votre panier")
        print("Exemple : WHITE HANGING HEART T-LIGHT HOLDER, REGENCY CAKESTAND 3 TIER")
        print("Tapez 'exit' pour quitter\n")

        while True:
            user_input = input("> Votre panier (produits séparés par des virgules) : ").strip()
            if user_input.lower() in ('exit', 'quit'):
                break
            if not user_input:
                continue

            cart = [p.strip().upper() for p in user_input.split(',') if p.strip()]
            recs = recommend_products(cart, rules, top_n=5, min_confidence=0.0, min_lift=1.0)

            if not recs:
                print("  Aucune recommandation trouvée.\n")
            else:
                df_rec = format_recommendations(recs)
                print(df_rec.to_string(index=False))
                print()
    else:
        # Exemple simple
        demo_cart = ["WHITE HANGING HEART T-LIGHT HOLDER"]
        print("\n[DEMO] Panier exemple :", demo_cart)
        recs = recommend_products(demo_cart, rules, top_n=5)
        if recs:
            df_rec = format_recommendations(recs)
            print("\nRecommandations :")
            print(df_rec.to_string(index=False))
        else:
            print("Aucune recommandation générée.")

        print("\nPour utiliser le mode interactif : python main.py --interactive")


if __name__ == "__main__":
    main()
import streamlit as st
import pickle
import pandas as pd

# Load rules
with open('models/rules.pkl', 'rb') as f:
    rules = pickle.load(f)

# Extract all unique products from rules
def get_all_products(rules):
    products = set()
    for _, row in rules.iterrows():
        products.update(row['antecedents'])
        products.update(row['consequents'])
    return sorted(list(products))

# Recommendation function
def get_recommendations(basket, rules, top_n=5):
    basket = set([item.upper() for item in basket])
    recommendations = []

    for _, row in rules.iterrows():
        antecedents = set([item.upper() for item in row['antecedents']])
        consequents = set([item.upper() for item in row['consequents']])

        if antecedents.issubset(basket):
            recommendations.extend(list(consequents))

    return list(set(recommendations))[:top_n]

# Initialize session state
if "basket" not in st.session_state:
    st.session_state.basket = []

# UI
st.title("🛒 FP-Growth Recommender System")

products = get_all_products(rules)

# Product selection
selected_product = st.selectbox("Select a product:", products)

# Add to basket
if st.button("➕ Add to Basket"):
    if selected_product not in st.session_state.basket:
        st.session_state.basket.append(selected_product)

# Show basket
st.subheader("🧺 Your Basket")
if st.session_state.basket:
    for item in st.session_state.basket:
        st.write(f"✔ {item}")
else:
    st.write("Basket is empty")

# Clear basket
if st.button("🗑️ Clear Basket"):
    st.session_state.basket = []

# Get recommendations
if st.button("🎯 Get Recommendations"):
    if st.session_state.basket:
        recs = get_recommendations(st.session_state.basket, rules)

        if recs:
            st.subheader("🔥 Recommended Products")
            for r in recs:
                st.write(f"👉 {r}")
        else:
            st.warning("No recommendations found.")
    else:
        st.warning("Please add products to basket first.")
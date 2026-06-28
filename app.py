import streamlit as st

st.title("🧊 Smart Fridge")

fridge = {
    "mléko": 2,
    "máslo": 1,
    "vejce": 6,
    "šunka": 0,
    "sýr": 0
}

recipes = {
    "omeleta": {"vejce": 3, "mléko": 1},
    "toast": {"šunka": 2, "sýr": 1}
}

st.subheader("🧊 Lednice")
for item, amount in fridge.items():
    st.write(f"{item}: {amount}")

st.subheader("🛒 Nákupní seznam")

shopping = {}

for recipe, ingredients in recipes.items():
    for ing, needed in ingredients.items():
        have = fridge.get(ing, 0)
        missing = needed - have
        if missing > 0:
            shopping[ing] = shopping.get(ing, 0) + missing

for item, amount in shopping.items():
    st.write(f"{item}: {amount}")

st.subheader("🍳 Co můžeme vařit")

for recipe, ingredients in recipes.items():
    can_make = True
    for ing, needed in ingredients.items():
        if fridge.get(ing, 0) < needed:
            can_make = False
    if can_make:
        st.success(recipe)
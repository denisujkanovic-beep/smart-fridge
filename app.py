import streamlit as st

st.title("🧊 Smart Fridge PRO")

# inicializace dat
if "fridge" not in st.session_state:
    st.session_state.fridge = {
        "mléko": 2,
        "máslo": 1,
        "vejce": 6,
        "šunka": 0,
        "sýr": 0
    }

fridge = st.session_state.fridge

# -------------------
# ➕ PŘIDÁNÍ POTRAVIN
# -------------------
st.subheader("➕ Přidat / upravit potravinu")

item = st.text_input("Název potraviny")
amount = st.number_input("Množství", min_value=0, step=1)

if st.button("Uložit"):
    if item:
        fridge[item] = amount
        st.success(f"{item} nastaveno na {amount}")

st.divider()

# -------------------
# 🧊 LEDNICE
# -------------------
st.subheader("🧊 Lednice")

for item, amount in fridge.items():
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**{item}**: {amount}")

    with col2:
        if st.button(f"❌ odstranit {item}"):
            del fridge[item]
            st.rerun()

st.divider()

# -------------------
# 🛒 NÁKUPNÍ SEZNAM
# -------------------
st.subheader("🛒 Nákupní seznam")

recipes = {
    "omeleta": {"vejce": 3, "mléko": 1},
    "toast": {"šunka": 2, "sýr": 1}
}

shopping = {}

for recipe, ingredients in recipes.items():
    for ing, needed in ingredients.items():
        have = fridge.get(ing, 0)
        missing = needed - have
        if missing > 0:
            shopping[ing] = shopping.get(ing, 0) + missing

if shopping:
    for item, amount in shopping.items():
        st.write(f"🛒 {item}: {amount}")
else:
    st.success("Nic nechybí 🎉")

st.divider()

# -------------------
# 🍳 CO MŮŽEME VAŘIT
# -------------------
st.subheader("🍳 Co můžeme vařit")

for recipe, ingredients in recipes.items():
    can_make = True

    for ing, needed in ingredients.items():
        if fridge.get(ing, 0) < needed:
            can_make = False

    if can_make:
        st.success(recipe)

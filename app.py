import streamlit as st

st.title("🧊 Smart Lednice")

# -------------------
# DATA
# -------------------
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
# UPDATE FUNKCE
# -------------------
def change_amount(item, delta):
    fridge[item] = max(0, fridge[item] + delta)


# -------------------
# LEDNICE
# -------------------
st.subheader("🧊 Lednice")

for item in list(fridge.keys()):
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        if fridge[item] == 0:
            st.markdown(f"❌ **{item}**: {fridge[item]}")
        else:
            st.markdown(f"✅ **{item}**: {fridge[item]}")

    with col2:
        if st.button(f"+ {item}", key=f"plus_{item}"):
            change_amount(item, 1)
            st.rerun()

    with col3:
        if st.button(f"- {item}", key=f"minus_{item}"):
            change_amount(item, -1)
            st.rerun()


# -------------------
# 🛒 NÁKUPNÍ SEZNAM
# -------------------
st.subheader("🛒 Nákupní seznam")

missing_items = [item for item, amount in fridge.items() if amount == 0]

if missing_items:
    for item in missing_items:
        st.write(f"🛒 {item}")
else:
    st.success("Nic nechybí 🎉")


# -------------------
# ➕ PŘIDÁNÍ NOVÉ POTRAVINY
# -------------------
st.divider()
st.subheader("➕ Přidat potravinu")

new_item = st.text_input("Název potraviny")

if st.button("Přidat"):
    if new_item and new_item not in fridge:
        fridge[new_item] = 0
        st.rerun()

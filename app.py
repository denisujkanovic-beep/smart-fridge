import streamlit as st
from db import get_conn, init

init()

st.set_page_config(page_title="Smart Fridge", layout="centered")

st.markdown("""
<style>
    .card {
        padding: 12px;
        border-radius: 12px;
        background: #111;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
    }

    .name {
        font-size: 18px;
    }

    .low {
        color: #ff4d4d;
    }

    .ok {
        color: #4dff88;
    }

    .btn {
        font-size: 20px;
        padding: 4px 10px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)


def load():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM fridge")
    data = c.fetchall()
    conn.close()
    return data


def update(item, delta):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE fridge SET amount = MAX(amount + ?, 0) WHERE item = ?", (delta, item))
    conn.commit()
    conn.close()


def add_item(name):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO fridge VALUES (?, 0)", (name,))
    conn.commit()
    conn.close()


st.title("🧊 Smart Fridge")

data = load()

# -------------------
# LEDNICE
# -------------------
for item, amount in data:
    col1, col2, col3 = st.columns([6, 1, 1])

    status = "low" if amount == 0 else "ok"

    with col1:
        st.markdown(f"**{item}**  <span class='{status}'>({amount})</span>", unsafe_allow_html=True)

    with col2:
        if st.button("➕", key=f"p_{item}"):
            update(item, 1)
            st.rerun()

    with col3:
        if st.button("➖", key=f"m_{item}"):
            update(item, -1)
            st.rerun()


# -------------------
# 🛒 NÁKUP
# -------------------
st.divider()
st.subheader("🛒 Nákupní seznam")

missing = [i for i, a in data if a == 0]

if missing:
    st.write(" • ".join(missing))
else:
    st.success("Všechno máme 🎉")


# -------------------
# ➕ PŘIDÁNÍ
# -------------------
st.divider()
new_item = st.text_input("Přidat potravinu")

if st.button("Přidat"):
    if new_item:
        add_item(new_item)
        st.rerun()

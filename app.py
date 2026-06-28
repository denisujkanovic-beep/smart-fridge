import streamlit as st
from db import get_conn, init

init()

st.set_page_config(page_title="Fridge", layout="wide")

# -------------------
# MODERN CENTERED APP CONTAINER
# -------------------
st.markdown("""
<style>

/* celé pozadí */
body {
    background: #f6f7f9;
}

/* app container */
.main .block-container {
    max-width: 520px;
    padding-top: 40px;
    margin: auto;
}

/* title */
h1 {
    text-align: center;
    font-weight: 600;
    font-size: 26px;
    margin-bottom: 20px;
}

/* card */
.card {
    background: white;
    border-radius: 14px;
    padding: 10px 12px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid #eee;
}

/* name */
.name {
    font-size: 14px;
    font-weight: 500;
}

/* status */
.ok { color: #16a34a; font-size: 12px; }
.low { color: #ef4444; font-size: 12px; }

/* buttons */
button {
    height: 26px !important;
    width: 26px !important;
    border-radius: 8px !important;
    padding: 0 !important;
}

/* shopping grid cards */
.shop-card {
    background: white;
    padding: 8px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #eee;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# -------------------
# DB
# -------------------
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
    c.execute("""
        UPDATE fridge
        SET amount = MAX(amount + ?, 0)
        WHERE item = ?
    """, (delta, item))
    conn.commit()
    conn.close()


def add_item(name):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO fridge VALUES (?, 0)", (name,))
    conn.commit()
    conn.close()


data = load()

st.title("🧊 Fridge")

# -------------------
# LEDNICE (CLEAN CENTERED LIST)
# -------------------
for item, amount in data:

    col1, col2, col3 = st.columns([7, 1, 1])

    status_class = "low" if amount == 0 else "ok"

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="name">{item}</div>
            <div class="{status_class}">{amount}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("+", key=f"p_{item}"):
            update(item, 1)
            st.rerun()

    with col3:
        if st.button("-", key=f"m_{item}"):
            update(item, -1)
            st.rerun()


# -------------------
# 🛒 NÁKUP (GRID 2-3 SLOUPCE)
# -------------------
st.markdown("## 🛒 Nákup")

missing = [i for i, a in data if a == 0]

if missing:

    cols = st.columns(3)

    for i, item in enumerate(missing):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="shop-card">
                {item}
            </div>
            """, unsafe_allow_html=True)

else:
    st.markdown("<p style='text-align:center;color:#16a34a;'>Všechno máme 🎉</p>", unsafe_allow_html=True)


# -------------------
# ➕ ADD ITEM (CENTERED)
# -------------------
st.markdown("---")

new_item = st.text_input("", placeholder="Přidat potravinu...")

if st.button("Přidat"):
    if new_item:
        add_item(new_item)
        st.rerun()

import streamlit as st
from db import get_conn, init

init()

st.set_page_config(page_title="Fridge", layout="centered")

# -------------------
# CLEAN STYLE (MINIMAL 2026)
# -------------------
st.markdown("""
<style>

html, body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI";
    background: #fafafa;
}

h1, h2 {
    text-align: center;
    font-weight: 600;
    letter-spacing: -0.5px;
}

.block {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 10px;
    margin: 4px 0;
    border-radius: 10px;
    background: white;
    border: 1px solid #eee;
    font-size: 14px;
}

.name {
    font-size: 14px;
}

.badge-low {
    color: #ef4444;
    font-size: 12px;
}

.badge-ok {
    color: #16a34a;
    font-size: 12px;
}

button {
    height: 28px !important;
    width: 28px !important;
    padding: 0 !important;
    border-radius: 8px !important;
    font-size: 14px !important;
}

div[data-testid="column"] {
    padding: 0px 4px;
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


# -------------------
# DATA
# -------------------
data = load()

st.title("🧊 Fridge")

# -------------------
# LEDNICE (CLEAN LIST)
# -------------------
for item, amount in data:

    col1, col2, col3 = st.columns([6, 1, 1])

    status = "badge-low" if amount == 0 else "badge-ok"

    with col1:
        st.markdown(f"""
        <div class="block">
            <div class="name">{item}</div>
            <div class="{status}">{amount}</div>
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
# 🛒 NÁKUP (MINIMAL TEXT)
# -------------------
st.markdown("## 🛒 Nákup")

missing = [i for i, a in data if a == 0]

if missing:
    cols = st.columns(3)

    for i, item in enumerate(missing):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="block">
                <div class="name">{item}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align:center;color:green;'>Všechno máme 🎉</p>", unsafe_allow_html=True)


# -------------------
# ➕ ADD ITEM (MINIMAL)
# -------------------
st.markdown("---")

new_item = st.text_input("", placeholder="Přidat potravinu...")

if st.button("Přidat"):
    if new_item:
        add_item(new_item)
        st.rerun()

import streamlit as st
from db import get_conn, init

init()

st.set_page_config(
    page_title="Smart Fridge",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------
# MODERN STYLE
# -------------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
}

.block {
    background: #ffffff;
    border-radius: 16px;
    padding: 14px 16px;
    margin-bottom: 10px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.name {
    font-size: 16px;
    font-weight: 500;
}

.badge-ok {
    color: #22c55e;
    font-weight: 600;
}

.badge-low {
    color: #ef4444;
    font-weight: 600;
}

button[kind="secondary"] {
    border-radius: 10px !important;
}

h1 {
    font-weight: 700;
    letter-spacing: -0.5px;
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

st.title("🧊 Smart Fridge")

# -------------------
# LEDNICE (GRID)
# -------------------
st.subheader("Lednice")

cols = st.columns(3)

for i, (item, amount) in enumerate(data):
    with cols[i % 3]:

        status = "badge-low" if amount == 0 else "badge-ok"
        icon = "🔴" if amount == 0 else "🟢"

        st.markdown(f"""
        <div class="block">
            <div>
                <div class="name">{icon} {item}</div>
                <div class="{status}">{amount} ks</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        if c1.button("➕", key=f"p_{item}"):
            update(item, 1)
            st.rerun()

        if c2.button("➖", key=f"m_{item}"):
            update(item, -1)
            st.rerun()


# -------------------
# 🛒 NÁKUP (GRID)
# -------------------
st.divider()
st.subheader("🛒 Nákupní seznam")

missing = [i for i, a in data if a == 0]

if missing:
    cols2 = st.columns(3)

    for i, item in enumerate(missing):
        with cols2[i % 3]:
            st.markdown(f"""
            <div class="block">
                <div class="name">🛒 {item}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.success("Všechno máme 🎉")


# -------------------
# ➕ PŘIDÁNÍ
# -------------------
st.divider()
st.subheader("➕ Přidat potravinu")

new_item = st.text_input("Název potraviny")

if st.button("Přidat"):
    if new_item:
        add_item(new_item)
        st.rerun()

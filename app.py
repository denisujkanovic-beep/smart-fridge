import streamlit as st
import sqlite3

# -------------------
# 1. DATABÁZOVÁ LOGIKA (Integrovaná přímo zde)
# -------------------
def get_conn():
    return sqlite3.connect("fridge.db", check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS fridge (
        item TEXT PRIMARY KEY,
        amount INTEGER
    )
    """)
    # Přidání výchozích dat, pokud je tabulka prázdná
    c.execute("SELECT COUNT(*) FROM fridge")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO fridge VALUES (?, ?)", [
            ("Mléko", 2),
            ("Máslo", 1),
            ("Vejce", 6),
            ("Šunka", 0),
            ("Sýr", 0)
        ])
    conn.commit()
    conn.close()

def load_data():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT item, amount FROM fridge ORDER BY item ASC")
    data = c.fetchall()
    conn.close()
    return data

def update_amount(item, delta):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE fridge SET amount = MAX(amount + ?, 0) WHERE item = ?", (delta, item))
    conn.commit()
    conn.close()

def add_item(name):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO fridge (item, amount) VALUES (?, 0)", (name.strip(),))
    conn.commit()
    conn.close()

def delete_item(item):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM fridge WHERE item = ?", (item,))
    conn.commit()
    conn.close()

# Inicializace DB při startu
init_db()

# -------------------
# 2. KONFIGURACE STRÁNKY
# -------------------
st.set_page_config(page_title="Potraviny", page_icon="🛒", layout="centered")

st.markdown("""
<style>
    .block-container { max-width: 800px; padding-top: 2rem; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* Úprava mezer mezi kartami */
    [data-testid="stVerticalBlock"] > div { margin-bottom: -5px; }
</style>
""", unsafe_allow_html=True)

# -------------------
# 3. HLAVNÍ UI
# -------------------
st.title("Seznam potravin :-)")
st.caption("Aby se Denis a Anett furt nehádali..")

# Načtení dat
data = load_data()

tab1, tab2 = st.tabs(["📋 Co máme doma", "🛒 Nákupní seznam"])

# --- TAB 1: INVENTÁŘ (2 SLOUPCE) ---
with tab1:
    # Sekce pro přidávání
    with st.expander("➕ Přidat novou věc do seznamu"):
        col_in, col_bt = st.columns([3, 1], vertical_alignment="bottom")
        with col_in:
            new_item = st.text_input("Název", placeholder="Např. Jogurt...", label_visibility="collapsed")
        with col_bt:
            if st.button("Přidat", use_container_width=True, type="primary"):
                if new_item:
                    add_item(new_item)
                    st.rerun()

    st.write("") # Mezera

    if not data:
        st.info("Seznam je prázdný.")
    else:
        # ROZDĚLENÍ DO DVOU SLOUPCŮ
        col_left, col_right = st.columns(2)
        
        for i, (item, amount) in enumerate(data):
            # Střídáme sloupce (sudé vlevo, liché vpravo)
            target_col = col_left if i % 2 == 0 else col_right
            
            with target_col:
                with st.container(border=True):
                    # Zmenšíme popis a tlačítka, aby se to vešlo vedle sebe v úzkém sloupci
                    c1, c2, c3, c4 = st.columns([2, 1, 1, 1], vertical_alignment="center")
                    
                    with c1:
                        st.markdown(f"**{item}**")
                        color = "#16a34a" if amount > 0 else "#ef4444"
                        st.markdown(f"<span style='color:{color}; font-size:12px;'>Kusů: {amount}</span>", unsafe_allow_html=True)

                    with c2:
                        if st.button("−", key=f"m_{item}", use_container_width=True):
                            update_amount(item, -1)
                            st.rerun()
                    with c3:
                        if st.button("＋", key=f"p_{item}", use_container_width=True):
                            update_amount(item, 1)
                            st.rerun()
                    with c4:
                        if st.button("🗑️", key=f"d_{item}", use_container_width=True):
                            delete_item(item)
                            st.rerun()

# --- TAB 2: NÁKUPNÍ SEZNAM ---
with tab2:
    missing = [item for item, amount in data if amount == 0]

    if missing:
        st.subheader("Co koupit: ")
        # Zobrazení nákupu v mřížce
        shop_cols = st.columns(2)
        for i, item in enumerate(missing):
            with shop_cols[i % 2]:
                st.error(f"❌ {item}")
    else:
        # ŽÁDNÉ BALÓNKY - jen čistá zpráva
        st.success("Máme všechno! Denis i Anett můžou být v klidu. ✅")

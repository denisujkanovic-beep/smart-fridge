import streamlit as st
from db import get_conn, init

# Inicializace databáze
init()

# -------------------
# KONFIGURACE STRÁNKY
# -------------------
st.set_page_config(
    page_title="Chytrá Lednice", 
    page_icon="🧊", 
    layout="centered" # "centered" je pro mobilní "app" feel lepší než "wide"
)

# Minimalistické CSS pro vyčištění defaultního Streamlit vzhledu
st.markdown("""
<style>
    /* Zúžení kontejneru pro mobilní vzhled */
    .block-container {
        max-width: 600px;
        padding-top: 2rem;
    }
    /* Skrytí defaultního Streamlit menu a patičky pro produkční vzhled */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# -------------------
# DATABÁZOVÉ FUNKCE
# -------------------
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
    # Strip odstraní nechtěné mezery před a za slovem
    c.execute("INSERT OR IGNORE INTO fridge (item, amount) VALUES (?, 0)", (name.strip(),))
    conn.commit()
    conn.close()
    
def delete_item(item):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM fridge WHERE item = ?", (item,))
    conn.commit()
    conn.close()


# -------------------
# HLAVNÍ UI
# -------------------
st.title("🧊 Moje Lednice")
st.markdown("Měj dokonalý přehled o tom, co ti doma chybí.")

# Načtení dat
data = load_data()

# Rozdělení do záložek pro lepší organizaci
tab1, tab2 = st.tabs(["📋 Inventář", "🛒 Nákupní seznam"])

# --- ZÁLOŽKA 1: INVENTÁŘ A PŘIDÁVÁNÍ ---
with tab1:
    
    # 1. Přidávací sekce nahoře
    st.subheader("Přidat novou položku")
    col_input, col_btn = st.columns([3, 1], vertical_alignment="bottom")
    
    with col_input:
        new_item = st.text_input("Název položky", placeholder="Např. Mléko, Vajíčka...", label_visibility="collapsed")
    with col_btn:
        if st.button("➕ Přidat", use_container_width=True, type="primary"):
            if new_item:
                add_item(new_item)
                st.toast(f"Položka '{new_item}' byla přidána! ✅")
                st.rerun()

    st.divider()

    # 2. Výpis položek
    if not data:
        st.info("Tvoje lednice je zatím prázdná. Přidej první položku výše 👆")
    else:
        for item, amount in data:
            # Využití nativního kontejneru s ohraničením (nahrazuje tvůj div class="card")
            with st.container(border=True):
                # vertical_alignment="center" zajistí, že text a tlačítka nelítají nahoru a dolů
                c1, c2, c3, c4 = st.columns([4, 1, 1, 1], vertical_alignment="center")

                with c1:
                    # Vizuální odlišení stavu přímo v markdownu
                    if amount == 0:
                        st.markdown(f"**{item}**<br>🔴 <span style='color:#ef4444; font-size:12px;'>Došlo</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"**{item}**<br>🟢 <span style='color:#16a34a; font-size:12px;'>Kusů: {amount}</span>", unsafe_allow_html=True)

                with c2:
                    if st.button("➖", key=f"m_{item}", use_container_width=True):
                        update_amount(item, -1)
                        st.rerun()

                with c3:
                    if st.button("➕", key=f"p_{item}", use_container_width=True):
                        update_amount(item, 1)
                        st.rerun()
                        
                with c4:
                    if st.button("🗑️", key=f"d_{item}", use_container_width=True):
                        delete_item(item)
                        st.toast(f"Položka '{item}' smazána.")
                        st.rerun()


# --- ZÁLOŽKA 2: NÁKUPNÍ SEZNAM ---
with tab2:
    missing = [item for item, amount in data if amount == 0]

    if missing:
        st.subheader("Tohle musíš koupit:")
        # Grid layout pro nákupní seznam
        cols = st.columns(3)
        for i, item in enumerate(missing):
            with cols[i % 3]:
                # Použití st.error pro červený "warning" look kartičky
                st.error(f"🛒 **{item}**")
                
    else:
        st.success("Všechno máme! 🎉 Žádný nákup není potřeba.")
        st.balloons() # Malý easter egg pro radost, když je nakoupeno

#!/usr/bin/env python3
"""
Dashboard Matematico Prop/Broker - Applicazione Principale
Dashboard per la gestione di broker, prop firm, wallet, pack copiatori e gruppi PAMM
Creato da Ezio Camporeale
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Aggiungi il percorso della directory corrente al path di Python
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from config import APP_TITLE, APP_ICON, PAGE_ICON, CUSTOM_COLORS
from database.supabase_manager import SupabaseManager
from components.crud_table import CRUDTable
from components.crud_form import CRUDForm
from components.auth_manager import AuthManager
from components.login_form import render_auth_guard, check_permissions

# Configurazione pagina
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        border-radius: 15px;
    }
    .header-content {
        position: relative;
        z-index: 2;
    }
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #2E86AB;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #2E86AB;
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

def render_header():
    """Renderizza l'header dell'applicazione"""
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="header-title">🧮 DASH_PROP_BROKER</div>
            <div class="header-subtitle">Dashboard Matematico per la Gestione di Broker, Prop Firm, Wallet e PAMM</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard():
    """Renderizza la dashboard principale"""
    
    # Inizializza il Supabase manager
    supabase_manager = SupabaseManager()
    
    if not supabase_manager.is_configured:
        st.error("❌ Supabase non configurato. Controlla le variabili d'ambiente.")
        return
    
    # Ottieni statistiche
    stats = supabase_manager.get_statistiche_generali()
    
    # Header della dashboard
    st.markdown("## 📊 Dashboard Principale")
    st.markdown("Panoramica generale su broker, prop firm, wallet e gruppi PAMM")
    
    # Metriche principali
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats.get('broker_attivi', 0)}</div>
            <div class="metric-label">Broker Attivi</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats.get('prop_attive', 0)}</div>
            <div class="metric-label">Prop Attive</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats.get('wallet_attivi', 0)}</div>
            <div class="metric-label">Wallet Attivi</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats.get('pack_copiatori_attivi', 0)}</div>
            <div class="metric-label">Pack Copiatori</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats.get('gruppi_pamm_attivi', 0)}</div>
            <div class="metric-label">Gruppi PAMM</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Grafici
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Distribuzione Broker per Regolamentazione")
        brokers = supabase_manager.get_brokers()
        if brokers:
            df_brokers = pd.DataFrame(brokers)
            if 'regolamentazione' in df_brokers.columns:
                reg_counts = df_brokers['regolamentazione'].value_counts()
                fig_reg = px.pie(
                    values=reg_counts.values,
                    names=reg_counts.index,
                    title="Broker per Regolamentazione"
                )
                st.plotly_chart(fig_reg, width='stretch')
            else:
                st.info("Nessun dato di regolamentazione disponibile")
        else:
            st.info("Nessun broker disponibile")
    
    with col2:
        st.markdown("### 📊 Performance Prop Firm")
        props = supabase_manager.get_props()
        if props:
            df_props = pd.DataFrame(props)
            if 'profit_target' in df_props.columns:
                fig_props = px.bar(
                    df_props,
                    x='nome_prop',
                    y='profit_target',
                    title="Profit Target per Prop Firm"
                )
                st.plotly_chart(fig_props, width='stretch')
            else:
                st.info("Nessun dato di performance disponibile")
        else:
            st.info("Nessuna prop firm disponibile")

def render_brokers_page():
    """Renderizza la pagina di gestione broker"""
    st.markdown("## 🏢 Gestione Broker")
    st.markdown("Gestisci i broker e le loro informazioni")
    
    supabase_manager = SupabaseManager()
    
    # Tab per organizzare le funzionalità
    tab_lista, tab_aggiungi, tab_modifica = st.tabs(["📋 Lista Broker", "➕ Aggiungi Broker", "✏️ Modifica/Elimina"])
    
    with tab_lista:
        brokers = supabase_manager.get_brokers()
        if brokers:
            df_brokers = pd.DataFrame(brokers)
            st.dataframe(df_brokers, width='stretch')
        else:
            st.info("Nessun broker presente nel database")
    
    with tab_modifica:
        st.markdown("### ✏️ Modifica o Elimina Broker")
        
        brokers = supabase_manager.get_brokers()
        if brokers:
            # Configurazione colonne per la tabella
            columns_config = {
                "id": st.column_config.TextColumn("ID", width=80),
                "nome_broker": st.column_config.TextColumn("Nome Broker", width=150),
                "tipo_broker": st.column_config.TextColumn("Tipo", width=100),
                "regolamentazione": st.column_config.TextColumn("Regolamentazione", width=120),
                "paese": st.column_config.TextColumn("Paese", width=100),
                "stato": st.column_config.TextColumn("Stato", width=100),
                "created_at": st.column_config.TextColumn("Creato", width=120)
            }
            
            # Usa il componente CRUD Table
            crud_table = CRUDTable("Broker Disponibili")
            selected_broker = crud_table.render_table_with_selection(
                data=brokers,
                columns_config=columns_config,
                on_edit=lambda data: handle_edit_broker(data),
                on_delete=lambda data: handle_delete_broker(data),
                key_prefix="broker_table"
            )
        else:
            st.info("Nessun broker presente nel database")
    
    with tab_aggiungi:
        st.markdown("### ➕ Aggiungi Nuovo Broker")
        
        with st.form("broker_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_broker = st.text_input("Nome Broker *", placeholder="Es: IC Markets")
                tipo_broker = st.selectbox("Tipo Broker", ["ECN", "STP", "Market Maker", "NDD", "Altro"])
                regolamentazione = st.text_input("Regolamentazione", placeholder="Es: ASIC, FCA, CySEC")
                paese = st.text_input("Paese", placeholder="Es: Australia")
                sito_web = st.text_input("Sito Web", placeholder="https://...")
            
            with col2:
                spread_minimo = st.number_input("Spread Minimo", min_value=0.0, value=0.0, step=0.1)
                commissioni = st.number_input("Commissioni", min_value=0.0, value=0.0, step=0.1)
                leverage_massimo = st.number_input("Leverage Massimo", min_value=1, value=500, step=1)
                deposito_minimo = st.number_input("Deposito Minimo", min_value=0.0, value=0.0, step=10.0)
                stato = st.selectbox("Stato", ["Attivo", "Inattivo", "Sospeso", "Bloccato"])
            
            note = st.text_area("Note", placeholder="Note aggiuntive...")
            
            submitted = st.form_submit_button("💾 Salva Broker", type="primary")
            
            if submitted:
                if nome_broker:
                    broker_data = {
                        'nome_broker': nome_broker,
                        'tipo_broker': tipo_broker,
                        'regolamentazione': regolamentazione,
                        'paese': paese,
                        'sito_web': sito_web,
                        'spread_minimo': spread_minimo,
                        'commissioni': commissioni,
                        'leverage_massimo': leverage_massimo,
                        'deposito_minimo': deposito_minimo,
                        'stato': stato,
                        'note': note,
                        'creato_da': 'admin'
                    }
                    
                    success, message = supabase_manager.add_broker(broker_data)
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Il nome del broker è obbligatorio")

def render_props_page():
    """Renderizza la pagina di gestione prop firm"""
    st.markdown("## 🏛️ Gestione Prop Firm")
    st.markdown("Gestisci le prop firm e le loro configurazioni")
    
    supabase_manager = SupabaseManager()
    
    # Tab per organizzare le funzionalità
    tab_lista, tab_aggiungi, tab_modifica = st.tabs(["📋 Lista Prop Firm", "➕ Aggiungi Prop Firm", "✏️ Modifica/Elimina"])
    
    with tab_lista:
        props = supabase_manager.get_props()
        if props:
            df_props = pd.DataFrame(props)
            st.dataframe(df_props, width='stretch')
        else:
            st.info("Nessuna prop firm presente nel database")
    
    with tab_modifica:
        st.markdown("### ✏️ Modifica o Elimina Prop Firm")
        
        props = supabase_manager.get_props()
        if props:
            # Configurazione colonne per la tabella
            columns_config = {
                "id": st.column_config.TextColumn("ID", width=80),
                "nome_prop": st.column_config.TextColumn("Nome Prop Firm", width=150),
                "tipo_prop": st.column_config.TextColumn("Tipo", width=120),
                "capitale_iniziale": st.column_config.TextColumn("Capitale Iniziale", width=120),
                "profit_target": st.column_config.TextColumn("Profit Target", width=120),
                "stato": st.column_config.TextColumn("Stato", width=100),
                "created_at": st.column_config.TextColumn("Creato", width=120)
            }
            
            # Usa il componente CRUD Table
            crud_table = CRUDTable("Prop Firm Disponibili")
            selected_prop = crud_table.render_table_with_selection(
                data=props,
                columns_config=columns_config,
                on_edit=lambda data: handle_edit_prop(data),
                on_delete=lambda data: handle_delete_prop(data),
                key_prefix="prop_table"
            )
        else:
            st.info("Nessuna prop firm presente nel database")
    
    with tab_aggiungi:
        st.markdown("### ➕ Aggiungi Nuova Prop Firm")
        
        with st.form("prop_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_prop = st.text_input("Nome Prop Firm *", placeholder="Es: FTMO")
                tipo_prop = st.selectbox("Tipo Prop", ["Evaluation", "Instant Funding", "Express", "Altro"])
                capitale_iniziale = st.number_input("Capitale Iniziale", min_value=0.0, value=10000.0, step=1000.0)
                drawdown_massimo = st.number_input("Drawdown Massimo (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
                profit_target = st.number_input("Profit Target (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
            
            with col2:
                commissioni = st.number_input("Commissioni", min_value=0.0, value=0.0, step=0.1)
                fee_mensile = st.number_input("Fee Mensile", min_value=0.0, value=0.0, step=10.0)
                stato = st.selectbox("Stato", ["Attiva", "Inattiva", "In Verifica", "Rifiutata"])
                regole_trading = st.text_area("Regole Trading", placeholder="Regole specifiche...")
                restrizioni_orarie = st.text_input("Restrizioni Orarie", placeholder="Es: Solo durante sessioni principali")
            
            note = st.text_area("Note", placeholder="Note aggiuntive...")
            
            submitted = st.form_submit_button("💾 Salva Prop Firm", type="primary")
            
            if submitted:
                if nome_prop:
                    prop_data = {
                        'nome_prop': nome_prop,
                        'tipo_prop': tipo_prop,
                        'capitale_iniziale': capitale_iniziale,
                        'drawdown_massimo': drawdown_massimo,
                        'profit_target': profit_target,
                        'commissioni': commissioni,
                        'fee_mensile': fee_mensile,
                        'stato': stato,
                        'regole_trading': regole_trading,
                        'restrizioni_orarie': restrizioni_orarie,
                        'note': note,
                        'creato_da': 'admin'
                    }
                    
                    success, message = supabase_manager.add_prop(prop_data)
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Il nome della prop firm è obbligatorio")

def render_wallets_page():
    """Renderizza la pagina di gestione wallet"""
    st.markdown("## 💰 Gestione Wallet")
    st.markdown("Gestisci i wallet e le loro informazioni")
    
    supabase_manager = SupabaseManager()
    
    # Tab per organizzare le funzionalità
    tab_lista, tab_aggiungi, tab_modifica = st.tabs(["📋 Lista Wallet", "➕ Aggiungi Wallet", "✏️ Modifica/Elimina"])
    
    with tab_lista:
        wallets = supabase_manager.get_wallets()
        if wallets:
            df_wallets = pd.DataFrame(wallets)
            # Nascondi informazioni sensibili
            if 'chiave_privata' in df_wallets.columns:
                df_wallets = df_wallets.drop(['chiave_privata', 'frase_seed'], axis=1, errors='ignore')
            st.dataframe(df_wallets, width='stretch')
        else:
            st.info("Nessun wallet presente nel database")
    
    with tab_modifica:
        st.markdown("### ✏️ Modifica o Elimina Wallet")
        
        wallets = supabase_manager.get_wallets()
        if wallets:
            # Configurazione colonne per la tabella
            columns_config = {
                "id": st.column_config.TextColumn("ID", width=80),
                "nome_wallet": st.column_config.TextColumn("Nome Wallet", width=150),
                "tipo_wallet": st.column_config.TextColumn("Tipo", width=120),
                "indirizzo_wallet": st.column_config.TextColumn("Indirizzo", width=200),
                "saldo_attuale": st.column_config.TextColumn("Saldo", width=120),
                "valuta": st.column_config.TextColumn("Valuta", width=80),
                "stato": st.column_config.TextColumn("Stato", width=100),
                "created_at": st.column_config.TextColumn("Creato", width=120)
            }
            
            # Usa il componente CRUD Table
            crud_table = CRUDTable("Wallet Disponibili")
            selected_wallet = crud_table.render_table_with_selection(
                data=wallets,
                columns_config=columns_config,
                on_edit=lambda data: handle_edit_wallet(data),
                on_delete=lambda data: handle_delete_wallet(data),
                key_prefix="wallet_table"
            )
        else:
            st.info("Nessun wallet presente nel database")
    
    with tab_aggiungi:
        st.markdown("### ➕ Aggiungi Nuovo Wallet")
        
        with st.form("wallet_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                indirizzo_wallet = st.text_input("Indirizzo Wallet *", placeholder="Es: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
                tipo_wallet = st.selectbox("Tipo Wallet", ["Bitcoin", "Ethereum", "Tether", "Tron", "Dogecoin", "Litecoin", "Altro"])
                nome_wallet = st.text_input("Nome Wallet", placeholder="Es: Wallet Principale")
                saldo_attuale = st.number_input("Saldo Attuale", min_value=0.0, value=0.0, step=0.001)
                valuta = st.text_input("Valuta", placeholder="Es: BTC, ETH, USDT")
            
            with col2:
                exchange = st.text_input("Exchange", placeholder="Es: Binance, Coinbase")
                stato = st.selectbox("Stato", ["Attivo", "Inattivo", "Sospeso", "Bloccato"])
                chiave_privata = st.text_input("Chiave Privata", type="password", placeholder="Chiave privata (crittografata)")
                frase_seed = st.text_input("Frase Seed", type="password", placeholder="Frase seed (crittografata)")
            
            note = st.text_area("Note", placeholder="Note aggiuntive...")
            
            submitted = st.form_submit_button("💾 Salva Wallet", type="primary")
            
            if submitted:
                if indirizzo_wallet:
                    wallet_data = {
                        'indirizzo_wallet': indirizzo_wallet,
                        'tipo_wallet': tipo_wallet,
                        'nome_wallet': nome_wallet,
                        'saldo_attuale': saldo_attuale,
                        'valuta': valuta,
                        'exchange': exchange,
                        'stato': stato,
                        'chiave_privata': chiave_privata,
                        'frase_seed': frase_seed,
                        'note': note,
                        'creato_da': 'admin'
                    }
                    
                    success, message = supabase_manager.add_wallet(wallet_data)
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ L'indirizzo del wallet è obbligatorio")

def render_pack_copiatori_page():
    """Renderizza la pagina di gestione pack copiatori"""
    st.markdown("## 📦 Gestione Pack Copiatori")
    st.markdown("Gestisci i pack copiatori e le loro configurazioni")
    
    supabase_manager = SupabaseManager()
    
    # Tab per organizzare le funzionalità
    tab_lista, tab_aggiungi, tab_modifica = st.tabs(["📋 Lista Pack Copiatori", "➕ Aggiungi Pack Copiatore", "✏️ Modifica/Elimina"])
    
    with tab_lista:
        packs = supabase_manager.get_pack_copiatori()
        if packs:
            df_packs = pd.DataFrame(packs)
            st.dataframe(df_packs, width='stretch')
        else:
            st.info("Nessun pack copiatore presente nel database")
    
    with tab_modifica:
        st.markdown("### ✏️ Modifica o Elimina Pack Copiatore")
        
        packs = supabase_manager.get_pack_copiatori()
        if packs:
            # Configurazione colonne per la tabella
            columns_config = {
                "id": st.column_config.TextColumn("ID", width=80),
                "numero_pack": st.column_config.TextColumn("Numero Pack", width=150),
                "account_number": st.column_config.TextColumn("Account", width=120),
                "server_broker": st.column_config.TextColumn("Server", width=150),
                "tipo_account": st.column_config.TextColumn("Tipo Account", width=120),
                "saldo_attuale": st.column_config.TextColumn("Saldo", width=120),
                "stato": st.column_config.TextColumn("Stato", width=100),
                "created_at": st.column_config.TextColumn("Creato", width=120)
            }
            
            # Usa il componente CRUD Table
            crud_table = CRUDTable("Pack Copiatori Disponibili")
            selected_pack = crud_table.render_table_with_selection(
                data=packs,
                columns_config=columns_config,
                on_edit=lambda data: handle_edit_pack(data),
                on_delete=lambda data: handle_delete_pack(data),
                key_prefix="pack_table"
            )
        else:
            st.info("Nessun pack copiatore presente nel database")
    
    with tab_aggiungi:
        st.markdown("### ➕ Aggiungi Nuovo Pack Copiatore")
        
        # Ottieni lista broker per il select
        brokers = supabase_manager.get_brokers()
        broker_options = {f"{b['nome_broker']} (ID: {b['id']})": b['id'] for b in brokers}
        
        with st.form("pack_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                numero_pack = st.text_input("Numero Pack *", placeholder="Es: PACK001")
                broker_id = st.selectbox("Broker", options=list(broker_options.keys()))
                account_number = st.text_input("Numero Account", placeholder="Es: 12345678")
                server_broker = st.text_input("Server Broker", placeholder="Es: ICMarketsSC-Demo")
                tipo_account = st.selectbox("Tipo Account", ["Demo", "Live", "Cent", "Micro"])
            
            with col2:
                capitale_iniziale = st.number_input("Capitale Iniziale", min_value=0.0, value=10000.0, step=1000.0)
                saldo_attuale = st.number_input("Saldo Attuale", min_value=0.0, value=10000.0, step=100.0)
                profit_loss = st.number_input("Profit/Loss", value=0.0, step=100.0)
                drawdown_massimo = st.number_input("Drawdown Massimo (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
                stato = st.selectbox("Stato", ["Attivo", "Inattivo", "In Test", "Errore"])
            
            password_account = st.text_input("Password Account", type="password", placeholder="Password account (crittografata)")
            note = st.text_area("Note", placeholder="Note aggiuntive...")
            
            submitted = st.form_submit_button("💾 Salva Pack Copiatore", type="primary")
            
            if submitted:
                if numero_pack:
                    pack_data = {
                        'numero_pack': numero_pack,
                        'broker_id': broker_options[broker_id],
                        'account_number': account_number,
                        'server_broker': server_broker,
                        'tipo_account': tipo_account,
                        'capitale_iniziale': capitale_iniziale,
                        'saldo_attuale': saldo_attuale,
                        'profit_loss': profit_loss,
                        'drawdown_massimo': drawdown_massimo,
                        'stato': stato,
                        'password_account': password_account,
                        'note': note,
                        'creato_da': 'admin'
                    }
                    
                    success, message = supabase_manager.add_pack_copiatore(pack_data)
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Il numero del pack è obbligatorio")

def render_gruppi_pamm_page():
    """Renderizza la pagina di gestione gruppi PAMM"""
    st.markdown("## 👥 Gestione Gruppi PAMM")
    st.markdown("Gestisci i gruppi PAMM e le loro performance")
    
    supabase_manager = SupabaseManager()
    
    # Tab per organizzare le funzionalità
    tab_lista, tab_aggiungi, tab_modifica = st.tabs(["📋 Lista Gruppi PAMM", "➕ Aggiungi Gruppo PAMM", "✏️ Modifica/Elimina"])
    
    with tab_lista:
        gruppi = supabase_manager.get_gruppi_pamm()
        if gruppi:
            df_gruppi = pd.DataFrame(gruppi)
            st.dataframe(df_gruppi, width='stretch')
        else:
            st.info("Nessun gruppo PAMM presente nel database")
    
    with tab_modifica:
        st.markdown("### ✏️ Modifica o Elimina Gruppo PAMM")
        
        gruppi = supabase_manager.get_gruppi_pamm()
        if gruppi:
            # Configurazione colonne per la tabella
            columns_config = {
                "id": st.column_config.TextColumn("ID", width=80),
                "nome_gruppo": st.column_config.TextColumn("Nome Gruppo", width=150),
                "manager": st.column_config.TextColumn("Manager", width=120),
                "account_pamm": st.column_config.TextColumn("Account PAMM", width=120),
                "capitale_totale": st.column_config.TextColumn("Capitale Totale", width=120),
                "performance_totale": st.column_config.TextColumn("Performance", width=120),
                "stato": st.column_config.TextColumn("Stato", width=100),
                "created_at": st.column_config.TextColumn("Creato", width=120)
            }
            
            # Usa il componente CRUD Table
            crud_table = CRUDTable("Gruppi PAMM Disponibili")
            selected_gruppo = crud_table.render_table_with_selection(
                data=gruppi,
                columns_config=columns_config,
                on_edit=lambda data: handle_edit_gruppo(data),
                on_delete=lambda data: handle_delete_gruppo(data),
                key_prefix="gruppo_table"
            )
        else:
            st.info("Nessun gruppo PAMM presente nel database")
    
    with tab_aggiungi:
        st.markdown("### ➕ Aggiungi Nuovo Gruppo PAMM")
        
        # Ottieni lista broker per il select
        brokers = supabase_manager.get_brokers()
        broker_options = {f"{b['nome_broker']} (ID: {b['id']})": b['id'] for b in brokers}
        
        with st.form("gruppo_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_gruppo = st.text_input("Nome Gruppo *", placeholder="Es: Gruppo Alpha")
                manager = st.text_input("Manager", placeholder="Es: Manager Alpha")
                broker_id = st.selectbox("Broker", options=list(broker_options.keys()))
                account_pamm = st.text_input("Account PAMM", placeholder="Es: PAMM001")
                capitale_totale = st.number_input("Capitale Totale", min_value=0.0, value=100000.0, step=10000.0)
            
            with col2:
                numero_partecipanti = st.number_input("Numero Partecipanti", min_value=0, value=0, step=1)
                performance_totale = st.number_input("Performance Totale (%)", value=0.0, step=0.1)
                performance_mensile = st.number_input("Performance Mensile (%)", value=0.0, step=0.1)
                drawdown_massimo = st.number_input("Drawdown Massimo (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
                stato = st.selectbox("Stato", ["Attivo", "Inattivo", "In Gestione", "Chiuso"])
            
            col3, col4 = st.columns(2)
            with col3:
                commissioni_manager = st.number_input("Commissioni Manager (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.1)
            with col4:
                commissioni_broker = st.number_input("Commissioni Broker (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
            
            note = st.text_area("Note", placeholder="Note aggiuntive...")
            
            submitted = st.form_submit_button("💾 Salva Gruppo PAMM", type="primary")
            
            if submitted:
                if nome_gruppo:
                    gruppo_data = {
                        'nome_gruppo': nome_gruppo,
                        'manager': manager,
                        'broker_id': broker_options[broker_id],
                        'account_pamm': account_pamm,
                        'capitale_totale': capitale_totale,
                        'numero_partecipanti': numero_partecipanti,
                        'performance_totale': performance_totale,
                        'performance_mensile': performance_mensile,
                        'drawdown_massimo': drawdown_massimo,
                        'stato': stato,
                        'commissioni_manager': commissioni_manager,
                        'commissioni_broker': commissioni_broker,
                        'note': note,
                        'creato_da': 'admin'
                    }
                    
                    success, message = supabase_manager.add_gruppo_pamm(gruppo_data)
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Il nome del gruppo è obbligatorio")

def render_incroci_page():
    """Renderizza la pagina di gestione incroci"""
    st.markdown("## 🔄 Gestione Incroci")
    st.markdown("Gestisci gli incroci tra broker, prop firm, wallet e gruppi PAMM")
    
    supabase_manager = SupabaseManager()
    
    # Tab per organizzare le funzionalità
    tab_lista, tab_aggiungi, tab_modifica = st.tabs(["📋 Lista Incroci", "➕ Aggiungi Incrocio", "✏️ Modifica/Elimina"])
    
    with tab_lista:
        incroci = supabase_manager.get_incroci()
        if incroci:
            df_incroci = pd.DataFrame(incroci)
            st.dataframe(df_incroci, width='stretch')
        else:
            st.info("Nessun incrocio presente nel database")
    
    with tab_modifica:
        st.markdown("### ✏️ Modifica o Elimina Incrocio")
        
        incroci = supabase_manager.get_incroci()
        if incroci:
            # Configurazione colonne per la tabella
            columns_config = {
                "id": st.column_config.TextColumn("ID", width=80),
                "nome_incrocio": st.column_config.TextColumn("Nome Incrocio", width=150),
                "tipo_incrocio": st.column_config.TextColumn("Tipo", width=120),
                "performance_totale": st.column_config.TextColumn("Performance", width=120),
                "rischio_totale": st.column_config.TextColumn("Rischio", width=120),
                "stato": st.column_config.TextColumn("Stato", width=100),
                "created_at": st.column_config.TextColumn("Creato", width=120)
            }
            
            # Usa il componente CRUD Table
            crud_table = CRUDTable("Incroci Disponibili")
            selected_incrocio = crud_table.render_table_with_selection(
                data=incroci,
                columns_config=columns_config,
                on_edit=lambda data: handle_edit_incrocio(data),
                on_delete=lambda data: handle_delete_incrocio(data),
                key_prefix="incrocio_table"
            )
        else:
            st.info("Nessun incrocio presente nel database")
    
    with tab_aggiungi:
        st.markdown("### ➕ Aggiungi Nuovo Incrocio")
        
        # Ottieni liste per i select
        brokers = supabase_manager.get_brokers()
        props = supabase_manager.get_props()
        wallets = supabase_manager.get_wallets()
        gruppi = supabase_manager.get_gruppi_pamm()
        packs = supabase_manager.get_pack_copiatori()
        
        broker_options = {f"{b['nome_broker']} (ID: {b['id']})": b['id'] for b in brokers}
        prop_options = {f"{p['nome_prop']} (ID: {p['id']})": p['id'] for p in props}
        wallet_options = {f"{w['nome_wallet']} (ID: {w['id']})": w['id'] for w in wallets}
        gruppo_options = {f"{g['nome_gruppo']} (ID: {g['id']})": g['id'] for g in gruppi}
        pack_options = {f"{p['numero_pack']} (ID: {p['id']})": p['id'] for p in packs}
        
        with st.form("incrocio_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_incrocio = st.text_input("Nome Incrocio *", placeholder="Es: Incrocio Alpha")
                broker_id = st.selectbox("Broker", options=list(broker_options.keys()))
                prop_id = st.selectbox("Prop Firm", options=list(prop_options.keys()))
                wallet_id = st.selectbox("Wallet", options=list(wallet_options.keys()))
            
            with col2:
                gruppo_pamm_id = st.selectbox("Gruppo PAMM", options=list(gruppo_options.keys()))
                pack_copiatore_id = st.selectbox("Pack Copiatore", options=list(pack_options.keys()))
                tipo_incrocio = st.text_input("Tipo Incrocio", placeholder="Es: Broker-Prop-Wallet-PAMM-Pack")
                performance_totale = st.number_input("Performance Totale (%)", value=0.0, step=0.1)
            
            rischio_totale = st.number_input("Rischio Totale (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
            stato = st.selectbox("Stato", ["Attivo", "Inattivo", "In Test", "Chiuso"])
            descrizione = st.text_area("Descrizione", placeholder="Descrizione dell'incrocio...")
            note = st.text_area("Note", placeholder="Note aggiuntive...")
            
            submitted = st.form_submit_button("💾 Salva Incrocio", type="primary")
            
            if submitted:
                if nome_incrocio:
                    incrocio_data = {
                        'nome_incrocio': nome_incrocio,
                        'broker_id': broker_options[broker_id],
                        'prop_id': prop_options[prop_id],
                        'wallet_id': wallet_options[wallet_id],
                        'gruppo_pamm_id': gruppo_options[gruppo_pamm_id],
                        'pack_copiatore_id': pack_options[pack_copiatore_id],
                        'tipo_incrocio': tipo_incrocio,
                        'performance_totale': performance_totale,
                        'rischio_totale': rischio_totale,
                        'stato': stato,
                        'descrizione': descrizione,
                        'note': note,
                        'creato_da': 'admin'
                    }
                    
                    success, message = supabase_manager.add_incrocio(incrocio_data)
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Il nome dell'incrocio è obbligatorio")

def render_users_page():
    """Renderizza la pagina di gestione utenti"""
    # Verifica permessi admin (solo Admin può gestire utenti)
    check_permissions(required_roles=['Admin'])
    
    st.markdown("### 👤 Gestione Utenti")
    
    # Tabs per gestione utenti
    tab1, tab2, tab3 = st.tabs(["👥 Lista Utenti", "➕ Nuovo Utente", "✏️ Modifica/Elimina"])
    
    with tab1:
        st.markdown("#### 📋 Lista Utenti")
        
        # Ottieni tutti gli utenti
        supabase_manager = SupabaseManager()
        users = supabase_manager.get_all_users()
        
        if users:
            # Crea DataFrame per visualizzazione
            import pandas as pd
            
            # Prepara i dati per la visualizzazione
            users_data = []
            for user in users:
                # Ottieni il nome del ruolo
                role_name = "N/A"
                if user.get('role_id'):
                    role = supabase_manager.get_role_by_id(user['role_id'])
                    if role:
                        role_name = role['name']
                
                users_data.append({
                    'ID': user['id'],
                    'Username': user['username'],
                    'Nome': f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(),
                    'Email': user['email'],
                    'Ruolo': role_name,
                    'Attivo': '✅' if user.get('is_active') else '❌',
                    'Admin': '✅' if user.get('is_admin') else '❌',
                    'Ultimo Login': user.get('last_login', 'N/A')
                })
            
            df = pd.DataFrame(users_data)
            st.dataframe(df, width='stretch')
        else:
            st.warning("Nessun utente trovato")
    
    with tab2:
        st.markdown("#### ➕ Crea Nuovo Utente")
        
        with st.form("create_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("👤 Username", placeholder="Inserisci username")
                email = st.text_input("📧 Email", placeholder="Inserisci email")
                password = st.text_input("🔒 Password", type="password", placeholder="Inserisci password")
                first_name = st.text_input("👤 Nome", placeholder="Inserisci nome")
            
            with col2:
                last_name = st.text_input("👤 Cognome", placeholder="Inserisci cognome")
                phone = st.text_input("📞 Telefono", placeholder="Inserisci telefono")
                
                # Selezione ruolo
                roles = supabase_manager.get_all_roles()
                role_options = {role['name']: role['id'] for role in roles}
                selected_role = st.selectbox("🎭 Ruolo", options=list(role_options.keys()))
                
                col_active, col_admin = st.columns(2)
                with col_active:
                    is_active = st.checkbox("✅ Attivo", value=True)
                with col_admin:
                    is_admin = st.checkbox("👑 Admin", value=False)
            
            notes = st.text_area("📝 Note", placeholder="Note aggiuntive")
            
            if st.form_submit_button("➕ Crea Utente", type="primary"):
                if username and email and password:
                    # Hash della password
                    auth_manager = AuthManager()
                    
                    user_data = {
                        'username': username,
                        'email': email,
                        'password_hash': auth_manager.hash_password(password),
                        'first_name': first_name,
                        'last_name': last_name,
                        'phone': phone,
                        'role_id': role_options[selected_role],
                        'is_active': is_active,
                        'is_admin': is_admin,
                        'notes': notes
                    }
                    
                    success, message = supabase_manager.create_user(user_data)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("❌ Username, email e password sono obbligatori")
    
    with tab3:
        st.markdown("#### ✏️ Modifica/Elimina Utenti")
        
        if users:
            # Selezione utente
            user_options = {f"{user['username']} ({user['first_name']} {user['last_name']})": user for user in users}
            selected_user_name = st.selectbox("Seleziona utente da modificare/eliminare:", list(user_options.keys()))
            
            if selected_user_name:
                selected_user = user_options[selected_user_name]
                
                st.markdown("#### 📋 Dettagli Utente Selezionato")
                
                # Mostra dettagli utente
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Username:** {selected_user['username']}")
                    st.write(f"**Email:** {selected_user['email']}")
                    st.write(f"**Nome:** {selected_user.get('first_name', 'N/A')} {selected_user.get('last_name', 'N/A')}")
                    st.write(f"**Telefono:** {selected_user.get('phone', 'N/A')}")
                
                with col2:
                    # Ruolo
                    role_name = "N/A"
                    if selected_user.get('role_id'):
                        role = supabase_manager.get_role_by_id(selected_user['role_id'])
                        if role:
                            role_name = role['name']
                    st.write(f"**Ruolo:** {role_name}")
                    st.write(f"**Attivo:** {'✅' if selected_user.get('is_active') else '❌'}")
                    st.write(f"**Admin:** {'✅' if selected_user.get('is_admin') else '❌'}")
                    st.write(f"**Ultimo Login:** {selected_user.get('last_login', 'N/A')}")
                
                # Pulsanti azione
                col_edit, col_delete = st.columns(2)
                
                with col_edit:
                    if st.button("✏️ Modifica", width='stretch'):
                        st.session_state['editing_user'] = selected_user
                        st.rerun()
                
                with col_delete:
                    if st.button("🗑️ Elimina", width='stretch'):
                        st.session_state['deleting_user'] = selected_user
                        st.rerun()
        else:
            st.warning("Nessun utente disponibile per la modifica")

def render_settings_page():
    """Renderizza la pagina delle impostazioni"""
    st.markdown("## ⚙️ Impostazioni Sistema")
    st.info("🚀 **CONFIGURAZIONE SUPABASE**: Gestisci sistema remoto, sicurezza e configurazione")
    
    # Tab per organizzare le impostazioni
    tab_supabase, tab_system = st.tabs(["🚀 Supabase", "ℹ️ Sistema"])
    
    # TAB 1: Supabase
    with tab_supabase:
        st.subheader("🚀 Gestione Supabase")
        st.info("📊 **DATABASE REMOTO**: Tutti i dati sono sincronizzati automaticamente con Supabase")
        
        # Stato Supabase
        supabase_manager = SupabaseManager()
        
        if supabase_manager.is_configured:
            st.success("✅ **SUPABASE ATTIVO** - Configurazione corretta")
            
            # Statistiche Supabase
            stats = supabase_manager.get_statistiche_generali()
            
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                st.metric("🏢 Broker", stats.get('broker_attivi', 0))
            with col_stats2:
                st.metric("🏛️ Prop Firm", stats.get('prop_attive', 0))
            with col_stats3:
                st.metric("💰 Wallet", stats.get('wallet_attivi', 0))
            
            col_stats4, col_stats5, col_stats6 = st.columns(3)
            with col_stats4:
                st.metric("📦 Pack Copiatori", stats.get('pack_copiatori_attivi', 0))
            with col_stats5:
                st.metric("👥 Gruppi PAMM", stats.get('gruppi_pamm_attivi', 0))
            with col_stats6:
                st.metric("🔄 Incroci", stats.get('incroci_totali', 0))
            
            # Test connessione
            st.markdown("---")
            st.subheader("🧪 Test Connessione")
            if st.button("🔍 Test Supabase", type="primary"):
                success, message = supabase_manager.test_connection()
                if success:
                    st.success(f"✅ **{message}**")
                else:
                    st.error(f"❌ **{message}**")
        else:
            st.error("❌ **SUPABASE NON CONFIGURATO** - Controlla le variabili d'ambiente")
    
    # TAB 2: Sistema
    with tab_system:
        st.subheader("ℹ️ Informazioni Sistema")
        st.info("📋 **STATO APPLICAZIONE**: Monitora lo stato generale del sistema")
        
        # Informazioni generali
        col_sys1, col_sys2 = st.columns(2)
        
        with col_sys1:
            st.write("**🖥️ Ambiente:**")
            st.write(f"• **OS:** {sys.platform}")
            st.write(f"• **Python:** {sys.version.split()[0]}")
            st.write(f"• **Streamlit:** {st.__version__}")
        
        with col_sys2:
            st.write("**📊 Componenti:**")
            st.write("• ✅ SupabaseManager")
            st.write("• ✅ Modelli Dati") 
            st.write("• ✅ Dashboard Streamlit")
            st.write("• ✅ Sistema CRUD")

# ==================== FUNZIONI DI GESTIONE CRUD ====================

def handle_edit_broker(broker_data):
    """Gestisce la modifica di un broker"""
    st.session_state['editing_broker'] = broker_data
    st.rerun()

def handle_delete_broker(broker_data):
    """Gestisce l'eliminazione di un broker"""
    st.session_state['deleting_broker'] = broker_data
    st.rerun()

def handle_edit_prop(prop_data):
    """Gestisce la modifica di una prop firm"""
    st.session_state['editing_prop'] = prop_data
    st.rerun()

def handle_delete_prop(prop_data):
    """Gestisce l'eliminazione di una prop firm"""
    st.session_state['deleting_prop'] = prop_data
    st.rerun()

def handle_edit_wallet(wallet_data):
    """Gestisce la modifica di un wallet"""
    st.session_state['editing_wallet'] = wallet_data
    st.rerun()

def handle_delete_wallet(wallet_data):
    """Gestisce l'eliminazione di un wallet"""
    st.session_state['deleting_wallet'] = wallet_data
    st.rerun()

def handle_edit_pack(pack_data):
    """Gestisce la modifica di un pack copiatore"""
    st.session_state['editing_pack'] = pack_data
    st.rerun()

def handle_delete_pack(pack_data):
    """Gestisce l'eliminazione di un pack copiatore"""
    st.session_state['deleting_pack'] = pack_data
    st.rerun()

def handle_edit_gruppo(gruppo_data):
    """Gestisce la modifica di un gruppo PAMM"""
    st.session_state['editing_gruppo'] = gruppo_data
    st.rerun()

def handle_delete_gruppo(gruppo_data):
    """Gestisce l'eliminazione di un gruppo PAMM"""
    st.session_state['deleting_gruppo'] = gruppo_data
    st.rerun()

def handle_edit_incrocio(incrocio_data):
    """Gestisce la modifica di un incrocio"""
    st.session_state['editing_incrocio'] = incrocio_data
    st.rerun()

def handle_delete_incrocio(incrocio_data):
    """Gestisce l'eliminazione di un incrocio"""
    st.session_state['deleting_incrocio'] = incrocio_data
    st.rerun()

def main():
    """Funzione principale dell'applicazione"""
    
    # Renderizza header (sempre visibile)
    render_header()
    
    # Verifica autenticazione
    render_auth_guard()
    
    # Menu di navigazione - SPOSTATO PRIMA DEI MODAL PER EVITARE PROBLEMI DOPO RERUN
    from streamlit_option_menu import option_menu
    
    # Mantieni la selezione del menu anche dopo rerun
    if 'selected_menu' not in st.session_state:
        st.session_state['selected_menu'] = "📊 Dashboard"
    
    selected = option_menu(
        menu_title=None,
        options=[
            "📊 Dashboard", 
            "🏢 Broker", 
            "🏛️ Prop Firm", 
            "💰 Wallet", 
            "📦 Pack Copiatori", 
            "👥 Gruppi PAMM", 
            "🔄 Incroci", 
            "👤 Gestione Utenti",
            "⚙️ Impostazioni"
        ],
        icons=["house", "building", "bank", "wallet", "box", "people", "arrows-collapse", "person", "gear"],
        orientation="horizontal",
        default_index=0,  # Default al Dashboard
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        },
        key="main_navigation_menu"  # Chiave unica per il menu
    )
    
    # Aggiorna lo stato del menu selezionato
    st.session_state['selected_menu'] = selected
    
    # Gestione modal di modifica ed eliminazione
    supabase_manager = SupabaseManager()
    
    # Modal modifica broker
    if 'editing_broker' in st.session_state:
        broker_data = st.session_state['editing_broker']
        st.markdown("### ✏️ Modifica Broker")
        
        # Configurazione campi per il form
        fields_config = {
            'nome_broker': {'type': 'text', 'label': 'Nome Broker', 'required': True},
            'tipo_broker': {'type': 'select', 'label': 'Tipo Broker', 'options': ['ECN', 'STP', 'Market Maker', 'NDD', 'Altro']},
            'regolamentazione': {'type': 'text', 'label': 'Regolamentazione'},
            'paese': {'type': 'text', 'label': 'Paese'},
            'sito_web': {'type': 'text', 'label': 'Sito Web'},
            'spread_minimo': {'type': 'number', 'label': 'Spread Minimo'},
            'commissioni': {'type': 'number', 'label': 'Commissioni'},
            'leverage_massimo': {'type': 'number', 'label': 'Leverage Massimo'},
            'deposito_minimo': {'type': 'number', 'label': 'Deposito Minimo'},
            'stato': {'type': 'select', 'label': 'Stato', 'options': ['Attivo', 'Inattivo', 'Sospeso', 'Bloccato']},
            'note': {'type': 'textarea', 'label': 'Note'}
        }
        
        crud_form = CRUDForm("Modifica Broker")
        
        def handle_broker_update(form_data, mode):
            """Gestisce l'aggiornamento broker e chiude il modal se riuscito"""
            success, message = supabase_manager.update_broker(broker_data['id'], form_data)
            if success:
                # Chiudi il modal di modifica
                del st.session_state['editing_broker']
                st.success(message)
                st.rerun()
                return True
            else:
                st.error(message)
                return False
        
        result = crud_form.render_form(
            fields_config=fields_config,
            data=broker_data,
            mode="edit",
            on_submit=handle_broker_update,
            key_prefix="edit_broker"
        )
        
        if st.button("❌ Annulla Modifica"):
            del st.session_state['editing_broker']
            st.rerun()
    
    # Modal eliminazione broker
    elif 'deleting_broker' in st.session_state:
        broker_data = st.session_state['deleting_broker']
        st.markdown("### 🗑️ Elimina Broker")
        st.warning(f"⚠️ Sei sicuro di voler eliminare il broker **{broker_data['nome_broker']}**?")
        st.write(f"**ID:** {broker_data['id']}")
        st.write(f"**Tipo:** {broker_data.get('tipo_broker', 'N/A')}")
        st.write(f"**Regolamentazione:** {broker_data.get('regolamentazione', 'N/A')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Conferma Eliminazione", type="primary"):
                success, message = supabase_manager.delete_broker(broker_data['id'])
                if success:
                    st.success(f"✅ {message}")
                    del st.session_state['deleting_broker']
                    # Mantieni la sezione corrente dopo eliminazione
                    st.session_state['selected_menu'] = "🏢 Broker"
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        with col2:
            if st.button("❌ Annulla"):
                del st.session_state['deleting_broker']
                st.rerun()
    
    # Modal modifica prop firm
    elif 'editing_prop' in st.session_state:
        prop_data = st.session_state['editing_prop']
        st.markdown("### ✏️ Modifica Prop Firm")
        
        # Configurazione campi per il form
        fields_config = {
            'nome_prop': {'type': 'text', 'label': 'Nome Prop Firm', 'required': True},
            'tipo_prop': {'type': 'select', 'label': 'Tipo Prop', 'options': ['Evaluation', 'Instant Funding', 'Express', 'Altro']},
            'capitale_iniziale': {'type': 'number', 'label': 'Capitale Iniziale'},
            'drawdown_massimo': {'type': 'number', 'label': 'Drawdown Massimo (%)'},
            'profit_target': {'type': 'number', 'label': 'Profit Target (%)'},
            'commissioni': {'type': 'number', 'label': 'Commissioni'},
            'fee_mensile': {'type': 'number', 'label': 'Fee Mensile'},
            'stato': {'type': 'select', 'label': 'Stato', 'options': ['Attiva', 'Inattiva', 'In Verifica', 'Rifiutata']},
            'regole_trading': {'type': 'textarea', 'label': 'Regole Trading'},
            'restrizioni_orarie': {'type': 'text', 'label': 'Restrizioni Orarie'},
            'note': {'type': 'textarea', 'label': 'Note'}
        }
        
        crud_form = CRUDForm("Modifica Prop Firm")
        
        def handle_prop_update(form_data, mode):
            """Gestisce l'aggiornamento prop firm e chiude il modal se riuscito"""
            success, message = supabase_manager.update_prop(prop_data['id'], form_data)
            if success:
                # Chiudi il modal di modifica
                del st.session_state['editing_prop']
                st.success(message)
                st.rerun()
                return True
            else:
                st.error(message)
                return False
        
        result = crud_form.render_form(
            fields_config=fields_config,
            data=prop_data,
            mode="edit",
            on_submit=handle_prop_update,
            key_prefix="edit_prop"
        )
        
        if st.button("❌ Annulla Modifica"):
            del st.session_state['editing_prop']
            st.rerun()
    
    # Modal eliminazione prop firm
    elif 'deleting_prop' in st.session_state:
        prop_data = st.session_state['deleting_prop']
        st.markdown("### 🗑️ Elimina Prop Firm")
        st.warning(f"⚠️ Sei sicuro di voler eliminare la prop firm **{prop_data['nome_prop']}**?")
        st.write(f"**ID:** {prop_data['id']}")
        st.write(f"**Tipo:** {prop_data.get('tipo_prop', 'N/A')}")
        st.write(f"**Capitale Iniziale:** {prop_data.get('capitale_iniziale', 'N/A')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Conferma Eliminazione", type="primary"):
                success, message = supabase_manager.delete_prop(prop_data['id'])
                if success:
                    st.success(f"✅ {message}")
                    del st.session_state['deleting_prop']
                    # Mantieni la sezione corrente dopo eliminazione
                    st.session_state['selected_menu'] = "🏛️ Prop Firm"
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        with col2:
            if st.button("❌ Annulla"):
                del st.session_state['deleting_prop']
                st.rerun()
    
    # Modal modifica wallet
    elif 'editing_wallet' in st.session_state:
        wallet_data = st.session_state['editing_wallet']
        st.markdown("### ✏️ Modifica Wallet")
        
        # Configurazione campi per il form
        fields_config = {
            'nome_wallet': {'type': 'text', 'label': 'Nome Wallet'},
            'tipo_wallet': {'type': 'select', 'label': 'Tipo Wallet', 'options': ['Bitcoin', 'Ethereum', 'Tether', 'Tron', 'Dogecoin', 'Litecoin', 'Altro']},
            'indirizzo_wallet': {'type': 'text', 'label': 'Indirizzo Wallet', 'required': True},
            'saldo_attuale': {'type': 'number', 'label': 'Saldo Attuale'},
            'valuta': {'type': 'text', 'label': 'Valuta'},
            'exchange': {'type': 'text', 'label': 'Exchange'},
            'stato': {'type': 'select', 'label': 'Stato', 'options': ['Attivo', 'Inattivo', 'Sospeso', 'Bloccato']},
            'chiave_privata': {'type': 'text', 'label': 'Chiave Privata'},
            'frase_seed': {'type': 'text', 'label': 'Frase Seed'},
            'note': {'type': 'textarea', 'label': 'Note'}
        }
        
        crud_form = CRUDForm("Modifica Wallet")
        
        def handle_wallet_update(form_data, mode):
            """Gestisce l'aggiornamento wallet e chiude il modal se riuscito"""
            success, message = supabase_manager.update_wallet(wallet_data['id'], form_data)
            if success:
                # Chiudi il modal di modifica
                del st.session_state['editing_wallet']
                st.success(message)
                st.rerun()
                return True
            else:
                st.error(message)
                return False
        
        result = crud_form.render_form(
            fields_config=fields_config,
            data=wallet_data,
            mode="edit",
            on_submit=handle_wallet_update,
            key_prefix="edit_wallet"
        )
        
        if st.button("❌ Annulla Modifica"):
            del st.session_state['editing_wallet']
            st.rerun()
    
    # Modal eliminazione wallet
    elif 'deleting_wallet' in st.session_state:
        wallet_data = st.session_state['deleting_wallet']
        st.markdown("### 🗑️ Elimina Wallet")
        st.warning(f"⚠️ Sei sicuro di voler eliminare il wallet **{wallet_data.get('nome_wallet', 'Senza Nome')}**?")
        st.write(f"**ID:** {wallet_data['id']}")
        st.write(f"**Tipo:** {wallet_data.get('tipo_wallet', 'N/A')}")
        st.write(f"**Indirizzo:** {wallet_data.get('indirizzo_wallet', 'N/A')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Conferma Eliminazione", type="primary"):
                success, message = supabase_manager.delete_wallet(wallet_data['id'])
                if success:
                    st.success(f"✅ {message}")
                    del st.session_state['deleting_wallet']
                    # Mantieni la sezione corrente dopo eliminazione
                    st.session_state['selected_menu'] = "💰 Wallet"
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        with col2:
            if st.button("❌ Annulla"):
                del st.session_state['deleting_wallet']
                st.rerun()
    
    # Modal modifica pack copiatore
    elif 'editing_pack' in st.session_state:
        pack_data = st.session_state['editing_pack']
        st.markdown("### ✏️ Modifica Pack Copiatore")
        
        # Configurazione campi per il form
        fields_config = {
            'numero_pack': {'type': 'text', 'label': 'Numero Pack', 'required': True},
            'broker_id': {'type': 'number', 'label': 'Broker ID'},
            'account_number': {'type': 'text', 'label': 'Numero Account'},
            'server_broker': {'type': 'text', 'label': 'Server Broker'},
            'tipo_account': {'type': 'select', 'label': 'Tipo Account', 'options': ['Demo', 'Live', 'Cent', 'Micro']},
            'capitale_iniziale': {'type': 'number', 'label': 'Capitale Iniziale'},
            'saldo_attuale': {'type': 'number', 'label': 'Saldo Attuale'},
            'profit_loss': {'type': 'number', 'label': 'Profit/Loss'},
            'drawdown_massimo': {'type': 'number', 'label': 'Drawdown Massimo (%)'},
            'stato': {'type': 'select', 'label': 'Stato', 'options': ['Attivo', 'Inattivo', 'In Test', 'Errore']},
            'password_account': {'type': 'text', 'label': 'Password Account'},
            'note': {'type': 'textarea', 'label': 'Note'}
        }
        
        crud_form = CRUDForm("Modifica Pack Copiatore")
        
        def handle_pack_update(form_data, mode):
            """Gestisce l'aggiornamento pack copiatore e chiude il modal se riuscito"""
            success, message = supabase_manager.update_pack_copiatore(pack_data['id'], form_data)
            if success:
                # Chiudi il modal di modifica
                del st.session_state['editing_pack']
                st.success(message)
                st.rerun()
                return True
            else:
                st.error(message)
                return False
        
        result = crud_form.render_form(
            fields_config=fields_config,
            data=pack_data,
            mode="edit",
            on_submit=handle_pack_update,
            key_prefix="edit_pack"
        )
        
        if st.button("❌ Annulla Modifica"):
            del st.session_state['editing_pack']
            st.rerun()
    
    # Modal eliminazione pack copiatore
    elif 'deleting_pack' in st.session_state:
        pack_data = st.session_state['deleting_pack']
        st.markdown("### 🗑️ Elimina Pack Copiatore")
        st.warning(f"⚠️ Sei sicuro di voler eliminare il pack **{pack_data.get('numero_pack', 'Senza Nome')}**?")
        st.write(f"**ID:** {pack_data['id']}")
        st.write(f"**Account:** {pack_data.get('account_number', 'N/A')}")
        st.write(f"**Server:** {pack_data.get('server_broker', 'N/A')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Conferma Eliminazione", type="primary"):
                success, message = supabase_manager.delete_pack_copiatore(pack_data['id'])
                if success:
                    st.success(f"✅ {message}")
                    del st.session_state['deleting_pack']
                    # Mantieni la sezione corrente dopo eliminazione
                    st.session_state['selected_menu'] = "📦 Pack Copiatori"
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        with col2:
            if st.button("❌ Annulla"):
                del st.session_state['deleting_pack']
                st.rerun()
    
    # Modal modifica gruppo PAMM
    elif 'editing_gruppo' in st.session_state:
        gruppo_data = st.session_state['editing_gruppo']
        st.markdown("### ✏️ Modifica Gruppo PAMM")
        
        # Configurazione campi per il form
        fields_config = {
            'nome_gruppo': {'type': 'text', 'label': 'Nome Gruppo', 'required': True},
            'manager': {'type': 'text', 'label': 'Manager'},
            'broker_id': {'type': 'number', 'label': 'Broker ID'},
            'account_pamm': {'type': 'text', 'label': 'Account PAMM'},
            'capitale_totale': {'type': 'number', 'label': 'Capitale Totale'},
            'numero_partecipanti': {'type': 'number', 'label': 'Numero Partecipanti'},
            'performance_totale': {'type': 'number', 'label': 'Performance Totale (%)'},
            'performance_mensile': {'type': 'number', 'label': 'Performance Mensile (%)'},
            'drawdown_massimo': {'type': 'number', 'label': 'Drawdown Massimo (%)'},
            'stato': {'type': 'select', 'label': 'Stato', 'options': ['Attivo', 'Inattivo', 'In Gestione', 'Chiuso']},
            'commissioni_manager': {'type': 'number', 'label': 'Commissioni Manager (%)'},
            'commissioni_broker': {'type': 'number', 'label': 'Commissioni Broker (%)'},
            'note': {'type': 'textarea', 'label': 'Note'}
        }
        
        crud_form = CRUDForm("Modifica Gruppo PAMM")
        
        def handle_gruppo_update(form_data, mode):
            """Gestisce l'aggiornamento gruppo PAMM e chiude il modal se riuscito"""
            success, message = supabase_manager.update_gruppo_pamm(gruppo_data['id'], form_data)
            if success:
                # Chiudi il modal di modifica
                del st.session_state['editing_gruppo']
                st.success(message)
                st.rerun()
                return True
            else:
                st.error(message)
                return False
        
        result = crud_form.render_form(
            fields_config=fields_config,
            data=gruppo_data,
            mode="edit",
            on_submit=handle_gruppo_update,
            key_prefix="edit_gruppo"
        )
        
        if st.button("❌ Annulla Modifica"):
            del st.session_state['editing_gruppo']
            st.rerun()
    
    # Modal eliminazione gruppo PAMM
    elif 'deleting_gruppo' in st.session_state:
        gruppo_data = st.session_state['deleting_gruppo']
        st.markdown("### 🗑️ Elimina Gruppo PAMM")
        st.warning(f"⚠️ Sei sicuro di voler eliminare il gruppo **{gruppo_data.get('nome_gruppo', 'Senza Nome')}**?")
        st.write(f"**ID:** {gruppo_data['id']}")
        st.write(f"**Manager:** {gruppo_data.get('manager', 'N/A')}")
        st.write(f"**Capitale Totale:** {gruppo_data.get('capitale_totale', 'N/A')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Conferma Eliminazione", type="primary"):
                success, message = supabase_manager.delete_gruppo_pamm(gruppo_data['id'])
                if success:
                    st.success(f"✅ {message}")
                    del st.session_state['deleting_gruppo']
                    # Mantieni la sezione corrente dopo eliminazione
                    st.session_state['selected_menu'] = "👥 Gruppi PAMM"
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        with col2:
            if st.button("❌ Annulla"):
                del st.session_state['deleting_gruppo']
                st.rerun()
    
    # Modal modifica incrocio
    elif 'editing_incrocio' in st.session_state:
        incrocio_data = st.session_state['editing_incrocio']
        st.markdown("### ✏️ Modifica Incrocio")
        
        # Configurazione campi per il form
        fields_config = {
            'nome_incrocio': {'type': 'text', 'label': 'Nome Incrocio', 'required': True},
            'broker_id': {'type': 'number', 'label': 'Broker ID'},
            'prop_id': {'type': 'number', 'label': 'Prop ID'},
            'wallet_id': {'type': 'number', 'label': 'Wallet ID'},
            'gruppo_pamm_id': {'type': 'number', 'label': 'Gruppo PAMM ID'},
            'pack_copiatore_id': {'type': 'number', 'label': 'Pack Copiatore ID'},
            'tipo_incrocio': {'type': 'text', 'label': 'Tipo Incrocio'},
            'performance_totale': {'type': 'number', 'label': 'Performance Totale (%)'},
            'rischio_totale': {'type': 'number', 'label': 'Rischio Totale (%)'},
            'stato': {'type': 'select', 'label': 'Stato', 'options': ['Attivo', 'Inattivo', 'In Test', 'Chiuso']},
            'descrizione': {'type': 'textarea', 'label': 'Descrizione'},
            'note': {'type': 'textarea', 'label': 'Note'}
        }
        
        crud_form = CRUDForm("Modifica Incrocio")
        
        def handle_incrocio_update(form_data, mode):
            """Gestisce l'aggiornamento incrocio e chiude il modal se riuscito"""
            success, message = supabase_manager.update_incrocio(incrocio_data['id'], form_data)
            if success:
                # Chiudi il modal di modifica
                del st.session_state['editing_incrocio']
                st.success(message)
                st.rerun()
                return True
            else:
                st.error(message)
                return False
        
        result = crud_form.render_form(
            fields_config=fields_config,
            data=incrocio_data,
            mode="edit",
            on_submit=handle_incrocio_update,
            key_prefix="edit_incrocio"
        )
        
        if st.button("❌ Annulla Modifica"):
            del st.session_state['editing_incrocio']
            st.rerun()
    
    # Modal eliminazione incrocio
    elif 'deleting_incrocio' in st.session_state:
        incrocio_data = st.session_state['deleting_incrocio']
        st.markdown("### 🗑️ Elimina Incrocio")
        st.warning(f"⚠️ Sei sicuro di voler eliminare l'incrocio **{incrocio_data.get('nome_incrocio', 'Senza Nome')}**?")
        st.write(f"**ID:** {incrocio_data['id']}")
        st.write(f"**Tipo:** {incrocio_data.get('tipo_incrocio', 'N/A')}")
        st.write(f"**Performance:** {incrocio_data.get('performance_totale', 'N/A')}%")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Conferma Eliminazione", type="primary"):
                success, message = supabase_manager.delete_incrocio(incrocio_data['id'])
                if success:
                    st.success(f"✅ {message}")
                    del st.session_state['deleting_incrocio']
                    # Mantieni la sezione corrente dopo eliminazione
                    st.session_state['selected_menu'] = "🔄 Incroci"
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        with col2:
            if st.button("❌ Annulla"):
                del st.session_state['deleting_incrocio']
                st.rerun()
    
    # Modal modifica utente
    if 'editing_user' in st.session_state:
        user_data = st.session_state['editing_user']
        st.markdown("### ✏️ Modifica Utente")
        
        # Configurazione campi per il form
        roles = supabase_manager.get_all_roles()
        role_options = {role['name']: role['id'] for role in roles}
        
        # Converti role_id in nome del ruolo per la visualizzazione iniziale
        user_data_display = user_data.copy()
        if user_data.get('role_id'):
            # Trova il nome del ruolo corrispondente all'ID
            for role in roles:
                if role['id'] == user_data['role_id']:
                    user_data_display['role_id'] = role['name']
                    break
        
        fields_config = {
            'username': {'type': 'text', 'label': 'Username', 'required': True},
            'email': {'type': 'text', 'label': 'Email', 'required': True},
            'first_name': {'type': 'text', 'label': 'Nome'},
            'last_name': {'type': 'text', 'label': 'Cognome'},
            'phone': {'type': 'text', 'label': 'Telefono'},
            'role_id': {'type': 'select', 'label': 'Ruolo', 'options': role_options},
            'is_active': {'type': 'checkbox', 'label': 'Attivo'},
            'is_admin': {'type': 'checkbox', 'label': 'Admin'},
            'notes': {'type': 'textarea', 'label': 'Note'}
        }
        
        crud_form = CRUDForm("Modifica Utente")
        
        def handle_user_update(form_data, mode):
            """Gestisce l'aggiornamento utente e chiude il modal se riuscito"""
            success, message = supabase_manager.update_user(user_data['id'], form_data)
            if success:
                # Chiudi il modal di modifica
                del st.session_state['editing_user']
                st.success(message)
                st.rerun()
                return True
            else:
                st.error(message)
                return False
        
        result = crud_form.render_form(
            fields_config=fields_config,
            data=user_data_display,
            mode="edit",
            on_submit=handle_user_update,
            key_prefix="edit_user"
        )
        
        if st.button("❌ Annulla Modifica"):
            del st.session_state['editing_user']
            st.rerun()
    
    # Modal eliminazione utente
    elif 'deleting_user' in st.session_state:
        user_data = st.session_state['deleting_user']
        st.markdown("### 🗑️ Elimina Utente")
        
        st.warning(f"⚠️ Sei sicuro di voler eliminare l'utente **{user_data['username']}**?")
        st.write(f"**Nome:** {user_data.get('first_name', '')} {user_data.get('last_name', '')}")
        st.write(f"**Email:** {user_data['email']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Conferma Eliminazione", type="primary"):
                success, message = supabase_manager.delete_user(user_data['id'])
                if success:
                    st.success(message)
                else:
                    st.error(message)
                del st.session_state['deleting_user']
                st.rerun()
        
        with col2:
            if st.button("❌ Annulla"):
                del st.session_state['deleting_user']
                st.rerun()
    
    # Contenuto principale basato sulla selezione
    if selected == "📊 Dashboard":
        render_dashboard()
    elif selected == "🏢 Broker":
        render_brokers_page()
    elif selected == "🏛️ Prop Firm":
        render_props_page()
    elif selected == "💰 Wallet":
        render_wallets_page()
    elif selected == "📦 Pack Copiatori":
        render_pack_copiatori_page()
    elif selected == "👥 Gruppi PAMM":
        render_gruppi_pamm_page()
    elif selected == "🔄 Incroci":
        render_incroci_page()
    elif selected == "👤 Gestione Utenti":
        render_users_page()
    elif selected == "⚙️ Impostazioni":
        render_settings_page()

if __name__ == "__main__":
    main()

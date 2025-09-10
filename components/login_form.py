#!/usr/bin/env python3
"""
Form di Login per DASH_PROP_BROKER
Interfaccia per l'autenticazione utenti
Creato da Ezio Camporeale
"""

import streamlit as st
from typing import Optional, Dict
import sys
from pathlib import Path

# Aggiungi il percorso della directory corrente al path di Python
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))

from components.auth_manager import AuthManager

def render_login_form() -> Optional[Dict]:
    """
    Renderizza il form di login
    
    Returns:
        Dict con i dati dell'utente se login riuscito, None altrimenti
    """
    
    # CSS per il form di login
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-title {
        font-size: 2rem;
        font-weight: 700;
        color: #2E86AB;
        margin-bottom: 0.5rem;
    }
    .login-subtitle {
        color: #666;
        font-size: 1rem;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(46, 134, 171, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Container del form
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="login-header">
        <div class="login-title">🧮 DASH_PROP_BROKER</div>
        <div class="login-subtitle">Dashboard Matematico per la Gestione di Broker, Prop Firm, Wallet e PAMM</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Form di login
    with st.form("login_form"):
        st.markdown("### 🔐 Accedi al Sistema")
        
        username = st.text_input(
            "👤 Username",
            placeholder="Inserisci il tuo username",
            help="Username per l'accesso al sistema"
        )
        
        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Inserisci la tua password",
            help="Password per l'accesso al sistema"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            login_button = st.form_submit_button(
                "🚀 Accedi",
                type="primary",
                width='stretch'
            )
        
        with col2:
            demo_button = st.form_submit_button(
                "🎯 Demo",
                width='stretch'
            )
        
        # Gestione login
        if login_button:
            if not username or not password:
                st.error("❌ Inserisci username e password")
                return None
            
            auth_manager = AuthManager()
            user_data = auth_manager.login(username, password)
            
            if user_data:
                st.success(f"✅ Benvenuto, {user_data['first_name']}!")
                st.rerun()
            else:
                st.error("❌ Username o password non corretti")
                return None
        
        # Login demo
        if demo_button:
            st.info("🎯 Funzionalità demo non disponibile. Contatta l'amministratore per le credenziali di accesso.")
            return None
    
    # Informazioni aggiuntive
    st.markdown("---")
    st.markdown("### ℹ️ Informazioni")
    
    with st.expander("🔑 Accesso al Sistema"):
        st.markdown("""
        **Per accedere al sistema:**
        - Contatta l'amministratore per ottenere le credenziali
        - Le credenziali vengono fornite in modo sicuro
        - Non sono disponibili credenziali di default pubbliche
        
        ⚠️ **Sicurezza:** Le credenziali sono personali e non devono essere condivise!
        """)
    
    with st.expander("🆘 Problemi di Accesso"):
        st.markdown("""
        **Se non riesci ad accedere:**
        1. Verifica che username e password siano corretti
        2. Controlla che il database Supabase sia configurato
        3. Assicurati che le tabelle users e roles siano create
        4. Contatta l'amministratore del sistema
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return None

def render_logout_section():
    """Renderizza la sezione di logout nella sidebar"""
    auth_manager = AuthManager()
    user = auth_manager.get_current_user()
    
    if user:
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 👤 Utente Corrente")
            
            # Informazioni utente
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("👤")
            with col2:
                st.write(f"**{user['first_name']} {user['last_name']}**")
                st.write(f"*{user['role_name']}*")
            
            # Pulsante logout
            if st.button("🚪 Logout", use_container_width=True):
                auth_manager.logout()
                st.rerun()

def render_auth_guard():
    """Renderizza la guardia di autenticazione"""
    auth_manager = AuthManager()
    
    if not auth_manager.is_authenticated():
        render_login_form()
        st.stop()
    else:
        render_logout_section()

def check_permissions(required_permissions: list = None, required_roles: list = None):
    """Verifica i permessi dell'utente corrente"""
    auth_manager = AuthManager()
    
    if not auth_manager.is_authenticated():
        st.error("🔒 Accesso non autorizzato. Effettua il login per continuare.")
        st.stop()
    
    if required_roles and not auth_manager.has_role(required_roles):
        st.error(f"🚫 Accesso negato. Ruoli richiesti: {', '.join(required_roles)}")
        st.stop()
    
    if required_permissions:
        for permission in required_permissions:
            if not auth_manager.has_permission(permission):
                st.error(f"🚫 Accesso negato. Permesso richiesto: {permission}")
                st.stop()

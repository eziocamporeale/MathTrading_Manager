#!/usr/bin/env python3
"""
Sistema di Autenticazione per DASH_PROP_BROKER
Gestisce login, logout, sessioni e permessi
Creato da Ezio Camporeale
"""

import streamlit as st
import bcrypt
import json
from typing import Dict, Optional, List, Tuple
from datetime import datetime, timedelta
import logging
import sys
from pathlib import Path

# Aggiungi il percorso della directory corrente al path di Python
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))

from database.supabase_manager import SupabaseManager

# Configurazione logging
logger = logging.getLogger(__name__)

class AuthManager:
    """Gestisce l'autenticazione e le sessioni degli utenti"""
    
    def __init__(self):
        """Inizializza il gestore di autenticazione"""
        self.supabase_manager = SupabaseManager()
        self.session_key = 'user_session'
        self.session_timeout = timedelta(days=7)  # 7 giorni di sessione
        
        # Inizializza la sessione se non esiste
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = None
    
    def hash_password(self, password: str) -> str:
        """Crea l'hash di una password"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica una password contro il suo hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"Errore verifica password: {e}")
            return False
    
    def login(self, username: str, password: str) -> Optional[Dict]:
        """Effettua il login di un utente"""
        try:
            # Ottieni l'utente dal database Supabase
            user = self.supabase_manager.get_user_by_username(username)
            
            if not user:
                logger.warning(f"Tentativo di login con username non esistente: {username}")
                return None
            
            # Verifica la password
            if not self.verify_password(password, user['password_hash']):
                logger.warning(f"Password errata per utente: {username}")
                return None
            
            # Verifica che l'utente sia attivo
            if not user['is_active']:
                logger.warning(f"Tentativo di login per utente disattivato: {username}")
                return None
            
            # Aggiorna l'ultimo login
            self.supabase_manager.update_user_last_login(user['id'])
            
            # Ottieni il nome del ruolo
            role_name = self._get_role_name(user['role_id'])
            
            # Salva la sessione
            session_data = {
                'user_id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'role_id': user['role_id'],
                'role_name': role_name,
                'login_time': datetime.now().isoformat(),
                'permissions': self._get_user_permissions(user['role_id'])
            }
            
            st.session_state[self.session_key] = session_data
            logger.info(f"Login effettuato con successo per utente: {username}")
            return session_data
            
        except Exception as e:
            logger.error(f"Errore durante il login: {e}")
            return None
    
    def logout(self):
        """Effettua il logout dell'utente"""
        if self.session_key in st.session_state and st.session_state[self.session_key]:
            username = st.session_state[self.session_key].get('username', 'Unknown')
            del st.session_state[self.session_key]
            logger.info(f"Logout effettuato per utente: {username}")
        else:
            logger.info("Logout effettuato (nessuna sessione attiva)")
    
    def get_current_user(self) -> Optional[Dict]:
        """Ottieni l'utente corrente dalla sessione"""
        if self.session_key not in st.session_state:
            return None
        
        session_data = st.session_state[self.session_key]
        if not session_data:
            return None
        
        # Verifica timeout sessione
        login_time = datetime.fromisoformat(session_data['login_time'])
        if datetime.now() - login_time > self.session_timeout:
            self.logout()
            return None
        
        return session_data
    
    def is_authenticated(self) -> bool:
        """Verifica se l'utente è autenticato"""
        return self.get_current_user() is not None
    
    def has_permission(self, permission: str) -> bool:
        """Verifica se l'utente ha un permesso specifico"""
        user = self.get_current_user()
        if not user:
            return False
        
        permissions = user.get('permissions', [])
        return permission in permissions or 'all' in permissions
    
    def has_role(self, roles: List[str]) -> bool:
        """Verifica se l'utente ha uno dei ruoli specificati"""
        user = self.get_current_user()
        if not user:
            return False
        
        user_role = user.get('role_name', '')
        return user_role in roles
    
    def require_auth(self):
        """Decoratore per richiedere autenticazione"""
        if not self.is_authenticated():
            st.error("🔒 Accesso non autorizzato. Effettua il login per continuare.")
            st.stop()
    
    def require_role(self, roles: List[str]):
        """Decoratore per richiedere ruoli specifici"""
        self.require_auth()
        if not self.has_role(roles):
            st.error(f"🚫 Accesso negato. Ruolo richiesto: {', '.join(roles)}")
            st.stop()
    
    def require_permission(self, permission: str):
        """Decoratore per richiedere permessi specifici"""
        self.require_auth()
        if not self.has_permission(permission):
            st.error(f"🚫 Accesso negato. Permesso richiesto: {permission}")
            st.stop()
    
    def _get_role_name(self, role_id: int) -> str:
        """Ottieni il nome del ruolo dall'ID"""
        try:
            role = self.supabase_manager.get_role_by_id(role_id)
            return role['name'] if role else 'Unknown'
        except Exception as e:
            logger.error(f"Errore recupero ruolo: {e}")
            return 'Unknown'
    
    def _get_user_permissions(self, role_id: int) -> List[str]:
        """Ottieni i permessi dell'utente dal ruolo"""
        try:
            role = self.supabase_manager.get_role_by_id(role_id)
            if role and role.get('permissions'):
                if isinstance(role['permissions'], str):
                    return json.loads(role['permissions'])
                elif isinstance(role['permissions'], list):
                    return role['permissions']
            return []
        except Exception as e:
            logger.error(f"Errore recupero permessi: {e}")
            return []
    
    def create_user(self, user_data: Dict) -> Tuple[bool, str]:
        """Crea un nuovo utente"""
        try:
            # Hash della password
            if 'password' in user_data:
                user_data['password_hash'] = self.hash_password(user_data['password'])
                del user_data['password']
            
            # Crea l'utente
            success, message = self.supabase_manager.create_user(user_data)
            if success:
                logger.info(f"Utente creato con successo: {user_data.get('username')}")
                return True, f"✅ Utente {user_data.get('username')} creato con successo"
            else:
                logger.error(f"Errore creazione utente: {message}")
                return False, f"❌ Errore creazione utente: {message}"
                
        except Exception as e:
            logger.error(f"Errore durante la creazione utente: {e}")
            return False, f"❌ Errore durante la creazione utente: {e}"
    
    def update_user(self, user_id: str, user_data: Dict) -> Tuple[bool, str]:
        """Aggiorna un utente esistente"""
        try:
            # Se viene fornita una nuova password, la hasha
            if 'password' in user_data and user_data['password']:
                user_data['password_hash'] = self.hash_password(user_data['password'])
                del user_data['password']
            
            # Aggiorna l'utente
            success, message = self.supabase_manager.update_user(user_id, user_data)
            if success:
                logger.info(f"Utente aggiornato con successo: {user_id}")
                return True, f"✅ Utente {user_id} aggiornato con successo"
            else:
                logger.error(f"Errore aggiornamento utente: {message}")
                return False, f"❌ Errore aggiornamento utente: {message}"
                
        except Exception as e:
            logger.error(f"Errore durante l'aggiornamento utente: {e}")
            return False, f"❌ Errore durante l'aggiornamento utente: {e}"
    
    def get_all_users(self) -> List[Dict]:
        """Ottieni tutti gli utenti"""
        try:
            return self.supabase_manager.get_all_users()
        except Exception as e:
            logger.error(f"Errore recupero utenti: {e}")
            return []
    
    def get_all_roles(self) -> List[Dict]:
        """Ottieni tutti i ruoli"""
        try:
            return self.supabase_manager.get_all_roles()
        except Exception as e:
            logger.error(f"Errore recupero ruoli: {e}")
            return []
    
    def render_user_info(self):
        """Renderizza le informazioni dell'utente corrente"""
        user = self.get_current_user()
        if not user:
            return
        
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 👤 Utente Corrente")
            st.write(f"**Nome:** {user['first_name']} {user['last_name']}")
            st.write(f"**Username:** {user['username']}")
            st.write(f"**Ruolo:** {user['role_name']}")
            st.write(f"**Email:** {user['email']}")
            
            if st.button("🚪 Logout", width='stretch'):
                self.logout()
                st.rerun()

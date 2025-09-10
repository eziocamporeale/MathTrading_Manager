#!/usr/bin/env python3
"""
Componente CRUD Table Generico
Tabella con pulsanti di modifica ed eliminazione
Creato da Ezio Camporeale
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Callable, Any
import logging

logger = logging.getLogger(__name__)

class CRUDTable:
    """
    Tabella generica con funzionalità CRUD
    Supporta modifica, eliminazione e visualizzazione
    """
    
    def __init__(self, title: str = "Tabella Dati"):
        """
        Inizializza la tabella CRUD
        
        Args:
            title: Titolo della tabella
        """
        self.title = title
        self.selected_row = None
        
    def render_table(
        self, 
        data: List[Dict], 
        columns_config: Dict[str, Dict],
        on_edit: Optional[Callable] = None,
        on_delete: Optional[Callable] = None,
        on_view: Optional[Callable] = None,
        key_prefix: str = "table",
        show_actions: bool = True
    ) -> Optional[Dict]:
        """
        Rende la tabella con pulsanti di azione
        
        Args:
            data: Lista di dizionari con i dati
            columns_config: Configurazione colonne per st.dataframe
            on_edit: Callback per modifica
            on_delete: Callback per eliminazione
            on_view: Callback per visualizzazione
            key_prefix: Prefisso per le chiavi Streamlit
            show_actions: Mostra colonna azioni
            
        Returns:
            Dizionario con i dati della riga selezionata o None
        """
        
        if not data:
            st.info("📭 Nessun dato disponibile")
            return None
            
        # Converti in DataFrame
        df = pd.DataFrame(data)
        
        if df.empty:
            st.info("📭 Nessun dato disponibile")
            return None
        
        # Aggiungi colonna azioni se richiesta
        if show_actions and (on_edit or on_delete or on_view):
            df['Azioni'] = ""
        
        # Mostra la tabella
        st.markdown(f"### {self.title}")
        
        # Configurazione colonne per st.dataframe
        column_config = columns_config.copy()
        
        if show_actions and (on_edit or on_delete or on_view):
            column_config['Azioni'] = st.column_config.TextColumn(
                "Azioni", 
                width=120,
                disabled=True
            )
        
        # Renderizza la tabella
        selected_data = st.dataframe(
            df,
            width='stretch',
            hide_index=True,
            column_config=column_config,
            key=f"{key_prefix}_main_table"
        )
        
        # Sezione pulsanti di azione
        if show_actions and (on_edit or on_delete or on_view):
            st.markdown("---")
            st.markdown("### ⚡ Azioni Rapide")
            
            # Pulsanti in colonne
            cols = []
            if on_view:
                cols.append(st.columns(1)[0])
            if on_edit:
                cols.append(st.columns(1)[0])
            if on_delete:
                cols.append(st.columns(1)[0])
            
            col_idx = 0
            
            if on_view:
                with cols[col_idx]:
                    if st.button("👁️ Visualizza Dettagli", key=f"{key_prefix}_view", width='stretch'):
                        st.info("👆 Seleziona una riga nella tabella per visualizzare i dettagli")
                col_idx += 1
            
            if on_edit:
                with cols[col_idx]:
                    if st.button("✏️ Modifica", key=f"{key_prefix}_edit", width='stretch'):
                        st.info("👆 Seleziona una riga nella tabella per modificarla")
                col_idx += 1
            
            if on_delete:
                with cols[col_idx]:
                    if st.button("🗑️ Elimina", key=f"{key_prefix}_delete", width='stretch'):
                        st.info("👆 Seleziona una riga nella tabella per eliminarla")
        
        return None
    
    def render_table_with_selection(
        self,
        data: List[Dict],
        columns_config: Dict[str, Dict],
        on_edit: Optional[Callable] = None,
        on_delete: Optional[Callable] = None,
        on_view: Optional[Callable] = None,
        key_prefix: str = "table"
    ) -> Optional[Dict]:
        """
        Rende la tabella con selezione riga per azioni
        
        Args:
            data: Lista di dizionari con i dati
            columns_config: Configurazione colonne
            on_edit: Callback per modifica
            on_delete: Callback per eliminazione
            on_view: Callback per visualizzazione
            key_prefix: Prefisso per le chiavi
            
        Returns:
            Dizionario con i dati della riga selezionata
        """
        
        if not data:
            st.info("📭 Nessun dato disponibile")
            return None
            
        # Converti in DataFrame
        df = pd.DataFrame(data)
        
        if df.empty:
            st.info("📭 Nessun dato disponibile")
            return None
        
        # Crea opzioni per selectbox
        if 'id' in df.columns:
            # Cerca colonne con nomi più intuitivi
            name_column = None
            for col in ['nome_broker', 'nome_prop', 'nome_wallet', 'numero_pack', 'nome_gruppo', 'nome_incrocio', 'name', 'title']:
                if col in df.columns:
                    name_column = col
                    break
            
            if name_column:
                # Usa nome come label principale, ID come riferimento
                options = [f"{row[name_column]} (ID: {row['id']})" for _, row in df.iterrows()]
            else:
                # Fallback: usa ID se non trova colonne nome
                options = [f"ID: {row['id']}" for _, row in df.iterrows()]
        else:
            # Usa indice come valore
            options = [f"Riga {i+1}" for i in range(len(df))]
        
        st.markdown(f"### {self.title}")
        
        # Selectbox per selezione
        selected_option = st.selectbox(
            "Seleziona elemento:",
            options=options,
            key=f"{key_prefix}_selection"
        )
        
        # Trova l'indice selezionato
        selected_idx = options.index(selected_option) if selected_option else None
        
        if selected_idx is not None:
            selected_data = df.iloc[selected_idx].to_dict()
            
            # Mostra dati selezionati
            st.markdown("---")
            st.markdown("### 📋 Dettagli Selezionati")
            
            # Mostra i dati in formato più leggibile
            for key, value in selected_data.items():
                if key != 'id':  # Nascondi ID dalla visualizzazione
                    # Formatta meglio i valori
                    if value is None or value == '':
                        display_value = "N/A"
                    elif isinstance(value, float):
                        display_value = f"{value:.2f}"
                    else:
                        display_value = str(value)
                    
                    # Traduci le chiavi in italiano
                    key_translations = {
                        # Broker
                        'nome_broker': 'Nome Broker',
                        'tipo_broker': 'Tipo Broker',
                        'regolamentazione': 'Regolamentazione',
                        'paese': 'Paese',
                        'sito_web': 'Sito Web',
                        'spread_minimo': 'Spread Minimo',
                        'commissioni': 'Commissioni',
                        'leverage_massimo': 'Leverage Massimo',
                        'deposito_minimo': 'Deposito Minimo',
                        # Prop Firm
                        'nome_prop': 'Nome Prop Firm',
                        'tipo_prop': 'Tipo Prop',
                        'capitale_iniziale': 'Capitale Iniziale',
                        'drawdown_massimo': 'Drawdown Massimo',
                        'profit_target': 'Profit Target',
                        'fee_mensile': 'Fee Mensile',
                        'regole_trading': 'Regole Trading',
                        'restrizioni_orarie': 'Restrizioni Orarie',
                        # Wallet
                        'nome_wallet': 'Nome Wallet',
                        'tipo_wallet': 'Tipo Wallet',
                        'indirizzo_wallet': 'Indirizzo Wallet',
                        'saldo_attuale': 'Saldo Attuale',
                        'valuta': 'Valuta',
                        'exchange': 'Exchange',
                        'chiave_privata': 'Chiave Privata',
                        'frase_seed': 'Frase Seed',
                        # Pack Copiatori
                        'numero_pack': 'Numero Pack',
                        'account_number': 'Numero Account',
                        'server_broker': 'Server Broker',
                        'tipo_account': 'Tipo Account',
                        'profit_loss': 'Profit/Loss',
                        'password_account': 'Password Account',
                        # Gruppi PAMM
                        'nome_gruppo': 'Nome Gruppo',
                        'manager': 'Manager',
                        'account_pamm': 'Account PAMM',
                        'capitale_totale': 'Capitale Totale',
                        'numero_partecipanti': 'Numero Partecipanti',
                        'performance_totale': 'Performance Totale',
                        'performance_mensile': 'Performance Mensile',
                        'commissioni_manager': 'Commissioni Manager',
                        'commissioni_broker': 'Commissioni Broker',
                        # Incroci
                        'nome_incrocio': 'Nome Incrocio',
                        'tipo_incrocio': 'Tipo Incrocio',
                        'performance_totale': 'Performance Totale',
                        'rischio_totale': 'Rischio Totale',
                        'descrizione': 'Descrizione',
                        # Generali
                        'stato': 'Stato',
                        'note': 'Note',
                        'created_at': 'Data Creazione',
                        'updated_at': 'Ultima Modifica'
                    }
                    
                    display_key = key_translations.get(key, key.replace('_', ' ').title())
                    st.write(f"**{display_key}:** {display_value}")
            
            # Pulsanti di azione
            st.markdown("---")
            st.markdown("### ⚡ Azioni")
            
            cols = []
            if on_view:
                cols.append(st.columns(1)[0])
            if on_edit:
                cols.append(st.columns(1)[0])
            if on_delete:
                cols.append(st.columns(1)[0])
            
            col_idx = 0
            
            if on_view:
                with cols[col_idx]:
                    if st.button("👁️ Visualizza Dettagli", key=f"{key_prefix}_view_btn", width='stretch'):
                        if on_view:
                            on_view(selected_data)
                col_idx += 1
            
            if on_edit:
                with cols[col_idx]:
                    if st.button("✏️ Modifica", key=f"{key_prefix}_edit_btn", width='stretch'):
                        if on_edit:
                            on_edit(selected_data)
                col_idx += 1
            
            if on_delete:
                with cols[col_idx]:
                    if st.button("🗑️ Elimina", key=f"{key_prefix}_delete_btn", width='stretch'):
                        if on_delete:
                            on_delete(selected_data)
            
            return selected_data
        
        return None
    
    def render_confirmation_modal(
        self,
        title: str,
        message: str,
        on_confirm: Callable,
        confirm_data: Optional[Dict] = None,
        key_prefix: str = "modal"
    ) -> bool:
        """
        Rende un modal di conferma per eliminazione
        
        Args:
            title: Titolo del modal
            message: Messaggio di conferma
            on_confirm: Callback per conferma
            confirm_data: Dati da passare al callback
            key_prefix: Prefisso per le chiavi
            
        Returns:
            True se confermato, False altrimenti
        """
        
        st.markdown("---")
        st.markdown(f"### ⚠️ {title}")
        st.warning(message)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Conferma", key=f"{key_prefix}_confirm", width='stretch'):
                if on_confirm:
                    result = on_confirm(confirm_data)
                    if result:
                        st.success("✅ Operazione completata con successo!")
                        st.rerun()
                    else:
                        st.error("❌ Errore durante l'operazione")
                return True
        
        with col2:
            if st.button("❌ Annulla", key=f"{key_prefix}_cancel", width='stretch'):
                st.info("Operazione annullata")
                return False
        
        return False

"""
Componente per tabella editabile Gruppi PAMM in stile Excel
Replica esattamente la struttura dell'Excel con modifica celle in tempo reale
Creato da Ezio Camporeale
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from models import StatoProp, DepositoPAMM, GruppiPAMM, dict_to_gruppi_pamm
from database.supabase_manager import SupabaseManager

class EditableGruppiTable:
    """Componente per tabella editabile Gruppi PAMM"""
    
    def __init__(self):
        self.supabase_manager = SupabaseManager()
        self.session_key = "editable_gruppi_data"
        self.changes_key = "pending_changes"
    
    def render_editable_table(self):
        """Rende la tabella editabile principale"""
        
        st.title("📊 Gruppi PAMM - Tabella Editabile")
        st.markdown("Modifica direttamente le celle come in Excel. Le modifiche vengono salvate automaticamente.")
        
        # Carica dati
        data = self.supabase_manager.get_gruppi_pamm()
        if not data:
            st.warning("Nessun dato disponibile")
            return
        
        # Inizializza session state
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = data
        if self.changes_key not in st.session_state:
            st.session_state[self.changes_key] = {}
        
        # Converti in DataFrame
        df = pd.DataFrame(st.session_state[self.session_key])
        
        # Ordina per gruppo e cliente
        df = df.sort_values(['nome_gruppo', 'nome_cliente'])
        
        # Raggruppa per gruppo
        gruppi = df['nome_gruppo'].unique()
        
        # Renderizza ogni gruppo
        for gruppo in gruppi:
            self._render_gruppo_section(gruppo, df[df['nome_gruppo'] == gruppo])
        
        # Pulsante salva modifiche
        if st.session_state[self.changes_key]:
            self._render_save_changes_button()
    
    def _render_gruppo_section(self, nome_gruppo: str, df_gruppo: pd.DataFrame):
        """Rende una sezione gruppo"""
        
        st.markdown(f"### 🏢 {nome_gruppo}")
        
        # Header del gruppo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Clienti", len(df_gruppo))
        with col2:
            svolti = len(df_gruppo[df_gruppo['stato_prop'] == 'Svolto'])
            st.metric("✅ Svolti", svolti)
        with col3:
            depositati = len(df_gruppo[df_gruppo['deposito_pamm'] == 'Depositata'])
            st.metric("💰 Depositati", depositati)
        
        # Tabella editabile per il gruppo
        self._render_group_editable_table(df_gruppo, nome_gruppo)
    
    def _render_group_editable_table(self, df_gruppo: pd.DataFrame, gruppo_nome: str):
        """Rende la tabella editabile per un gruppo - REPLICA ESATTA DELL'EXCEL"""
        
        # Reset index per avere indici continui
        df_gruppo = df_gruppo.reset_index(drop=True)
        
        # Crea colonne per la tabella editabile - TUTTE LE COLONNE DELL'EXCEL
        cols = st.columns(14)  # 14 colonne come nell'Excel
        
        # Header delle colonne (esattamente come nell'Excel)
        headers = [
            "Cliente",
            "Deposito Pamm", 
            "Quota Prop",
            "Ciclo #",
            "Fase Prop",
            "Operazione #",
            "ESITO BROKER",
            "ESITO PROP",
            "Prelievo prop",
            "Prelievo profit", 
            "Commissioni 25%",
            "Credenziali Broker",
            "Credenziali PROP (MAI ACCESSI)",
            "CHI HA COMPRATO PROP"
        ]
        
        # Renderizza header
        for i, header in enumerate(headers):
            with cols[i]:
                st.markdown(f"**{header}**")
        
        # Renderizza ogni riga editabile con chiavi uniche
        for idx, row in df_gruppo.iterrows():
            self._render_editable_row(row['id'], row, gruppo_nome)
        
        st.divider()
    
    def _render_editable_row(self, record_id: int, row: Dict[str, Any], gruppo_nome: str):
        """Rende una riga editabile - TUTTE LE 14 COLONNE DELL'EXCEL"""
        
        # Crea chiave unica usando ID del record e gruppo
        unique_key_prefix = f"{gruppo_nome}_{record_id}"
        
        # Crea 14 colonne come nell'Excel
        cols = st.columns(14)
        
        with cols[0]:
            # Cliente (non editabile, solo visualizzazione)
            cliente_display = f"{row['nome_cliente']}"
            st.text(cliente_display)
        
        with cols[1]:
            # Deposito PAMM (dropdown editabile)
            deposito_options = ["Depositata", ""]
            current_deposito = row['deposito_pamm']
            new_deposito = st.selectbox(
                f"deposito_{unique_key_prefix}",
                options=deposito_options,
                index=deposito_options.index(current_deposito) if current_deposito in deposito_options else 1,
                key=f"deposito_select_{unique_key_prefix}",
                label_visibility="collapsed"
            )
            
            # Applica colore condizionale
            if new_deposito == "Depositata":
                st.markdown('<div style="background-color: #d1ecf1; color: #0c5460; padding: 5px; border-radius: 3px;">💰 Depositata</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="background-color: #f8f9fa; color: #6c757d; padding: 5px; border-radius: 3px;">⚪ Non depositata</div>', unsafe_allow_html=True)
            
            # Salva cambiamento
            if new_deposito != current_deposito:
                self._save_change(record_id, 'deposito_pamm', new_deposito)
        
        with cols[2]:
            # Quota Prop (input numerico editabile)
            current_quota = row['quota_prop'] or 1
            new_quota = st.number_input(
                f"quota_{unique_key_prefix}",
                min_value=1,
                max_value=999,
                value=int(current_quota),
                key=f"quota_input_{unique_key_prefix}",
                label_visibility="collapsed"
            )
            
            # Salva cambiamento
            if new_quota != current_quota:
                self._save_change(record_id, 'quota_prop', new_quota)
        
        with cols[3]:
            # Ciclo # (input numerico editabile)
            current_ciclo = row['ciclo_numero'] or 0
            new_ciclo = st.number_input(
                f"ciclo_{unique_key_prefix}",
                min_value=0,
                max_value=999,
                value=int(current_ciclo),
                key=f"ciclo_input_{unique_key_prefix}",
                label_visibility="collapsed"
            )
            
            # Salva cambiamento
            if new_ciclo != current_ciclo:
                self._save_change(record_id, 'ciclo_numero', new_ciclo)
        
        with cols[4]:
            # Fase Prop (input testuale editabile)
            current_fase = row['fase_prop'] or ""
            new_fase = st.text_input(
                f"fase_{unique_key_prefix}",
                value=current_fase,
                key=f"fase_input_{unique_key_prefix}",
                label_visibility="collapsed",
                placeholder="Es: 1 fase"
            )
            
            # Salva cambiamento
            if new_fase != current_fase:
                self._save_change(record_id, 'fase_prop', new_fase)
        
        with cols[5]:
            # Operazione # (input testuale editabile)
            current_operazione = row['operazione_numero'] or ""
            new_operazione = st.text_input(
                f"operazione_{unique_key_prefix}",
                value=str(current_operazione),
                key=f"operazione_input_{unique_key_prefix}",
                label_visibility="collapsed",
                placeholder="Es: Prima operazione"
            )
            
            # Salva cambiamento
            if str(new_operazione) != str(current_operazione):
                self._save_change(record_id, 'operazione_numero', new_operazione)
        
        with cols[6]:
            # ESITO BROKER (input testuale editabile)
            current_esito_broker = row['esito_broker'] or ""
            new_esito_broker = st.text_input(
                f"esito_broker_{unique_key_prefix}",
                value=current_esito_broker,
                key=f"esito_broker_input_{unique_key_prefix}",
                label_visibility="collapsed",
                placeholder="Esito broker"
            )
            
            # Salva cambiamento
            if new_esito_broker != current_esito_broker:
                self._save_change(record_id, 'esito_broker', new_esito_broker)
        
        with cols[7]:
            # ESITO PROP (input testuale editabile)
            current_esito_prop = row['esito_prop'] or ""
            new_esito_prop = st.text_input(
                f"esito_prop_{unique_key_prefix}",
                value=current_esito_prop,
                key=f"esito_prop_input_{unique_key_prefix}",
                label_visibility="collapsed",
                placeholder="Esito prop"
            )
            
            # Salva cambiamento
            if new_esito_prop != current_esito_prop:
                self._save_change(record_id, 'esito_prop', new_esito_prop)
        
        with cols[8]:
            # Prelievo prop (input numerico editabile)
            current_prelievo_prop = row['prelievo_prop'] or 0.0
            new_prelievo_prop = st.number_input(
                f"prelievo_prop_{unique_key_prefix}",
                min_value=0.0,
                max_value=999999.99,
                value=float(current_prelievo_prop),
                key=f"prelievo_prop_input_{unique_key_prefix}",
                label_visibility="collapsed",
                format="%.2f"
            )
            
            # Salva cambiamento
            if new_prelievo_prop != current_prelievo_prop:
                self._save_change(record_id, 'prelievo_prop', new_prelievo_prop)
        
        with cols[9]:
            # Prelievo profit (input numerico editabile)
            current_prelievo_profit = row['prelievo_profit'] or 0.0
            new_prelievo_profit = st.number_input(
                f"prelievo_profit_{unique_key_prefix}",
                min_value=0.0,
                max_value=999999.99,
                value=float(current_prelievo_profit),
                key=f"prelievo_profit_input_{unique_key_prefix}",
                label_visibility="collapsed",
                format="%.2f"
            )
            
            # Salva cambiamento
            if new_prelievo_profit != current_prelievo_profit:
                self._save_change(record_id, 'prelievo_profit', new_prelievo_profit)
        
        with cols[10]:
            # Commissioni 25% (input numerico editabile)
            current_commissioni = row['commissioni_percentuale'] or 25.0
            new_commissioni = st.number_input(
                f"commissioni_{unique_key_prefix}",
                min_value=0.0,
                max_value=100.0,
                value=float(current_commissioni),
                key=f"commissioni_input_{unique_key_prefix}",
                label_visibility="collapsed",
                format="%.1f"
            )
            
            # Applica colore condizionale
            if new_commissioni == 25.0:
                st.markdown('<div style="background-color: #d4edda; color: #155724; padding: 5px; border-radius: 3px;">25%</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="background-color: #fff3cd; color: #856404; padding: 5px; border-radius: 3px;">{:.1f}%</div>'.format(new_commissioni), unsafe_allow_html=True)
            
            # Salva cambiamento
            if new_commissioni != current_commissioni:
                self._save_change(record_id, 'commissioni_percentuale', new_commissioni)
        
        with cols[11]:
            # Credenziali Broker (input editabile)
            current_credenziali_broker = row['credenziali_broker'] or ""
            new_credenziali_broker = st.text_input(
                f"credenziali_broker_{unique_key_prefix}",
                value=current_credenziali_broker,
                key=f"credenziali_broker_input_{unique_key_prefix}",
                label_visibility="collapsed",
                placeholder="Es: 6001855"
            )
            
            # Salva cambiamento
            if new_credenziali_broker != current_credenziali_broker:
                self._save_change(record_id, 'credenziali_broker', new_credenziali_broker)
        
        with cols[12]:
            # Credenziali PROP (MAI ACCESSI) (input editabile)
            current_credenziali_prop = row['credenziali_prop'] or ""
            new_credenziali_prop = st.text_input(
                f"credenziali_prop_{unique_key_prefix}",
                value=current_credenziali_prop,
                key=f"credenziali_prop_input_{unique_key_prefix}",
                label_visibility="collapsed",
                placeholder="Es: 1125804"
            )
            
            # Salva cambiamento
            if new_credenziali_prop != current_credenziali_prop:
                self._save_change(record_id, 'credenziali_prop', new_credenziali_prop)
        
        with cols[13]:
            # CHI HA COMPRATO PROP (input testuale editabile)
            current_chi_ha_comprato = row.get('chi_ha_comprato_prop', '') or ""
            new_chi_ha_comprato = st.text_input(
                f"chi_ha_comprato_{unique_key_prefix}",
                value=current_chi_ha_comprato,
                key=f"chi_ha_comprato_input_{unique_key_prefix}",
                label_visibility="collapsed",
                placeholder="Es: MATTEO"
            )
            
            # Salva cambiamento
            if new_chi_ha_comprato != current_chi_ha_comprato:
                self._save_change(record_id, 'chi_ha_comprato_prop', new_chi_ha_comprato)
    
    def _save_change(self, record_id: int, field: str, value: Any):
        """Salva un cambiamento nella session state"""
        
        if self.changes_key not in st.session_state:
            st.session_state[self.changes_key] = {}
        
        # Salva il cambiamento
        change_key = f"{record_id}_{field}"
        st.session_state[self.changes_key][change_key] = {
            'id': record_id,
            'field': field,
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_save_changes_button(self):
        """Rende il pulsante per salvare le modifiche"""
        
        changes_count = len(st.session_state[self.changes_key])
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button(f"💾 Salva {changes_count} Modifiche", type="primary", use_container_width=True):
                self._save_all_changes()
    
    def _save_all_changes(self):
        """Salva tutte le modifiche nel database"""
        
        changes = st.session_state[self.changes_key]
        success_count = 0
        error_count = 0
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_changes = len(changes)
        
        for i, (change_key, change_data) in enumerate(changes.items()):
            try:
                # Aggiorna il record nel database (tabella clienti_gruppi_pamm)
                success, message = self.supabase_manager.update_cliente_gruppo_pamm(
                    change_data['id'],
                    {change_data['field']: change_data['value']}
                )
                
                if success:
                    success_count += 1
                else:
                    error_count += 1
                    st.error(f"Errore aggiornamento record {change_data['id']}: {message}")
                
                # Aggiorna progress bar
                progress_bar.progress((i + 1) / total_changes)
                status_text.text(f"Salvando modifiche... {i + 1}/{total_changes}")
                
            except Exception as e:
                error_count += 1
                st.error(f"Errore durante il salvataggio: {e}")
        
        # Risultato finale
        if success_count > 0:
            st.success(f"✅ {success_count} modifiche salvate con successo!")
        
        if error_count > 0:
            st.error(f"❌ {error_count} modifiche non salvate")
        
        # Pulisci le modifiche salvate
        st.session_state[self.changes_key] = {}
        
        # Ricarica i dati
        st.session_state[self.session_key] = self.supabase_manager.get_gruppi_pamm()
        
        # Riavvia la pagina per mostrare i dati aggiornati
        st.rerun()
    
    def render_quick_actions(self):
        """Rende azioni rapide per la tabella"""
        
        st.sidebar.markdown("## ⚡ Azioni Rapide")
        
        # Filtri
        st.sidebar.markdown("### 🔍 Filtri")
        
        data = self.supabase_manager.get_gruppi_pamm()
        if data:
            df = pd.DataFrame(data)
            
            # Filtro per stato
            stati_unici = ['Tutti'] + list(df['stato_prop'].unique())
            stato_selezionato = st.sidebar.selectbox("Filtra per Stato Prop", stati_unici)
            
            # Filtro per gruppo
            gruppi_unici = ['Tutti'] + list(df['nome_gruppo'].unique())
            gruppo_selezionato = st.sidebar.selectbox("Filtra per Gruppo", gruppi_unici)
            
            # Applica filtri
            if stato_selezionato != 'Tutti':
                df = df[df['stato_prop'] == stato_selezionato]
            
            if gruppo_selezionato != 'Tutti':
                df = df[df['nome_gruppo'] == gruppo_selezionato]
            
            st.sidebar.info(f"Mostrando {len(df)} clienti")
        
        # Azioni bulk
        st.sidebar.markdown("### ⚡ Azioni Bulk")
        
        if st.sidebar.button("🔄 Aggiorna Dati", use_container_width=True):
            st.session_state[self.session_key] = self.supabase_manager.get_gruppi_pamm()
            st.rerun()
        
        if st.sidebar.button("📊 Statistiche", use_container_width=True):
            self._show_statistics()
    
    def _show_statistics(self):
        """Mostra statistiche dettagliate"""
        
        data = self.supabase_manager.get_gruppi_pamm()
        if not data:
            return
        
        df = pd.DataFrame(data)
        
        st.markdown("## 📊 Statistiche Dettagliate")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Totale Clienti", len(df))
        
        with col2:
            svolti = len(df[df['stato_prop'] == 'Svolto'])
            st.metric("✅ Svolti", svolti)
        
        with col3:
            non_svolti = len(df[df['stato_prop'] == 'Non svolto'])
            st.metric("❌ Non Svolti", non_svolti)
        
        with col4:
            depositati = len(df[df['deposito_pamm'] == 'Depositata'])
            st.metric("💰 Depositati", depositati)
        
        # Grafico a torta per stati
        import plotly.express as px
        
        stato_counts = df['stato_prop'].value_counts()
        fig = px.pie(
            values=stato_counts.values,
            names=stato_counts.index,
            title="Distribuzione Stati Prop",
            color_discrete_map={
                'Svolto': '#28a745',
                'Non svolto': '#dc3545',
                'mancanza saldo': '#ffc107'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

def render_editable_gruppi_page():
    """Rende la pagina completa con tabella editabile"""
    
    st.set_page_config(
        page_title="Gruppi PAMM Editabile",
        page_icon="📊",
        layout="wide"
    )
    
    # Inizializza componente
    editable_table = EditableGruppiTable()
    
    # Sidebar con azioni rapide
    editable_table.render_quick_actions()
    
    # Tabella principale editabile
    editable_table.render_editable_table()

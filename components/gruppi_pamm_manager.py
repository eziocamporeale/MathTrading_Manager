"""
Componente per la gestione completa dei gruppi PAMM
CRUD completo con calcoli automatici e gestione clienti
Creato da Ezio Camporeale
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from models import (
    GruppoPAMM, ClienteGruppoPAMM, 
    gruppo_pamm_to_dict, dict_to_gruppo_pamm,
    cliente_gruppo_pamm_to_dict, dict_to_cliente_gruppo_pamm,
    StatoProp, DepositoPAMM
)
from database.supabase_manager import SupabaseManager
from components.crud_table import CRUDTable
from components.crud_form import CRUDForm

class GruppiPAMMManager:
    """Manager per la gestione completa dei gruppi PAMM"""
    
    def __init__(self):
        self.supabase_manager = SupabaseManager()
        self.session_key = "gruppi_pamm_data"
        self.clienti_key = "clienti_gruppi_pamm_data"
    
    def render_gruppi_pamm_page(self):
        """Rende la pagina principale per la gestione gruppi PAMM"""
        
        st.title("🏢 Gestione Gruppi PAMM")
        st.markdown("Gestisci i gruppi PAMM e i loro clienti con calcoli automatici")
        
        # Tab per navigazione
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Gruppi PAMM", "👥 Clienti per Gruppo", "📋 Panoramica Gruppi", "📈 Statistiche"])
        
        with tab1:
            self._render_gruppi_tab()
        
        with tab2:
            self._render_clienti_tab()
        
        with tab3:
            self._render_panoramica_tab()
        
        with tab4:
            self._render_statistiche_tab()
    
    def _render_panoramica_tab(self):
        """Tab per panoramica compatta e riassuntiva dei gruppi"""
        
        st.subheader("📋 Panoramica Gruppi PAMM")
        st.markdown("Visualizzazione compatta e riassuntiva di tutti i gruppi e clienti")
        
        # Carica tutti i dati
        all_data = self.supabase_manager.get_all_gruppi_pamm_for_editable_table()
        if not all_data:
            st.warning("Nessun dato disponibile")
            return
        
        # Converti in DataFrame
        df = pd.DataFrame(all_data)
        
        # Raggruppa per gruppo e calcola statistiche
        gruppi_summary = []
        for gruppo in df['nome_gruppo'].unique():
            gruppo_data = df[df['nome_gruppo'] == gruppo]
            
            # Calcola statistiche per il gruppo
            summary = {
                'Gruppo': gruppo,
                'Manager': gruppo_data['manager'].iloc[0],
                'Clienti': len(gruppo_data),
                'Totale Importi': f"€{gruppo_data['importo_cliente'].sum():,.2f}",
                'Svolti': len(gruppo_data[gruppo_data['stato_prop'] == 'Svolto']),
                'Depositati': len(gruppo_data[gruppo_data['deposito_pamm'] == 'Depositata']),
                'Totale Prelievi Prop': f"€{gruppo_data['prelievo_prop'].sum():,.2f}",
                'Totale Prelievi Profit': f"€{gruppo_data['prelievo_profit'].sum():,.2f}",
                'Commissioni Medie': f"{gruppo_data['commissioni_percentuale'].mean():.1f}%",
                'Stato': gruppo_data['stato'].iloc[0]
            }
            gruppi_summary.append(summary)
        
        # Crea DataFrame riassuntivo
        summary_df = pd.DataFrame(gruppi_summary)
        
        # Mostra metriche generali
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Gruppi Totali", len(summary_df))
        
        with col2:
            total_clienti = summary_df['Clienti'].sum()
            st.metric("👥 Clienti Totali", total_clienti)
        
        with col3:
            total_importi = df['importo_cliente'].sum()
            st.metric("💰 Importi Totali", f"€{total_importi:,.2f}")
        
        with col4:
            total_svolti = summary_df['Svolti'].sum()
            st.metric("✅ Svolti Totali", total_svolti)
        
        st.divider()
        
        # Mostra tabella riassuntiva
        st.markdown("### 📊 Riepilogo per Gruppo")
        
        # Formatta la tabella per una migliore visualizzazione
        display_df = summary_df.copy()
        display_df = display_df.set_index('Gruppo')
        
        # Usa st.dataframe per una visualizzazione più pulita
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400
        )
        
        # Mostra dettagli clienti in formato compatto
        st.markdown("### 👥 Dettagli Clienti per Gruppo")
        
        for gruppo in df['nome_gruppo'].unique():
            gruppo_data = df[df['nome_gruppo'] == gruppo]
            
            with st.expander(f"📋 {gruppo} - {len(gruppo_data)} clienti"):
                # Crea tabella compatta per i clienti
                clienti_display = gruppo_data[['nome_cliente', 'importo_cliente', 'stato_prop', 'deposito_pamm', 'prelievo_prop', 'prelievo_profit']].copy()
                clienti_display['importo_cliente'] = clienti_display['importo_cliente'].apply(lambda x: f"€{x:,.2f}")
                clienti_display['prelievo_prop'] = clienti_display['prelievo_prop'].apply(lambda x: f"€{x:,.2f}")
                clienti_display['prelievo_profit'] = clienti_display['prelievo_profit'].apply(lambda x: f"€{x:,.2f}")
                
                # Rinomina le colonne per una migliore visualizzazione
                clienti_display.columns = ['Cliente', 'Importo', 'Stato Prop', 'Deposito', 'Prelievo Prop', 'Prelievo Profit']
                
                st.dataframe(
                    clienti_display,
                    use_container_width=True,
                    hide_index=True
                )
    
    def _render_gruppi_tab(self):
        """Tab per la gestione dei gruppi PAMM"""
        
        st.subheader("📊 Gestione Gruppi PAMM")
        
        # Pulsanti azioni
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Nuovo Gruppo", type="primary", use_container_width=True):
                st.session_state['show_create_gruppo'] = True
        
        with col2:
            if st.button("🔄 Aggiorna Dati", use_container_width=True):
                self._refresh_data()
                st.rerun()
        
        with col3:
            if st.button("📊 Calcola Statistiche", use_container_width=True):
                self._calculate_all_statistics()
                st.success("Statistiche calcolate!")
                st.rerun()
        
        # Form per creare nuovo gruppo
        if st.session_state.get('show_create_gruppo', False):
            self._render_create_gruppo_form()
        
        # Tabella gruppi esistenti
        self._render_gruppi_table()
    
    def _render_create_gruppo_form(self):
        """Form per creare un nuovo gruppo PAMM"""
        
        st.markdown("---")
        st.subheader("➕ Crea Nuovo Gruppo PAMM")
        
        with st.form("create_gruppo_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_gruppo = st.text_input("Nome Gruppo*", placeholder="Es: Gruppo 1")
                manager = st.text_input("Manager*", placeholder="Es: frank andre")
                broker_id = st.number_input("Broker ID*", min_value=1, value=1)
                account_pamm = st.text_input("Account PAMM*", placeholder="Es: PAMM001")
            
            with col2:
                capitale_totale = st.number_input("Capitale Totale", min_value=0.0, value=0.0, format="%.2f")
                numero_membri_gruppo = st.number_input("Numero Membri Gruppo", min_value=0, value=0)
                responsabili_gruppo = st.text_input("Responsabili Gruppo", placeholder="Es: frank andre, mario")
                note = st.text_area("Note", placeholder="Note aggiuntive...")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                submit = st.form_submit_button("✅ Crea Gruppo", type="primary")
            
            with col2:
                cancel = st.form_submit_button("❌ Annulla")
            
            if submit:
                if nome_gruppo and manager and broker_id and account_pamm:
                    success, message = self._create_gruppo(
                        nome_gruppo, manager, broker_id, account_pamm,
                        capitale_totale, numero_membri_gruppo, responsabili_gruppo, note
                    )
                    if success:
                        st.success(f"✅ {message}")
                        st.session_state['show_create_gruppo'] = False
                        self._refresh_data()
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Compila tutti i campi obbligatori (*)")
            
            if cancel:
                st.session_state['show_create_gruppo'] = False
                st.rerun()
    
    def _render_gruppi_table(self):
        """Tabella dei gruppi PAMM con azioni"""
        
        gruppi = self.supabase_manager.get_gruppi_pamm_gruppi()
        
        if not gruppi:
            st.info("Nessun gruppo PAMM trovato. Crea il primo gruppo!")
            return
        
        # Converti in DataFrame
        df = pd.DataFrame(gruppi)
        
        # Calcola statistiche per ogni gruppo
        df_with_stats = self._add_group_statistics(df)
        
        # Mostra tabella con azioni
        st.markdown("### 📋 Gruppi PAMM Esistenti")
        
        for _, gruppo in df_with_stats.iterrows():
            with st.expander(f"🏢 {gruppo['nome_gruppo']} - {gruppo['manager']} ({gruppo['numero_clienti_attivi']} clienti)"):
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("💰 Capitale Totale", f"€{gruppo['capitale_totale']:,.2f}")
                
                with col2:
                    st.metric("👥 Clienti Attivi", gruppo['numero_clienti_attivi'])
                
                with col3:
                    st.metric("✅ Svolti", gruppo['numero_clienti_svolti'])
                
                with col4:
                    st.metric("💰 Depositati", gruppo['numero_clienti_depositati'])
                
                # Azioni per il gruppo
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button(f"✏️ Modifica", key=f"edit_{gruppo['id']}"):
                        st.session_state['edit_gruppo_id'] = gruppo['id']
                        st.rerun()
                
                with col2:
                    if st.button(f"👥 Gestisci Clienti", key=f"clienti_{gruppo['id']}"):
                        st.session_state['selected_gruppo_id'] = gruppo['id']
                        st.rerun()
                
                with col3:
                    if st.button(f"📊 Dettagli", key=f"details_{gruppo['id']}"):
                        self._show_gruppo_details(gruppo)
                
                with col4:
                    if st.button(f"🗑️ Elimina", key=f"delete_{gruppo['id']}"):
                        st.session_state['delete_gruppo_id'] = gruppo['id']
                        st.rerun()
    
    def _render_clienti_tab(self):
        """Tab per la gestione dei clienti per gruppo"""
        
        st.subheader("👥 Gestione Clienti per Gruppo")
        
        # Seleziona gruppo
        gruppi = self.supabase_manager.get_gruppi_pamm_gruppi()
        if not gruppi:
            st.info("Nessun gruppo PAMM disponibile. Crea prima un gruppo!")
            return
        
        gruppo_options = {f"{g['nome_gruppo']} - {g['manager']}": g['id'] for g in gruppi}
        selected_gruppo_name = st.selectbox("Seleziona Gruppo", list(gruppo_options.keys()))
        
        if selected_gruppo_name:
            gruppo_id = gruppo_options[selected_gruppo_name]
            self._render_clienti_for_gruppo(gruppo_id)
    
    def _render_clienti_for_gruppo(self, gruppo_id: int):
        """Rende la gestione clienti per un gruppo specifico"""
        
        # Pulsanti azioni
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Aggiungi Cliente", type="primary", use_container_width=True):
                st.session_state['show_create_cliente'] = gruppo_id
        
        with col2:
            if st.button("🔄 Aggiorna", use_container_width=True):
                self._refresh_data()
                st.rerun()
        
        with col3:
            if st.button("📊 Calcola Totali", use_container_width=True):
                self._calculate_gruppo_statistics(gruppo_id)
                st.success("Totali calcolati!")
                st.rerun()
        
        # Form per aggiungere cliente
        if st.session_state.get('show_create_cliente') == gruppo_id:
            self._render_create_cliente_form(gruppo_id)
        
        # Tabella clienti del gruppo
        self._render_clienti_table(gruppo_id)
    
    def _render_create_cliente_form(self, gruppo_id: int):
        """Form per aggiungere un nuovo cliente al gruppo"""
        
        st.markdown("---")
        st.subheader("➕ Aggiungi Nuovo Cliente")
        
        with st.form("create_cliente_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_cliente = st.text_input("Nome Cliente*", placeholder="Es: MANUEL CARINI [4000]")
                importo_cliente = st.number_input("Importo Cliente", min_value=0.0, value=0.0, format="%.2f")
                stato_prop = st.selectbox("Stato Prop", ["Non svolto", "Svolto", "mancanza saldo"])
                deposito_pamm = st.selectbox("Deposito PAMM", ["", "Depositata"])
            
            with col2:
                quota_prop = st.number_input("Quota Prop", min_value=1, value=1)
                ciclo_numero = st.number_input("Ciclo #", min_value=0, value=0)
                fase_prop = st.text_input("Fase Prop", placeholder="Es: 1 fase")
                operazione_numero = st.text_input("Operazione #", placeholder="Es: Prima operazione")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                submit = st.form_submit_button("✅ Aggiungi Cliente", type="primary")
            
            with col2:
                cancel = st.form_submit_button("❌ Annulla")
            
            if submit:
                if nome_cliente:
                    success, message = self._create_cliente(
                        gruppo_id, nome_cliente, importo_cliente, stato_prop, deposito_pamm,
                        quota_prop, ciclo_numero, fase_prop, operazione_numero
                    )
                    if success:
                        st.success(f"✅ {message}")
                        st.session_state['show_create_cliente'] = None
                        self._refresh_data()
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Nome cliente obbligatorio")
            
            if cancel:
                st.session_state['show_create_cliente'] = None
                st.rerun()
    
    def _render_clienti_table(self, gruppo_id: int):
        """Tabella clienti per un gruppo specifico"""
        
        clienti = self.supabase_manager.get_clienti_by_gruppo(gruppo_id)
        
        if not clienti:
            st.info("Nessun cliente trovato per questo gruppo. Aggiungi il primo cliente!")
            return
        
        # Converti in DataFrame
        df = pd.DataFrame(clienti)
        
        # Mostra totali del gruppo
        self._show_gruppo_totals(df)
        
        # Tabella clienti editabile
        st.markdown("### 📋 Clienti del Gruppo")
        
        # Usa il componente tabella editabile esistente
        from components.editable_gruppi_table import EditableGruppiTable
        editable_table = EditableGruppiTable()
        
        # Mostra solo i clienti di questo gruppo
        st.session_state[editable_table.session_key] = clienti
        editable_table.render_editable_table()
    
    def _show_gruppo_totals(self, df_clienti: pd.DataFrame):
        """Mostra i totali calcolati per il gruppo"""
        
        if df_clienti.empty:
            return
        
        # Calcola totali
        totale_importi = df_clienti['importo_cliente'].sum()
        totale_prelievi_prop = df_clienti['prelievo_prop'].sum()
        totale_prelievi_profit = df_clienti['prelievo_profit'].sum()
        totale_commissioni = df_clienti['commissioni_percentuale'].mean()
        
        numero_clienti = len(df_clienti)
        numero_svolti = len(df_clienti[df_clienti['stato_prop'] == 'Svolto'])
        numero_depositati = len(df_clienti[df_clienti['deposito_pamm'] == 'Depositata'])
        
        # Mostra metriche
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Totale Importi", f"€{totale_importi:,.2f}")
        
        with col2:
            st.metric("📤 Totale Prelievi Prop", f"€{totale_prelievi_prop:,.2f}")
        
        with col3:
            st.metric("📤 Totale Prelievi Profit", f"€{totale_prelievi_profit:,.2f}")
        
        with col4:
            st.metric("📊 Commissioni Medie", f"{totale_commissioni:.1f}%")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👥 Totale Clienti", numero_clienti)
        
        with col2:
            st.metric("✅ Clienti Svolti", numero_svolti)
        
        with col3:
            st.metric("💰 Clienti Depositati", numero_depositati)
    
    def _render_statistiche_tab(self):
        """Tab per le statistiche generali"""
        
        st.subheader("📈 Statistiche Generali")
        
        # Calcola statistiche globali
        gruppi = self.supabase_manager.get_gruppi_pamm_gruppi()
        clienti = self.supabase_manager.get_all_clienti_gruppi()
        
        if not gruppi or not clienti:
            st.info("Nessun dato disponibile per le statistiche")
            return
        
        df_gruppi = pd.DataFrame(gruppi)
        df_clienti = pd.DataFrame(clienti)
        
        # Statistiche generali
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🏢 Totale Gruppi", len(gruppi))
        
        with col2:
            st.metric("👥 Totale Clienti", len(clienti))
        
        with col3:
            totale_importi = df_clienti['importo_cliente'].sum()
            st.metric("💰 Totale Importi", f"€{totale_importi:,.2f}")
        
        with col4:
            gruppi_attivi = len(df_gruppi[df_gruppi['stato'] == 'ATTIVO'])
            st.metric("✅ Gruppi Attivi", gruppi_attivi)
        
        # Grafico a torta per stati prop
        import plotly.express as px
        
        stato_counts = df_clienti['stato_prop'].value_counts()
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
    
    def _create_gruppo(self, nome_gruppo: str, manager: str, broker_id: int, account_pamm: str,
                      capitale_totale: float, numero_membri_gruppo: int, responsabili_gruppo: str, note: str) -> tuple:
        """Crea un nuovo gruppo PAMM"""
        
        gruppo = GruppoPAMM(
            nome_gruppo=nome_gruppo,
            manager=manager,
            broker_id=broker_id,
            account_pamm=account_pamm,
            capitale_totale=capitale_totale,
            numero_membri_gruppo=numero_membri_gruppo,
            responsabili_gruppo=responsabili_gruppo,
            note=note,
            creato_da=st.session_state.get('user', {}).get('username', 'admin'),
            aggiornato_da=st.session_state.get('user', {}).get('username', 'admin')
        )
        
        return self.supabase_manager.create_gruppo_pamm(gruppo)
    
    def _create_cliente(self, gruppo_id: int, nome_cliente: str, importo_cliente: float,
                       stato_prop: str, deposito_pamm: str, quota_prop: int, ciclo_numero: int,
                       fase_prop: str, operazione_numero: str) -> tuple:
        """Crea un nuovo cliente per un gruppo"""
        
        cliente = ClienteGruppoPAMM(
            gruppo_pamm_id=gruppo_id,
            nome_cliente=nome_cliente,
            importo_cliente=importo_cliente,
            stato_prop=StatoProp(stato_prop),
            deposito_pamm=DepositoPAMM(deposito_pamm),
            quota_prop=quota_prop,
            ciclo_numero=ciclo_numero,
            fase_prop=fase_prop,
            operazione_numero=operazione_numero,
            creato_da=st.session_state.get('user', {}).get('username', 'admin'),
            aggiornato_da=st.session_state.get('user', {}).get('username', 'admin')
        )
        
        return self.supabase_manager.create_cliente_gruppo_pamm(cliente)
    
    def _refresh_data(self):
        """Aggiorna i dati dalla sessione"""
        st.session_state[self.session_key] = self.supabase_manager.get_gruppi_pamm_gruppi()
        st.session_state[self.clienti_key] = self.supabase_manager.get_all_clienti_gruppi()
    
    def _add_group_statistics(self, df_gruppi: pd.DataFrame) -> pd.DataFrame:
        """Aggiunge statistiche calcolate ai gruppi"""
        
        clienti = self.supabase_manager.get_all_clienti_gruppi()
        df_clienti = pd.DataFrame(clienti)
        
        for idx, gruppo in df_gruppi.iterrows():
            gruppo_clienti = df_clienti[df_clienti['gruppo_pamm_id'] == gruppo['id']]
            
            df_gruppi.at[idx, 'numero_clienti_attivi'] = len(gruppo_clienti)
            df_gruppi.at[idx, 'numero_clienti_svolti'] = len(gruppo_clienti[gruppo_clienti['stato_prop'] == 'Svolto'])
            df_gruppi.at[idx, 'numero_clienti_depositati'] = len(gruppo_clienti[gruppo_clienti['deposito_pamm'] == 'Depositata'])
            df_gruppi.at[idx, 'totale_depositi'] = gruppo_clienti['importo_cliente'].sum()
            df_gruppi.at[idx, 'totale_prelievi_prop'] = gruppo_clienti['prelievo_prop'].sum()
            df_gruppi.at[idx, 'totale_prelievi_profit'] = gruppo_clienti['prelievo_profit'].sum()
        
        return df_gruppi
    
    def _calculate_all_statistics(self):
        """Calcola statistiche per tutti i gruppi"""
        # Implementazione per calcolare e aggiornare statistiche
        pass
    
    def _calculate_gruppo_statistics(self, gruppo_id: int):
        """Calcola statistiche per un gruppo specifico"""
        # Implementazione per calcolare statistiche del gruppo
        pass
    
    def _show_gruppo_details(self, gruppo: pd.Series):
        """Mostra dettagli completi di un gruppo"""
        st.json(gruppo.to_dict())

def render_gruppi_pamm_manager_page():
    """Rende la pagina completa per la gestione gruppi PAMM"""
    
    st.set_page_config(
        page_title="Gestione Gruppi PAMM",
        page_icon="🏢",
        layout="wide"
    )
    
    # Inizializza manager
    manager = GruppiPAMMManager()
    
    # Rende la pagina principale
    manager.render_gruppi_pamm_page()

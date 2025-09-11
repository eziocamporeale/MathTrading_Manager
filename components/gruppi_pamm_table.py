"""
Componente per visualizzazione Gruppi PAMM in stile Excel
Replica la struttura della scheda "gruppi DEF" dell'Excel originale
Creato da Ezio Camporeale
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
from models import StatoProp, DepositoPAMM, GruppiPAMM, dict_to_gruppi_pamm
from database.supabase_manager import SupabaseManager

class GruppiPAMMTable:
    """Componente per visualizzazione tabellare Gruppi PAMM"""
    
    def __init__(self):
        self.supabase_manager = SupabaseManager()
    
    def render_gruppi_pamm_table(self, data: List[Dict[str, Any]], title: str = "Gruppi PAMM"):
        """Rende la tabella Gruppi PAMM con formattazione Excel-like"""
        
        if not data:
            st.warning("Nessun dato disponibile")
            return
        
        # Converti in DataFrame per facilità di manipolazione
        df = pd.DataFrame(data)
        
        # Ordina per gruppo e poi per nome cliente
        df = df.sort_values(['nome_gruppo', 'nome_cliente'])
        
        # Crea colonne principali come nell'Excel
        display_columns = [
            'nome_cliente',
            'stato_prop', 
            'deposito_pamm',
            'quota_prop',
            'ciclo_numero',
            'fase_prop',
            'operazione_numero',
            'esito_broker',
            'esito_prop',
            'prelievo_prop',
            'prelievo_profit',
            'commissioni_percentuale',
            'credenziali_broker',
            'credenziali_prop'
        ]
        
        # Filtra solo le colonne esistenti
        available_columns = [col for col in display_columns if col in df.columns]
        df_display = df[available_columns].copy()
        
        # Rinomina colonne per visualizzazione italiana
        column_mapping = {
            'nome_cliente': 'Cliente',
            'stato_prop': 'Stato Prop',
            'deposito_pamm': 'Deposito PAMM',
            'quota_prop': 'Quota Prop',
            'ciclo_numero': 'Ciclo #',
            'fase_prop': 'Fase Prop',
            'operazione_numero': 'Operazione #',
            'esito_broker': 'Esito Broker',
            'esito_prop': 'Esito Prop',
            'prelievo_prop': 'Prelievo Prop',
            'prelievo_profit': 'Prelievo Profit',
            'commissioni_percentuale': 'Commissioni %',
            'credenziali_broker': 'Credenziali Broker',
            'credenziali_prop': 'Credenziali Prop'
        }
        
        df_display = df_display.rename(columns=column_mapping)
        
        # Applica formattazione condizionale
        styled_df = self._apply_conditional_formatting(df_display)
        
        # Mostra la tabella
        st.subheader(f"📊 {title}")
        
        # Statistiche rapide
        self._render_quick_stats(df)
        
        # Legenda colori
        self._render_color_legend()
        
        # Tabella principale con colori condizionali
        styled_df_colored = self._apply_status_colors(styled_df)
        
        st.dataframe(
            styled_df_colored,
            use_container_width=True,
            height=400,
            hide_index=True
        )
        
        # Filtri e controlli
        self._render_filters_and_controls(df)
    
    def _apply_conditional_formatting(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applica formattazione condizionale basata sui valori"""
        
        # Crea una copia per la formattazione
        styled_df = df.copy()
        
        # Formatta numeri
        if 'Ciclo #' in styled_df.columns:
            styled_df['Ciclo #'] = styled_df['Ciclo #'].fillna(0).astype(int)
        
        if 'Operazione #' in styled_df.columns:
            styled_df['Operazione #'] = styled_df['Operazione #'].fillna(0).astype(int)
        
        if 'Quota Prop' in styled_df.columns:
            styled_df['Quota Prop'] = styled_df['Quota Prop'].fillna(1).astype(int)
        
        if 'Commissioni %' in styled_df.columns:
            styled_df['Commissioni %'] = styled_df['Commissioni %'].fillna(25.0).astype(float)
        
        # Formatta importi monetari
        money_columns = ['Prelievo Prop', 'Prelievo Profit']
        for col in money_columns:
            if col in styled_df.columns:
                styled_df[col] = styled_df[col].fillna(0.0).apply(lambda x: f"€{x:,.2f}" if x > 0 else "")
        
        return styled_df
    
    def _apply_status_colors(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applica colori condizionali basati sullo stato prop"""
        
        # Crea una copia per i colori
        colored_df = df.copy()
        
        # Applica colori di sfondo per stato prop
        if 'Stato Prop' in colored_df.columns:
            def color_status(val):
                if val == 'Svolto':
                    return 'background-color: #d4edda; color: #155724'  # Verde chiaro
                elif val == 'Non svolto':
                    return 'background-color: #f8d7da; color: #721c24'  # Rosso chiaro
                elif val == 'mancanza saldo':
                    return 'background-color: #fff3cd; color: #856404'  # Giallo chiaro
                else:
                    return ''
            
            colored_df['Stato Prop'] = colored_df['Stato Prop'].apply(color_status)
        
        # Applica colori per deposito PAMM
        if 'Deposito PAMM' in colored_df.columns:
            def color_deposito(val):
                if val == 'Depositata':
                    return 'background-color: #d1ecf1; color: #0c5460'  # Azzurro chiaro
                else:
                    return 'background-color: #f8f9fa; color: #6c757d'  # Grigio chiaro
            
            colored_df['Deposito PAMM'] = colored_df['Deposito PAMM'].apply(color_deposito)
        
        # Applica colori per commissioni (evidenzia se diverse da 25%)
        if 'Commissioni %' in colored_df.columns:
            def color_commissioni(val):
                try:
                    commissione = float(str(val).replace('%', '').replace('€', '').replace(',', ''))
                    if commissione != 25.0:
                        return 'background-color: #ffeaa7; color: #d63031'  # Arancione per valori non standard
                    else:
                        return 'background-color: #d4edda; color: #155724'  # Verde per valore standard
                except:
                    return ''
            
            colored_df['Commissioni %'] = colored_df['Commissioni %'].apply(color_commissioni)
        
        return colored_df
    
    def _render_color_legend(self):
        """Rende la legenda dei colori condizionali"""
        
        st.markdown("### 🎨 Legenda Colori")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **Stato Prop:**
            - 🟢 **Verde**: Svolto
            - 🔴 **Rosso**: Non svolto  
            - 🟡 **Giallo**: Mancanza saldo
            """)
        
        with col2:
            st.markdown("""
            **Deposito PAMM:**
            - 🔵 **Azzurro**: Depositata
            - ⚪ **Grigio**: Non depositata
            """)
        
        with col3:
            st.markdown("""
            **Commissioni:**
            - 🟢 **Verde**: 25% (standard)
            - 🟠 **Arancione**: Diverso da 25%
            """)
    
    def _render_quick_stats(self, df: pd.DataFrame):
        """Rende statistiche rapide sopra la tabella"""
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            totale_clienti = len(df)
            st.metric("👥 Totale Clienti", totale_clienti)
        
        with col2:
            svolti = len(df[df['stato_prop'] == 'Svolto']) if 'stato_prop' in df.columns else 0
            st.metric("✅ Svolti", svolti)
        
        with col3:
            non_svolti = len(df[df['stato_prop'] == 'Non svolto']) if 'stato_prop' in df.columns else 0
            st.metric("❌ Non Svolti", non_svolti)
        
        with col4:
            depositati = len(df[df['deposito_pamm'] == 'Depositata']) if 'deposito_pamm' in df.columns else 0
            st.metric("💰 Depositati", depositati)
    
    def _render_filters_and_controls(self, df: pd.DataFrame):
        """Rende filtri e controlli sotto la tabella"""
        
        st.subheader("🔍 Filtri e Controlli")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Filtro per stato prop
            if 'stato_prop' in df.columns:
                stati_unici = ['Tutti'] + list(df['stato_prop'].unique())
                stato_selezionato = st.selectbox("Filtra per Stato Prop", stati_unici)
                
                if stato_selezionato != 'Tutti':
                    df_filtrato = df[df['stato_prop'] == stato_selezionato]
                    st.write(f"Mostrando {len(df_filtrato)} clienti con stato '{stato_selezionato}'")
        
        with col2:
            # Filtro per deposito PAMM
            if 'deposito_pamm' in df.columns:
                depositi_unici = ['Tutti'] + list(df['deposito_pamm'].unique())
                deposito_selezionato = st.selectbox("Filtra per Deposito PAMM", depositi_unici)
                
                if deposito_selezionato != 'Tutti':
                    df_filtrato = df[df['deposito_pamm'] == deposito_selezionato]
                    st.write(f"Mostrando {len(df_filtrato)} clienti con deposito '{deposito_selezionato}'")
        
        with col3:
            # Filtro per gruppo
            if 'nome_gruppo' in df.columns:
                gruppi_unici = ['Tutti'] + list(df['nome_gruppo'].unique())
                gruppo_selezionato = st.selectbox("Filtra per Gruppo", gruppi_unici)
                
                if gruppo_selezionato != 'Tutti':
                    df_filtrato = df[df['nome_gruppo'] == gruppo_selezionato]
                    st.write(f"Mostrando {len(df_filtrato)} clienti del gruppo '{gruppo_selezionato}'")
    
    def render_gruppi_summary(self, data: List[Dict[str, Any]]):
        """Rende riepilogo per gruppi con statistiche"""
        
        if not data:
            st.warning("Nessun dato disponibile per il riepilogo")
            return
        
        df = pd.DataFrame(data)
        
        # Raggruppa per gruppo
        gruppi_summary = df.groupby('nome_gruppo').agg({
            'nome_cliente': 'count',
            'stato_prop': lambda x: (x == 'Svolto').sum(),
            'deposito_pamm': lambda x: (x == 'Depositata').sum(),
            'importo_cliente': 'sum',
            'responsabili_gruppo': 'first',
            'numero_membri_gruppo': 'first'
        }).reset_index()
        
        gruppi_summary.columns = [
            'Gruppo', 'Totale Clienti', 'Svolti', 'Depositati', 
            'Importo Totale', 'Responsabili', 'Membri Gruppo'
        ]
        
        # Calcola percentuali
        gruppi_summary['% Svolti'] = (gruppi_summary['Svolti'] / gruppi_summary['Totale Clienti'] * 100).round(1)
        gruppi_summary['% Depositati'] = (gruppi_summary['Depositati'] / gruppi_summary['Totale Clienti'] * 100).round(1)
        
        # Formatta importi
        gruppi_summary['Importo Totale'] = gruppi_summary['Importo Totale'].apply(lambda x: f"€{x:,.2f}")
        
        st.subheader("📈 Riepilogo per Gruppi")
        st.dataframe(
            gruppi_summary,
            use_container_width=True,
            hide_index=True
        )
    
    def render_bulk_operations(self, data: List[Dict[str, Any]]):
        """Rende operazioni bulk per aggiornamento multipli clienti"""
        
        if not data:
            st.warning("Nessun dato disponibile per operazioni bulk")
            return
        
        st.subheader("⚡ Operazioni Bulk")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Aggiorna Stato Prop**")
            
            # Selezione multipla clienti
            clienti_options = [f"{row['nome_cliente']} (ID: {row['id']})" for row in data]
            clienti_selezionati = st.multiselect("Seleziona Clienti", clienti_options)
            
            # Nuovo stato
            nuovo_stato = st.selectbox("Nuovo Stato Prop", ["Svolto", "Non svolto", "mancanza saldo"])
            
            if st.button("Aggiorna Stato Prop"):
                if clienti_selezionati:
                    # Estrai IDs
                    ids = []
                    for cliente in clienti_selezionati:
                        id_str = cliente.split("(ID: ")[1].split(")")[0]
                        ids.append(int(id_str))
                    
                    # Aggiorna
                    success, message = self.supabase_manager.update_stato_prop_bulk(
                        ids, StatoProp(nuovo_stato)
                    )
                    
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Seleziona almeno un cliente")
        
        with col2:
            st.write("**Aggiorna Deposito PAMM**")
            
            # Selezione multipla clienti per deposito
            clienti_options_dep = [f"{row['nome_cliente']} (ID: {row['id']})" for row in data]
            clienti_selezionati_dep = st.multiselect("Seleziona Clienti", clienti_options_dep, key="deposito")
            
            # Nuovo deposito
            nuovo_deposito = st.selectbox("Nuovo Deposito PAMM", ["Depositata", ""], key="deposito_select")
            
            if st.button("Aggiorna Deposito PAMM"):
                if clienti_selezionati_dep:
                    # Estrai IDs
                    ids = []
                    for cliente in clienti_selezionati_dep:
                        id_str = cliente.split("(ID: ")[1].split(")")[0]
                        ids.append(int(id_str))
                    
                    # Aggiorna
                    deposito_enum = DepositoPAMM.DEPOSITATA if nuovo_deposito == "Depositata" else DepositoPAMM.NON_DEPOSITATA
                    success, message = self.supabase_manager.update_deposito_pamm_bulk(
                        ids, deposito_enum
                    )
                    
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Seleziona almeno un cliente")

def render_gruppi_pamm_page():
    """Rende la pagina completa Gruppi PAMM"""
    
    st.title("🏢 Gestione Gruppi PAMM")
    st.markdown("Visualizzazione e gestione gruppi PAMM in stile Excel")
    
    # Inizializza componente
    gruppi_table = GruppiPAMMTable()
    
    # Carica dati
    data = gruppi_table.supabase_manager.get_gruppi_pamm()
    
    if not data:
        st.warning("Nessun gruppo PAMM trovato nel database")
        return
    
    # Tab per diverse visualizzazioni
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Tabella Completa", "📈 Riepilogo Gruppi", "⚡ Operazioni Bulk", "🔍 Ricerca"])
    
    with tab1:
        gruppi_table.render_gruppi_pamm_table(data, "Gruppi PAMM - Vista Completa")
    
    with tab2:
        gruppi_table.render_gruppi_summary(data)
    
    with tab3:
        gruppi_table.render_bulk_operations(data)
    
    with tab4:
        st.subheader("🔍 Ricerca Avanzata")
        
        search_term = st.text_input("Cerca per nome cliente o gruppo")
        if search_term:
            results = gruppi_table.supabase_manager.search_gruppi_pamm(search_term)
            if results:
                gruppi_table.render_gruppi_pamm_table(results, f"Risultati per '{search_term}'")
            else:
                st.info(f"Nessun risultato trovato per '{search_term}'")

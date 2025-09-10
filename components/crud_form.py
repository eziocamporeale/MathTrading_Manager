#!/usr/bin/env python3
"""
Componente CRUD Form Generico
Form per creazione e modifica entità
Creato da Ezio Camporeale
"""

import streamlit as st
from typing import Dict, List, Optional, Callable, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CRUDForm:
    """
    Form generico per operazioni CRUD
    Supporta creazione e modifica
    """
    
    def __init__(self, title: str = "Form"):
        """
        Inizializza il form CRUD
        
        Args:
            title: Titolo del form
        """
        self.title = title
        
    def render_form(
        self,
        fields_config: Dict[str, Dict],
        data: Optional[Dict] = None,
        mode: str = "create",
        on_submit: Optional[Callable] = None,
        key_prefix: str = "form"
    ) -> Optional[Dict]:
        """
        Rende il form per creazione/modifica
        
        Args:
            fields_config: Configurazione campi del form
            data: Dati esistenti per modifica
            mode: "create" o "edit"
            on_submit: Callback per submit
            key_prefix: Prefisso per le chiavi
            
        Returns:
            Dizionario con i dati del form o None
        """
        
        # Titolo del form
        if mode == "create":
            st.markdown(f"### ➕ {self.title} - Nuovo")
        else:
            st.markdown(f"### ✏️ {self.title} - Modifica")
        
        # Form container
        with st.form(key=f"{key_prefix}_main_form"):
            
            form_data = {}
            
            # Rendi i campi del form
            for field_name, field_config in fields_config.items():
                field_value = self._render_field(
                    field_name, 
                    field_config, 
                    data.get(field_name) if data else None,
                    key_prefix
                )
                form_data[field_name] = field_value
            
            # Pulsanti submit
            col1, col2 = st.columns(2)
            
            with col1:
                submit_text = "✅ Salva" if mode == "create" else "✅ Aggiorna"
                submit_button = st.form_submit_button(
                    submit_text,
                    width='stretch'
                )
            
            with col2:
                cancel_button = st.form_submit_button(
                    "❌ Annulla",
                    width='stretch'
                )
            
            # Gestione submit
            if submit_button:
                # Validazione
                validation_result = self._validate_form(form_data, fields_config)
                
                if validation_result['valid']:
                    # Chiama callback se fornito
                    if on_submit:
                        result = on_submit(form_data, mode)
                        if result:
                            success_msg = "✅ Creato con successo!" if mode == "create" else "✅ Aggiornato con successo!"
                            st.success(success_msg)
                            st.rerun()
                        else:
                            st.error("❌ Errore durante il salvataggio")
                    else:
                        return form_data
                else:
                    st.error(f"❌ Errori di validazione: {', '.join(validation_result['errors'])}")
            
            elif cancel_button:
                st.info("Operazione annullata")
                return None
        
        return None
    
    def _render_field(
        self, 
        field_name: str, 
        field_config: Dict, 
        current_value: Any = None,
        key_prefix: str = "form"
    ) -> Any:
        """
        Rende un singolo campo del form
        
        Args:
            field_name: Nome del campo
            field_config: Configurazione del campo
            current_value: Valore corrente
            key_prefix: Prefisso per le chiavi
            
        Returns:
            Valore del campo
        """
        
        field_type = field_config.get('type', 'text')
        field_label = field_config.get('label', field_name.replace('_', ' ').title())
        field_required = field_config.get('required', False)
        field_help = field_config.get('help', '')
        field_options = field_config.get('options', [])
        field_default = field_config.get('default', None)
        
        # Usa valore corrente o default
        initial_value = current_value if current_value is not None else field_default
        
        # Label con asterisco per campi obbligatori
        display_label = f"{field_label} {'*' if field_required else ''}"
        
        # Rendi il campo in base al tipo
        if field_type == 'text':
            return st.text_input(
                display_label,
                value=initial_value or '',
                help=field_help,
                key=f"{key_prefix}_{field_name}"
            )
        
        elif field_type == 'textarea':
            return st.text_area(
                display_label,
                value=initial_value or '',
                help=field_help,
                key=f"{key_prefix}_{field_name}"
            )
        
        elif field_type == 'number':
            return st.number_input(
                display_label,
                value=initial_value or 0,
                help=field_help,
                key=f"{key_prefix}_{field_name}"
            )
        
        elif field_type == 'select':
            # Se non c'è valore iniziale, usa il primo della lista
            index = 0
            if initial_value and initial_value in field_options:
                index = field_options.index(initial_value)
            
            return st.selectbox(
                display_label,
                options=field_options,
                index=index,
                help=field_help,
                key=f"{key_prefix}_{field_name}"
            )
        
        elif field_type == 'multiselect':
            # Per multiselect, il valore iniziale deve essere una lista
            if not isinstance(initial_value, list):
                initial_value = []
            
            return st.multiselect(
                display_label,
                options=field_options,
                default=initial_value,
                help=field_help,
                key=f"{key_prefix}_{field_name}"
            )
        
        elif field_type == 'checkbox':
            return st.checkbox(
                display_label,
                value=initial_value or False,
                help=field_help,
                key=f"{key_prefix}_{field_name}"
            )
        
        elif field_type == 'date':
            # Converte stringa in datetime se necessario
            date_value = None
            if initial_value:
                if isinstance(initial_value, str):
                    try:
                        date_value = datetime.fromisoformat(initial_value.split('T')[0])
                    except:
                        date_value = None
                elif isinstance(initial_value, datetime):
                    date_value = initial_value
            
            return st.date_input(
                display_label,
                value=date_value,
                help=field_help,
                key=f"{key_prefix}_{field_name}"
            )
        
        elif field_type == 'time':
            # Converte stringa in time se necessario
            time_value = None
            if initial_value:
                if isinstance(initial_value, str):
                    try:
                        time_value = datetime.fromisoformat(initial_value).time()
                    except:
                        time_value = None
            
            return st.time_input(
                display_label,
                value=time_value,
                help=field_help,
                key=f"{key_prefix}_{field_name}"
            )
        
        else:
            # Default a text input
            return st.text_input(
                display_label,
                value=initial_value or '',
                help=field_help,
                key=f"{key_prefix}_{field_name}"
            )
    
    def _validate_form(self, form_data: Dict, fields_config: Dict) -> Dict:
        """
        Valida i dati del form
        
        Args:
            form_data: Dati del form
            fields_config: Configurazione campi
            
        Returns:
            Dizionario con risultato validazione
        """
        
        errors = []
        
        for field_name, field_config in fields_config.items():
            field_value = form_data.get(field_name)
            field_required = field_config.get('required', False)
            field_type = field_config.get('type', 'text')
            
            # Controllo campi obbligatori
            if field_required:
                if field_value is None or field_value == '' or field_value == []:
                    field_label = field_config.get('label', field_name)
                    errors.append(f"{field_label} è obbligatorio")
            
            # Validazioni specifiche per tipo
            if field_type == 'email' and field_value:
                if '@' not in field_value:
                    errors.append(f"Email non valida per {field_name}")
            
            if field_type == 'number' and field_value is not None:
                try:
                    float(field_value)
                except ValueError:
                    errors.append(f"Valore numerico non valido per {field_name}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def render_quick_edit_form(
        self,
        data: Dict,
        editable_fields: List[str],
        fields_config: Dict[str, Dict],
        on_submit: Optional[Callable] = None,
        key_prefix: str = "quick_edit"
    ) -> Optional[Dict]:
        """
        Rende un form di modifica rapida
        
        Args:
            data: Dati esistenti
            editable_fields: Lista campi modificabili
            fields_config: Configurazione campi
            on_submit: Callback per submit
            key_prefix: Prefisso per le chiavi
            
        Returns:
            Dizionario con i dati modificati
        """
        
        st.markdown("### ⚡ Modifica Rapida")
        
        with st.form(key=f"{key_prefix}_quick_form"):
            
            form_data = data.copy()
            
            # Rendi solo i campi modificabili
            for field_name in editable_fields:
                if field_name in fields_config:
                    field_config = fields_config[field_name]
                    field_value = self._render_field(
                        field_name, 
                        field_config, 
                        data.get(field_name),
                        key_prefix
                    )
                    form_data[field_name] = field_value
            
            # Pulsanti
            col1, col2 = st.columns(2)
            
            with col1:
                submit_button = st.form_submit_button(
                    "✅ Salva Modifiche",
                    width='stretch'
                )
            
            with col2:
                cancel_button = st.form_submit_button(
                    "❌ Annulla",
                    width='stretch'
                )
            
            if submit_button:
                if on_submit:
                    result = on_submit(form_data)
                    if result:
                        st.success("✅ Modifiche salvate con successo!")
                        st.rerun()
                    else:
                        st.error("❌ Errore durante il salvataggio")
                else:
                    return form_data
            
            elif cancel_button:
                st.info("Modifiche annullate")
                return None
        
        return None

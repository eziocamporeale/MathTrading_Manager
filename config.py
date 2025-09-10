# Configurazione Dashboard Matematico Prop/Broker
import os
from pathlib import Path

# Percorsi base
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
COMPONENTS_DIR = BASE_DIR / "components"
UTILS_DIR = BASE_DIR / "utils"
LOCALES_DIR = BASE_DIR / "locales"
DATABASE_DIR = BASE_DIR / "database"
LOGS_DIR = BASE_DIR / "logs"
BACKUPS_DIR = BASE_DIR / "backups"

# Database
DATABASE_PATH = DATA_DIR / "matematico_database.db"

# Configurazione Supabase
SUPABASE_URL = "https://znkhbkiexrqujqwgzueq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpua2hia2lleHJxdWpxd2d6dWVxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc1MDU0OTQsImV4cCI6MjA3MzA4MTQ5NH0.OPAUp3lDz4ms8ftizS0bELInOaZdouxFx2jbcgD9NAc"

# Configurazione database (SQLite per sviluppo locale, Supabase per produzione)
USE_SUPABASE = True  # Cambia a False per usare SQLite locale

# Configurazione app
APP_TITLE = "Dashboard Matematico Prop/Broker"
APP_ICON = "🧮"
PAGE_ICON = "🧮"

# Configurazione tema
CUSTOM_COLORS = {
    'primary': '#2E86AB',      # Blu principale
    'secondary': '#A23B72',    # Viola secondario
    'success': '#28A745',      # Verde per successi
    'info': '#17A2B8',         # Azzurro per info
    'warning': '#FFC107',      # Giallo per warning
    'danger': '#DC3545',       # Rosso per errori
    'light': '#F8F9FA',        # Grigio chiaro
    'dark': '#343A40',         # Grigio scuro
    'white': '#FFFFFF',        # Bianco
    'broker_active': '#28A745',    # Verde per broker attivi
    'broker_inactive': '#6C757D',  # Grigio per broker inattivi
    'prop_active': '#17A2B8',      # Azzurro per prop attive
    'prop_inactive': '#6C757D',    # Grigio per prop inattive
    'wallet_positive': '#28A745',   # Verde per saldi positivi
    'wallet_negative': '#DC3545',  # Rosso per saldi negativi
    'neutral': '#6C757D'       # Grigio neutro
}

# Configurazione autenticazione
AUTH_CONFIG = {
    'cookie_name': 'matematico_dashboard_auth',
    'cookie_key': 'matematico_dashboard_key',
    'cookie_expiry_days': 30,
    'preauthorized': ['admin@matematico.com']
}

# Configurazione stati Broker
BROKER_STATES = [
    {'id': 1, 'name': 'Attivo', 'color': '#28A745', 'order': 1},
    {'id': 2, 'name': 'Inattivo', 'color': '#6C757D', 'order': 2},
    {'id': 3, 'name': 'Sospeso', 'color': '#FFC107', 'order': 3},
    {'id': 4, 'name': 'Bloccato', 'color': '#DC3545', 'order': 4}
]

# Configurazione stati Prop
PROP_STATES = [
    {'id': 1, 'name': 'Attiva', 'color': '#28A745', 'order': 1},
    {'id': 2, 'name': 'Inattiva', 'color': '#6C757D', 'order': 2},
    {'id': 3, 'name': 'In Verifica', 'color': '#FFC107', 'order': 3},
    {'id': 4, 'name': 'Rifiutata', 'color': '#DC3545', 'order': 4}
]

# Configurazione stati Wallet
WALLET_STATES = [
    {'id': 1, 'name': 'Attivo', 'color': '#28A745', 'order': 1},
    {'id': 2, 'name': 'Inattivo', 'color': '#6C757D', 'order': 2},
    {'id': 3, 'name': 'Sospeso', 'color': '#FFC107', 'order': 3},
    {'id': 4, 'name': 'Bloccato', 'color': '#DC3545', 'order': 4}
]

# Configurazione stati Pack Copiatore
PACK_COPIATORE_STATES = [
    {'id': 1, 'name': 'Attivo', 'color': '#28A745', 'order': 1},
    {'id': 2, 'name': 'Inattivo', 'color': '#6C757D', 'order': 2},
    {'id': 3, 'name': 'In Test', 'color': '#FFC107', 'order': 3},
    {'id': 4, 'name': 'Errore', 'color': '#DC3545', 'order': 4}
]

# Configurazione stati Gruppi PAMM
GRUPPI_PAMM_STATES = [
    {'id': 1, 'name': 'Attivo', 'color': '#28A745', 'order': 1},
    {'id': 2, 'name': 'Inattivo', 'color': '#6C757D', 'order': 2},
    {'id': 3, 'name': 'In Gestione', 'color': '#FFC107', 'order': 3},
    {'id': 4, 'name': 'Chiuso', 'color': '#DC3545', 'order': 4}
]

# Configurazione ruoli utenti
USER_ROLES = [
    {'id': 1, 'name': 'Admin', 'permissions': ['all']},
    {'id': 2, 'name': 'Manager', 'permissions': ['manage_brokers', 'manage_props', 'manage_wallets', 'view_reports']},
    {'id': 3, 'name': 'Trader', 'permissions': ['manage_wallets', 'view_brokers', 'view_props']},
    {'id': 4, 'name': 'Copiatore', 'permissions': ['manage_pack_copiatore', 'view_wallets']},
    {'id': 5, 'name': 'PAMM Manager', 'permissions': ['manage_gruppi_pamm', 'view_wallets']},
    {'id': 6, 'name': 'Viewer', 'permissions': ['view_all']}
]

# Configurazione paginazione
ITEMS_PER_PAGE = 20

# Configurazione backup
BACKUP_RETENTION_DAYS = 30

# Configurazione logging
LOG_LEVEL = "INFO"
LOG_FILE = LOGS_DIR / "app.log"

# Configurazione AI Assistant DeepSeek
DEEPSEEK_API_KEY = "sk-f7531fb25e8a4ba3ae22d8b33c7d97a1"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

# Configurazione AI Assistant
AI_ASSISTANT_CONFIG = {
    'max_tokens': 1500,
    'temperature': 0.7,
    'timeout': 60,
    'retry_attempts': 3,
    'cache_responses': True,
    'cache_duration_hours': 24
}

# Prompt templates per AI Assistant Matematico
AI_PROMPTS = {
    'broker_analysis': """
    Analizza i dati del broker e fornisci insights professionali:
    
    DATI BROKER:
    - Nome: {nome_broker}
    - Stato: {stato}
    - Tipo: {tipo_broker}
    - Regolamentazione: {regolamentazione}
    - Spread: {spread}
    - Commissioni: {commissioni}
    - Leverage: {leverage}
    - Data Creazione: {data_creazione}
    
    ANALISI RICHIESTA:
    1. **Performance Generale**: Valuta la performance del broker
    2. **Competitività**: Confronta con altri broker del settore
    3. **Sicurezza**: Valuta la sicurezza e affidabilità
    4. **Raccomandazioni**: Suggerimenti per l'utilizzo ottimale
    
    Risposta in formato markdown, professionale e dettagliata.
    """,
    
    'prop_analysis': """
    Analizza i dati della prop firm e fornisci insights:
    
    DATI PROP:
    - Nome: {nome_prop}
    - Stato: {stato}
    - Capitale Iniziale: {capitale_iniziale}
    - Drawdown Massimo: {drawdown_massimo}
    - Profit Target: {profit_target}
    - Regole: {regole}
    - Data Creazione: {data_creazione}
    
    ANALISI RICHIESTA:
    1. **Valutazione Rischi**: Analizza i rischi della prop
    2. **Opportunità**: Identifica le opportunità di profitto
    3. **Strategia**: Suggerimenti per approcciare la prop
    4. **Monitoraggio**: Come monitorare la performance
    
    Risposta in formato markdown, con analisi dettagliate.
    """,
    
    'wallet_analysis': """
    Analizza i dati del wallet e fornisci insights:
    
    DATI WALLET:
    - Indirizzo: {indirizzo_wallet}
    - Tipo: {tipo_wallet}
    - Saldo Attuale: {saldo_attuale}
    - Valuta: {valuta}
    - Stato: {stato}
    - Data Creazione: {data_creazione}
    
    STORIA TRANSAZIONI:
    {storia_transazioni}
    
    ANALISI RICHIESTA:
    1. **Performance**: Analizza la performance del wallet
    2. **Trend**: Identifica i trend delle transazioni
    3. **Rischi**: Valuta i rischi associati
    4. **Ottimizzazione**: Suggerimenti per ottimizzare
    
    Risposta in formato markdown, con grafici e analisi.
    """,
    
    'pack_copiatore_analysis': """
    Analizza i dati del pack copiatore:
    
    DATI PACK:
    - Numero Pack: {numero_pack}
    - Broker: {broker}
    - Account: {account}
    - Stato: {stato}
    - Performance: {performance}
    - Data Creazione: {data_creazione}
    
    ANALISI RICHIESTA:
    1. **Efficacia**: Valuta l'efficacia del pack
    2. **Rischi**: Identifica i rischi associati
    3. **Ottimizzazione**: Suggerimenti per migliorare
    4. **Monitoraggio**: Come monitorare la performance
    
    Risposta in formato markdown, professionale.
    """,
    
    'gruppi_pamm_analysis': """
    Analizza i dati dei gruppi PAMM:
    
    DATI GRUPPO PAMM:
    - Nome: {nome_gruppo}
    - Manager: {manager}
    - Capitale Totale: {capitale_totale}
    - Numero Partecipanti: {numero_partecipanti}
    - Performance: {performance}
    - Data Creazione: {data_creazione}
    
    ANALISI RICHIESTA:
    1. **Performance Gruppo**: Analizza la performance del gruppo
    2. **Gestione Rischi**: Valuta la gestione dei rischi
    3. **Crescita**: Analizza il potenziale di crescita
    4. **Raccomandazioni**: Suggerimenti per il gruppo
    
    Risposta in formato markdown, dettagliata.
    """,
    
    'incroci_analysis': """
    Analizza gli incroci tra broker, prop, wallet e gruppi PAMM:
    
    DATI INCROCI:
    {incroci_data}
    
    ANALISI RICHIESTA:
    1. **Pattern di Successo**: Identifica i pattern vincenti
    2. **Sinergie**: Analizza le sinergie tra componenti
    3. **Rischi**: Valuta i rischi degli incroci
    4. **Ottimizzazione**: Suggerimenti per ottimizzare gli incroci
    
    Risposta in formato markdown, con analisi comparative.
    """
}

# Creazione directory necessarie
def create_directories():
    """Crea le directory necessarie per il funzionamento dell'app"""
    directories = [DATA_DIR, COMPONENTS_DIR, UTILS_DIR, LOCALES_DIR, DATABASE_DIR, LOGS_DIR, BACKUPS_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Inizializzazione
if __name__ == "__main__":
    create_directories()
    print("✅ Directory create con successo")

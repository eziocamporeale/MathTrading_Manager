# 🧮 DASH_PROP_BROKER

Dashboard Matematico per la Gestione di Broker, Prop Firm, Wallet e Gruppi PAMM

## 📋 Descrizione

DASH_PROP_BROKER è una dashboard Streamlit completa per la gestione di:
- **Broker**: Gestione broker forex e CFD con informazioni dettagliate
- **Prop Firm**: Gestione prop firm con regole e configurazioni
- **Wallet**: Gestione wallet crypto con saldi e transazioni
- **Pack Copiatori**: Gestione pack copiatori per trading automatico
- **Gruppi PAMM**: Gestione gruppi PAMM con performance tracking
- **Incroci**: Gestione incroci tra tutti i componenti del sistema

## 🚀 Caratteristiche Principali

### 📊 Dashboard Principale
- Panoramica generale con metriche in tempo reale
- Grafici interattivi per analisi performance
- Statistiche aggregate per tutti i componenti

### 🏢 Gestione Broker
- CRUD completo per broker
- Informazioni dettagliate: regolamentazione, spread, commissioni
- Supporto per diversi tipi di broker (ECN, STP, Market Maker)

### 🏛️ Gestione Prop Firm
- Gestione prop firm con regole specifiche
- Tracking di drawdown e profit target
- Configurazione commissioni e fee

### 💰 Gestione Wallet
- Gestione wallet crypto sicura
- Tracking saldi e transazioni
- Supporto per multiple valute

### 📦 Gestione Pack Copiatori
- Gestione pack copiatori per trading automatico
- Collegamento con broker specifici
- Monitoring performance e drawdown

### 👥 Gestione Gruppi PAMM
- Gestione gruppi PAMM con manager
- Tracking performance e partecipanti
- Calcolo commissioni automatico

### 🔄 Gestione Incroci
- Creazione incroci tra tutti i componenti
- Analisi performance aggregate
- Gestione rischi centralizzata

## 🛠️ Tecnologie Utilizzate

- **Frontend**: Streamlit
- **Database**: Supabase (PostgreSQL)
- **Visualizzazione**: Plotly
- **Autenticazione**: Supabase Auth
- **Sicurezza**: Row Level Security (RLS)

## 📦 Installazione

### Prerequisiti
- Python 3.8+
- Account Supabase

### Setup

1. **Clona il repository**
```bash
git clone <repository-url>
cd DASH_PROP_BROKER
```

2. **Installa le dipendenze**
```bash
pip install -r requirements.txt
```

3. **Configura Supabase**
   - Crea un progetto Supabase
   - Esegui lo schema SQL in `database/supabase_schema.sql`
   - Configura le variabili d'ambiente:
   ```bash
   export SUPABASE_URL="your-supabase-url"
   export SUPABASE_KEY="your-supabase-anon-key"
   ```

4. **Avvia l'applicazione**
```bash
streamlit run app.py
```

## 🗄️ Schema Database

Il database include le seguenti tabelle:

### Tabelle Principali
- `brokers`: Informazioni broker
- `prop_firms`: Configurazioni prop firm
- `wallets`: Wallet crypto
- `pack_copiatori`: Pack copiatori
- `gruppi_pamm`: Gruppi PAMM
- `incroci`: Incroci tra componenti

### Tabelle Supporto
- `users`: Utenti del sistema
- `transazioni_wallet`: Transazioni wallet
- `performance_history`: Storico performance

## 🔐 Sicurezza

- **Row Level Security (RLS)** abilitato su tutte le tabelle
- **Crittografia** per dati sensibili (chiavi private, password)
- **Autenticazione** tramite Supabase Auth
- **Autorizzazione** basata su ruoli utente

## 📊 Funzionalità AI Assistant

Il sistema include un AI Assistant integrato con DeepSeek per:
- Analisi performance broker e prop firm
- Consigli di ottimizzazione
- Predizione rischi
- Generazione report automatici

## 🎯 Ruoli Utente

- **Admin**: Accesso completo a tutte le funzionalità
- **Manager**: Gestione broker, prop, wallet, visualizzazione report
- **Trader**: Gestione wallet, visualizzazione broker e prop
- **Copiatore**: Gestione pack copiatori, visualizzazione wallet
- **PAMM Manager**: Gestione gruppi PAMM, visualizzazione wallet
- **Viewer**: Solo visualizzazione dati

## 📈 Metriche e Analytics

- Performance tracking in tempo reale
- Analisi drawdown e rischio
- Grafici interattivi con Plotly
- Export dati in Excel/CSV
- Report personalizzabili

## 🔧 Configurazione

### Variabili d'Ambiente
```bash
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
DEEPSEEK_API_KEY=your-deepseek-api-key
```

### Configurazione App
Modifica `config.py` per personalizzare:
- Colori tema
- Stati e ruoli
- Configurazioni AI Assistant
- Impostazioni database

## 📝 Utilizzo

### Dashboard Principale
- Visualizza metriche generali
- Analizza performance aggregate
- Monitora stato sistema

### Gestione Broker
1. Vai su "🏢 Broker"
2. Visualizza lista broker esistenti
3. Aggiungi nuovo broker con "➕ Aggiungi Broker"
4. Compila form con informazioni broker

### Gestione Prop Firm
1. Vai su "🏛️ Prop Firm"
2. Visualizza prop firm esistenti
3. Aggiungi nuova prop firm
4. Configura regole e parametri

### Gestione Wallet
1. Vai su "💰 Wallet"
2. Visualizza wallet esistenti
3. Aggiungi nuovo wallet
4. Configura informazioni crypto

### Gestione Pack Copiatori
1. Vai su "📦 Pack Copiatori"
2. Visualizza pack esistenti
3. Aggiungi nuovo pack
4. Collega con broker specifico

### Gestione Gruppi PAMM
1. Vai su "👥 Gruppi PAMM"
2. Visualizza gruppi esistenti
3. Aggiungi nuovo gruppo
4. Configura manager e parametri

### Gestione Incroci
1. Vai su "🔄 Incroci"
2. Visualizza incroci esistenti
3. Crea nuovo incrocio
4. Collega tutti i componenti

## 🚨 Troubleshooting

### Problemi Comuni

1. **Errore connessione Supabase**
   - Verifica URL e chiave Supabase
   - Controlla configurazione RLS
   - Testa connessione in Impostazioni

2. **Errore import moduli**
   - Verifica installazione dipendenze
   - Controlla percorsi Python
   - Reinstalla requirements.txt

3. **Errore autenticazione**
   - Verifica configurazione Supabase Auth
   - Controlla politiche RLS
   - Verifica ruoli utente

## 📞 Supporto

Per supporto tecnico o domande:
- Contatta: admin@matematico.com
- Documentazione: README.md
- Issues: GitHub Issues

## 📄 Licenza

Proprietario: Ezio Camporeale
Tutti i diritti riservati.

## 🔄 Changelog

### v1.0.0 (2025-01-XX)
- Release iniziale
- Gestione completa broker, prop firm, wallet
- Dashboard Streamlit con Supabase
- Sistema CRUD completo
- AI Assistant integrato
- Sicurezza RLS implementata

---

**Creato da Ezio Camporeale** 🧮

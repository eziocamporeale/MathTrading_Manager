# 📋 ISTRUZIONI PER ESEGUIRE LO SCHEMA SQL SU SUPABASE

## 🎯 **OBIETTIVO**: Creare tutte le tabelle necessarie nel database Supabase

---

## 🚀 **STEP 1: ACCEDI AL DASHBOARD SUPABASE**

1. **Vai su**: https://supabase.com/dashboard
2. **Accedi** al tuo account Supabase
3. **Seleziona il progetto**: `znkhbkiexrqujqwgzueq`

---

## 🚀 **STEP 2: APRI L'SQL EDITOR**

1. **Nel menu laterale**, clicca su **"SQL Editor"**
2. **Clicca su "New Query"** per creare una nuova query
3. **Dai un nome** alla query: `DASH_PROP_BROKER_Schema`

---

## 🚀 **STEP 3: COPIA E INCOLLA LO SCHEMA**

1. **Apri il file**: `database/supabase_schema.sql`
2. **Copia tutto il contenuto** del file (Ctrl+A, Ctrl+C)
3. **Incolla nell'editor SQL** di Supabase (Ctrl+V)

---

## 🚀 **STEP 4: ESEGUI LO SCHEMA**

1. **Clicca sul pulsante "Run"** (o premi Ctrl+Enter)
2. **Attendi** che l'esecuzione sia completata
3. **Verifica** che non ci siano errori nella console

---

## 🚀 **STEP 5: VERIFICA CREAZIONE TABELLE**

1. **Vai su "Table Editor"** nel menu laterale
2. **Verifica** che siano state create queste tabelle:

### ✅ **Tabelle Principali**
- `brokers` - Gestione broker
- `prop_firms` - Gestione prop firm
- `wallets` - Gestione wallet crypto
- `pack_copiatori` - Gestione pack copiatori
- `gruppi_pamm` - Gestione gruppi PAMM
- `incroci` - Gestione incroci tra componenti

### ✅ **Tabelle Supporto**
- `users` - Utenti del sistema
- `transazioni_wallet` - Transazioni wallet
- `performance_history` - Storico performance

---

## 🚀 **STEP 6: VERIFICA DATI DI ESEMPIO**

1. **Clicca su una tabella** (es. `brokers`)
2. **Verifica** che ci siano dati di esempio inseriti
3. **Controlla** che i dati siano corretti

### 📊 **Dati di Esempio Attesi**

#### **Brokers (5 record)**
- IC Markets, Pepperstone, XM, FXCM, OANDA

#### **Prop Firms (5 record)**
- FTMO, MyForexFunds, The5ers, TopStep, Apex Trader Funding

#### **Wallets (5 record)**
- Bitcoin, Ethereum, Tron, Dogecoin, Litecoin

#### **Pack Copiatori (5 record)**
- PACK001, PACK002, PACK003, PACK004, PACK005

#### **Gruppi PAMM (5 record)**
- Gruppo Alpha, Beta, Gamma, Delta, Epsilon

#### **Incroci (5 record)**
- Incrocio Alpha, Beta, Gamma, Delta, Epsilon

---

## 🚨 **PROBLEMI COMUNI E SOLUZIONI**

### ❌ **Errore: "relation already exists"**
**Soluzione**: Le tabelle esistono già. Puoi ignorare questo errore o eliminare le tabelle esistenti.

### ❌ **Errore: "permission denied"**
**Soluzione**: Verifica di avere i permessi di amministratore sul progetto Supabase.

### ❌ **Errore: "syntax error"**
**Soluzione**: Controlla che tutto il contenuto del file sia stato copiato correttamente.

### ❌ **Errore: "connection timeout"**
**Soluzione**: Riprova l'esecuzione o controlla la connessione internet.

---

## 🎯 **VERIFICA FINALE**

Dopo l'esecuzione dello schema, dovresti vedere:

✅ **9 tabelle create** nel Table Editor
✅ **Dati di esempio inseriti** in tutte le tabelle
✅ **Indici creati** per ottimizzare le performance
✅ **Trigger configurati** per aggiornamenti automatici
✅ **RLS abilitato** per la sicurezza

---

## 🚀 **PROSSIMO STEP**

Una volta completato lo schema SQL:

1. **Torna al terminale**
2. **Esegui**: `python3 test_supabase_connection.py`
3. **Verifica** che la connessione funzioni
4. **Avvia l'app**: `streamlit run app.py`

---

## 📞 **SUPPORTO**

Se hai problemi:

1. **Controlla i log** nell'SQL Editor di Supabase
2. **Verifica le credenziali** del progetto
3. **Contatta**: admin@matematico.com

---

**🎉 Una volta completato questo step, il database sarà pronto e l'applicazione funzionerà al 100%!**

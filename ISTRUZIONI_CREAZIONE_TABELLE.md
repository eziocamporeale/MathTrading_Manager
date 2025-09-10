# 🚨 RISOLUZIONE ERRORE: "relation 'roles' does not exist"

## 🔍 **PROBLEMA IDENTIFICATO:**
L'errore `ERROR: 42P01: relation "roles" does not exist` indica che le tabelle di autenticazione non sono state create nel database Supabase.

## ✅ **SOLUZIONE IMMEDIATA:**

### **STEP 1: Creare Tabelle di Autenticazione**
1. Vai su **Supabase Dashboard** → **SQL Editor**
2. Esegui il file `create_auth_tables.sql`
3. Questo script creerà:
   - Tabella `roles` con 6 ruoli predefiniti
   - Tabella `users` con 2 utenti predefiniti
   - Politiche RLS permissive

### **STEP 2: Verificare Creazione**
Dopo aver eseguito lo script, dovresti vedere:
```
table_name | row_count
-----------+----------
roles      | 6
users      | 2
```

### **STEP 3: Testare Login**
1. Esegui `streamlit run app.py`
2. Prova login con:
   - **Admin:** `admin` / `admin123`
   - **Demo:** `demo` / `demo123`

## 📋 **ORDINE DI ESECUZIONE SCRIPT:**

1. **PRIMO:** `create_auth_tables.sql` (crea tabelle)
2. **SECONDO:** `fix_rls_auth.sql` (risolve RLS)
3. **TERZO:** Testare l'applicazione

## 🔧 **SE PERSISTONO ERRORI:**

### **Controlla:**
- ✅ Credenziali Supabase in `config.py`
- ✅ Connessione con `test_supabase_connection.py`
- ✅ Log del terminale per errori specifici

### **Riavvia:**
1. Chiudi Streamlit (Ctrl+C)
2. Esegui `streamlit run app.py`
3. Testa login

## 🎯 **RISULTATO ATTESO:**
- ✅ Nessun errore "relation does not exist"
- ✅ Login funzionante
- ✅ Accesso alle sezioni protette
- ✅ Gestione utenti accessibile

---

**Il sistema di autenticazione è implementato correttamente, serve solo creare le tabelle nel database!** 🚀

# 🔧 ISTRUZIONI PER RISOLVERE ERRORI

## 🚨 **ERRORI IDENTIFICATI:**

1. **❌ Colonna 'phone' mancante** nella tabella users
2. **❌ Foreign key constraint** impedisce eliminazione broker

## 📋 **PASSI PER RISOLVERE:**

### **1️⃣ FIX COLONNA PHONE**

Esegui nel **SQL Editor di Supabase**:

```sql
-- Aggiungi colonna phone se non esiste
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS phone VARCHAR(20);
```

### **2️⃣ FIX FOREIGN KEY CONSTRAINTS**

Esegui nel **SQL Editor di Supabase**:

```sql
-- Modifica foreign key per pack_copiatori per permettere eliminazione a cascata
ALTER TABLE pack_copiatori 
DROP CONSTRAINT IF EXISTS pack_copiatori_broker_id_fkey;

ALTER TABLE pack_copiatori 
ADD CONSTRAINT pack_copiatori_broker_id_fkey 
FOREIGN KEY (broker_id) REFERENCES brokers(id) 
ON DELETE CASCADE;

-- Modifica foreign key per wallets per permettere eliminazione a cascata
ALTER TABLE wallets 
DROP CONSTRAINT IF EXISTS wallets_broker_id_fkey;

ALTER TABLE wallets 
ADD CONSTRAINT wallets_broker_id_fkey 
FOREIGN KEY (broker_id) REFERENCES brokers(id) 
ON DELETE CASCADE;

-- Modifica foreign key per gruppi_pamm per permettere eliminazione a cascata
ALTER TABLE gruppi_pamm 
DROP CONSTRAINT IF EXISTS gruppi_pamm_broker_id_fkey;

ALTER TABLE gruppi_pamm 
ADD CONSTRAINT gruppi_pamm_broker_id_fkey 
FOREIGN KEY (broker_id) REFERENCES brokers(id) 
ON DELETE CASCADE;

-- Modifica foreign key per incroci per permettere eliminazione a cascata
ALTER TABLE incroci 
DROP CONSTRAINT IF EXISTS incroci_broker_id_fkey;

ALTER TABLE incroci 
ADD CONSTRAINT incroci_broker_id_fkey 
FOREIGN KEY (broker_id) REFERENCES brokers(id) 
ON DELETE CASCADE;
```

## ✅ **RISULTATO ATTESO:**

- ✅ **Creazione utenti** funzionante (colonna phone aggiunta)
- ✅ **Eliminazione broker** funzionante (foreign key a cascata)
- ✅ **Sistema completo** operativo

## 🔍 **VERIFICA:**

Dopo aver eseguito gli script, testa:
1. **Creazione nuovo utente** nella dashboard
2. **Eliminazione broker** (dovrebbe eliminare anche i record correlati)

---

**Esegui questi script e poi riprova la creazione utenti!** 🚀

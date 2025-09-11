# 🚀 ISTRUZIONI ESTENSIONE TABELLA GRUPPI PAMM

## 📋 **COSA È STATO FATTO**

✅ **Modello GruppiPAMM esteso** con tutti i campi identificati dall'Excel gruppi DEF
✅ **Script SQL** per aggiornare il database Supabase
✅ **Funzioni di utilità** per conversione dati
✅ **Dati di esempio** basati sull'Excel originale

## 🎯 **NUOVI CAMPI AGGIUNTI**

### **Campi Cliente**
- `nome_cliente`: Nome completo cliente (es. "MANUEL CARINI [4000]")
- `importo_cliente`: Importo tra parentesi quadre

### **Campi Stato Prop**
- `stato_prop`: "Svolto", "Non svolto", "mancanza saldo"
- `deposito_pamm`: "Depositata" o vuoto
- `quota_prop`: Sempre 1 (come nell'Excel)

### **Campi Tracking**
- `ciclo_numero`: Numero ciclo progressivo
- `fase_prop`: Fase prop firm
- `operazione_numero`: Numero operazione

### **Campi Esiti**
- `esito_broker`: Esito broker
- `esito_prop`: Esito prop firm

### **Campi Finanziari**
- `prelievo_prop`: Importo prelievo prop
- `prelievo_profit`: Importo prelievo profit
- `commissioni_percentuale`: Commissioni (default 25%)

### **Campi Credenziali**
- `credenziali_broker`: Credenziali broker (da crittografare)
- `credenziali_prop`: Credenziali prop firm (da crittografare)

### **Campi Gruppo**
- `responsabili_gruppo`: Responsabili identificati (es. "frank andre", "mario")
- `numero_membri_gruppo`: Numero membri gruppo (es. 12k, 10k, 7k)

## 🔧 **ISTRUZIONI PER APPLICARE LE MODIFICHE**

### **1. Eseguire Script SQL in Supabase**

1. **Vai su Supabase Dashboard**
2. **Apri SQL Editor**
3. **Copia e incolla** il contenuto del file `extend_gruppi_pamm_table.sql`
4. **Esegui lo script**

### **2. Verificare l'Applicazione**

Lo script:
- ✅ Aggiunge tutte le nuove colonne
- ✅ Crea indici per performance
- ✅ Aggiunge commenti esplicativi
- ✅ Inserisce dati di esempio
- ✅ Verifica la struttura finale

### **3. Controllare Risultati**

Dopo l'esecuzione dovresti vedere:
- **Nuove colonne** nella tabella `gruppi_pamm`
- **Dati di esempio** inseriti
- **Indici** creati per performance
- **Struttura verificata** con query finale

## 📊 **DATI DI ESEMPIO INSERITI**

### **Gruppo 1** (12k membri - frank andre)
- MANUEL CARINI [4000] - mancanza saldo
- MIRKO CARINI [8000] - mancanza saldo

### **Gruppo 2** (10k membri - mario)
- LUIGI GUGLIELMELLI (2404) - Svolto, Depositata
- VITO ZONNO [801] - Svolto, Depositata
- VINCENZO VOZZA [972] - Svolto, Depositata
- MARIO MAZZA 2 [2000] - Svolto

### **Gruppo 3** (7k membri - fede trott|mario)
- MIRKO MINATI RIZZI [1876] - Svolto, Depositata
- SILVIA SAMMARTANO [1887] - Svolto, Depositata
- PIERA ANDRANI [1000] - Non svolto
- PAOLA PIRAS [1000] - Non svolto
- MAURIZIO PETRACHI [1000] - Non svolto

## ⚠️ **NOTE IMPORTANTI**

1. **Backup**: Lo script è sicuro e non elimina dati esistenti
2. **Conflitti**: Usa `ON CONFLICT DO NOTHING` per evitare duplicati
3. **Performance**: Indici creati per query ottimali
4. **Sicurezza**: Credenziali da crittografare in futuro

## 🎯 **PROSSIMI PASSI**

Dopo aver eseguito lo script:

1. **✅ Conferma** che le colonne sono state aggiunte
2. **✅ Verifica** i dati di esempio
3. **✅ Procedi** con l'implementazione CRUD
4. **✅ Crea** la visualizzazione Excel-like

---

**🚀 PRONTO PER IL PROSSIMO STEP!**

Una volta eseguito lo script, dimmi e procederemo con l'implementazione CRUD completa!

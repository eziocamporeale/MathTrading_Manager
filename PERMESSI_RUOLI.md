# 🔐 SISTEMA DI PERMESSI PER RUOLI

## 📊 **TABELLA PERMESSI COMPLETA**

| Funzionalità | Admin | Manager | Trader | Copiatore | PAMM Manager | Viewer |
|--------------|-------|---------|--------|-----------|--------------|--------|
| **🏢 Broker** | ✅ Tutto | ✅ Gestione | 👁️ Solo vista | 👁️ Solo vista | 👁️ Solo vista | 👁️ Solo vista |
| **🏛️ Prop Firm** | ✅ Tutto | ✅ Gestione | 👁️ Solo vista | 👁️ Solo vista | 👁️ Solo vista | 👁️ Solo vista |
| **💰 Wallet** | ✅ Tutto | ✅ Gestione | ✅ Gestione | 👁️ Solo vista | 👁️ Solo vista | 👁️ Solo vista |
| **📦 Pack Copiatori** | ✅ Tutto | ✅ Gestione | 👁️ Solo vista | ✅ Gestione | 👁️ Solo vista | 👁️ Solo vista |
| **👥 Gruppi PAMM** | ✅ Tutto | ✅ Gestione | 👁️ Solo vista | 👁️ Solo vista | ✅ Gestione | 👁️ Solo vista |
| **🔄 Incroci** | ✅ Tutto | ✅ Gestione | 👁️ Solo vista | 👁️ Solo vista | 👁️ Solo vista | 👁️ Solo vista |
| **👤 Gestione Utenti** | ✅ Solo Admin | ❌ Negato | ❌ Negato | ❌ Negato | ❌ Negato | ❌ Negato |
| **⚙️ Impostazioni** | ✅ Solo Admin | ❌ Negato | ❌ Negato | ❌ Negato | ❌ Negato | ❌ Negato |

## 🎯 **DETTAGLIO PERMESSI**

### **👑 ADMIN**
- **Potere:** Completo controllo del sistema
- **Accesso:** Tutte le funzionalità
- **Gestione:** Utenti, ruoli, impostazioni, tutti i dati
- **Sicurezza:** Massimo livello di accesso

### **👨‍💼 MANAGER**
- **Potere:** Gestione operativa completa
- **Accesso:** Tutte le sezioni business (Broker, Prop, Wallet, Pack, PAMM, Incroci)
- **Limitazioni:** Non può gestire utenti o impostazioni di sistema
- **Sicurezza:** Alto livello operativo

### **📈 TRADER**
- **Potere:** Gestione wallet e visualizzazione dati
- **Accesso:** Gestione wallet, visualizzazione di tutto il resto
- **Limitazioni:** Non può gestire Broker, Prop, Pack, PAMM, Incroci
- **Sicurezza:** Livello trading

### **📋 COPIATORE**
- **Potere:** Gestione pack copiatori e visualizzazione limitata
- **Accesso:** Gestione pack, visualizzazione Broker, Prop, Wallet
- **Limitazioni:** Non può gestire PAMM, Incroci
- **Sicurezza:** Livello operativo limitato

### **👥 PAMM MANAGER**
- **Potere:** Gestione PAMM e visualizzazione correlata
- **Accesso:** Gestione PAMM, visualizzazione Broker, Wallet, Incroci
- **Limitazioni:** Non può gestire Prop, Pack
- **Sicurezza:** Livello PAMM specializzato

### **👁️ VIEWER**
- **Potere:** Solo visualizzazione
- **Accesso:** Visualizzazione di tutte le sezioni
- **Limitazioni:** Non può modificare nulla
- **Sicurezza:** Livello consultivo

## 🔒 **SICUREZZA IMPLEMENTATA**

- ✅ **Controllo ruoli** per ogni pagina
- ✅ **Verifica permessi** prima di ogni azione
- ✅ **Accesso negato** con messaggio chiaro
- ✅ **Sessione sicura** con timeout automatico
- ✅ **Hash password** con bcrypt

---

**Il sistema garantisce che ogni ruolo abbia solo i permessi necessari per la sua funzione!** 🛡️

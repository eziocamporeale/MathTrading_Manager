#!/usr/bin/env python3
"""
Test Connessione Supabase per DASH_PROP_BROKER
Script per verificare la connessione e configurazione Supabase
Creato da Ezio Camporeale
"""

import sys
from pathlib import Path
import os

# Aggiungi il percorso della directory corrente al path di Python
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def test_supabase_connection():
    """Testa la connessione a Supabase"""
    print("🧮 DASH_PROP_BROKER - Test Connessione Supabase")
    print("=" * 50)
    
    try:
        # Importa il SupabaseManager
        from database.supabase_manager import SupabaseManager
        print("✅ SupabaseManager importato correttamente")
        
        # Inizializza il manager
        supabase_manager = SupabaseManager()
        print(f"✅ SupabaseManager inizializzato")
        print(f"   URL: {supabase_manager.url}")
        print(f"   Configurato: {supabase_manager.is_configured}")
        
        if not supabase_manager.is_configured:
            print("❌ Supabase non configurato correttamente")
            return False
        
        # Test connessione
        print("\n🔍 Testando connessione Supabase...")
        success, message = supabase_manager.test_connection()
        
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            return False
        
        # Test operazioni CRUD base
        print("\n📊 Testando operazioni CRUD...")
        
        # Test lettura broker
        print("   📖 Test lettura broker...")
        brokers = supabase_manager.get_brokers()
        print(f"   ✅ Broker trovati: {len(brokers)}")
        
        # Test lettura prop firm
        print("   📖 Test lettura prop firm...")
        props = supabase_manager.get_props()
        print(f"   ✅ Prop firm trovate: {len(props)}")
        
        # Test lettura wallet
        print("   📖 Test lettura wallet...")
        wallets = supabase_manager.get_wallets()
        print(f"   ✅ Wallet trovati: {len(wallets)}")
        
        # Test lettura pack copiatori
        print("   📖 Test lettura pack copiatori...")
        packs = supabase_manager.get_pack_copiatori()
        print(f"   ✅ Pack copiatori trovati: {len(packs)}")
        
        # Test lettura gruppi PAMM
        print("   📖 Test lettura gruppi PAMM...")
        gruppi = supabase_manager.get_gruppi_pamm()
        print(f"   ✅ Gruppi PAMM trovati: {len(gruppi)}")
        
        # Test lettura incroci
        print("   📖 Test lettura incroci...")
        incroci = supabase_manager.get_incroci()
        print(f"   ✅ Incroci trovati: {len(incroci)}")
        
        # Test statistiche
        print("\n📈 Testando statistiche...")
        stats = supabase_manager.get_statistiche_generali()
        print(f"   📊 Statistiche: {stats}")
        
        print("\n🎉 Tutti i test sono stati superati con successo!")
        print("✅ Supabase è configurato correttamente e operativo")
        
        return True
        
    except ImportError as e:
        print(f"❌ Errore import: {e}")
        print("💡 Assicurati di aver installato le dipendenze: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        return False

def test_app_startup():
    """Testa l'avvio dell'applicazione Streamlit"""
    print("\n🚀 Test Avvio Applicazione Streamlit")
    print("=" * 50)
    
    try:
        # Test import app
        import app
        print("✅ App Streamlit importata correttamente")
        
        # Test import config
        from config import APP_TITLE, SUPABASE_URL, SUPABASE_KEY
        print(f"✅ Config importata correttamente")
        print(f"   Titolo App: {APP_TITLE}")
        print(f"   Supabase URL: {SUPABASE_URL}")
        print(f"   Supabase Key: {SUPABASE_KEY[:20]}...")
        
        print("✅ L'applicazione può essere avviata correttamente")
        print("💡 Per avviare l'app: streamlit run app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore durante il test app: {e}")
        return False

def main():
    """Funzione principale di test"""
    print("🧮 DASH_PROP_BROKER - Test Completo Sistema")
    print("=" * 60)
    
    # Test 1: Connessione Supabase
    supabase_ok = test_supabase_connection()
    
    # Test 2: Avvio App
    app_ok = test_app_startup()
    
    # Risultato finale
    print("\n" + "=" * 60)
    print("📋 RISULTATI FINALI:")
    print(f"   Supabase: {'✅ OK' if supabase_ok else '❌ ERRORE'}")
    print(f"   App: {'✅ OK' if app_ok else '❌ ERRORE'}")
    
    if supabase_ok and app_ok:
        print("\n🎉 SISTEMA COMPLETAMENTE OPERATIVO!")
        print("🚀 Puoi avviare l'applicazione con: streamlit run app.py")
    else:
        print("\n⚠️ SISTEMA NON COMPLETAMENTE OPERATIVO")
        print("🔧 Controlla gli errori sopra e risolvi i problemi")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

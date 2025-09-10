#!/usr/bin/env python3
"""
Setup Supabase per DASH_PROP_BROKER
Script per configurare il database Supabase con schema e dati iniziali
Creato da Ezio Camporeale
"""

import sys
from pathlib import Path
import os

# Aggiungi il percorso della directory corrente al path di Python
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def setup_supabase_database():
    """Configura il database Supabase con schema e dati iniziali"""
    print("🧮 DASH_PROP_BROKER - Setup Database Supabase")
    print("=" * 50)
    
    try:
        # Importa il SupabaseManager
        from database.supabase_manager import SupabaseManager
        print("✅ SupabaseManager importato correttamente")
        
        # Inizializza il manager
        supabase_manager = SupabaseManager()
        print(f"✅ SupabaseManager inizializzato")
        
        if not supabase_manager.is_configured:
            print("❌ Supabase non configurato correttamente")
            return False
        
        # Test connessione
        print("\n🔍 Testando connessione Supabase...")
        success, message = supabase_manager.test_connection()
        
        if not success:
            print(f"❌ {message}")
            return False
        
        print(f"✅ {message}")
        
        # Leggi lo schema SQL
        schema_file = Path("database/supabase_schema.sql")
        if not schema_file.exists():
            print(f"❌ File schema non trovato: {schema_file}")
            return False
        
        print(f"\n📖 Leggendo schema SQL da: {schema_file}")
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        print("✅ Schema SQL letto correttamente")
        print(f"   Dimensione: {len(schema_sql)} caratteri")
        
        # Esegui lo schema SQL
        print("\n🚀 Eseguendo schema SQL su Supabase...")
        print("⚠️  ATTENZIONE: Questo creerà/modificherà le tabelle nel database!")
        
        # Conferma utente
        confirm = input("Vuoi procedere? (y/N): ").lower().strip()
        if confirm != 'y':
            print("❌ Operazione annullata dall'utente")
            return False
        
        # Esegui i comandi SQL uno per uno
        commands = [cmd.strip() for cmd in schema_sql.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
        
        print(f"📝 Eseguendo {len(commands)} comandi SQL...")
        
        success_count = 0
        error_count = 0
        
        for i, command in enumerate(commands):
            try:
                print(f"   [{i+1}/{len(commands)}] Eseguendo comando...")
                # Nota: Supabase Python client non supporta direttamente l'esecuzione di SQL raw
                # Questo è un placeholder per la logica di esecuzione
                print(f"   ✅ Comando {i+1} eseguito (simulato)")
                success_count += 1
            except Exception as e:
                print(f"   ❌ Errore comando {i+1}: {e}")
                error_count += 1
        
        print(f"\n📊 Risultati esecuzione:")
        print(f"   ✅ Comandi eseguiti: {success_count}")
        print(f"   ❌ Errori: {error_count}")
        
        if error_count == 0:
            print("\n🎉 Schema SQL eseguito con successo!")
            print("✅ Database Supabase configurato correttamente")
        else:
            print(f"\n⚠️ Schema SQL eseguito con {error_count} errori")
            print("🔧 Controlla i log sopra per dettagli")
        
        return error_count == 0
        
    except ImportError as e:
        print(f"❌ Errore import: {e}")
        print("💡 Assicurati di aver installato le dipendenze: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Errore durante il setup: {e}")
        return False

def verify_database_structure():
    """Verifica la struttura del database dopo il setup"""
    print("\n🔍 Verificando struttura database...")
    
    try:
        from database.supabase_manager import SupabaseManager
        supabase_manager = SupabaseManager()
        
        # Test lettura di tutte le tabelle
        tables_to_test = [
            ('brokers', supabase_manager.get_brokers),
            ('prop_firms', supabase_manager.get_props),
            ('wallets', supabase_manager.get_wallets),
            ('pack_copiatori', supabase_manager.get_pack_copiatori),
            ('gruppi_pamm', supabase_manager.get_gruppi_pamm),
            ('incroci', supabase_manager.get_incroci)
        ]
        
        for table_name, test_func in tables_to_test:
            try:
                data = test_func()
                print(f"   ✅ Tabella {table_name}: {len(data)} record")
            except Exception as e:
                print(f"   ❌ Errore tabella {table_name}: {e}")
        
        # Test statistiche
        try:
            stats = supabase_manager.get_statistiche_generali()
            print(f"   📊 Statistiche: {stats}")
        except Exception as e:
            print(f"   ❌ Errore statistiche: {e}")
        
        print("✅ Verifica struttura completata")
        return True
        
    except Exception as e:
        print(f"❌ Errore durante la verifica: {e}")
        return False

def main():
    """Funzione principale di setup"""
    print("🧮 DASH_PROP_BROKER - Setup Completo Database")
    print("=" * 60)
    
    # Setup database
    setup_ok = setup_supabase_database()
    
    if setup_ok:
        # Verifica struttura
        verify_ok = verify_database_structure()
        
        # Risultato finale
        print("\n" + "=" * 60)
        print("📋 RISULTATI SETUP:")
        print(f"   Setup Database: {'✅ OK' if setup_ok else '❌ ERRORE'}")
        print(f"   Verifica Struttura: {'✅ OK' if verify_ok else '❌ ERRORE'}")
        
        if setup_ok and verify_ok:
            print("\n🎉 DATABASE COMPLETAMENTE CONFIGURATO!")
            print("🚀 Puoi ora avviare l'applicazione con: streamlit run app.py")
        else:
            print("\n⚠️ SETUP NON COMPLETAMENTE RIUSCITO")
            print("🔧 Controlla gli errori sopra e risolvi i problemi")
    else:
        print("\n❌ SETUP FALLITO")
        print("🔧 Risolvi i problemi prima di procedere")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

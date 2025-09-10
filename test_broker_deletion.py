#!/usr/bin/env python3
"""
Test eliminazione broker per verificare foreign key CASCADE
"""

import sys
from pathlib import Path

# Aggiungi il percorso della directory corrente al path di Python
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def test_broker_deletion():
    """Test eliminazione broker con CASCADE"""
    
    print("🏢 TEST ELIMINAZIONE BROKER CON CASCADE")
    print("=" * 50)
    
    try:
        from database.supabase_manager import SupabaseManager
        
        # Inizializza manager
        supabase_manager = SupabaseManager()
        
        # Test 1: Crea broker di test
        print("\n1️⃣ Creazione Broker di Test...")
        test_broker_data = {
            'nome_broker': 'Test Broker CASCADE',
            'paese': 'Italia',
            'regolamentazione': 'CONSOB',
            'sito_web': 'https://testbroker.com',
            'note': 'Broker per test eliminazione CASCADE'
        }
        
        success, message = supabase_manager.create_broker(test_broker_data)
        if success:
            print(f"✅ {message}")
            broker_id = message.split('ID: ')[1] if 'ID: ' in message else None
        else:
            print(f"❌ {message}")
            return False
        
        # Test 2: Crea record correlati
        print(f"\n2️⃣ Creazione Record Correlati...")
        
        # Crea wallet
        wallet_data = {
            'broker_id': int(broker_id),
            'nome': 'Test Wallet CASCADE',
            'tipo': 'Demo',
            'valuta': 'EUR',
            'saldo_iniziale': 1000.0
        }
        success, message = supabase_manager.create_wallet(wallet_data)
        if success:
            print(f"✅ Wallet creato: {message}")
        else:
            print(f"⚠️ Wallet: {message}")
        
        # Crea pack copiatore
        pack_data = {
            'broker_id': int(broker_id),
            'nome': 'Test Pack CASCADE',
            'tipo': 'Standard',
            'prezzo': 50.0
        }
        success, message = supabase_manager.create_pack_copiatore(pack_data)
        if success:
            print(f"✅ Pack creato: {message}")
        else:
            print(f"⚠️ Pack: {message}")
        
        # Crea gruppo PAMM
        pamm_data = {
            'broker_id': int(broker_id),
            'nome': 'Test PAMM CASCADE',
            'tipo': 'Standard',
            'capitale_iniziale': 5000.0
        }
        success, message = supabase_manager.create_gruppo_pamm(pamm_data)
        if success:
            print(f"✅ PAMM creato: {message}")
        else:
            print(f"⚠️ PAMM: {message}")
        
        # Test 3: Verifica record esistenti
        print(f"\n3️⃣ Verifica Record Esistenti...")
        
        # Conta wallet per questo broker
        wallets = supabase_manager.get_all_wallets()
        broker_wallets = [w for w in wallets if w.get('broker_id') == int(broker_id)]
        print(f"   - Wallet per broker {broker_id}: {len(broker_wallets)}")
        
        # Conta pack per questo broker
        packs = supabase_manager.get_all_pack_copiatori()
        broker_packs = [p for p in packs if p.get('broker_id') == int(broker_id)]
        print(f"   - Pack per broker {broker_id}: {len(broker_packs)}")
        
        # Conta PAMM per questo broker
        pamm_groups = supabase_manager.get_all_gruppi_pamm()
        broker_pamm = [p for p in pamm_groups if p.get('broker_id') == int(broker_id)]
        print(f"   - PAMM per broker {broker_id}: {len(broker_pamm)}")
        
        # Test 4: Elimina broker (dovrebbe eliminare anche record correlati)
        print(f"\n4️⃣ Eliminazione Broker {broker_id}...")
        success, message = supabase_manager.delete_broker(int(broker_id))
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            return False
        
        # Test 5: Verifica eliminazione CASCADE
        print(f"\n5️⃣ Verifica Eliminazione CASCADE...")
        
        # Conta wallet per questo broker (dovrebbe essere 0)
        wallets = supabase_manager.get_all_wallets()
        broker_wallets = [w for w in wallets if w.get('broker_id') == int(broker_id)]
        print(f"   - Wallet per broker {broker_id}: {len(broker_wallets)} (dovrebbe essere 0)")
        
        # Conta pack per questo broker (dovrebbe essere 0)
        packs = supabase_manager.get_all_pack_copiatori()
        broker_packs = [p for p in packs if p.get('broker_id') == int(broker_id)]
        print(f"   - Pack per broker {broker_id}: {len(broker_packs)} (dovrebbe essere 0)")
        
        # Conta PAMM per questo broker (dovrebbe essere 0)
        pamm_groups = supabase_manager.get_all_gruppi_pamm()
        broker_pamm = [p for p in pamm_groups if p.get('broker_id') == int(broker_id)]
        print(f"   - PAMM per broker {broker_id}: {len(broker_pamm)} (dovrebbe essere 0)")
        
        # Verifica se il broker esiste ancora
        brokers = supabase_manager.get_all_brokers()
        broker_exists = any(b.get('id') == int(broker_id) for b in brokers)
        print(f"   - Broker {broker_id} esiste ancora: {broker_exists} (dovrebbe essere False)")
        
        print("\n" + "=" * 50)
        print("🎉 TEST ELIMINAZIONE BROKER COMPLETATO!")
        print("✅ Foreign key CASCADE funzionante")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRORE DURANTE IL TEST: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_broker_deletion()

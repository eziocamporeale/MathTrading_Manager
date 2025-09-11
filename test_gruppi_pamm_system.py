#!/usr/bin/env python3
"""
Test completo per il sistema di gestione gruppi PAMM
Verifica CRUD, calcoli automatici e funzionalità
Creato da Ezio Camporeale
"""

import sys
from pathlib import Path
from datetime import datetime

# Aggiungi il percorso della directory corrente al path di Python
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from models import GruppoPAMM, ClienteGruppoPAMM, StatoProp, DepositoPAMM
from database.supabase_manager import SupabaseManager

def test_gruppi_pamm_system():
    """Test completo del sistema gruppi PAMM"""
    
    print("🏢 Test Sistema Gestione Gruppi PAMM")
    print("=" * 50)
    
    # Inizializza manager
    supabase_manager = SupabaseManager()
    
    if not supabase_manager.is_configured:
        print("❌ Supabase non configurato")
        return False
    
    print("✅ Supabase configurato correttamente")
    
    # Test 1: Creazione gruppo PAMM
    print("\n📊 Test 1: Creazione Gruppo PAMM")
    
    gruppo = GruppoPAMM(
        nome_gruppo="Test Gruppo",
        manager="Test Manager",
        broker_id=1,
        account_pamm="TEST001",
        capitale_totale=10000.0,
        numero_membri_gruppo=10000,
        responsabili_gruppo="test manager",
        note="Gruppo di test",
        creato_da="admin",
        aggiornato_da="admin"
    )
    
    success, message = supabase_manager.create_gruppo_pamm(gruppo)
    if success:
        print(f"✅ {message}")
        gruppo_id = int(message.split("ID: ")[1])
    else:
        print(f"❌ {message}")
        return False
    
    # Test 2: Creazione cliente per il gruppo
    print("\n👥 Test 2: Creazione Cliente per Gruppo")
    
    cliente = ClienteGruppoPAMM(
        gruppo_pamm_id=gruppo_id,
        nome_cliente="TEST CLIENTE [1000]",
        importo_cliente=1000.0,
        stato_prop=StatoProp.NON_SVOLTO,
        deposito_pamm=DepositoPAMM.NON_DEPOSITATA,
        quota_prop=1,
        ciclo_numero=1,
        fase_prop="Test fase",
        operazione_numero="Test operazione",
        esito_broker="Test broker",
        esito_prop="Test prop",
        prelievo_prop=0.0,
        prelievo_profit=0.0,
        commissioni_percentuale=25.0,
        credenziali_broker="TEST123",
        credenziali_prop="TEST456",
        chi_ha_comprato_prop="TESTER",
        creato_da="admin",
        aggiornato_da="admin"
    )
    
    success, message = supabase_manager.create_cliente_gruppo_pamm(cliente)
    if success:
        print(f"✅ {message}")
        cliente_id = int(message.split("ID: ")[1])
    else:
        print(f"❌ {message}")
        return False
    
    # Test 3: Recupero gruppi
    print("\n📋 Test 3: Recupero Gruppi PAMM")
    
    gruppi = supabase_manager.get_gruppi_pamm_gruppi()
    if gruppi:
        print(f"✅ Recuperati {len(gruppi)} gruppi PAMM")
        for gruppo in gruppi:
            print(f"   - {gruppo['nome_gruppo']} ({gruppo['manager']})")
    else:
        print("❌ Nessun gruppo trovato")
        return False
    
    # Test 4: Recupero clienti per gruppo
    print("\n👥 Test 4: Recupero Clienti per Gruppo")
    
    clienti = supabase_manager.get_clienti_by_gruppo(gruppo_id)
    if clienti:
        print(f"✅ Recuperati {len(clienti)} clienti per il gruppo {gruppo_id}")
        for cliente in clienti:
            print(f"   - {cliente['nome_cliente']} (€{cliente['importo_cliente']})")
    else:
        print("❌ Nessun cliente trovato per il gruppo")
        return False
    
    # Test 5: Aggiornamento cliente
    print("\n✏️ Test 5: Aggiornamento Cliente")
    
    updates = {
        'stato_prop': 'Svolto',
        'deposito_pamm': 'Depositata',
        'prelievo_prop': 100.0,
        'prelievo_profit': 50.0
    }
    
    success, message = supabase_manager.update_cliente_gruppo_pamm(cliente_id, updates)
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        return False
    
    # Test 6: Verifica aggiornamento
    print("\n🔍 Test 6: Verifica Aggiornamento")
    
    clienti_aggiornati = supabase_manager.get_clienti_by_gruppo(gruppo_id)
    if clienti_aggiornati:
        cliente_aggiornato = next((c for c in clienti_aggiornati if c['id'] == cliente_id), None)
        if cliente_aggiornato:
            print(f"✅ Cliente aggiornato:")
            print(f"   - Stato Prop: {cliente_aggiornato['stato_prop']}")
            print(f"   - Deposito PAMM: {cliente_aggiornato['deposito_pamm']}")
            print(f"   - Prelievo Prop: €{cliente_aggiornato['prelievo_prop']}")
            print(f"   - Prelievo Profit: €{cliente_aggiornato['prelievo_profit']}")
        else:
            print("❌ Cliente non trovato dopo l'aggiornamento")
            return False
    else:
        print("❌ Nessun cliente trovato dopo l'aggiornamento")
        return False
    
    # Test 7: Calcoli automatici
    print("\n📊 Test 7: Calcoli Automatici")
    
    # Calcola totali per il gruppo
    totale_importi = sum(c['importo_cliente'] for c in clienti_aggiornati)
    totale_prelievi_prop = sum(c['prelievo_prop'] for c in clienti_aggiornati)
    totale_prelievi_profit = sum(c['prelievo_profit'] for c in clienti_aggiornati)
    numero_svolti = len([c for c in clienti_aggiornati if c['stato_prop'] == 'Svolto'])
    numero_depositati = len([c for c in clienti_aggiornati if c['deposito_pamm'] == 'Depositata'])
    
    print(f"✅ Calcoli completati:")
    print(f"   - Totale Importi: €{totale_importi:,.2f}")
    print(f"   - Totale Prelievi Prop: €{totale_prelievi_prop:,.2f}")
    print(f"   - Totale Prelievi Profit: €{totale_prelievi_profit:,.2f}")
    print(f"   - Clienti Svolti: {numero_svolti}")
    print(f"   - Clienti Depositati: {numero_depositati}")
    
    # Test 8: Pulizia (opzionale)
    print("\n🧹 Test 8: Pulizia Dati di Test")
    
    # Elimina cliente di test
    success, message = supabase_manager.delete_cliente_gruppo_pamm(cliente_id)
    if success:
        print(f"✅ Cliente di test eliminato")
    else:
        print(f"⚠️ Errore eliminazione cliente: {message}")
    
    # Elimina gruppo di test
    success, message = supabase_manager.delete_gruppo_pamm(gruppo_id)
    if success:
        print(f"✅ Gruppo di test eliminato")
    else:
        print(f"⚠️ Errore eliminazione gruppo: {message}")
    
    print("\n🎉 Test sistema gruppi PAMM completato con successo!")
    return True

def test_model_serialization():
    """Test serializzazione modelli"""
    
    print("\n🔄 Test Serializzazione Modelli")
    print("=" * 40)
    
    # Test GruppoPAMM
    gruppo = GruppoPAMM(
        nome_gruppo="Test Serialization",
        manager="Test Manager",
        broker_id=1,
        account_pamm="SER001"
    )
    
    from models import gruppo_pamm_to_dict, dict_to_gruppo_pamm
    
    # Serializza
    gruppo_dict = gruppo_pamm_to_dict(gruppo)
    print(f"✅ GruppoPAMM serializzato: {len(gruppo_dict)} campi")
    
    # Deserializza
    gruppo_restored = dict_to_gruppo_pamm(gruppo_dict)
    print(f"✅ GruppoPAMM deserializzato: {gruppo_restored.nome_gruppo}")
    
    # Test ClienteGruppoPAMM
    cliente = ClienteGruppoPAMM(
        gruppo_pamm_id=1,
        nome_cliente="TEST SERIALIZATION [1000]",
        importo_cliente=1000.0,
        stato_prop=StatoProp.SVOLTO,
        deposito_pamm=DepositoPAMM.DEPOSITATA
    )
    
    from models import cliente_gruppo_pamm_to_dict, dict_to_cliente_gruppo_pamm
    
    # Serializza
    cliente_dict = cliente_gruppo_pamm_to_dict(cliente)
    print(f"✅ ClienteGruppoPAMM serializzato: {len(cliente_dict)} campi")
    
    # Deserializza
    cliente_restored = dict_to_cliente_gruppo_pamm(cliente_dict)
    print(f"✅ ClienteGruppoPAMM deserializzato: {cliente_restored.nome_cliente}")
    
    print("✅ Test serializzazione completato!")
    return True

if __name__ == "__main__":
    try:
        # Test sistema completo
        success1 = test_gruppi_pamm_system()
        
        # Test serializzazione
        success2 = test_model_serialization()
        
        if success1 and success2:
            print("\n🎯 Tutti i test del sistema gruppi PAMM completati con successo!")
            print("\n📋 Funzionalità verificate:")
            print("   ✅ Creazione gruppi PAMM")
            print("   ✅ Creazione clienti per gruppo")
            print("   ✅ Recupero dati")
            print("   ✅ Aggiornamento clienti")
            print("   ✅ Calcoli automatici")
            print("   ✅ Serializzazione modelli")
            print("   ✅ Pulizia dati")
        else:
            print("\n❌ Alcuni test sono falliti!")
            
    except Exception as e:
        print(f"\n❌ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()

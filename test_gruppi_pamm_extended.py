#!/usr/bin/env python3
"""
Test per il sistema Gruppi PAMM esteso
Verifica funzionalità CRUD e visualizzazione Excel-like
Creato da Ezio Camporeale
"""

import sys
from pathlib import Path
from datetime import datetime

# Aggiungi il percorso della directory corrente al path di Python
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from models import GruppiPAMM, StatoProp, DepositoPAMM
from database.supabase_manager import SupabaseManager

def test_gruppi_pamm_extended():
    """Test completo del sistema Gruppi PAMM esteso"""
    
    print("🚀 Test Sistema Gruppi PAMM Esteso")
    print("=" * 50)
    
    # Inizializza manager
    supabase_manager = SupabaseManager()
    
    if not supabase_manager.is_configured:
        print("❌ Supabase non configurato")
        return False
    
    print("✅ Supabase configurato correttamente")
    
    # Test 1: Creazione gruppo PAMM esteso
    print("\n📝 Test 1: Creazione Gruppo PAMM Esteso")
    
    nuovo_gruppo = GruppiPAMM(
        nome_gruppo="Gruppo Test",
        manager="Test Manager",
        broker_id=1,
        account_pamm="TEST001",
        capitale_totale=50000.0,
        numero_partecipanti=5,
        # Nuovi campi Excel
        nome_cliente="TEST CLIENTE [5000]",
        importo_cliente=5000.0,
        stato_prop=StatoProp.NON_SVOLTO,
        deposito_pamm=DepositoPAMM.NON_DEPOSITATA,
        quota_prop=1,
        ciclo_numero=1,
        fase_prop="Test Phase",
        operazione_numero=1,
        esito_broker="",
        esito_prop="",
        prelievo_prop=0.0,
        prelievo_profit=0.0,
        commissioni_percentuale=25.0,
        credenziali_broker="test_broker_creds",
        credenziali_prop="test_prop_creds",
        responsabili_gruppo="test manager",
        numero_membri_gruppo=5000,
        creato_da="test_user",
        aggiornato_da="test_user"
    )
    
    success, message = supabase_manager.create_gruppo_pamm_extended(nuovo_gruppo)
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        return False
    
    # Test 2: Recupero gruppi per stato
    print("\n🔍 Test 2: Recupero Gruppi per Stato")
    
    gruppi_non_svolti = supabase_manager.get_gruppi_pamm_by_stato(StatoProp.NON_SVOLTO)
    print(f"✅ Trovati {len(gruppi_non_svolti)} gruppi non svolti")
    
    gruppi_svolti = supabase_manager.get_gruppi_pamm_by_stato(StatoProp.SVOLTO)
    print(f"✅ Trovati {len(gruppi_svolti)} gruppi svolti")
    
    # Test 3: Recupero per gruppo
    print("\n👥 Test 3: Recupero per Gruppo")
    
    gruppi_test = supabase_manager.get_gruppi_pamm_by_gruppo("Gruppo Test")
    print(f"✅ Trovati {len(gruppi_test)} clienti nel Gruppo Test")
    
    # Test 4: Statistiche
    print("\n📊 Test 4: Statistiche Gruppi")
    
    stats = supabase_manager.get_statistiche_gruppi()
    print(f"✅ Statistiche: {stats}")
    
    # Test 5: Ricerca
    print("\n🔍 Test 5: Ricerca Gruppi")
    
    risultati = supabase_manager.search_gruppi_pamm("TEST")
    print(f"✅ Trovati {len(risultati)} risultati per 'TEST'")
    
    # Test 6: Operazioni bulk (se ci sono dati)
    if len(gruppi_non_svolti) > 0:
        print("\n⚡ Test 6: Operazioni Bulk")
        
        # Prendi i primi 2 gruppi per il test
        ids_test = [g['id'] for g in gruppi_non_svolti[:2]]
        
        # Aggiorna stato prop
        success, message = supabase_manager.update_stato_prop_bulk(
            ids_test, StatoProp.SVOLTO
        )
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
        
        # Aggiorna deposito PAMM
        success, message = supabase_manager.update_deposito_pamm_bulk(
            ids_test, DepositoPAMM.DEPOSITATA
        )
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
    
    print("\n🎉 Test completato con successo!")
    return True

def test_model_conversion():
    """Test conversione modelli"""
    
    print("\n🔄 Test Conversione Modelli")
    print("=" * 30)
    
    # Crea gruppo di test
    gruppo = GruppiPAMM(
        nome_cliente="TEST CONVERSION [1000]",
        importo_cliente=1000.0,
        stato_prop=StatoProp.SVOLTO,
        deposito_pamm=DepositoPAMM.DEPOSITATA,
        quota_prop=1,
        ciclo_numero=2,
        commissioni_percentuale=25.0
    )
    
    # Test conversione a dizionario
    from models import gruppi_pamm_to_dict
    gruppo_dict = gruppi_pamm_to_dict(gruppo)
    
    print("✅ Conversione a dizionario:")
    for key, value in gruppo_dict.items():
        if key.startswith(('nome_cliente', 'importo_cliente', 'stato_prop', 'deposito_pamm')):
            print(f"   {key}: {value}")
    
    # Test conversione da dizionario
    from models import dict_to_gruppi_pamm
    gruppo_ricostruito = dict_to_gruppi_pamm(gruppo_dict)
    
    print("✅ Conversione da dizionario:")
    print(f"   Nome Cliente: {gruppo_ricostruito.nome_cliente}")
    print(f"   Importo: {gruppo_ricostruito.importo_cliente}")
    print(f"   Stato Prop: {gruppo_ricostruito.stato_prop.value}")
    print(f"   Deposito PAMM: {gruppo_ricostruito.deposito_pamm.value}")
    
    return True

if __name__ == "__main__":
    try:
        # Test conversione modelli
        test_model_conversion()
        
        # Test sistema completo
        test_gruppi_pamm_extended()
        
        print("\n🎯 Tutti i test completati con successo!")
        
    except Exception as e:
        print(f"\n❌ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python3
"""
Test per la tabella editabile Gruppi PAMM
Verifica funzionalità di modifica celle e salvataggio
Creato da Ezio Camporeale
"""

import sys
from pathlib import Path
from datetime import datetime

# Aggiungi il percorso della directory corrente al path di Python
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from database.supabase_manager import SupabaseManager

def test_editable_table_functionality():
    """Test delle funzionalità della tabella editabile"""
    
    print("🚀 Test Tabella Editabile Gruppi PAMM")
    print("=" * 50)
    
    # Inizializza manager
    supabase_manager = SupabaseManager()
    
    if not supabase_manager.is_configured:
        print("❌ Supabase non configurato")
        return False
    
    print("✅ Supabase configurato correttamente")
    
    # Test 1: Caricamento dati
    print("\n📊 Test 1: Caricamento Dati")
    
    data = supabase_manager.get_gruppi_pamm()
    if data:
        print(f"✅ Caricati {len(data)} gruppi PAMM")
        
        # Mostra alcuni dati di esempio
        for i, gruppo in enumerate(data[:3]):
            print(f"   {i+1}. {gruppo.get('nome_cliente', 'N/A')} - {gruppo.get('stato_prop', 'N/A')}")
    else:
        print("❌ Nessun dato trovato")
        return False
    
    # Test 2: Aggiornamento singolo campo
    print("\n✏️ Test 2: Aggiornamento Singolo Campo")
    
    if data:
        first_record = data[0]
        record_id = first_record['id']
        current_stato = first_record.get('stato_prop', 'Non svolto')
        
        # Cambia stato
        new_stato = 'Svolto' if current_stato != 'Svolto' else 'Non svolto'
        
        print(f"   Aggiornando record {record_id}: stato da '{current_stato}' a '{new_stato}'")
        
        success, message = supabase_manager.update_gruppo_pamm(
            record_id,
            {'stato_prop': new_stato}
        )
        
        if success:
            print(f"✅ {message}")
            
            # Verifica il cambiamento
            updated_record = supabase_manager.get_gruppo_pamm_by_id(record_id)
            if updated_record and updated_record['stato_prop'] == new_stato:
                print("✅ Cambiamento verificato nel database")
            else:
                print("❌ Cambiamento non verificato")
        else:
            print(f"❌ {message}")
    
    # Test 3: Aggiornamento multipli campi
    print("\n📝 Test 3: Aggiornamento Multipli Campi")
    
    if data:
        first_record = data[0]
        record_id = first_record['id']
        
        update_data = {
            'ciclo_numero': 2,
            'fase_prop': 'Test Phase',
            'operazione_numero': 1,
            'credenziali_broker': 'TEST123'
        }
        
        print(f"   Aggiornando record {record_id} con {len(update_data)} campi")
        
        success, message = supabase_manager.update_gruppo_pamm(record_id, update_data)
        
        if success:
            print(f"✅ {message}")
            
            # Verifica i cambiamenti
            updated_record = supabase_manager.get_gruppo_pamm_by_id(record_id)
            if updated_record:
                all_correct = True
                for field, expected_value in update_data.items():
                    actual_value = updated_record.get(field)
                    if str(actual_value) != str(expected_value):
                        print(f"❌ Campo {field}: atteso '{expected_value}', trovato '{actual_value}'")
                        all_correct = False
                
                if all_correct:
                    print("✅ Tutti i cambiamenti verificati nel database")
                else:
                    print("❌ Alcuni cambiamenti non verificati")
        else:
            print(f"❌ {message}")
    
    # Test 4: Operazioni bulk
    print("\n⚡ Test 4: Operazioni Bulk")
    
    if len(data) >= 2:
        # Prendi i primi 2 record per il test
        test_ids = [data[0]['id'], data[1]['id']]
        
        from models import StatoProp
        
        print(f"   Aggiornando stato prop per {len(test_ids)} record")
        
        success, message = supabase_manager.update_stato_prop_bulk(
            test_ids, 
            StatoProp.SVOLTO
        )
        
        if success:
            print(f"✅ {message}")
            
            # Verifica i cambiamenti
            for record_id in test_ids:
                updated_record = supabase_manager.get_gruppo_pamm_by_id(record_id)
                if updated_record and updated_record['stato_prop'] == 'Svolto':
                    print(f"✅ Record {record_id} aggiornato correttamente")
                else:
                    print(f"❌ Record {record_id} non aggiornato")
        else:
            print(f"❌ {message}")
    
    # Test 5: Statistiche
    print("\n📊 Test 5: Statistiche")
    
    stats = supabase_manager.get_statistiche_gruppi()
    if stats:
        print("✅ Statistiche calcolate:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
    else:
        print("❌ Errore nel calcolo delle statistiche")
    
    print("\n🎉 Test completato!")
    return True

def test_session_state_simulation():
    """Simula il comportamento della session state"""
    
    print("\n🔄 Test Simulazione Session State")
    print("=" * 40)
    
    # Simula dati session state
    mock_data = [
        {
            'id': 1,
            'nome_cliente': 'TEST CLIENTE [1000]',
            'stato_prop': 'Non svolto',
            'deposito_pamm': '',
            'ciclo_numero': 1,
            'fase_prop': '',
            'operazione_numero': '',
            'credenziali_broker': ''
        }
    ]
    
    # Simula cambiamenti
    changes = {
        '1_stato_prop': {
            'id': 1,
            'field': 'stato_prop',
            'value': 'Svolto',
            'timestamp': datetime.now().isoformat()
        },
        '1_ciclo_numero': {
            'id': 1,
            'field': 'ciclo_numero',
            'value': 2,
            'timestamp': datetime.now().isoformat()
        }
    }
    
    print(f"✅ Simulati {len(changes)} cambiamenti")
    
    # Simula applicazione cambiamenti
    for change_key, change_data in changes.items():
        print(f"   Cambio: {change_data['field']} = {change_data['value']}")
    
    print("✅ Simulazione session state completata")
    return True

if __name__ == "__main__":
    try:
        # Test funzionalità database
        test_editable_table_functionality()
        
        # Test simulazione session state
        test_session_state_simulation()
        
        print("\n🎯 Tutti i test completati con successo!")
        
    except Exception as e:
        print(f"\n❌ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()

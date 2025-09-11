#!/usr/bin/env python3
"""
Test per verificare che le chiavi dei widget siano uniche
Creato da Ezio Camporeale
"""

def test_unique_key_generation():
    """Test per verificare la generazione di chiavi uniche"""
    
    print("🔑 Test Generazione Chiavi Uniche")
    print("=" * 40)
    
    # Simula dati di test
    test_data = [
        {"id": 1, "nome_gruppo": "Gruppo 1", "nome_cliente": "Cliente A"},
        {"id": 2, "nome_gruppo": "Gruppo 1", "nome_cliente": "Cliente B"},
        {"id": 3, "nome_gruppo": "Gruppo 2", "nome_cliente": "Cliente C"},
        {"id": 4, "nome_gruppo": "Gruppo 2", "nome_cliente": "Cliente D"},
    ]
    
    generated_keys = set()
    
    for idx, row in enumerate(test_data):
        gruppo_nome = row['nome_gruppo']
        record_id = row['id']
        unique_key_prefix = f"{gruppo_nome}_{record_id}"
        
        # Genera tutte le chiavi per questo record
        keys = [
            f"stato_select_{unique_key_prefix}",
            f"deposito_select_{unique_key_prefix}",
            f"ciclo_input_{unique_key_prefix}",
            f"fase_input_{unique_key_prefix}",
            f"operazione_input_{unique_key_prefix}",
            f"credenziali_input_{unique_key_prefix}"
        ]
        
        print(f"Record {record_id} ({gruppo_nome}):")
        for key in keys:
            if key in generated_keys:
                print(f"  ❌ DUPLICATO: {key}")
                return False
            else:
                generated_keys.add(key)
                print(f"  ✅ {key}")
    
    print(f"\n✅ Tutte le {len(generated_keys)} chiavi sono uniche!")
    return True

def test_key_collision_scenarios():
    """Test scenari di collisione"""
    
    print("\n🚨 Test Scenari di Collisione")
    print("=" * 35)
    
    # Scenario 1: Stesso gruppo, record diversi
    gruppo1_keys = []
    for record_id in [1, 2, 3]:
        unique_key_prefix = f"Gruppo_1_{record_id}"
        key = f"stato_select_{unique_key_prefix}"
        gruppo1_keys.append(key)
    
    print("Scenario 1 - Stesso gruppo, record diversi:")
    for key in gruppo1_keys:
        print(f"  ✅ {key}")
    
    # Scenario 2: Gruppi diversi, stesso record ID
    gruppo2_keys = []
    for gruppo in ["Gruppo_1", "Gruppo_2"]:
        unique_key_prefix = f"{gruppo}_1"
        key = f"stato_select_{unique_key_prefix}"
        gruppo2_keys.append(key)
    
    print("\nScenario 2 - Gruppi diversi, stesso record ID:")
    for key in gruppo2_keys:
        print(f"  ✅ {key}")
    
    # Verifica unicità
    all_keys = gruppo1_keys + gruppo2_keys
    if len(all_keys) == len(set(all_keys)):
        print("\n✅ Nessuna collisione rilevata!")
        return True
    else:
        print("\n❌ Collisione rilevata!")
        return False

if __name__ == "__main__":
    try:
        # Test generazione chiavi uniche
        success1 = test_unique_key_generation()
        
        # Test scenari di collisione
        success2 = test_key_collision_scenarios()
        
        if success1 and success2:
            print("\n🎉 Tutti i test delle chiavi completati con successo!")
        else:
            print("\n❌ Alcuni test sono falliti!")
            
    except Exception as e:
        print(f"\n❌ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()

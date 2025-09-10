#!/usr/bin/env python3
"""
Test finale creazione utenti
"""

import sys
import time
from pathlib import Path

# Aggiungi il percorso della directory corrente al path di Python
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def test_create_user_final():
    """Test finale creazione utente"""
    
    print("👤 TEST FINALE CREAZIONE UTENTE")
    print("=" * 45)
    
    try:
        from components.auth_manager import AuthManager
        from database.supabase_manager import SupabaseManager
        
        # Inizializza manager
        auth_manager = AuthManager()
        supabase_manager = SupabaseManager()
        
        # Username unico basato su timestamp
        timestamp = int(time.time())
        test_username = f"test_user_{timestamp}"
        
        # Test 1: Dati utente di test
        print(f"\n1️⃣ Test Creazione Utente: {test_username}")
        test_user_data = {
            'username': test_username,
            'email': f'test{timestamp}@example.com',
            'password': 'test123',
            'first_name': 'Test',
            'last_name': 'User',
            'role_id': 6,  # Viewer
            'is_active': True,
            'is_admin': False
        }
        
        print(f"Dati utente: {test_user_data}")
        
        # Test 2: Crea utente
        success, message = auth_manager.create_user(test_user_data)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            return False
        
        # Test 3: Verifica utente creato
        print(f"\n2️⃣ Test Verifica Utente Creato...")
        created_user = supabase_manager.get_user_by_username(test_username)
        if created_user:
            print(f"✅ Utente creato trovato:")
            print(f"   - Username: {created_user['username']}")
            print(f"   - Email: {created_user['email']}")
            print(f"   - Nome: {created_user.get('first_name', 'N/A')} {created_user.get('last_name', 'N/A')}")
            print(f"   - Ruolo ID: {created_user.get('role_id', 'N/A')}")
            print(f"   - Attivo: {created_user.get('is_active', 'N/A')}")
            print(f"   - Admin: {created_user.get('is_admin', 'N/A')}")
        else:
            print("❌ Utente creato non trovato")
            return False
        
        # Test 4: Test login utente creato
        print(f"\n3️⃣ Test Login Utente Creato...")
        auth_manager.logout()  # Logout admin
        login_user = auth_manager.login(test_username, 'test123')
        if login_user:
            print(f"✅ Login utente creato riuscito:")
            print(f"   - Nome: {login_user['first_name']} {login_user['last_name']}")
            print(f"   - Ruolo: {login_user['role_name']}")
        else:
            print("❌ Login utente creato fallito")
            return False
        
        # Test 5: Cleanup - elimina utente di test
        print(f"\n4️⃣ Cleanup - Eliminazione Utente Test...")
        success, message = supabase_manager.delete_user(created_user['id'])
        if success:
            print(f"✅ {message}")
        else:
            print(f"⚠️ {message} (non critico)")
        
        print("\n" + "=" * 45)
        print("🎉 TEST CREAZIONE UTENTE COMPLETATO!")
        print("✅ Sistema di creazione utenti funzionante")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRORE DURANTE IL TEST: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_create_user_final()
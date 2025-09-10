#!/usr/bin/env python3
"""
Test del Sistema di Autenticazione per DASH_PROP_BROKER
Testa login, logout, gestione utenti e permessi
Creato da Ezio Camporeale
"""

import sys
from pathlib import Path

# Aggiungi il percorso della directory corrente al path di Python
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from components.auth_manager import AuthManager
from database.supabase_manager import SupabaseManager

def test_auth_system():
    """Testa il sistema di autenticazione completo"""
    
    print("🔐 TEST SISTEMA DI AUTENTICAZIONE")
    print("=" * 50)
    
    # Inizializza manager
    auth_manager = AuthManager()
    supabase_manager = SupabaseManager()
    
    # Test 1: Connessione Supabase
    print("\n1️⃣ Test Connessione Supabase...")
    success, message = supabase_manager.test_connection()
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        return False
    
    # Test 2: Recupero ruoli
    print("\n2️⃣ Test Recupero Ruoli...")
    roles = supabase_manager.get_all_roles()
    if roles:
        print(f"✅ Trovati {len(roles)} ruoli:")
        for role in roles:
            print(f"   - {role['name']}: {role['description']}")
    else:
        print("❌ Nessun ruolo trovato")
        return False
    
    # Test 3: Recupero utenti
    print("\n3️⃣ Test Recupero Utenti...")
    users = supabase_manager.get_all_users()
    if users:
        print(f"✅ Trovati {len(users)} utenti:")
        for user in users:
            print(f"   - {user['username']} ({user['first_name']} {user['last_name']})")
    else:
        print("❌ Nessun utente trovato")
        return False
    
    # Test 4: Test login con utente demo
    print("\n4️⃣ Test Login Demo...")
    demo_user = auth_manager.login("demo", "demo123")
    if demo_user:
        print(f"✅ Login demo riuscito: {demo_user['first_name']} {demo_user['last_name']}")
        print(f"   Ruolo: {demo_user['role_name']}")
        print(f"   Permessi: {demo_user['permissions']}")
    else:
        print("❌ Login demo fallito")
        return False
    
    # Test 5: Test permessi
    print("\n5️⃣ Test Permessi...")
    if auth_manager.has_permission("view_brokers"):
        print("✅ Permesso 'view_brokers' confermato")
    else:
        print("❌ Permesso 'view_brokers' negato")
    
    if auth_manager.has_role(["Manager", "Admin"]):
        print("✅ Ruolo Manager/Admin confermato")
    else:
        print("❌ Ruolo Manager/Admin negato")
    
    # Test 6: Test logout
    print("\n6️⃣ Test Logout...")
    auth_manager.logout()
    if not auth_manager.is_authenticated():
        print("✅ Logout riuscito")
    else:
        print("❌ Logout fallito")
        return False
    
    # Test 7: Test creazione utente (se admin)
    print("\n7️⃣ Test Creazione Utente...")
    admin_user = auth_manager.login("admin", "admin123")
    if admin_user:
        print(f"✅ Login admin riuscito: {admin_user['first_name']} {admin_user['last_name']}")
        
        # Crea utente di test
        test_user_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'test123',
            'first_name': 'Test',
            'last_name': 'User',
            'role_id': 6,  # Viewer
            'is_active': True,
            'is_admin': False
        }
        
        success, message = auth_manager.create_user(test_user_data)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
    else:
        print("❌ Login admin fallito")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 TUTTI I TEST COMPLETATI CON SUCCESSO!")
    print("✅ Sistema di autenticazione funzionante")
    return True

if __name__ == "__main__":
    test_auth_system()

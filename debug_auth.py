#!/usr/bin/env python3
"""
Debug del Sistema di Autenticazione
Diagnostica problemi di login e connessione
Creato da Ezio Camporeale
"""

import sys
from pathlib import Path

# Aggiungi il percorso della directory corrente al path di Python
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def debug_auth_system():
    """Debug completo del sistema di autenticazione"""
    
    print("🔍 DEBUG SISTEMA DI AUTENTICAZIONE")
    print("=" * 50)
    
    try:
        # Test 1: Importazione moduli
        print("\n1️⃣ Test Importazione Moduli...")
        from components.auth_manager import AuthManager
        from database.supabase_manager import SupabaseManager
        print("✅ Moduli importati correttamente")
        
        # Test 2: Connessione Supabase
        print("\n2️⃣ Test Connessione Supabase...")
        supabase_manager = SupabaseManager()
        if supabase_manager.is_configured:
            print("✅ Supabase configurato")
        else:
            print("❌ Supabase non configurato")
            return False
        
        # Test 3: Test connessione database
        print("\n3️⃣ Test Connessione Database...")
        success, message = supabase_manager.test_connection()
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            return False
        
        # Test 4: Verifica tabella roles
        print("\n4️⃣ Test Tabella Roles...")
        roles = supabase_manager.get_all_roles()
        if roles:
            print(f"✅ Trovati {len(roles)} ruoli:")
            for role in roles:
                print(f"   - {role['id']}: {role['name']}")
        else:
            print("❌ Nessun ruolo trovato")
            return False
        
        # Test 5: Verifica tabella users
        print("\n5️⃣ Test Tabella Users...")
        users = supabase_manager.get_all_users()
        if users:
            print(f"✅ Trovati {len(users)} utenti:")
            for user in users:
                print(f"   - {user['username']}: {user.get('first_name', 'N/A')} {user.get('last_name', 'N/A')}")
                print(f"     Role ID: {user.get('role_id', 'N/A')}, Admin: {user.get('is_admin', 'N/A')}, Active: {user.get('is_active', 'N/A')}")
        else:
            print("❌ Nessun utente trovato")
            return False
        
        # Test 6: Test login admin
        print("\n6️⃣ Test Login Admin...")
        auth_manager = AuthManager()
        # NOTA: Le credenziali devono essere fornite dall'amministratore
        print("⚠️ Test login admin richiede credenziali fornite dall'amministratore")
        return True
        
        # Test 7: Test login demo
        print("\n7️⃣ Test Login Demo...")
        # NOTA: Le credenziali devono essere fornite dall'amministratore
        print("⚠️ Test login demo richiede credenziali fornite dall'amministratore")
        return True
        
        print("\n" + "=" * 50)
        print("🎉 TUTTI I TEST COMPLETATI CON SUCCESSO!")
        print("✅ Sistema di autenticazione funzionante")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRORE DURANTE IL DEBUG: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_auth_system()

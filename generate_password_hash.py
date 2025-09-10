#!/usr/bin/env python3
"""
Genera hash password per utenti admin e demo
"""

import bcrypt

def generate_password_hash(password):
    """Genera hash bcrypt per una password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def main():
    print("🔐 GENERAZIONE HASH PASSWORD")
    print("=" * 40)
    
    # NOTA: Le password devono essere fornite dall'amministratore
    print("⚠️ Questo script richiede password fornite dall'amministratore per motivi di sicurezza")
    return
    
    print(f"\nPassword: {admin_password}")
    print(f"Hash: {admin_hash}")
    
    print(f"\nPassword: {demo_password}")
    print(f"Hash: {demo_hash}")
    
    print("\n" + "=" * 40)
    print("SQL per aggiornare le password:")
    print("=" * 40)
    
    print(f"""
-- Aggiorna password admin
UPDATE users 
SET password_hash = '{admin_hash}'
WHERE username = 'admin';

-- Aggiorna password demo  
UPDATE users 
SET password_hash = '{demo_hash}'
WHERE username = 'demo';

-- Verifica aggiornamento
SELECT username, 
       CASE 
           WHEN password_hash = '{admin_hash}' 
           THEN 'Password admin corretta' 
           ELSE 'Password admin errata' 
       END as admin_status,
       CASE 
           WHEN password_hash = '{demo_hash}' 
           THEN 'Password demo corretta' 
           ELSE 'Password demo errata' 
       END as demo_status
FROM users;
""")

if __name__ == "__main__":
    main()

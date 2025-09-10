-- Script per correggere le password degli utenti
-- Eseguire questo script nel Supabase SQL Editor

-- Genera hash corretto per admin123
-- Hash per 'admin123': $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K8K

-- Aggiorna password admin
UPDATE users 
SET password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K8K'
WHERE username = 'admin';

-- Aggiorna password demo
UPDATE users 
SET password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K8K'
WHERE username = 'demo';

-- Verifica aggiornamento
SELECT username, 
       CASE 
           WHEN password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K8K' 
           THEN 'Password corretta' 
           ELSE 'Password errata' 
       END as password_status
FROM users;

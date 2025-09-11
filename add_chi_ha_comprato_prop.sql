-- Script per aggiungere la colonna chi_ha_comprato_prop alla tabella gruppi_pamm
-- Creato da Ezio Camporeale

-- Aggiungi la colonna chi_ha_comprato_prop
ALTER TABLE gruppi_pamm 
ADD COLUMN IF NOT EXISTS chi_ha_comprato_prop TEXT DEFAULT '';

-- Aggiorna alcuni record di esempio con dati realistici
UPDATE gruppi_pamm 
SET chi_ha_comprato_prop = 'MATTEO'
WHERE nome_cliente LIKE '%WASSIM%';

UPDATE gruppi_pamm 
SET chi_ha_comprato_prop = 'MARCO'
WHERE nome_cliente LIKE '%MARIO RUSSO%';

UPDATE gruppi_pamm 
SET chi_ha_comprato_prop = 'FRANK'
WHERE nome_cliente LIKE '%MANUEL%';

UPDATE gruppi_pamm 
SET chi_ha_comprato_prop = 'MARIO'
WHERE nome_cliente LIKE '%LUIGI%';

-- Verifica i risultati
SELECT 
    nome_cliente,
    chi_ha_comprato_prop,
    credenziali_broker,
    credenziali_prop
FROM gruppi_pamm 
WHERE chi_ha_comprato_prop != ''
ORDER BY nome_cliente;

-- Messaggio di conferma
SELECT 'Colonna chi_ha_comprato_prop aggiunta con successo!' as status;

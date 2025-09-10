"""
Manager Supabase per Dashboard Matematico Prop/Broker
Gestisce tutte le operazioni CRUD con Supabase
Creato da Ezio Camporeale
"""

import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from supabase import create_client, Client
from models import (
    Broker, PropFirm, Wallet, PackCopiatore, GruppiPAMM, Incroci, User,
    TransazioneWallet, PerformanceHistory,
    broker_to_dict, dict_to_broker, prop_to_dict, dict_to_prop
)

class SupabaseManager:
    """Manager per le operazioni Supabase"""
    
    def __init__(self):
        """Inizializza il client Supabase"""
        self.url = os.getenv('SUPABASE_URL', 'https://znkhbkiexrqujqwgzueq.supabase.co')
        self.key = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpua2hia2lleHJxdWpxd2d6dWVxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc1MDU0OTQsImV4cCI6MjA3MzA4MTQ5NH0.OPAUp3lDz4ms8ftizS0bELInOaZdouxFx2jbcgD9NAc')
        
        try:
            self.supabase: Client = create_client(self.url, self.key)
            self.is_configured = True
            logging.info("✅ Supabase client inizializzato correttamente")
        except Exception as e:
            self.is_configured = False
            logging.error(f"❌ Errore inizializzazione Supabase: {e}")
    
    # ==================== BROKER OPERATIONS ====================
    
    def get_brokers(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """Ottiene tutti i broker dal database"""
        try:
            if not self.is_configured:
                return []
            
            query = self.supabase.table('brokers').select('*')
            if active_only:
                query = query.eq('stato', 'Attivo')
            
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            logging.error(f"❌ Errore recupero broker: {e}")
            return []
    
    def get_broker_by_id(self, broker_id: int) -> Optional[Dict[str, Any]]:
        """Ottiene un broker specifico per ID"""
        try:
            if not self.is_configured:
                return None
            
            result = self.supabase.table('brokers').select('*').eq('id', broker_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logging.error(f"❌ Errore recupero broker {broker_id}: {e}")
            return None
    
    def add_broker(self, broker_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiunge un nuovo broker"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Aggiungi timestamp
            broker_data['data_creazione'] = datetime.now().isoformat()
            broker_data['data_aggiornamento'] = datetime.now().isoformat()
            
            result = self.supabase.table('brokers').insert(broker_data).execute()
            
            if result.data:
                return True, f"Broker {broker_data.get('nome_broker', '')} aggiunto con successo"
            else:
                return False, "Errore durante l'inserimento"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiunta broker: {e}")
            return False, str(e)
    
    def update_broker(self, broker_id: int, broker_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiorna un broker esistente"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Aggiungi timestamp aggiornamento
            broker_data['data_aggiornamento'] = datetime.now().isoformat()
            
            result = self.supabase.table('brokers').update(broker_data).eq('id', broker_id).execute()
            
            if result.data:
                return True, f"Broker {broker_id} aggiornato con successo"
            else:
                return False, "Errore durante l'aggiornamento"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiornamento broker {broker_id}: {e}")
            return False, str(e)
    
    def delete_broker(self, broker_id: int) -> Tuple[bool, str]:
        """Elimina un broker"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            result = self.supabase.table('brokers').delete().eq('id', broker_id).execute()
            
            if result.data:
                return True, f"Broker {broker_id} eliminato con successo"
            else:
                return False, "Errore durante l'eliminazione"
                
        except Exception as e:
            logging.error(f"❌ Errore eliminazione broker {broker_id}: {e}")
            return False, str(e)
    
    # ==================== PROP FIRM OPERATIONS ====================
    
    def get_props(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """Ottiene tutte le prop firm dal database"""
        try:
            if not self.is_configured:
                return []
            
            query = self.supabase.table('prop_firms').select('*')
            if active_only:
                query = query.eq('stato', 'Attiva')
            
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            logging.error(f"❌ Errore recupero prop firms: {e}")
            return []
    
    def get_prop_by_id(self, prop_id: int) -> Optional[Dict[str, Any]]:
        """Ottiene una prop firm specifica per ID"""
        try:
            if not self.is_configured:
                return None
            
            result = self.supabase.table('prop_firms').select('*').eq('id', prop_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logging.error(f"❌ Errore recupero prop firm {prop_id}: {e}")
            return None
    
    def add_prop(self, prop_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiunge una nuova prop firm"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Aggiungi timestamp
            prop_data['data_creazione'] = datetime.now().isoformat()
            prop_data['data_aggiornamento'] = datetime.now().isoformat()
            
            result = self.supabase.table('prop_firms').insert(prop_data).execute()
            
            if result.data:
                return True, f"Prop firm {prop_data.get('nome_prop', '')} aggiunta con successo"
            else:
                return False, "Errore durante l'inserimento"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiunta prop firm: {e}")
            return False, str(e)
    
    def update_prop(self, prop_id: int, prop_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiorna una prop firm esistente"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Aggiungi timestamp aggiornamento
            prop_data['data_aggiornamento'] = datetime.now().isoformat()
            
            result = self.supabase.table('prop_firms').update(prop_data).eq('id', prop_id).execute()
            
            if result.data:
                return True, f"Prop firm {prop_id} aggiornata con successo"
            else:
                return False, "Errore durante l'aggiornamento"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiornamento prop firm {prop_id}: {e}")
            return False, str(e)
    
    def delete_prop(self, prop_id: int) -> Tuple[bool, str]:
        """Elimina una prop firm"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            result = self.supabase.table('prop_firms').delete().eq('id', prop_id).execute()
            
            if result.data:
                return True, f"Prop firm {prop_id} eliminata con successo"
            else:
                return False, "Errore durante l'eliminazione"
                
        except Exception as e:
            logging.error(f"❌ Errore eliminazione prop firm {prop_id}: {e}")
            return False, str(e)
    
    # ==================== WALLET OPERATIONS ====================
    
    def get_wallets(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """Ottiene tutti i wallet dal database"""
        try:
            if not self.is_configured:
                return []
            
            query = self.supabase.table('wallets').select('*')
            if active_only:
                query = query.eq('stato', 'Attivo')
            
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            logging.error(f"❌ Errore recupero wallets: {e}")
            return []
    
    def get_wallet_by_id(self, wallet_id: int) -> Optional[Dict[str, Any]]:
        """Ottiene un wallet specifico per ID"""
        try:
            if not self.is_configured:
                return None
            
            result = self.supabase.table('wallets').select('*').eq('id', wallet_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logging.error(f"❌ Errore recupero wallet {wallet_id}: {e}")
            return None
    
    def add_wallet(self, wallet_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiunge un nuovo wallet"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Aggiungi timestamp
            wallet_data['data_creazione'] = datetime.now().isoformat()
            wallet_data['data_aggiornamento'] = datetime.now().isoformat()
            
            result = self.supabase.table('wallets').insert(wallet_data).execute()
            
            if result.data:
                return True, f"Wallet {wallet_data.get('nome_wallet', '')} aggiunto con successo"
            else:
                return False, "Errore durante l'inserimento"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiunta wallet: {e}")
            return False, str(e)
    
    def update_wallet(self, wallet_id: int, wallet_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiorna un wallet esistente"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Aggiungi timestamp aggiornamento
            wallet_data['data_aggiornamento'] = datetime.now().isoformat()
            
            result = self.supabase.table('wallets').update(wallet_data).eq('id', wallet_id).execute()
            
            if result.data:
                return True, f"Wallet {wallet_id} aggiornato con successo"
            else:
                return False, "Errore durante l'aggiornamento"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiornamento wallet {wallet_id}: {e}")
            return False, str(e)
    
    def delete_wallet(self, wallet_id: int) -> Tuple[bool, str]:
        """Elimina un wallet"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            result = self.supabase.table('wallets').delete().eq('id', wallet_id).execute()
            
            if result.data:
                return True, f"Wallet {wallet_id} eliminato con successo"
            else:
                return False, "Errore durante l'eliminazione"
                
        except Exception as e:
            logging.error(f"❌ Errore eliminazione wallet {wallet_id}: {e}")
            return False, str(e)
    
    # ==================== PACK COPIATORE OPERATIONS ====================
    
    def get_pack_copiatori(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """Ottiene tutti i pack copiatore dal database"""
        try:
            if not self.is_configured:
                return []
            
            query = self.supabase.table('pack_copiatori').select('*')
            if active_only:
                query = query.eq('stato', 'Attivo')
            
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            logging.error(f"❌ Errore recupero pack copiatori: {e}")
            return []
    
    def get_pack_copiatore_by_id(self, pack_id: int) -> Optional[Dict[str, Any]]:
        """Ottiene un pack copiatore specifico per ID"""
        try:
            if not self.is_configured:
                return None
            
            result = self.supabase.table('pack_copiatori').select('*').eq('id', pack_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logging.error(f"❌ Errore recupero pack copiatore {pack_id}: {e}")
            return None
    
    def add_pack_copiatore(self, pack_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiunge un nuovo pack copiatore"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Aggiungi timestamp
            pack_data['data_creazione'] = datetime.now().isoformat()
            pack_data['data_aggiornamento'] = datetime.now().isoformat()
            
            result = self.supabase.table('pack_copiatori').insert(pack_data).execute()
            
            if result.data:
                return True, f"Pack copiatore {pack_data.get('numero_pack', '')} aggiunto con successo"
            else:
                return False, "Errore durante l'inserimento"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiunta pack copiatore: {e}")
            return False, str(e)
    
    def update_pack_copiatore(self, pack_id: int, pack_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiorna un pack copiatore esistente"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Aggiungi timestamp aggiornamento
            pack_data['data_aggiornamento'] = datetime.now().isoformat()
            
            result = self.supabase.table('pack_copiatori').update(pack_data).eq('id', pack_id).execute()
            
            if result.data:
                return True, f"Pack copiatore {pack_id} aggiornato con successo"
            else:
                return False, "Errore durante l'aggiornamento"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiornamento pack copiatore {pack_id}: {e}")
            return False, str(e)
    
    def delete_pack_copiatore(self, pack_id: int) -> Tuple[bool, str]:
        """Elimina un pack copiatore"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            result = self.supabase.table('pack_copiatori').delete().eq('id', pack_id).execute()
            
            if result.data:
                return True, f"Pack copiatore {pack_id} eliminato con successo"
            else:
                return False, "Errore durante l'eliminazione"
                
        except Exception as e:
            logging.error(f"❌ Errore eliminazione pack copiatore {pack_id}: {e}")
            return False, str(e)
    
    # ==================== GRUPPI PAMM OPERATIONS ====================
    
    def get_gruppi_pamm(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """Ottiene tutti i gruppi PAMM dal database"""
        try:
            if not self.is_configured:
                return []
            
            query = self.supabase.table('gruppi_pamm').select('*')
            if active_only:
                query = query.eq('stato', 'Attivo')
            
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            logging.error(f"❌ Errore recupero gruppi PAMM: {e}")
            return []
    
    def get_gruppo_pamm_by_id(self, gruppo_id: int) -> Optional[Dict[str, Any]]:
        """Ottiene un gruppo PAMM specifico per ID"""
        try:
            if not self.is_configured:
                return None
            
            result = self.supabase.table('gruppi_pamm').select('*').eq('id', gruppo_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logging.error(f"❌ Errore recupero gruppo PAMM {gruppo_id}: {e}")
            return None
    
    def add_gruppo_pamm(self, gruppo_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiunge un nuovo gruppo PAMM"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Aggiungi timestamp
            gruppo_data['data_creazione'] = datetime.now().isoformat()
            gruppo_data['data_aggiornamento'] = datetime.now().isoformat()
            
            result = self.supabase.table('gruppi_pamm').insert(gruppo_data).execute()
            
            if result.data:
                return True, f"Gruppo PAMM {gruppo_data.get('nome_gruppo', '')} aggiunto con successo"
            else:
                return False, "Errore durante l'inserimento"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiunta gruppo PAMM: {e}")
            return False, str(e)
    
    def update_gruppo_pamm(self, gruppo_id: int, gruppo_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiorna un gruppo PAMM esistente"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Aggiungi timestamp aggiornamento
            gruppo_data['data_aggiornamento'] = datetime.now().isoformat()
            
            result = self.supabase.table('gruppi_pamm').update(gruppo_data).eq('id', gruppo_id).execute()
            
            if result.data:
                return True, f"Gruppo PAMM {gruppo_id} aggiornato con successo"
            else:
                return False, "Errore durante l'aggiornamento"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiornamento gruppo PAMM {gruppo_id}: {e}")
            return False, str(e)
    
    def delete_gruppo_pamm(self, gruppo_id: int) -> Tuple[bool, str]:
        """Elimina un gruppo PAMM"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            result = self.supabase.table('gruppi_pamm').delete().eq('id', gruppo_id).execute()
            
            if result.data:
                return True, f"Gruppo PAMM {gruppo_id} eliminato con successo"
            else:
                return False, "Errore durante l'eliminazione"
                
        except Exception as e:
            logging.error(f"❌ Errore eliminazione gruppo PAMM {gruppo_id}: {e}")
            return False, str(e)
    
    # ==================== INCROCI OPERATIONS ====================
    
    def get_incroci(self) -> List[Dict[str, Any]]:
        """Ottiene tutti gli incroci dal database"""
        try:
            if not self.is_configured:
                return []
            
            result = self.supabase.table('incroci').select('*').execute()
            return result.data if result.data else []
        except Exception as e:
            logging.error(f"❌ Errore recupero incroci: {e}")
            return []
    
    def add_incrocio(self, incrocio_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiunge un nuovo incrocio"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Aggiungi timestamp
            incrocio_data['data_creazione'] = datetime.now().isoformat()
            incrocio_data['data_aggiornamento'] = datetime.now().isoformat()
            
            result = self.supabase.table('incroci').insert(incrocio_data).execute()
            
            if result.data:
                return True, f"Incrocio {incrocio_data.get('nome_incrocio', '')} aggiunto con successo"
            else:
                return False, "Errore durante l'inserimento"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiunta incrocio: {e}")
            return False, str(e)
    
    def update_incrocio(self, incrocio_id: int, incrocio_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiorna un incrocio esistente"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Aggiungi timestamp aggiornamento
            incrocio_data['data_aggiornamento'] = datetime.now().isoformat()
            
            result = self.supabase.table('incroci').update(incrocio_data).eq('id', incrocio_id).execute()
            
            if result.data:
                return True, f"Incrocio {incrocio_id} aggiornato con successo"
            else:
                return False, "Errore durante l'aggiornamento"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiornamento incrocio {incrocio_id}: {e}")
            return False, str(e)
    
    def delete_incrocio(self, incrocio_id: int) -> Tuple[bool, str]:
        """Elimina un incrocio"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            result = self.supabase.table('incroci').delete().eq('id', incrocio_id).execute()
            
            if result.data:
                return True, f"Incrocio {incrocio_id} eliminato con successo"
            else:
                return False, "Errore durante l'eliminazione"
                
        except Exception as e:
            logging.error(f"❌ Errore eliminazione incrocio {incrocio_id}: {e}")
            return False, str(e)
    
    # ==================== STATISTICHE ====================
    
    def get_statistiche_generali(self) -> Dict[str, Any]:
        """Ottiene statistiche generali del sistema"""
        try:
            if not self.is_configured:
                return {}
            
            stats = {}
            
            # Conta broker attivi
            brokers = self.get_brokers(active_only=True)
            stats['broker_attivi'] = len(brokers)
            
            # Conta prop attive
            props = self.get_props(active_only=True)
            stats['prop_attive'] = len(props)
            
            # Conta wallet attivi
            wallets = self.get_wallets(active_only=True)
            stats['wallet_attivi'] = len(wallets)
            
            # Conta pack copiatori attivi
            packs = self.get_pack_copiatori(active_only=True)
            stats['pack_copiatori_attivi'] = len(packs)
            
            # Conta gruppi PAMM attivi
            gruppi = self.get_gruppi_pamm(active_only=True)
            stats['gruppi_pamm_attivi'] = len(gruppi)
            
            # Conta incroci totali
            incroci = self.get_incroci()
            stats['incroci_totali'] = len(incroci)
            
            return stats
            
        except Exception as e:
            logging.error(f"❌ Errore recupero statistiche: {e}")
            return {}
    
    # ==================== USER MANAGEMENT ====================
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Ottiene un utente per username"""
        try:
            if not self.is_configured:
                return None
            
            result = self.supabase.table('users').select('*').eq('username', username).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            logging.error(f"❌ Errore recupero utente per username: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Ottiene un utente per ID"""
        try:
            if not self.is_configured:
                return None
            
            result = self.supabase.table('users').select('*').eq('id', user_id).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            logging.error(f"❌ Errore recupero utente per ID: {e}")
            return None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Ottiene tutti gli utenti"""
        try:
            if not self.is_configured:
                return []
            
            result = self.supabase.table('users').select('*').execute()
            return result.data if result.data else []
            
        except Exception as e:
            logging.error(f"❌ Errore recupero utenti: {e}")
            return []
    
    def create_user(self, user_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea un nuovo utente"""
        try:
            if not self.is_configured:
                return False, "❌ Supabase non configurato"
            
            # Rimuovi campi non necessari
            user_data_clean = {k: v for k, v in user_data.items() if k not in ['id', 'created_at', 'updated_at']}
            
            result = self.supabase.table('users').insert(user_data_clean).execute()
            
            if result.data:
                return True, f"✅ Utente creato con successo"
            else:
                return False, "❌ Errore durante la creazione dell'utente"
                
        except Exception as e:
            logging.error(f"❌ Errore creazione utente: {e}")
            return False, f"❌ Errore: {str(e)}"
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiorna un utente esistente"""
        try:
            if not self.is_configured:
                return False, "❌ Supabase non configurato"
            
            # Rimuovi campi non modificabili
            user_data_clean = {k: v for k, v in user_data.items() if k not in ['id', 'created_at']}
            user_data_clean['updated_at'] = datetime.now().isoformat()
            
            result = self.supabase.table('users').update(user_data_clean).eq('id', user_id).execute()
            
            if result.data:
                return True, f"✅ Utente aggiornato con successo"
            else:
                return False, "❌ Errore durante l'aggiornamento dell'utente"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiornamento utente: {e}")
            return False, f"❌ Errore: {str(e)}"
    
    def delete_user(self, user_id: str) -> Tuple[bool, str]:
        """Elimina un utente"""
        try:
            if not self.is_configured:
                return False, "❌ Supabase non configurato"
            
            result = self.supabase.table('users').delete().eq('id', user_id).execute()
            
            if result.data:
                return True, f"✅ Utente eliminato con successo"
            else:
                return False, "❌ Errore durante l'eliminazione dell'utente"
                
        except Exception as e:
            logging.error(f"❌ Errore eliminazione utente: {e}")
            return False, f"❌ Errore: {str(e)}"
    
    def update_user_last_login(self, user_id: str) -> bool:
        """Aggiorna l'ultimo login dell'utente"""
        try:
            if not self.is_configured:
                return False
            
            result = self.supabase.table('users').update({
                'last_login': datetime.now().isoformat()
            }).eq('id', user_id).execute()
            
            return bool(result.data)
            
        except Exception as e:
            logging.error(f"❌ Errore aggiornamento ultimo login: {e}")
            return False
    
    # ==================== ROLE MANAGEMENT ====================
    
    def get_role_by_id(self, role_id: int) -> Optional[Dict[str, Any]]:
        """Ottiene un ruolo per ID"""
        try:
            if not self.is_configured:
                return None
            
            result = self.supabase.table('roles').select('*').eq('id', role_id).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            logging.error(f"❌ Errore recupero ruolo per ID: {e}")
            return None
    
    def get_all_roles(self) -> List[Dict[str, Any]]:
        """Ottiene tutti i ruoli"""
        try:
            if not self.is_configured:
                return []
            
            result = self.supabase.table('roles').select('*').execute()
            return result.data if result.data else []
            
        except Exception as e:
            logging.error(f"❌ Errore recupero ruoli: {e}")
            return []
    
    def create_role(self, role_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea un nuovo ruolo"""
        try:
            if not self.is_configured:
                return False, "❌ Supabase non configurato"
            
            # Rimuovi campi non necessari
            role_data_clean = {k: v for k, v in role_data.items() if k not in ['id', 'created_at', 'updated_at']}
            
            result = self.supabase.table('roles').insert(role_data_clean).execute()
            
            if result.data:
                return True, f"✅ Ruolo creato con successo"
            else:
                return False, "❌ Errore durante la creazione del ruolo"
                
        except Exception as e:
            logging.error(f"❌ Errore creazione ruolo: {e}")
            return False, f"❌ Errore: {str(e)}"
    
    def update_role(self, role_id: int, role_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiorna un ruolo esistente"""
        try:
            if not self.is_configured:
                return False, "❌ Supabase non configurato"
            
            # Rimuovi campi non modificabili
            role_data_clean = {k: v for k, v in role_data.items() if k not in ['id', 'created_at']}
            role_data_clean['updated_at'] = datetime.now().isoformat()
            
            result = self.supabase.table('roles').update(role_data_clean).eq('id', role_id).execute()
            
            if result.data:
                return True, f"✅ Ruolo aggiornato con successo"
            else:
                return False, "❌ Errore durante l'aggiornamento del ruolo"
                
        except Exception as e:
            logging.error(f"❌ Errore aggiornamento ruolo: {e}")
            return False, f"❌ Errore: {str(e)}"
    
    def delete_role(self, role_id: int) -> Tuple[bool, str]:
        """Elimina un ruolo"""
        try:
            if not self.is_configured:
                return False, "❌ Supabase non configurato"
            
            result = self.supabase.table('roles').delete().eq('id', role_id).execute()
            
            if result.data:
                return True, f"✅ Ruolo eliminato con successo"
            else:
                return False, "❌ Errore durante l'eliminazione del ruolo"
                
        except Exception as e:
            logging.error(f"❌ Errore eliminazione ruolo: {e}")
            return False, f"❌ Errore: {str(e)}"

    def test_connection(self) -> Tuple[bool, str]:
        """Testa la connessione a Supabase"""
        try:
            if not self.is_configured:
                return False, "Supabase non configurato"
            
            # Prova a leggere una tabella
            result = self.supabase.table('brokers').select('id').limit(1).execute()
            
            if result is not None:
                return True, "Connessione Supabase OK"
            else:
                return False, "Errore connessione Supabase"
                
        except Exception as e:
            logging.error(f"❌ Errore test connessione Supabase: {e}")
            return False, f"Errore connessione: {e}"
    
    # ==================== BROKER CRUD ====================
    def create_broker(self, broker_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea un nuovo broker"""
        try:
            result = self.supabase.table('brokers').insert(broker_data).execute()
            if result.data:
                broker_id = result.data[0]['id']
                logging.info(f"✅ Broker creato con successo: {broker_data.get('nome')}")
                return True, f"✅ Broker creato con successo. ID: {broker_id}"
            else:
                return False, "❌ Errore: Nessun dato restituito"
        except Exception as e:
            logging.error(f"❌ Errore creazione broker: {e}")
            return False, f"❌ Errore creazione broker: {e}"
    
    def get_all_brokers(self) -> List[Dict[str, Any]]:
        """Ottieni tutti i broker"""
        try:
            result = self.supabase.table('brokers').select('*').execute()
            return result.data or []
        except Exception as e:
            logging.error(f"❌ Errore recupero broker: {e}")
            return []
    
    def delete_broker(self, broker_id: int) -> Tuple[bool, str]:
        """Elimina un broker"""
        try:
            result = self.supabase.table('brokers').delete().eq('id', broker_id).execute()
            logging.info(f"✅ Broker eliminato con successo: {broker_id}")
            return True, f"✅ Broker {broker_id} eliminato con successo"
        except Exception as e:
            logging.error(f"❌ Errore eliminazione broker {broker_id}: {e}")
            return False, f"❌ Errore eliminazione broker: {e}"
    
    # ==================== WALLET CRUD ====================
    def create_wallet(self, wallet_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea un nuovo wallet"""
        try:
            result = self.supabase.table('wallets').insert(wallet_data).execute()
            if result.data:
                wallet_id = result.data[0]['id']
                logging.info(f"✅ Wallet creato con successo: {wallet_data.get('nome')}")
                return True, f"✅ Wallet creato con successo. ID: {wallet_id}"
            else:
                return False, "❌ Errore: Nessun dato restituito"
        except Exception as e:
            logging.error(f"❌ Errore creazione wallet: {e}")
            return False, f"❌ Errore creazione wallet: {e}"
    
    def get_all_wallets(self) -> List[Dict[str, Any]]:
        """Ottieni tutti i wallet"""
        try:
            result = self.supabase.table('wallets').select('*').execute()
            return result.data or []
        except Exception as e:
            logging.error(f"❌ Errore recupero wallet: {e}")
            return []
    
    # ==================== PACK COPIATORI CRUD ====================
    def create_pack_copiatore(self, pack_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea un nuovo pack copiatore"""
        try:
            result = self.supabase.table('pack_copiatori').insert(pack_data).execute()
            if result.data:
                pack_id = result.data[0]['id']
                logging.info(f"✅ Pack copiatore creato con successo: {pack_data.get('nome')}")
                return True, f"✅ Pack copiatore creato con successo. ID: {pack_id}"
            else:
                return False, "❌ Errore: Nessun dato restituito"
        except Exception as e:
            logging.error(f"❌ Errore creazione pack copiatore: {e}")
            return False, f"❌ Errore creazione pack copiatore: {e}"
    
    def get_all_pack_copiatori(self) -> List[Dict[str, Any]]:
        """Ottieni tutti i pack copiatori"""
        try:
            result = self.supabase.table('pack_copiatori').select('*').execute()
            return result.data or []
        except Exception as e:
            logging.error(f"❌ Errore recupero pack copiatori: {e}")
            return []
    
    # ==================== GRUPPI PAMM CRUD ====================
    def create_gruppo_pamm(self, pamm_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea un nuovo gruppo PAMM"""
        try:
            result = self.supabase.table('gruppi_pamm').insert(pamm_data).execute()
            if result.data:
                pamm_id = result.data[0]['id']
                logging.info(f"✅ Gruppo PAMM creato con successo: {pamm_data.get('nome')}")
                return True, f"✅ Gruppo PAMM creato con successo. ID: {pamm_id}"
            else:
                return False, "❌ Errore: Nessun dato restituito"
        except Exception as e:
            logging.error(f"❌ Errore creazione gruppo PAMM: {e}")
            return False, f"❌ Errore creazione gruppo PAMM: {e}"
    
    def get_all_gruppi_pamm(self) -> List[Dict[str, Any]]:
        """Ottieni tutti i gruppi PAMM"""
        try:
            result = self.supabase.table('gruppi_pamm').select('*').execute()
            return result.data or []
        except Exception as e:
            logging.error(f"❌ Errore recupero gruppi PAMM: {e}")
            return []

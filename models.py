"""
Modelli dati per Dashboard Matematico Prop/Broker
Creato da Ezio Camporeale
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum

class BrokerState(Enum):
    """Stati possibili per un broker"""
    ATTIVO = "Attivo"
    INATTIVO = "Inattivo"
    SOSPESO = "Sospeso"
    BLOCCATO = "Bloccato"

class PropState(Enum):
    """Stati possibili per una prop firm"""
    ATTIVA = "Attiva"
    INATTIVA = "Inattiva"
    IN_VERIFICA = "In Verifica"
    RIFIUTATA = "Rifiutata"

class WalletState(Enum):
    """Stati possibili per un wallet"""
    ATTIVO = "Attivo"
    INATTIVO = "Inattivo"
    SOSPESO = "Sospeso"
    BLOCCATO = "Bloccato"

class PackCopiatoreState(Enum):
    """Stati possibili per un pack copiatore"""
    ATTIVO = "Attivo"
    INATTIVO = "Inattivo"
    IN_TEST = "In Test"
    ERRORE = "Errore"

class GruppiPAMMState(Enum):
    """Stati possibili per un gruppo PAMM"""
    ATTIVO = "Attivo"
    INATTIVO = "Inattivo"
    IN_GESTIONE = "In Gestione"
    CHIUSO = "Chiuso"

class UserRole(Enum):
    """Ruoli utenti del sistema"""
    ADMIN = "Admin"
    MANAGER = "Manager"
    TRADER = "Trader"
    COPIATORE = "Copiatore"
    PAMM_MANAGER = "PAMM Manager"
    VIEWER = "Viewer"

@dataclass
class Broker:
    """Modello per i broker"""
    id: Optional[int] = None
    nome_broker: str = ""
    tipo_broker: str = ""  # ECN, STP, Market Maker, etc.
    regolamentazione: str = ""  # FCA, CySEC, ASIC, etc.
    paese: str = ""
    sito_web: str = ""
    spread_minimo: float = 0.0
    commissioni: float = 0.0
    leverage_massimo: int = 0
    deposito_minimo: float = 0.0
    valute_supportate: List[str] = field(default_factory=list)
    piattaforme: List[str] = field(default_factory=list)  # MT4, MT5, cTrader, etc.
    stato: BrokerState = BrokerState.ATTIVO
    note: str = ""
    data_creazione: datetime = field(default_factory=datetime.now)
    data_aggiornamento: datetime = field(default_factory=datetime.now)
    creato_da: str = ""
    aggiornato_da: str = ""

@dataclass
class PropFirm:
    """Modello per le prop firm"""
    id: Optional[int] = None
    nome_prop: str = ""
    tipo_prop: str = ""  # Evaluation, Instant Funding, etc.
    capitale_iniziale: float = 0.0
    drawdown_massimo: float = 0.0
    profit_target: float = 0.0
    regole_trading: str = ""
    restrizioni_orarie: str = ""
    strumenti_permessi: List[str] = field(default_factory=list)
    broker_associati: List[int] = field(default_factory=list)
    commissioni: float = 0.0
    fee_mensile: float = 0.0
    stato: PropState = PropState.ATTIVA
    note: str = ""
    data_creazione: datetime = field(default_factory=datetime.now)
    data_aggiornamento: datetime = field(default_factory=datetime.now)
    creato_da: str = ""
    aggiornato_da: str = ""

@dataclass
class Wallet:
    """Modello per i wallet"""
    id: Optional[int] = None
    indirizzo_wallet: str = ""
    tipo_wallet: str = ""  # Bitcoin, Ethereum, Tether, etc.
    nome_wallet: str = ""
    saldo_attuale: float = 0.0
    valuta: str = ""
    exchange: str = ""
    chiave_privata: str = ""  # Crittografata
    frase_seed: str = ""  # Crittografata
    stato: WalletState = WalletState.ATTIVO
    note: str = ""
    data_creazione: datetime = field(default_factory=datetime.now)
    data_aggiornamento: datetime = field(default_factory=datetime.now)
    creato_da: str = ""
    aggiornato_da: str = ""

@dataclass
class PackCopiatore:
    """Modello per i pack copiatore"""
    id: Optional[int] = None
    numero_pack: str = ""
    broker_id: int = 0
    account_number: str = ""
    password_account: str = ""  # Crittografata
    server_broker: str = ""
    tipo_account: str = ""  # Demo, Live, etc.
    capitale_iniziale: float = 0.0
    saldo_attuale: float = 0.0
    profit_loss: float = 0.0
    drawdown_massimo: float = 0.0
    stato: PackCopiatoreState = PackCopiatoreState.ATTIVO
    note: str = ""
    data_creazione: datetime = field(default_factory=datetime.now)
    data_aggiornamento: datetime = field(default_factory=datetime.now)
    creato_da: str = ""
    aggiornato_da: str = ""

class StatoProp(Enum):
    """Stati prop firm per gruppi PAMM"""
    SVOLTO = "Svolto"
    NON_SVOLTO = "Non svolto"
    MANCANZA_SALDO = "mancanza saldo"

class DepositoPAMM(Enum):
    """Stati deposito PAMM"""
    DEPOSITATA = "Depositata"
    NON_DEPOSITATA = ""

@dataclass
class GruppiPAMM:
    """Modello esteso per i gruppi PAMM basato su Excel gruppi DEF"""
    id: Optional[int] = None
    nome_gruppo: str = ""
    manager: str = ""
    broker_id: int = 0
    account_pamm: str = ""
    capitale_totale: float = 0.0
    numero_partecipanti: int = 0
    performance_totale: float = 0.0
    performance_mensile: float = 0.0
    drawdown_massimo: float = 0.0
    commissioni_manager: float = 0.0
    commissioni_broker: float = 0.0
    stato: GruppiPAMMState = GruppiPAMMState.ATTIVO
    note: str = ""
    data_creazione: datetime = field(default_factory=datetime.now)
    data_aggiornamento: datetime = field(default_factory=datetime.now)
    creato_da: str = ""
    aggiornato_da: str = ""
    
    # Nuovi campi basati su Excel gruppi DEF
    nome_cliente: str = ""  # Nome completo cliente (es. "MANUEL CARINI [4000]")
    importo_cliente: float = 0.0  # Importo tra parentesi quadre
    stato_prop: StatoProp = StatoProp.NON_SVOLTO  # Svolto, Non svolto, mancanza saldo
    deposito_pamm: DepositoPAMM = DepositoPAMM.NON_DEPOSITATA  # Depositata o vuoto
    quota_prop: int = 1  # Sempre 1 nell'Excel
    ciclo_numero: int = 0  # Numero ciclo progressivo
    fase_prop: str = ""  # Fase prop firm
    operazione_numero: int = 0  # Numero operazione
    esito_broker: str = ""  # Esito broker
    esito_prop: str = ""  # Esito prop firm
    prelievo_prop: float = 0.0  # Importo prelievo prop
    prelievo_profit: float = 0.0  # Importo prelievo profit
    commissioni_percentuale: float = 25.0  # Commissioni fisse 25%
    credenziali_broker: str = ""  # Credenziali broker (crittografate)
    credenziali_prop: str = ""  # Credenziali prop firm (crittografate)
    responsabili_gruppo: str = ""  # Responsabili identificati (es. "frank andre", "mario")
    numero_membri_gruppo: int = 0  # Numero membri gruppo (es. 12k, 10k, 7k)

@dataclass
class Incroci:
    """Modello per gli incroci tra broker, prop, wallet e gruppi PAMM"""
    id: Optional[int] = None
    nome_incrocio: str = ""
    broker_id: int = 0
    prop_id: int = 0
    wallet_id: int = 0
    gruppo_pamm_id: int = 0
    pack_copiatore_id: int = 0
    tipo_incrocio: str = ""  # Broker-Prop, Wallet-PAMM, etc.
    descrizione: str = ""
    performance_totale: float = 0.0
    rischio_totale: float = 0.0
    stato: str = "Attivo"
    note: str = ""
    data_creazione: datetime = field(default_factory=datetime.now)
    data_aggiornamento: datetime = field(default_factory=datetime.now)
    creato_da: str = ""
    aggiornato_da: str = ""

@dataclass
class User:
    """Modello per gli utenti del sistema"""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    nome: str = ""
    cognome: str = ""
    ruolo: UserRole = UserRole.VIEWER
    attivo: bool = True
    ultimo_accesso: Optional[datetime] = None
    data_creazione: datetime = field(default_factory=datetime.now)
    data_aggiornamento: datetime = field(default_factory=datetime.now)
    creato_da: str = ""
    aggiornato_da: str = ""

@dataclass
class TransazioneWallet:
    """Modello per le transazioni dei wallet"""
    id: Optional[int] = None
    wallet_id: int = 0
    tipo_transazione: str = ""  # Deposito, Prelievo, Transfer, etc.
    importo: float = 0.0
    valuta: str = ""
    indirizzo_destinazione: str = ""
    hash_transazione: str = ""
    fee_transazione: float = 0.0
    stato: str = "Pending"  # Pending, Completed, Failed
    note: str = ""
    data_transazione: datetime = field(default_factory=datetime.now)
    data_creazione: datetime = field(default_factory=datetime.now)
    creato_da: str = ""

@dataclass
class PerformanceHistory:
    """Modello per lo storico delle performance"""
    id: Optional[int] = None
    entita_tipo: str = ""  # broker, prop, wallet, pack_copiatore, gruppo_pamm
    entita_id: int = 0
    data_performance: datetime = field(default_factory=datetime.now)
    valore_iniziale: float = 0.0
    valore_finale: float = 0.0
    profit_loss: float = 0.0
    percentuale_variazione: float = 0.0
    drawdown: float = 0.0
    note: str = ""
    data_creazione: datetime = field(default_factory=datetime.now)
    creato_da: str = ""

# Funzioni di utilità per i modelli
def broker_to_dict(broker: Broker) -> Dict[str, Any]:
    """Converte un oggetto Broker in dizionario"""
    return {
        'id': broker.id,
        'nome_broker': broker.nome_broker,
        'tipo_broker': broker.tipo_broker,
        'regolamentazione': broker.regolamentazione,
        'paese': broker.paese,
        'sito_web': broker.sito_web,
        'spread_minimo': broker.spread_minimo,
        'commissioni': broker.commissioni,
        'leverage_massimo': broker.leverage_massimo,
        'deposito_minimo': broker.deposito_minimo,
        'valute_supportate': ','.join(broker.valute_supportate),
        'piattaforme': ','.join(broker.piattaforme),
        'stato': broker.stato.value,
        'note': broker.note,
        'data_creazione': broker.data_creazione.isoformat(),
        'data_aggiornamento': broker.data_aggiornamento.isoformat(),
        'creato_da': broker.creato_da,
        'aggiornato_da': broker.aggiornato_da
    }

def dict_to_broker(data: Dict[str, Any]) -> Broker:
    """Converte un dizionario in oggetto Broker"""
    return Broker(
        id=data.get('id'),
        nome_broker=data.get('nome_broker', ''),
        tipo_broker=data.get('tipo_broker', ''),
        regolamentazione=data.get('regolamentazione', ''),
        paese=data.get('paese', ''),
        sito_web=data.get('sito_web', ''),
        spread_minimo=float(data.get('spread_minimo', 0.0)),
        commissioni=float(data.get('commissioni', 0.0)),
        leverage_massimo=int(data.get('leverage_massimo', 0)),
        deposito_minimo=float(data.get('deposito_minimo', 0.0)),
        valute_supportate=data.get('valute_supportate', '').split(',') if data.get('valute_supportate') else [],
        piattaforme=data.get('piattaforme', '').split(',') if data.get('piattaforme') else [],
        stato=BrokerState(data.get('stato', 'Attivo')),
        note=data.get('note', ''),
        data_creazione=datetime.fromisoformat(data.get('data_creazione', datetime.now().isoformat())),
        data_aggiornamento=datetime.fromisoformat(data.get('data_aggiornamento', datetime.now().isoformat())),
        creato_da=data.get('creato_da', ''),
        aggiornato_da=data.get('aggiornato_da', '')
    )

# Funzioni per GruppiPAMM esteso
def gruppi_pamm_to_dict(gruppo: GruppiPAMM) -> Dict[str, Any]:
    """Converte un oggetto GruppiPAMM in dizionario"""
    return {
        'id': gruppo.id,
        'nome_gruppo': gruppo.nome_gruppo,
        'manager': gruppo.manager,
        'broker_id': gruppo.broker_id,
        'account_pamm': gruppo.account_pamm,
        'capitale_totale': gruppo.capitale_totale,
        'numero_partecipanti': gruppo.numero_partecipanti,
        'performance_totale': gruppo.performance_totale,
        'performance_mensile': gruppo.performance_mensile,
        'drawdown_massimo': gruppo.drawdown_massimo,
        'commissioni_manager': gruppo.commissioni_manager,
        'commissioni_broker': gruppo.commissioni_broker,
        'stato': gruppo.stato.value,
        'note': gruppo.note,
        'data_creazione': gruppo.data_creazione.isoformat(),
        'data_aggiornamento': gruppo.data_aggiornamento.isoformat(),
        'creato_da': gruppo.creato_da,
        'aggiornato_da': gruppo.aggiornato_da,
        # Nuovi campi Excel
        'nome_cliente': gruppo.nome_cliente,
        'importo_cliente': gruppo.importo_cliente,
        'stato_prop': gruppo.stato_prop.value,
        'deposito_pamm': gruppo.deposito_pamm.value,
        'quota_prop': gruppo.quota_prop,
        'ciclo_numero': gruppo.ciclo_numero,
        'fase_prop': gruppo.fase_prop,
        'operazione_numero': gruppo.operazione_numero,
        'esito_broker': gruppo.esito_broker,
        'esito_prop': gruppo.esito_prop,
        'prelievo_prop': gruppo.prelievo_prop,
        'prelievo_profit': gruppo.prelievo_profit,
        'commissioni_percentuale': gruppo.commissioni_percentuale,
        'credenziali_broker': gruppo.credenziali_broker,
        'credenziali_prop': gruppo.credenziali_prop,
        'responsabili_gruppo': gruppo.responsabili_gruppo,
        'numero_membri_gruppo': gruppo.numero_membri_gruppo
    }

def dict_to_gruppi_pamm(data: Dict[str, Any]) -> GruppiPAMM:
    """Converte un dizionario in oggetto GruppiPAMM"""
    return GruppiPAMM(
        id=data.get('id'),
        nome_gruppo=data.get('nome_gruppo', ''),
        manager=data.get('manager', ''),
        broker_id=int(data.get('broker_id', 0)),
        account_pamm=data.get('account_pamm', ''),
        capitale_totale=float(data.get('capitale_totale', 0.0)),
        numero_partecipanti=int(data.get('numero_partecipanti', 0)),
        performance_totale=float(data.get('performance_totale', 0.0)),
        performance_mensile=float(data.get('performance_mensile', 0.0)),
        drawdown_massimo=float(data.get('drawdown_massimo', 0.0)),
        commissioni_manager=float(data.get('commissioni_manager', 0.0)),
        commissioni_broker=float(data.get('commissioni_broker', 0.0)),
        stato=GruppiPAMMState(data.get('stato', 'Attivo')),
        note=data.get('note', ''),
        data_creazione=datetime.fromisoformat(data.get('data_creazione', datetime.now().isoformat())),
        data_aggiornamento=datetime.fromisoformat(data.get('data_aggiornamento', datetime.now().isoformat())),
        creato_da=data.get('creato_da', ''),
        aggiornato_da=data.get('aggiornato_da', ''),
        # Nuovi campi Excel
        nome_cliente=data.get('nome_cliente', ''),
        importo_cliente=float(data.get('importo_cliente', 0.0)),
        stato_prop=StatoProp(data.get('stato_prop', 'Non svolto')),
        deposito_pamm=DepositoPAMM(data.get('deposito_pamm', '')),
        quota_prop=int(data.get('quota_prop', 1)),
        ciclo_numero=int(data.get('ciclo_numero', 0)),
        fase_prop=data.get('fase_prop', ''),
        operazione_numero=int(data.get('operazione_numero', 0)),
        esito_broker=data.get('esito_broker', ''),
        esito_prop=data.get('esito_prop', ''),
        prelievo_prop=float(data.get('prelievo_prop', 0.0)),
        prelievo_profit=float(data.get('prelievo_profit', 0.0)),
        commissioni_percentuale=float(data.get('commissioni_percentuale', 25.0)),
        credenziali_broker=data.get('credenziali_broker', ''),
        credenziali_prop=data.get('credenziali_prop', ''),
        responsabili_gruppo=data.get('responsabili_gruppo', ''),
        numero_membri_gruppo=int(data.get('numero_membri_gruppo', 0))
    )

# Funzioni simili per gli altri modelli...
def prop_to_dict(prop: PropFirm) -> Dict[str, Any]:
    """Converte un oggetto PropFirm in dizionario"""
    return {
        'id': prop.id,
        'nome_prop': prop.nome_prop,
        'tipo_prop': prop.tipo_prop,
        'capitale_iniziale': prop.capitale_iniziale,
        'drawdown_massimo': prop.drawdown_massimo,
        'profit_target': prop.profit_target,
        'regole_trading': prop.regole_trading,
        'restrizioni_orarie': prop.restrizioni_orarie,
        'strumenti_permessi': ','.join(prop.strumenti_permessi),
        'broker_associati': ','.join(map(str, prop.broker_associati)),
        'commissioni': prop.commissioni,
        'fee_mensile': prop.fee_mensile,
        'stato': prop.stato.value,
        'note': prop.note,
        'data_creazione': prop.data_creazione.isoformat(),
        'data_aggiornamento': prop.data_aggiornamento.isoformat(),
        'creato_da': prop.creato_da,
        'aggiornato_da': prop.aggiornato_da
    }

def dict_to_prop(data: Dict[str, Any]) -> PropFirm:
    """Converte un dizionario in oggetto PropFirm"""
    return PropFirm(
        id=data.get('id'),
        nome_prop=data.get('nome_prop', ''),
        tipo_prop=data.get('tipo_prop', ''),
        capitale_iniziale=float(data.get('capitale_iniziale', 0.0)),
        drawdown_massimo=float(data.get('drawdown_massimo', 0.0)),
        profit_target=float(data.get('profit_target', 0.0)),
        regole_trading=data.get('regole_trading', ''),
        restrizioni_orarie=data.get('restrizioni_orarie', ''),
        strumenti_permessi=data.get('strumenti_permessi', '').split(',') if data.get('strumenti_permessi') else [],
        broker_associati=[int(x) for x in data.get('broker_associati', '').split(',') if x] if data.get('broker_associati') else [],
        commissioni=float(data.get('commissioni', 0.0)),
        fee_mensile=float(data.get('fee_mensile', 0.0)),
        stato=PropState(data.get('stato', 'Attiva')),
        note=data.get('note', ''),
        data_creazione=datetime.fromisoformat(data.get('data_creazione', datetime.now().isoformat())),
        data_aggiornamento=datetime.fromisoformat(data.get('data_aggiornamento', datetime.now().isoformat())),
        creato_da=data.get('creato_da', ''),
        aggiornato_da=data.get('aggiornato_da', '')
    )

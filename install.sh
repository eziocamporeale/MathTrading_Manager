#!/bin/bash

# Script di Installazione DASH_PROP_BROKER
# Creato da Ezio Camporeale

echo "🧮 DASH_PROP_BROKER - Installazione Automatica"
echo "=============================================="

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzione per stampare messaggi colorati
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verifica Python
print_status "Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION trovato"
else
    print_error "Python3 non trovato. Installa Python 3.8+ prima di continuare."
    exit 1
fi

# Verifica pip
print_status "Verificando pip..."
if command -v pip3 &> /dev/null; then
    print_success "pip3 trovato"
else
    print_error "pip3 non trovato. Installa pip prima di continuare."
    exit 1
fi

# Crea ambiente virtuale (opzionale)
print_status "Creando ambiente virtuale..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Ambiente virtuale creato"
else
    print_warning "Ambiente virtuale già esistente"
fi

# Attiva ambiente virtuale
print_status "Attivando ambiente virtuale..."
source venv/bin/activate
print_success "Ambiente virtuale attivato"

# Installa dipendenze
print_status "Installando dipendenze Python..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    print_success "Dipendenze installate correttamente"
else
    print_error "Errore durante l'installazione delle dipendenze"
    exit 1
fi

# Verifica installazione
print_status "Verificando installazione..."
python3 -c "import streamlit, supabase, pandas, plotly" 2>/dev/null
if [ $? -eq 0 ]; then
    print_success "Tutte le dipendenze sono state installate correttamente"
else
    print_error "Alcune dipendenze non sono state installate correttamente"
    exit 1
fi

# Test connessione Supabase
print_status "Testando connessione Supabase..."
python3 test_supabase_connection.py
if [ $? -eq 0 ]; then
    print_success "Connessione Supabase OK"
else
    print_warning "Problemi con la connessione Supabase"
    print_warning "Esegui manualmente: python3 setup_supabase.py"
fi

# Crea script di avvio
print_status "Creando script di avvio..."
cat > start_app.sh << 'EOF'
#!/bin/bash
echo "🧮 Avviando DASH_PROP_BROKER..."
source venv/bin/activate
streamlit run app.py
EOF

chmod +x start_app.sh
print_success "Script di avvio creato: start_app.sh"

# Crea script di test
print_status "Creando script di test..."
cat > test_app.sh << 'EOF'
#!/bin/bash
echo "🧪 Testando DASH_PROP_BROKER..."
source venv/bin/activate
python3 test_supabase_connection.py
EOF

chmod +x test_app.sh
print_success "Script di test creato: test_app.sh"

# Informazioni finali
echo ""
echo "🎉 INSTALLAZIONE COMPLETATA!"
echo "=========================="
echo ""
echo "📋 Prossimi passi:"
echo "   1. Testa l'applicazione: ./test_app.sh"
echo "   2. Avvia l'applicazione: ./start_app.sh"
echo "   3. Oppure: streamlit run app.py"
echo ""
echo "🌐 L'applicazione sarà disponibile su:"
echo "   http://localhost:8501"
echo ""
echo "📚 Documentazione: README.md"
echo "📋 TODO List: TODO_COMPLETAMENTO.md"
echo ""
echo "🔧 Per problemi:"
echo "   - Controlla i log sopra"
echo "   - Verifica la connessione Supabase"
echo "   - Esegui: python3 setup_supabase.py"
echo ""
echo "✅ Installazione completata con successo!"

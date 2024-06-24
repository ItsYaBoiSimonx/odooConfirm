try:
    import json
    import datetime
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService
    import time
except ImportError as e:
    import os
    os.system('pip install selenium')
    os.system('pip install webdriver_manager')
    import json
    import datetime
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService
    import time

# Funzione per colorare il testo per l'output del terminale
def colorize(text, color_code):
    return f"\033[{color_code}{text}\033[0m"

# Funzioni di logging
def log_warning(message):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    print(f"{colorize(timestamp, '33m')} {colorize('Attenzione!', '33m')} {message.capitalize()}.")

def log_success(message):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    print(f"{colorize(timestamp, '201m')} {colorize('Successo!', '201m')} {message.capitalize()}.")

def log_error(message):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    print(f"{colorize(timestamp, '31m')} {colorize('Errore!', '31m')} {message.capitalize()}.")

# Leggi il file config.json
with open('config.json') as config_file:
    config = json.load(config_file)

# Ottieni username, password e sales_page_url da config
username = config['username']
password = config['password']
sales_page_url = config['sales_page_url']


logo = colorize('''

                $$\                     
                $$ |                    
 $$$$$$\   $$$$$$$ | $$$$$$\   $$$$$$\  
$$  __$$\ $$  __$$ |$$  __$$\ $$  __$$\ 
$$ /  $$ |$$ /  $$ |$$ /  $$ |$$ /  $$ |
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |
\$$$$$$  |\$$$$$$$ |\$$$$$$  |\$$$$$$  |
 \______/  \_______| \______/  \______/  v1.0.0 
    |
    |-> Developed by: itsyaboisimonx@unitiva
    |-> https://github.com/itsyaboisimonx
                
''', '201m')

print(logo)

# Inizializza il driver Chrome
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Apri l'URL della pagina di vendita
driver.get(sales_page_url)
log_success("Pagina di vendita aperta")

# Trova il campo di input dell'username e digita l'username
try:
    username_input = driver.find_element(By.ID, 'login')
    username_input.send_keys(username)
    log_success("Username inserito")
except Exception as e:
    log_error("Inserimento username fallito")

# Trova il campo di input della password e digita la password
try:
    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(password)
    log_success("Password inserita")
except Exception as e:
    log_error("Inserimento password fallito")

# Invia il modulo
password_input.send_keys(Keys.RETURN)
log_success("Modulo inviato")

# Attendi il caricamento del corpo della tabella
wait = WebDriverWait(driver, 20)  # Regola il timeout secondo necessità
try:
    table_body = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[3]/div/table/tbody')))
    log_success("Corpo della tabella caricato")
except Exception as e:
    log_error("Caricamento corpo della tabella fallito")

# Trova tutti gli elementi <tr> all'interno del corpo della tabella
rows = table_body.find_elements(By.TAG_NAME, 'tr')

# Lista per contenere gli elementi <td> con la classe 'text-bg-info'
info_class_tds = []

# Itera attraverso ogni riga
for row in rows:
    # Trova tutti gli elementi <td> nella riga
    tds = row.find_elements(By.TAG_NAME, 'td')
    # Controlla ogni <td> per le parole specificate
    for td in tds:
        if "quotation" in td.text.lower() or "preventivo" in td.text.lower():
            # Se la condizione è soddisfatta, aggiungi il <td> alla lista
            log_warning("Quotation trovata! Aggiungo all'array...")
            info_class_tds.append(td)

# Stampa il numero di elementi trovati
log_warning(f"Quotation da confermare: {len(info_class_tds)}")

# Inizializza un contatore per le righe per gestire il caricamento dinamico dei contenuti
row_index = 0

while True:
    # Aggiorna il corpo della tabella e la lista delle righe dopo ogni navigazione
    table_body = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[3]/div/table/tbody')))
    rows = table_body.find_elements(By.TAG_NAME, 'tr')
    
    # Interrompi il ciclo se row_index supera il numero di righe
    if row_index >= len(rows):
        log_success("Tutte le righe sono state elaborate")
        break
    
    row = rows[row_index]
    tds = row.find_elements(By.TAG_NAME, 'td')
    
    for td in tds:
        if "quotation" in td.text.lower() or "preventivo" in td.text.lower():
            if "inviato" in td.text.lower():
                pass 

            td.click()
            log_success("Tentativo di conferma inviato...")

            # Attendi il completamento della navigazione, se necessario
            confirm = wait.until(EC.element_to_be_clickable((By.NAME, 'action_confirm')))
            confirm.click()
            log_success("Conferma inviata")

            time.sleep(3)
            
            # Torna indietro
            driver.back()
            
            # Attendi che la tabella sia nuovamente presente dopo essere tornato indietro
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[3]/div/table/tbody')))
            
            # Interrompi il ciclo interno per evitare errori di riferimento a elementi non più validi
            break
    
    # Incrementa row_index dopo aver elaborato ogni riga e essere tornato indietro
    row_index += 1

# Chiudi il browser
log_success("Ho finito! Premi invio per chiudere..")

input()
driver.quit()
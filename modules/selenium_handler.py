import os
import time
import shutil
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def _setup_driver(download_dir):
    """Configura e retorna uma instância do WebDriver do Chrome."""
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    # Esconde logs do webdriver no console
    log_path = 'NUL' if os.name == 'nt' else '/dev/null'
    
    # Em vez de um Service vazio, agora ele usa o ChromeDriverManager para
    # baixar e instalar o driver correto automaticamente.
    service = Service(ChromeDriverManager().install(), log_path=log_path)
    
    return webdriver.Chrome(service=service, options=chrome_options)

def _rename_latest_download(download_dir, new_name="respostas_forms.xlsx", timeout=30):
    """Espera por um download .xlsx, renomeia e retorna seu caminho."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if f.endswith('.xlsx')]
        if not files:
            time.sleep(1)
            continue

        latest_file = max(files, key=os.path.getmtime)
        # Checa se o arquivo não é um download temporário
        if not latest_file.endswith(".crdownload"):
            destination = os.path.join(download_dir, new_name)
            if os.path.exists(destination):
                os.remove(destination)
            shutil.move(latest_file, destination)
            return destination
    raise FileNotFoundError(f"Nenhum arquivo .xlsx encontrado em {download_dir} em {timeout}s.")

def download_form_responses(config, email, password, login_url):
    """Orquestra o processo de login e download do arquivo Excel do Forms."""

    # Garante que o diretório de download exista antes de iniciar o Chrome
    os.makedirs(config["download_dir"], exist_ok=True)

    driver = _setup_driver(config["download_dir"])
    driver.implicitly_wait(20) # Embora usemos waits explícitos, é uma boa segurança
    
    try:
        print("🚀 Iniciando login na Microsoft...")
        driver.get(login_url)
        # Usando WebDriverWait para maior robustez
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "i0116"))).send_keys(email)
        driver.find_element(By.ID, "idSIButton9").click()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "i0118"))).send_keys(password)
        driver.find_element(By.ID, "idSIButton9").click()

        # Lida com a tela "Permanecer conectado?"
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "idBtn_Back"))).click()
        except Exception:
            pass # Se o botão não aparecer, ótimo, seguimos em frente.

        print("✅ Login realizado. Navegando para o formulário...")
        driver.get(config["form_url"])

        # Simplificando a lógica de cliques com um try-except mais genérico
        # Nota: XPaths são frágeis. Se possível, use IDs ou seletores CSS.
        try:
            # Tenta clicar no botão "Insights" se existir
            insights_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Insights e ações']]")))
            insights_button.click()
        except Exception:
            pass # Se não encontrar, não há problema

        print("📥 Clicando para baixar o arquivo Excel...")
        dropdown_menu = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[id*="ExcelDropdownMenu"]')))
        dropdown_menu.click()
        
        download_copy_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@role, "menuitem") and contains(@aria-label, "Baixar uma cópia")]')))
        download_copy_button.click()
        
        print("⏳ Aguardando e renomeando o download...")
        final_path = _rename_latest_download(config["download_dir"])
        print(f"✔️ Arquivo salvo em: {final_path}")
        return final_path

    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado no Selenium.")
        print("="*30 + " TRACEBACK DETALHADO " + "="*30)
        traceback.print_exc() # Isso vai imprimir o mapa completo do erro
        print("="*82)
        # driver.save_screenshot('error_screenshot.png')
        return None
    finally:
        driver.quit()
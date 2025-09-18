# config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Constrói o caminho para a raiz do projeto de forma dinâmica
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega o arquivo .env da raiz do projeto
load_dotenv(BASE_DIR / '.env')

# Credenciais e Tokens
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
NOTION_TOKEN = os.getenv('NOTION_TOKEN')

if not all([EMAIL, PASSWORD, NOTION_TOKEN]):
    missing_vars = [var for var, val in {"EMAIL": EMAIL, "PASSWORD": PASSWORD, "NOTION_TOKEN": NOTION_TOKEN}.items() if not val]
    raise ValueError(f"Erro: As seguintes variáveis de ambiente estão faltando no seu arquivo .env: {', '.join(missing_vars)}")


FORM_URL_LOGIN = "https://login.microsoftonline.com/"

# Configuração das Áreas (agora usando caminhos relativos)
AREAS_CONFIG = {
    "Area1": {
        "form_url": "https://forms.office.com/Pages/DesignPageV2.aspx?prevorigin=shell&origin=NeoPortalPage&subpage=design&id=M083D5gGVkaWZUrSp05YCkqq-Y7ndlVMog_6jqTL4MBUNlNNUkxaUjMwM0tNNkhTVE1JVjk0TEFIMyQlQCN0PWcu&analysis=true",
        "notion_db_id": os.getenv('NOTION_DATABASE_ID_AREA1'),
        # Caminhos relativos a partir da raiz do projeto
        "download_dir": str(BASE_DIR / "RespostaForms" / "Area1"),
        "validation_file": str(BASE_DIR / "ValidarRespostas" / "Area1" / "registros_forms.xlsx"),
        "title_field": "O que você deseja solicitar?"
    },
    # Você pode adicionar Area2, Area3 aqui...
}
# Forms-to-Notion 🤖

###Help Desk Improvisado

## 🎯 Objetivo

Este projeto automatiza o processo de extrair respostas de um formulário do **Microsoft Forms**, processá-las e criar tarefas correspondentes em um banco de dados do **Notion**. Ele foi projetado para atuar como um sistema de help desk improvisado, onde as solicitações feitas via Forms são convertidas automaticamente em cards de tarefas rastreáveis.

---

## ✨ Funcionalidades

-   **Login Automatizado**: Realiza o login seguro na plataforma da Microsoft.
-   **Web Scraping com Selenium**: Navega até a página de respostas do Forms e baixa a planilha Excel.
-   **Processamento de Dados**: Lê o arquivo Excel e identifica apenas as respostas novas, que ainda não foram processadas.
-   **Integração com API do Notion**: Cria uma nova página (card) no banco de dados do Notion para cada nova resposta, preenchendo propriedades como título, solicitante e prioridade.
-   **Configurável**: Permite configurar múltiplas automações para diferentes formulários e bancos de dados do Notion através de um único arquivo de configuração.

---

## 🛠️ Tecnologias Utilizadas

-   **Python 3.12+**
-   **Selenium**: Para automação e web scraping do Microsoft Forms.
-   **Notion API**: Para integração e criação de páginas.
-   **Openpyxl**: Para leitura e escrita de arquivos `.xlsx`.
-   **Dotenv**: Para gerenciamento de variáveis de ambiente e segredos.

---

## 🚀 Como Executar

### 1. Pré-requisitos

-   Python 3.12 ou superior instalado.
-   Google Chrome instalado.
-   Uma conta Microsoft com acesso ao Forms. **Observação:** Contas com autenticação de dois fatores (2FA) podem exigir a criação de uma "Senha de Aplicativo" para funcionar com automações.
-   Uma [integração do Notion](https://www.notion.so/my-integrations) devidamente configurada e adicionada ao seu banco de dados de destino.

### 2. Instalação

Clone o repositório:
```bash
git clone [https://github.com/7ogeid/FormsToNotion.git](https://github.com/7ogeid/FormsToNotion.git)
cd FormsToNotion
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

### 3. Configuração

1.  Na raiz do projeto, renomeie o arquivo `.env.example` para `.env`.
2.  Abra o arquivo `.env` e preencha as variáveis com suas credenciais e IDs, conforme o exemplo abaixo:

```env
# .env
EMAIL="seu_email@microsoft.com"
PASSWORD="sua_senha"

# Notion
NOTION_TOKEN="secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
NOTION_DATABASE_ID_AREA1="xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# NOTION_DATABASE_ID_AREA2="..."
```

### 4. Execução

Para rodar a automação para todas as áreas configuradas em `config/settings.py`, execute:
```bash
python main.py
```
---
## ⚙️ Configurando as Áreas

A principal vantagem deste projeto é a sua capacidade de gerenciar múltiplos formulários e bancos de dados do Notion de forma centralizada. Para adicionar ou modificar uma automação, basta editar o dicionário `AREAS_CONFIG` no arquivo `config/settings.py`.

**Exemplo de Configuração:**
```python
# config/settings.py

AREAS_CONFIG = {
    "Area1": {
        "form_url": "URL_DO_SEU_FORMULARIO_1",
        "notion_db_id": os.getenv('NOTION_DATABASE_ID_AREA1'),
        "download_dir": str(BASE_DIR / "RespostaForms" / "Area1"),
        "validation_file": str(BASE_DIR / "ValidarRespostas" / "Area1" / "registros_forms.xlsx"),
        "title_field": "O que você deseja solicitar?"
    },
    # Para adicionar uma nova área, basta copiar o bloco acima
    "Area2": {
        "form_url": "URL_DO_SEU_FORMULARIO_2",
        "notion_db_id": os.getenv('NOTION_DATABASE_ID_AREA2'),
        "download_dir": str(BASE_DIR / "RespostaForms" / "Area2"),
        "validation_file": str(BASE_DIR / "ValidarRespostas" / "Area2" / "registros_forms.xlsx"),
        "title_field": "Qual a sua solicitação para a Area2?"
    }
}
```
**Importante:** Ao adicionar uma nova área (como a "Area2" no exemplo), não se esqueça de adicionar a variável de ID correspondente (ex: `NOTION_DATABASE_ID_AREA2`) ao seu arquivo `.env`.

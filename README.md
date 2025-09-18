# Forms-to-Notion Automator 🤖

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

-   **Python 3.12.9**
-   **Selenium**: Para automação e web scraping do Microsoft Forms.
-   **Notion API**: Para integração e criação de páginas.
-   **Openpyxl**: Para leitura e escrita de arquivos `.xlsx`.
-   **Dotenv**: Para gerenciamento de variáveis de ambiente e segredos.

---

## 🚀 Como Executar

### 1. Pré-requisitos

-   Python 3.12.9 ou superior instalado.
-   Google Chrome instalado.
-   Uma conta Microsoft com acesso ao Forms sem autenticador de dois fatoes e uma integração com o Notion configurada.

### 2. Instalação

Clone o repositório:
```bash
git clone [https://github.com/SEU_USUARIO/FormsToNotion.git](https://github.com/SEU_USUARIO/FormsToNotion.git)
cd FormsToNotion
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

### 3. Configuração

Renomeie o arquivo `.env.example` (que você deve criar) para `.env` e preencha com suas credenciais:

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
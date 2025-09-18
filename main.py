# main.py
from notion_client import Client
from config import settings
from modules import selenium_handler, excel_handler, notion_handler

def process_area(area_name, config):
    """Executa todo o fluxo de automação para uma área específica."""
    print(f"\n{'='*20}\n🤖 Iniciando processamento para: {area_name}\n{'='*20}")
    
    # 1. Baixar o arquivo Excel do Microsoft Forms
    excel_path = selenium_handler.download_form_responses(
        config, settings.EMAIL, settings.PASSWORD, settings.FORM_URL_LOGIN
    )
    if not excel_path:
        print(f"Falha ao baixar respostas para {area_name}. Pulando para a próxima.")
        return

    # 2. Extrair todas as respostas do arquivo
    all_responses = excel_handler.extract_responses(excel_path)
    if not all_responses:
        print(f"Nenhuma resposta encontrada no arquivo Excel para {area_name}.")
        return

    # 3. Filtrar apenas as novas respostas
    new_responses = excel_handler.filter_new_responses(
        config["validation_file"], all_responses
    )
    if not new_responses:
        print(f"Nenhuma nova resposta para processar em {area_name}.")
        return

    print(f"✨ Encontradas {len(new_responses)} novas respostas em {area_name}.")

    # 4. Conectar ao Notion e criar as páginas
    notion = Client(auth=settings.NOTION_TOKEN)
    for response in new_responses:
        notion_handler.create_notion_page(
            client=notion,
            db_id=config["notion_db_id"],
            data=response,
            title_field=config["title_field"]
        )
    
    # 5. Atualizar o arquivo de controle com os IDs processados
    excel_handler.update_validation_file(config["validation_file"], new_responses)
    print(f"✔️ Arquivo de validação para {area_name} atualizado.")

def main():
    """Função principal que itera sobre todas as áreas configuradas."""
    for area_name, config in settings.AREAS_CONFIG.items():
        process_area(area_name, config)

if __name__ == "__main__":
    main()
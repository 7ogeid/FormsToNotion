from notion_client import Client

# Constantes para evitar "magic strings"
MAX_BLOCK_LENGTH = 2000
FIELDS_TO_EXCLUDE_FROM_BODY = [
    "ID", "Hora de início", "Hora de conclusão", "Email", "Nome", 
    "Defina a prioridade desta demanda:", "O que você deseja solicitar?", 
    "O que você deseja solicitar? ", "Anexo", "Anexo "
]

def _split_text_into_blocks(text, max_length=MAX_BLOCK_LENGTH):
    """Divide um texto longo em blocos com o tamanho máximo permitido pelo Notion."""
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def create_notion_page(client, db_id, data, title_field):
    """Cria uma nova página em um banco de dados do Notion com os dados da resposta."""
    
    # Limpando os nomes de campo para evitar problemas com espaços extras
    cleaned_data = {k.strip(): v for k, v in data.items()}
    
    # Monta o corpo da página Notion
    body_content = "\n\n".join(
        f"📌 **{key}**\n{value}"
        for key, value in cleaned_data.items()
        if value and key not in FIELDS_TO_EXCLUDE_FROM_BODY
    )
    
    page_title = f"{cleaned_data.get('ID', 'N/A')} - {cleaned_data.get(title_field, 'Sem Título')}"
    solicited_by = f"{cleaned_data.get('Email', '')}\n{cleaned_data.get('Nome', '')}"
    priority = cleaned_data.get('Defina a prioridade desta demanda:', 'Média').strip().capitalize()
    attachment_url = cleaned_data.get("Anexo")

    try:
        client.pages.create(
            parent={"database_id": db_id},
            properties={
                "Nome": {"title": [{"text": {"content": page_title}}]},
                "Solicitado por": {"rich_text": [{"text": {"content": solicited_by}}]},
                "Prioridade": {"select": {"name": priority or 'Média'}},
                "Documentos Anexados": {"url": attachment_url},
            },
            # Adiciona o corpo como blocos de parágrafo filhos
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": block}}]}
                }
                for block in _split_text_into_blocks(body_content)
            ]
        )
        print(f"✅ Tarefa criada no Notion para ID {cleaned_data['ID']}")
    except Exception as e:
        print(f"❌ Erro ao criar tarefa no Notion para ID {cleaned_data['ID']}: {e}")
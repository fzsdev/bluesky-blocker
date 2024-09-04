#!caminho/para/seu/repositorio/bluesky-blocker/venv/bin/python
# modificar para onde está o binario do python

from atproto import Client, models
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

# Carregar variáveis de ambiente
load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

# Inicializar cliente
client = Client(base_url='https://bsky.social')


# Função para autenticação
def authenticate():
    try:
        client.login(username, password)
        print("Autenticado com sucesso!")
    except Exception as e:
        logging.error(f"Erro na autenticação: {e}")
        print("Falha na autenticação. Verifique os logs para mais detalhes.")
        exit(1)


# Função para buscar postagens por uma palavra-chave
def search_posts(client, keyword, with_hashtag=False):
    try:
        query = f"#{keyword}" if with_hashtag else keyword  # Adiciona o # se necessário
        params = models.app.bsky.feed.search_posts.Params(
            q=query,  # Passa a palavra-chave para pesquisa.
            limit=100  # Limite para evitar grandes volumes de dados, o padrão é 25.
        )
        response = client.app.bsky.feed.search_posts(params=params)
        return response.posts
    except Exception as e:
        logging.error(f"Erro na pesquisa por palavra-chave '{keyword}': {e}")
        return []


# Função para bloquear um usuário pelo DID
def block_user(client, blocked_user_did):
    try:
        block_record = models.AppBskyGraphBlock.Record(
            subject=blocked_user_did,
            created_at=client.get_current_time_iso()
        )
        uri = client.app.bsky.graph.block.create(client.me.did, block_record).uri
        print(f"Usuário com DID {blocked_user_did} bloqueado com sucesso. URI do bloqueio: {uri}")
        return uri
    except Exception as e:
        logging.error(f"Erro ao bloquear o usuário com DID {blocked_user_did}: {e}")
        return None


# Função para registrar o conteúdo das postagens.
def log_post_content(post):
    """Registra o conteúdo da postagem em um arquivo separado com timestamp."""
    try:
        # Cria a pasta log_post_blocked se não existir.
        log_dir = 'log_post_blocked'
        os.makedirs(log_dir, exist_ok=True)

        # Formata o timestamp atual
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{log_dir}/post_{timestamp}.txt"

        # Cria o conteúdo do log
        with open(filename, 'w') as file:
            author = post.author.display_name
            content = post.record.text  # Ajuste se o conteúdo estiver em outro campo.
            file.write(f"Author: {author}\n")
            file.write(f"Content: {content}\n")
            file.write(f"URI: {post.uri}\n")

        print(f"Conteúdo da postagem registrado com sucesso em {filename}")
    except Exception as e:
        logging.error(f"Erro ao registrar o conteúdo da postagem: {e}")


# Função principal
def main():
    authenticate()
    keyword = input("Digite a palavra-chave para buscar e bloquear contas (ou hashtag se preferir): ")
    with_hashtag = input("Deseja buscar com hashtag? (s/n): ").strip().lower() == 's'
    posts = search_posts(client, keyword, with_hashtag=with_hashtag)

    if posts:
        for post in posts:
            try:
                author_did = post.author.did  # Acessa o DID do autor diretamente.
                block_uri = block_user(client, author_did)
                if block_uri:
                    log_post_content(post)  # Log do conteúdo da postagem
            except AttributeError as e:
                logging.error(f"Erro ao acessar o DID do autor: {e}")
            except Exception as e:
                logging.error(f"Erro ao processar a postagem: {e}")
    else:
        print("Nenhuma postagem encontrada ou erro na busca. Verifique os logs.")

    # Mensagem final
    print(
        "Sanitização do feed até o momento foi completada com sucesso! Rode novamente o script para bloquear novas" +
        "contas que estão utilizando as palavras procuradas.")


if __name__ == "__main__":
    main()

### Como utilizar `bluesky-blocker`:

- Clonar o repositório;
- Criar venv com o seguinte comando na pasta do projeto: `python3.10 -m venv venv`;
- Comando para ativar venv `source venv/bin/activate`;
- Instalar as dependências do projeto: `$ pip install -r requirements.txt`;
- Criar um arquivo `.env` na raiz do projeto com seu usuário e senha do Bluesky no seguinte padrão:
  ```
  USERNAME=seu_usuario
  PASSWORD=sua_senha
  ```

Após utilizar o script, rodar o comando `$ deactivate` no terminal para desativar o venv.

___

#### Documentação utilizada:

- BlueSky: https://docs.bsky.app
- AT Protocol: https://atproto.blue/en/latest/index.html
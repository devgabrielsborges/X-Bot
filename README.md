# X-Bot: Twitter Automation Bot

## Descrição
X-Bot é um bot de automação para o Twitter, que publica tweets sobre promoções usando dados armazenados no Firebase, gera textos com IA via Groq Cloud, e envia notificações via SMS com a API Twilio.

## Funcionalidades
- Obtém o índice atual para a postagem.
- Busca informações do produto no Firebase.
- Gera texto promocional usando Groq Cloud.
- Publica o texto no Twitter.
- Atualiza o Firebase com o status da postagem.
- Envia notificação SMS via Twilio.

## Pré-requisitos
- Python 3.8+
- Conta no Firebase
- Conta no Twilio
- Conta no Groq Cloud
- Conta de Desenvolvedor no Twitter

## Instalação
1. Clone o repositório:
    ```bash
    git clone https://github.com/devgabrielsborges/X-Bot.git
    cd X-Bot
    ```
2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/MacOS
    venv\Scripts\activate  # Para Windows
    ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
    ```env
    x_apikey=YOUR_TWITTER_API_KEY
    x_apisecret=YOUR_TWITTER_API_SECRET
    x_token=YOUR_TWITTER_ACCESS_TOKEN
    x_tokensecret=YOUR_TWITTER_ACCESS_TOKEN_SECRET
    x_bearertoken=YOUR_TWITTER_BEARER_TOKEN
    twilio_sid=YOUR_TWILIO_SID
    twilio_token=YOUR_TWILIO_AUTH_TOKEN
    number_from=YOUR_TWILIO_PHONE_NUMBER
    number_to=YOUR_PHONE_NUMBER
    firebase_api_key=YOUR_FIREBASE_API_KEY
    firebase_db_url=YOUR_FIREBASE_DB_URL
    ```

## Executando o Bot
1. Certifique-se de que o índice inicial está corretamente definido no Firebase sob `actual_index`.
2. Execute o script principal:
    ```bash
    python main.py
    ```

## Estrutura de Arquivos
- `classes.py`: Contém todas as classes auxiliares e métodos usados pelo script principal.
  - `FirebaseAPI`: Classe para operações com o Firebase.
  - `TwilioAPI`: Classe para operações com a API Twilio.
  - `GroqCloud`: Classe para operações com o Groq Cloud.
  - `Product`: Classe que representa o produto e suas informações.
- `main.py`: Script principal que executa toda a automação.

## Dependências
- `firebase-admin`: Interação com o Firebase.
- `pytz`: Manipulação de fuso horário.
- `requests`: Requisições HTTP.
- `tweepy`: Interação com a API do Twitter.
- `python-dotenv`: Carregamento de variáveis de ambiente de um arquivo `.env`.
- `twilio`: Envio de SMS via Twilio.
- `langchain_core` e `langchain_groq`: Integração com o Groq Cloud.

## Licença
Este projeto é licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contribuição
1. Faça um fork do projeto.
2. Crie um novo branch (`git checkout -b feature/novo-recurso`).
3. Commit suas alterações (`git commit -am 'Adiciona novo recurso'`).
4. Push para o branch (`git push origin feature/novo-recurso`).
5. Crie um novo Pull Request.

Para dúvidas ou problemas, abra uma issue neste repositório.

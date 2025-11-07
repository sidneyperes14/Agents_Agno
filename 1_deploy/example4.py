# 1 - IMPORTS==========================================                                                                                  # Seção de importações

import requests                                             # Biblioteca para realizar requisições HTTP (comunicação entre cliente e servidor)
import json                                                 # Biblioteca para conversão e manipulação de dados no formato JSON
import streamlit as st                                      # Framework que permite criar interfaces web interativas em Python

AGENT_ID = "pdf_agent"                                      # Identificador único do agente configurado no servidor AGNO
ENDPOINT = f"https://agentapi-0j4b.onrender.com/agents/{AGENT_ID}/runs"  # URL do endpoint responsável por gerenciar as execuções (runs) do agente

# 2 - REQUISICOES/CONEXÃO COM O AGNO FRAMEWORK (SERVER)============                                 # Função responsável pela comunicação com o servidor AGNO
def get_response(message: str):                             # Define a função que enviará a mensagem ao servidor e processará a resposta

    response = requests.post(                               # Envia uma requisição POST ao servidor para iniciar a execução do agente
        url=ENDPOINT,                                       # URL do endpoint definido anteriormente
        data={"message": message,                           # Dicionário com a mensagem que será enviada ao agente
              "stream": True},                              # Parâmetro para habilitar streaming (resposta em tempo real)
        stream=True                                         # Mantém a conexão aberta para processar dados de forma contínua
    )

# 2.1 STREAMING (PROCESSAMENTO)=======================                                             # Processamento das respostas transmitidas em tempo real
    for line in response.iter_lines():                      # Itera sobre cada linha recebida da conexão (stream de eventos)
        if line:                                            # Garante que a linha não esteja vazia
            # Parse Server-Sent Events
            if line.startswith(b"data: "):                  # Verifica se a linha começa com "data: ", indicando um evento válido
                data = line[6:]                             # Remove o prefixo "data: " para capturar somente o conteúdo JSON
                try:
                    event = json.loads(data)                # Converte a string JSON em um dicionário Python
                    yield event                             # Retorna o evento (permite enviar dados ao Streamlit de forma contínua)
                except json.JSONDecodeError:                # Caso o JSON esteja malformado ou incompleto
                    continue                                # Ignora a linha e continua o loop

# 3 - STREAMLIT INTERFACE============================                                           # Construção da interface do app no Streamlit

st.set_page_config(page_title="Agente de PDF com RAG")       # Define o título da página exibido no navegador
st.title("Agente de PDF com RAG")                            # Define o título principal exibido no corpo da interface

# 3.1 - STREAMLIT HISTORY============================                                           # Controle da memória de conversas no Streamlit
if "messages" not in st.session_state:                       # Verifica se ainda não há histórico salvo na sessão
    st.session_state.messages = []                           # Cria uma lista vazia para armazenar as mensagens (usuário e agente)

# 3.2 - SHOW STREAMLIT HISTORY=======================                                           # Exibe o histórico de conversas anteriores na interface
for msg in st.session_state.messages:                        # Itera sobre todas as mensagens armazenadas na sessão
    with st.chat_message(msg["role"]):                       # Cria um balão de mensagem de acordo com o papel (user/assistant)
        if msg["role"] == "assistant" and msg.get("process"): # Se for uma mensagem do assistente com dados de processo
            with st.expander(label="Process", expanded=False):# Cria um painel expansível para exibir detalhes técnicos
                st.json(msg["process"])                       # Exibe o conteúdo do processo em formato JSON
        st.markdown(msg["content"])                           # Exibe o texto da mensagem na tela

# 3.3 - USER INPUT===================================                                           # Campo de entrada para o usuário enviar novas perguntas
if prompt := st.chat_input("Digite sua pergunta aqui..."):    # Cria o campo de input tipo chat (mensagem única por envio)
    # Adiciona a mensagem do usuário à memória do Streamlit
    st.session_state.messages.append({"role": "user", "content": prompt})  # Armazena a mensagem do usuário no histórico
    with st.chat_message("user"):                             # Exibe a mensagem enviada pelo usuário na interface
        st.markdown(prompt)                                   # Mostra o conteúdo digitado

    # Resposta do agente
    with st.chat_message("assistant"):                        # Cria o balão de resposta do assistente
        response_placeholder = st.empty()                     # Cria um espaço vazio que será atualizado em tempo real
        full_response = ""                                    # Inicializa a variável para armazenar a resposta completa do agente

# 4 - PRINT STREAMING RESPONSE========================                                          # Lógica para processar e exibir a resposta transmitida pelo agente
    for event in get_response(prompt):                        # Itera sobre cada evento recebido do servidor AGNO
        event_type = event.get("event", "")                   # Obtém o tipo do evento (ex: RunContent, ToolCallStarted etc.)

        # Tool Call Started
        if event_type == "ToolCallStarted":                   # Caso o agente tenha iniciado a execução de uma ferramenta
            tool_name = event.get("tool", {}).get("tool_name")# Extrai o nome da ferramenta sendo chamada
            with st.status(f"Executando ferramenta: {tool_name}", expanded=True):  # Exibe status de execução na interface
                st.json(event.get("tool", {}).get("tool_args", {}))                # Mostra os argumentos passados à ferramenta

        # Conteúdo da resposta
        elif event_type == "RunContent":                      # Evento contendo o texto parcial da resposta do agente
            content = event.get("content", "")                # Extrai o conteúdo textual recebido
            if content:                                       # Se houver conteúdo válido
                full_response += content                      # Adiciona o trecho ao texto acumulado
                response_placeholder.markdown(full_response + "▌")  # Atualiza o campo de resposta em tempo real com um cursor piscante

    response_placeholder.markdown(full_response)              # Substitui o cursor pela resposta final completa

    # Salvar a resposta do agente na memória do Streamlit
    st.session_state.messages.append(                         # Armazena a resposta no histórico da sessão
        {"role": "assistant",                                 # Define o papel como "assistente"
         "content": full_response,                            # Guarda o conteúdo textual da resposta
         })
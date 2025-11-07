# 1 - IMPORTS==========================================                                                                                 # Seção de importação de bibliotecas

import requests                                             # Biblioteca usada para fazer requisições HTTP (enviar e receber dados de servidores)
import json                                                 # Biblioteca para manipulação de dados em formato JSON (conversão entre dict e JSON)

AGENT_ID = "pdf_agent"                                      # Identificador do agente configurado no servidor local (nome ou ID único)
ENDPOINT = f"http://localhost:7777/agents/{AGENT_ID}/runs"  # URL do endpoint do servidor AGNO responsável por processar as requisições do agente

# 2 - CONEXÃO COM O AGNO FRAMEWORK (SERVER)============                                      # Início da função que faz a comunicação com o servidor do AGNO
def get_response(message: str):                             # Define a função que recebe uma string 'message' e retorna respostas do servidor em tempo real

    response = requests.post(                               # Envia uma requisição POST para o servidor do AGNO
        url=ENDPOINT,                                       # Define o endereço do endpoint para o qual a requisição será enviada
        data={"message": message,                           # Envia a mensagem digitada pelo usuário como dado principal da requisição
              "stream": True},                              # Ativa o modo de transmissão contínua (streaming) para receber eventos em tempo real
        stream=True                                         # Mantém a conexão aberta para processar dados recebidos em partes
    )

    for line in response.iter_lines():                      # Itera linha por linha das respostas transmitidas pelo servidor
        if line:                                            # Verifica se a linha não está vazia
            # Parse Server-Sent Events
            if line.startswith(b"data: "):                  # Verifica se a linha recebida começa com o prefixo "data: ", padrão SSE
                data = line[6:]                             # Remove o prefixo "data: " para obter somente o conteúdo útil
                try:
                    event = json.loads(data)                # Converte a string JSON recebida em um dicionário Python
                    yield event                             # Retorna o evento como dicionário (permite processar em tempo real)
                except json.JSONDecodeError:                # Caso a conversão falhe (JSON inválido)
                    continue                                # Ignora a linha e continua o loop sem interromper a execução

# 3 - PRINTA A RESPOSTA================================                                   # Funções e estrutura para exibir as respostas do agente

"""
RunStarted
ToolCallStarted
ToolCallCompleted
RunContent
RunContentCompleted
MemoryUpdateStarted
RunCompleted
"""                                                      # Comentário explicando os tipos de eventos possíveis retornados pelo servidor

def print_streaming_response(message: str):                 # Função para processar e imprimir as respostas recebidas em streaming
    for event in get_response(message):                     # Itera sobre cada evento retornado pela função get_response
        event_type = event.get("event", "")                 # Obtém o tipo de evento (ex: RunStarted, RunContent, etc.)

        # Início da execução
        if event_type == "RunStarted":                      # Caso o evento indique o início da execução do agente
            print("Iniciando a execução do agente...")      # Exibe uma mensagem de início de execução

        # Conteúdo da resposta
        elif event_type == "RunContent":                    # Evento que contém parte do conteúdo textual da resposta do agente
            content = event.get("content", "")              # Extrai o texto da resposta
            if content:                                     # Se houver conteúdo
                print(content, end="", flush=True)          # Imprime o texto sem quebrar linha, exibindo em tempo real

        # Tool Call Started
        elif event_type == "ToolCallStarted":               # Evento indicando que o agente iniciou o uso de uma ferramenta externa
            tool = event.get("tool", {})                    # Obtém o dicionário com informações da ferramenta
            tool_name = tool.get("tool_name", "desconhecida")  # Extrai o nome da ferramenta ou define "desconhecida" se não existir
            tool_args = tool.get("tool_args", {})           # Extrai os argumentos usados na chamada da ferramenta
            print(f"Iniciando chamada da ferramenta: {tool_name}")  # Mostra qual ferramenta está sendo chamada
            print(f"Argumentos: {json.dumps(tool_args, indent=2)}") # Exibe os argumentos formatados de forma legível (JSON identado)
            print("-"*50)                                   # Linha divisória para clareza visual

        elif event_type == "ToolCallCompleted":             # Evento indicando que a execução da ferramenta foi concluída
            tool_name = event.get("tool", {}).get("tool_name")  # Obtém o nome da ferramenta concluída
            print(f"Tool Concluída: {tool_name}")           # Exibe mensagem de conclusão
            print("-"*50)                                   # Linha divisória

        elif event_type == "RunCompleted":                  # Evento indicando que o processo do agente terminou
            print("Execução do agente concluída.")          # Mensagem de término
            metrics = event.get("metrics", {})              # Obtém métricas de execução (tempo, tokens, etc.)
            if metrics:                                     # Se existirem métricas
                print(f"Métricas da execução: {json.dumps(metrics, indent=2)}")  # Exibe-as formatadas
            print("-"*50)                                   # Linha divisória final

# 4 - RUN (Loop)=======================================                                      # Ponto de entrada principal do script
if __name__ == "__main__":                                 # Verifica se o script está sendo executado diretamente (não importado como módulo)
        message = input("Digite sua pergunta: ")            # Solicita a primeira mensagem do usuário
        print_streaming_response(message)                   # Envia a mensagem ao servidor e imprime as respostas em tempo real

        while True:                                         # Mantém o programa rodando em loop para novas interações
            message = input("Digite sua pergunta: ")        # Solicita nova entrada do usuário
            print_streaming_response(message)               # Envia a nova mensagem e imprime o retorno do agente

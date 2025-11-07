# ============================ IMPORTAÇÕES =============================
from fastapi import FastAPI
import uvicorn
import asyncio
from dotenv import load_dotenv

# Importações do Agno Framework
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.chroma import ChromaDb

# ============================ CONFIGURAÇÕES INICIAIS =====================
# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# ============================ RAG TECHNIQUE ==============================
# Cria um banco vetorial para armazenar embeddings (representações vetoriais de textos).
# O parâmetro `persistent_client=True` garante que os dados sejam salvos em disco.
vector_db = ChromaDb(
    collection="pdf_agent", 
    path="tmp/chromadb", 
    persistent_client=True
)

# Cria um gerenciador de conhecimento que usa o banco vetorial
knowledge = Knowledge(vector_db=vector_db)

# ============================ BANCO DE DADOS LOCAL =======================
# Banco SQLite para armazenar o histórico e sessões do agente.
db = SqliteDb(
    session_table="agent_session",
    db_file="tmp/agent.db",
)

# ============================ AGENTE DE IA ===============================
# Configuração do agente principal com memória, contexto e integração com o modelo da OpenAI.
agent = Agent(
    name="Agente de PDF",
    model=OpenAIChat(id="gpt-5-nano"),      # Modelo de linguagem (substitua por gpt-4.1-mini ou outro se preferir)
    db=db,                                  # Banco de sessões em SQLite
    knowledge=knowledge,                    # Fonte de conhecimento com RAG
    add_history_to_context=True,            # Mantém o contexto entre interações
    search_knowledge=True,                  # Habilita busca no banco vetorial
    num_history_runs=3,                     # Quantas interações anteriores são mantidas
    debug_mode=True                         # Log detalhado no terminal (útil em desenvolvimento)
)

# ============================ APLICAÇÃO FASTAPI ==========================
app = FastAPI(
    title="Agente de PDF com RAG",
    description="Um agente de IA que consulta relatórios trimestrais em PDF usando a técnica RAG.",
    version="1.0.0"
)

# Endpoint principal: recebe uma pergunta e retorna a resposta do agente
@app.post("/agent_pdf")
async def agent_pdf(pergunta: str):
    """
    Endpoint que processa perguntas enviadas ao agente.
    Exemplo de uso com JSON:
    {
        "pergunta": "Qual foi o lucro líquido da Grendene no 2T25?"
    }
    """
    resposta = await asyncio.to_thread(agent.run, pergunta)  # Executa o agente em thread separada (evita travar o loop principal)
    message = resposta.messages[-1]
    return {"resposta": message.content}

# ============================ EXECUÇÃO LOCAL =============================
if __name__ == "__main__":
    # Adiciona o conteúdo do PDF ao conhecimento do agente antes de iniciar o servidor
    asyncio.run(
        knowledge.add_content_async(
            url="https://s3.sa-east-1.amazonaws.com/static.grendene.aatb.com.br/releases/2417_2T25.pdf",
            metadata={"source": "Grendene", "type": "relatorio trimestral 2T25"},
            skip_if_exists=True,
            reader=PDFReader(),
        )
    )

    # Executa o servidor FastAPI usando Uvicorn
    uvicorn.run(
        "exemple1:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

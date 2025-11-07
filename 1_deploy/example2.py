from agno.agent import Agent
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat

load_dotenv()

from agno.knowledge.knowledge import Knowledge                          # Importantes para processar um grupo de PDF's e disponibilizar isso como uma ferramenta para o modelo de IA consultar quando for preciso.
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.chroma import ChromaDb                               # Database para guardar informações e conhecimentos.
from agno.os import AgentOS

# ============================ RAG TECHNIQUE =====================
vector_db = ChromaDb(collection='pdf_agent', path='tmp/chromadb', persistent_client=True)              # Como ele será armazenado na nossa pasta tmp, o nome da tabela será 'pdf_agent' e o arquivo será o chromadb. As informações serao disponibilizadas em vetores.
knowledge = Knowledge(vector_db= vector_db)



# ============================ BANCO DE DADOS =====================
db = SqliteDb(                                            # Cria o banco SQLite local para armazenar sessões e histórico de interações do agente.
    session_table = "agent_session",    
    db_file    = "tmp/agent.db",
)

# ============================ AGENTE =============================
agent = Agent(                                                  # Instancia o agente de IA com as configurações desejadas.
    id                       = "pdf_agent",
    name                     = "Agente de PDF",                 # Nome do agente.
    model                    = OpenAIChat(id = 'gpt-5-nano'), # Modelo de linguagem utilizado (GPT-4.1-mini).
    db                       = db,                              # Define o armazenamento local em SQLite.
    knowledge                = knowledge,
    enable_user_memories     = True,
    instructions             = "Você é um agente especializado em responder perguntas com base em relatórios em PDF. Utilize o conhecimento disponível para fornecer respostas precisas e relevantes, chamando o usuário sempre de senhor Sidney.",
    add_history_to_context   = True,                            # Inclui o histórico das interações nas próximas mensagens, mantendo o contexto.
    search_knowledge         = True,
    num_history_runs         = 3,                               # Quantas interações anteriores o agente mantém em memória.
    debug_mode               = True                             # Ativa o modo de depuração para logs detalhados no terminal.
)

# ============================ AGENTOS =====================
agent_os = AgentOS(
    name="PDF Agent OS",
    agents = [agent]
)

app = agent_os.get_app()

# ============================= RUN ========================

if __name__ == "__main__":
    knowledge.add_content(url="https://s3.sa-east-1.amazonaws.com/static.grendene.aatb.com.br/releases/2417_2T25.pdf",     # Adiciona o conteúdo do PDF ao conhecimento do agente, utilizando o leitor de PDF.
                      metadata={"source": "Grendene", "type": "relatorio trimestral 2T25"},
                      skip_if_exists=True,
                      reader=PDFReader()
                     )
    agent_os.serve(app="example2:app", reload=True)
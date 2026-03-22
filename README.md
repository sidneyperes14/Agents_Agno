# 🤖 Agentes de IA com Agno - Módulo 3

Repositório educacional dedicado ao aprendizado e implementação de **Agentes de Inteligência Artificial** utilizando o **framework Agno**. Este módulo explora técnicas avançadas de RAG (Retrieval-Augmented Generation), integração com modelos de IA e desenvolvimento de APIs.

---

## 📋 Conteúdo do Projeto

### 📚 Estrutura

```
modulo-3/
├── 0_intro/              # Exemplos introdutórios
│   ├── Exemple1.py      # FastAPI básico
│   └── Exemple2.py      # Implementações iniciais
├── 1_deploy/            # Exemplos avançados e pronto para produção
│   ├── example1.py      # Agente PDF com RAG
│   ├── example2.py      # AgentOS com integração completa
│   ├── example3.py      # Cliente HTTP para consumir o agente
│   └── example4.py      # Exemplos adicionais
├── streamlit/           # Aplicações Streamlit (interface web)
├── tmp/                 # Dados persistentes (ChromaDB, SQLite)
├── main.py              # Ponto de entrada principal
├── pyproject.toml       # Configurações do projeto
└── README.md            # Este arquivo
```

---

## 🎯 Objetivos de Aprendizado

1. ✅ **Framework Agno**: Entender e utilizar o framework para criar agentes inteligentes
2. ✅ **RAG (Retrieval-Augmented Generation)**: Implementar busca vetorial em PDFs e documentos
3. ✅ **ChromaDB**: Armazenar e recuperar embeddings vetoriais
4. ✅ **APIs com FastAPI**: Criar endpoints para comunicação com agentes
5. ✅ **Streaming em Tempo Real**: Implementar respostas usando Server-Sent Events (SSE)
6. ✅ **Memória de Agentes**: Persistir sessões e histórico com SQLite

---

## 🚀 Funcionalidades Principais

### 1. **Agente de PDF com RAG**
- Carrega e processa arquivos PDF
- Armazena embeddings em ChromaDb (vetorização de conteúdo)
- Responde perguntas com base no conhecimento do PDF
- Mantém histórico de conversas

```python
# Exemplo de uso
knowledge.add_content(
    url="seu-pdf.pdf",
    metadata={"source": "Relatório", "type": "documento"},
    reader=PDFReader()
)
```

### 2. **API FastAPI com Agento**
- Endpoints para comunicação com o agente
- Suporte a streaming de respostas em tempo real
- Integração com múltiplos agentes (AgentOS)

### 3. **Cliente HTTP com Streaming**
- Consome a API do agente
- Processa eventos Server-Sent Events (SSE)
- Exibe respostas em tempo real no terminal
- Monitora métricas de execução

### 4. **Banco de Dados Local**
- **SQLite**: Armazena sessões, histórico e memória do agente
- **ChromaDB**: Banco vetorial para recuperação de conhecimento

---

## 📦 Dependências

O projeto utiliza as seguintes bibliotecas principais:

```
agno>=2.2.3              # Framework para agentes de IA
chromadb>=1.3.0          # Banco vetorial
fastapi>=0.120.1         # Framework web
openai>=2.6.1            # Integração com modelos OpenAI
pypdf>=6.1.3             # Processamento de PDFs
sqlalchemy>=2.0.44       # ORM para banco de dados
streamlit>=1.51.0        # Interface web interativa
uvicorn>=0.38.0          # Servidor ASGI
watchdog>=6.0.0          # Monitoramento de arquivos
```

---

## ⚙️ Instalação

### 1. **Pré-requisitos**
- Python ≥ 3.12
- UV (gerenciador de pacotes)
- Chave de API OpenAI

### 2. **Clonar e Configurar**

```bash
# Clone o repositório
git clone <repo-url>
cd modulo-3

# Crie um arquivo .env na raiz do projeto
echo "OPENAI_API_KEY=sua-chave-aqui" > .env
```

### 3. **Instalar Dependências**

```bash
# Usando UV
uv sync

# Ou ativar virtual environment
./.venv/Scripts/Activate.ps1  # Windows
source ./.venv/bin/activate     # Linux/Mac

pip install -e .
```

---

## 🔧 Como Usar

### Exemplo 1: Agente PDF Básico
```bash
python 1_deploy/example1.py
```
Inicia um agente que pode responder perguntas sobre um PDF específico.

### Exemplo 2: AgentOS com Interface Web
```bash
python 1_deploy/example2.py
```
Serve o agente em `http://localhost:10000` com interface interativa.

### Exemplo 3: Cliente de Streaming
```bash
python 1_deploy/example3.py
```
Conecta-se a um agente em execução e envia perguntas em streaming.

### Usar Streamlit (Interface Web)
```bash
streamlit run streamlit/app.py
```

---

## 📝 Estrutura de um Agente

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb

# 1. Banco Vetorial (RAG)
vector_db = ChromaDb(
    collection='pdf_agent',
    path='tmp/chromadb',
    persistent_client=True
)

# 2. Conhecimento
knowledge = Knowledge(vector_db=vector_db)

# 3. Banco de Dados Local
db = SqliteDb(
    session_table="agent_session",
    db_file="tmp/agent.db",
)

# 4. Agente
agent = Agent(
    name="Agente PDF",
    model=OpenAIChat(id="gpt-4-turbo"),
    db=db,
    knowledge=knowledge,
    instructions="Você é um especialista em responder perguntas com base em PDFs.",
    add_history_to_context=True,
    search_knowledge=True,
    debug_mode=True
)
```

---

## 🔍 Conceitos-Chave

### RAG (Retrieval-Augmented Generation)
Esta técnica combina busca por relevância com geração de texto:
1. **Retrieval**: Busca trechos relevantes do conhecimento (PDF, documentos)
2. **Augmentation**: Adiciona os trechos ao contexto da pergunta
3. **Generation**: O modelo gera resposta usando o contexto aumentado

### Server-Sent Events (SSE)
Padrão para enviar atualizações de servidor para cliente em tempo real:
```python
# Resposta em tempo real
response = requests.post(endpoint, stream=True)
for line in response.iter_lines():
    if line.startswith(b"data: "):
        event = json.loads(line[6:])
        print(event)  # Processa em tempo real
```

---

## 📊 Estrutura de Dados

### ChromaDB (Vetores)
Armazena embeddings de PDF em `tmp/chromadb/`
```
tmp/chromadb/
├── chroma.sqlite3
└── <collection-id>/
```

### SQLite (Sessões)
Armazena histórico em `tmp/agent.db`
```sql
agent_session table
├── session_id
├── message_history
└── state
```

---

## 🛠️ Troubleshooting

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError: agno` | Rode `uv sync` ou instale com `pip install -e .` |
| `OPENAI_API_KEY not found` | Crie arquivo `.env` com sua chave |
| `ChromaDB connection error` | Verifique permissões na pasta `tmp/` |
| `Port already in use` | Mude a porta no código: `port=OUTRA_PORTA` |

---

## 📚 Recursos Adicionais

- [Documentação Agno](https://docs.agno.ai)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)

---

## 👤 Autor

**Sidney Peres**
- Email: sidneyperes98@outlook.com
- Curso: Criando Agentes de IA com Agno - Asimov

---

## 📄 Licença

Este projeto é fornecido para fins educacionais.

---

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Sinta-se à vontade para:
- Abrir issues
- Propor melhorias
- Compartilhar exemplos

---

**Última atualização**: Março de 2026

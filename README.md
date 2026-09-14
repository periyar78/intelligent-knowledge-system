# Agentic University Knowledge System

An AI agent that autonomously decides whether to query **MySQL** (structured
data), **ChromaDB** (semantic search over policy documents), or **Neo4j**
(relationship graph) — or combine several — to answer a question.

## 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configure environment

```bash
cp .env.example .env
# then edit .env with your real MySQL password, Neo4j password, and OpenAI API key
```

## 3. Set up MySQL

Make sure MySQL is running, then:

```bash
mysql -u root -p < mysql_db/setup.sql
```

This creates the `university` database with **15 students**, 4 departments,
5 faculty, 7 courses, and enrollment records. Test it:

```bash
python mysql_db/connection.py
```

## 4. Set up ChromaDB (vector database)

No server needed — it's file-based. Just run the ingestion script:

```bash
python vector/ingest.py
```

This reads the 5 `.txt` policy documents in `/documents`, chunks them,
embeds them, and stores them in `./chroma_data`. Test it:

```bash
python vector/search.py
```

## 5. Set up Neo4j

Start Neo4j (Desktop app, or Docker):

```bash
docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/your_password neo4j
```

Then populate the graph with the same students/courses/faculty:

```bash
python graph/setup_graph.py
```

Test it:

```bash
python graph/connection.py
```

## 6. Test the agent directly (no UI)

```bash
python agent/agent.py
```

This runs 4 sample questions through the agent and prints which tool(s)
it chose and the final answer — good for your viva/demo prep.

## 7. Run the full app

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually http://localhost:8501).

## Demo questions to show during your presentation

| Type | Question |
|---|---|
| MySQL only | What is Arun's GPA? |
| MySQL only | How many students are in the CSE department? |
| Vector only | What is the minimum attendance required for exams? |
| Vector only | What happens if I return a library book late? |
| Graph only | Who teaches Machine Learning? |
| Graph only | Which faculty specialize in Artificial Intelligence? |
| MySQL + Graph | Which CSE students with GPA above 8 are enrolled in courses taught by AI-specialized faculty? |
| Vector + MySQL | Explain the attendance policy, and tell me which students currently have a GPA below 7 who might be at risk. |

## Project structure

```
intelligent_knowledge_system/
├── app.py                  # Streamlit UI
├── .env.example
├── requirements.txt
├── agent/
│   ├── agent.py             # LangGraph ReAct agent (the "brain")
│   ├── tools.py             # LangChain tool wrappers for MySQL/Chroma/Neo4j
│   └── prompts.py           # System prompt guiding tool selection
├── mysql_db/
│   ├── setup.sql            # 15 students, courses, faculty, enrollments
│   ├── connection.py
│   └── queries.py
├── vector/
│   ├── ingest.py            # Chunk + embed + store documents
│   └── search.py            # Semantic search
├── graph/
│   ├── setup_graph.py       # Populate Neo4j with matching graph data
│   ├── connection.py
│   └── queries.py
└── documents/                # 5 sample policy .txt files
```

## Notes for your viva

- The **agentic** part is in `agent/agent.py` — `create_react_agent` lets the
  LLM read each tool's docstring and autonomously decide which to call,
  observe the result, and decide if it needs another tool — this is NOT
  hardcoded `if/elif` keyword matching.
- All SQL/Cypher tools are restricted to read-only queries as a safety
  measure (see `tools.py`), which is worth mentioning if asked about
  security in your project.
- To swap the LLM provider (e.g. away from OpenAI), you only need to change
  `agent/agent.py` — everything else stays the same.

from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from agent.tools import ALL_TOOLS


# ============================================================
# LOCAL AI MODEL
# ============================================================

model = ChatOllama(
    model="qwen3:4b",
    temperature=0
)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are UniMind, an intelligent university knowledge assistant.

Your job is to answer university questions using the available
database tools.

IMPORTANT TOOL RULES:

1. MySQL tools
Use MySQL tools for structured information:
- student GPA
- student records
- department counts
- structured student information

2. ChromaDB
Use semantic_policy_search for:
- attendance policies
- examination rules
- library rules
- hostel rules
- academic regulations
- other university documents

3. Neo4j
Use Neo4j tools for:
- who teaches a course
- faculty specializations
- student-course relationships
- relationship-based questions

4. HYBRID QUESTIONS
A question can require more than one tool.

For example:

"Which CSE students with GPA above 8 are
enrolled in courses taught by AI-specialized faculty?"

For this type of question:
- Use MySQL to identify the CSE students and GPA.
- Use Neo4j to identify students in courses taught
  by AI-specialized faculty.
- Combine the results.
- Only return students satisfying BOTH conditions.

Do not invent information.

Always use the database tools when factual university
information is requested.

After retrieving data, provide a concise and clear answer.

If no matching information is found, say so clearly.

Do not expose internal tool names or technical reasoning
unless the user asks for it.
"""


# ============================================================
# CREATE AGENT
# ============================================================

agent = create_agent(
    model=model,
    tools=ALL_TOOLS,
    system_prompt=SYSTEM_PROMPT
)


# ============================================================
# COMMAND LINE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 55)
    print("        UNIMIND AI UNIVERSITY ASSISTANT")
    print("=" * 55)

    print("Local Model: Qwen3 4B")
    print("Knowledge Sources: MySQL + ChromaDB + Neo4j")

    while True:

        question = input(
            "\nYou: "
        ).strip()

        if question.lower() in {
            "exit",
            "quit",
            "bye"
        }:
            print("Goodbye bro! 👋")
            break

        if not question:
            continue

        try:

            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                }
            )

            print("\nUniMind:")

            print(
                result["messages"][-1].content
            )

        except Exception as e:

            print("\nError:")
            print(e)
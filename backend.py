from flask import Flask, request, jsonify
from flask_cors import CORS

from agent.agent import agent


# ============================================================
# CREATE FLASK APP
# ============================================================

app = Flask(__name__)

# Allow the HTML frontend to communicate with Python backend
CORS(app)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "UniMind backend is running"
    })


# ============================================================
# ASK AI ENDPOINT
# ============================================================

@app.route("/api/ask", methods=["POST"])
def ask_ai():

    try:

        # --------------------------------------------
        # Read JSON sent by frontend
        # --------------------------------------------

        data = request.get_json(silent=True) or {}

        question = data.get("question", "").strip()

        if not question:

            return jsonify({
                "error": "Please enter a question."
            }), 400


        # --------------------------------------------
        # Send question to Agentic AI
        # --------------------------------------------

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


        # --------------------------------------------
        # Get final answer
        # --------------------------------------------

        answer = result["messages"][-1].content


        # --------------------------------------------
        # Find tools used by the agent
        # --------------------------------------------

        tool_names = []

        for message in result["messages"]:

            # AI tool calls
            calls = getattr(
                message,
                "tool_calls",
                []
            )

            for call in calls:

                name = call.get("name")

                if name and name not in tool_names:

                    tool_names.append(name)


            # Tool message
            name = getattr(
                message,
                "name",
                None
            )

            if name and name not in tool_names:

                tool_names.append(name)


        # --------------------------------------------
        # Convert internal tool names into UI names
        # --------------------------------------------

        source_map = {

            # MySQL
            "get_student_gpa": "MySQL",
            "count_students_by_department": "MySQL",
            "get_students_by_gpa": "MySQL",
            "get_all_students": "MySQL",

            # ChromaDB
            "semantic_policy_search": "ChromaDB",

            # Neo4j
            "find_course_teacher": "Neo4j",
            "find_ai_specialized_faculty": "Neo4j",
            "find_students_in_ai_faculty_courses": "Neo4j",
            "find_students_in_course": "Neo4j"
        }


        sources = []

        for tool_name in tool_names:

            display_name = source_map.get(
                tool_name,
                tool_name
            )

            if display_name not in sources:

                sources.append(display_name)


        # --------------------------------------------
        # Send response to frontend
        # --------------------------------------------

        return jsonify({

            "answer": answer,

            "sources": sources,

            "chart": None

        })


    except Exception as e:

        print("Backend error:", e)

        return jsonify({

            "error": str(e)

        }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("         UNIMIND AI BACKEND")
    print("=" * 60)

    print("Agent: Qwen3 4B + Ollama")
    print("MySQL: Connected through agent tools")
    print("ChromaDB: Connected through agent tools")
    print("Neo4j: Connected through agent tools")

    print()
    print("Backend URL:")
    print("http://localhost:5000")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
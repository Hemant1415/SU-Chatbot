from flask import Flask, render_template, request, session
from sentence_transformers import SentenceTransformer
import psycopg2
import random
from together import Together
client = Together(api_key="")

# Generating 
random_integer = random.randint(10**11, 10**12 - 1)

app = Flask(__name__)
model = SentenceTransformer('all-MiniLM-L6-v2')


app.secret_key = str(random_integer) 


DB_NAME = "suchatbot"
DB_USER = "postgres"
DB_PASSWORD = "Hemant1415"
DB_HOST = "localhost"
DB_PORT = "5432"


@app.route("/", methods=["GET", "POST"])
def chatbot():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        query = request.form.get("query")
        try:
            connection = psycopg2.connect(
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            cursor = connection.cursor()
            emquery = model.encode(query).tolist()

            cursor.execute(
                """
                SELECT question, answer
                FROM embeddings
                ORDER BY questionemb <=> %s::vector
                LIMIT 5;
                """,
                (emquery,)
            )
            result = cursor.fetchall()

            if result:
                top_result = result[0]
                remaining = result[1:]
                question, answer = top_result[0],top_result[1]
                stream = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                messages=[{"role": "user", "content": f"{answer}. Please rephrase this text. Provide medium length text"}],
                stream=True,
                )
                answer=""
                for chunk in stream:
                    answer+=chunk.choices[0].delta.content
                qE = model.encode(question)
                similarity = model.similarity(emquery, qE)

                if similarity.item() < 0.5:
                    response = "No relevant answer found in the database."
                else:
                    response = answer
            else:
                response = "No match found in the database."
        except Exception as e:
            response = f"An error occurred: {e}"
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'connection' in locals() and connection is not None:
                connection.close()

    
        session["chat_history"].append({"query": query, "response": response})
        session["remaining"] = remaining 
        session.modified = True

    return render_template("index.html", chat_history=session.get("chat_history", []), remaining=session.get("remaining", []))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submitf', methods=['POST'])
def submit_feedback():
    query = request.form.get('query') 
    response=request.form.get('response')
    return render_template("feedback.html",query=query,response=response)


if __name__ == "__main__":
    app.run(debug=True)

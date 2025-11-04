import os
import time
import psycopg2

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )


def init_db():
    """Cria tabela products e insere dados iniciais"""
    for i in range(10):  # tenta conectar até 10 vezes
        try:
            conn = get_connection()
            break
        except psycopg2.OperationalError:
            print("Banco ainda não está pronto, tentando novamente...")
            time.sleep(2)
    else:
        raise Exception("Não foi possível conectar ao banco")

    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL
        )
    """)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM products")
    count = cur.fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO products (name, price) VALUES (%s, %s)",
            [
                ("Notebook", 3500.00),
                ("Mouse", 80.00),
                ("Teclado Mecânico", 250.00),
            ],
        )
        conn.commit()

    cur.close()
    conn.close()

def render_products():
    """Retorna HTML com lista de produtos"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, price FROM products")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        items = "".join([f"<li>{n} — R$ {p:.2f}</li>" for n, p in rows])
        html = f"""
        <html>
            <head>
                <meta charset="utf-8">
                <title>Produtos</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <body>
                <h1>Lista de Produtos</h1>
                <ul>{items}</ul>
            </body>
        </html>
        """
        return html.encode("utf-8")
    except Exception as e:
        return f"<h1>Erro ao acessar o banco: {e}</h1>".encode("utf-8")

def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")

    if path == "/":
        response_body = render_products()
        status = "200 OK"
        headers = [("Content-Type", "text/html; charset=utf-8")]

    elif path.startswith("/static/"):
        file_path = os.path.join(os.path.dirname(__file__), path.lstrip("/"))
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                response_body = f.read()
            if file_path.endswith(".css"):
                content_type = "text/css"
            else:
                content_type = "application/octet-stream"
            headers = [("Content-Type", content_type)]
            status = "200 OK"
        else:
            response_body = b"Not Found"
            status = "404 Not Found"
            headers = [("Content-Type", "text/plain")]

    else:
        response_body = b"<h1>404 Not Found</h1>"
        status = "404 Not Found"
        headers = [("Content-Type", "text/html; charset=utf-8")]

    start_response(status, headers)
    return [response_body]


# Inicializa o banco de dados ao subir o container
if __name__ == "__main__":
    init_db()
    from wsgiref.simple_server import make_server
    with make_server("", 8000, application) as httpd:
        print("Servidor rodando na porta 8000...")
        httpd.serve_forever()
else:
    # Quando o Gunicorn carregar, inicializa o banco também
    init_db()
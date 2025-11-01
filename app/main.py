import os

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')

    # Serve arquivos estáticos
    if path.startswith("/static/"):
        file_path = os.path.join(os.path.dirname(__file__), path.lstrip("/"))
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                response_body = f.read()
            # Define Content-Type para CSS ou outros tipos simples
            if file_path.endswith(".css"):
                content_type = "text/css; charset=utf-8"
            elif file_path.endswith(".js"):
                content_type = "application/javascript"
            else:
                content_type = "text/plain"
            status = "200 OK"
            headers = [("Content-Type", content_type)]
        else:
            response_body = b"404 Not Found"
            status = "404 Not Found"
            headers = [("Content-Type", "text/plain")]
        start_response(status, headers)
        return [response_body]

    # Página inicial
    if path == '/':
        response_body = """
        <html>
        <head>
            <title>Landpage Python Puro</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <h1>Página Inicial</h1>
            <p>App Python puro com WSGI e CSS!</p>
        </body>
        </html>
        """
        response_body = response_body.encode("utf-8")  # importante: WSGI espera bytes
        status = "200 OK"
    else:
        response_body = b"<h1>404 Not Found</h1>"
        status = "404 Not Found"

    headers = [("Content-Type", "text/html; charset=utf-8")]
    start_response(status, headers)
    return [response_body]

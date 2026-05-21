"""
SERVIDOR LOCAL PARA TESTAR O SITE
=================================
Os navegadores não deixam o site abrir arquivos locais por segurança (CORS).
Por isso, pra testar o site no PC, a gente precisa de um servidor pequeno.

Como usar:
    python servidor.py

Depois abra no navegador: http://localhost:8080
"""

import http.server
import socketserver
import webbrowser
from pathlib import Path
import os

PORT = 8080
PASTA_RAIZ = Path(__file__).parent

# Vai pra pasta raiz do projeto (aresta-online/)
os.chdir(PASTA_RAIZ)

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Permite acesso aos JSONs
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def log_message(self, format, *args):
        # Log mais limpo
        if "favicon" not in args[0]:
            print(f"  → {args[0]}")


print("=" * 60)
print("🏨  ARESTA ONLINE — Servidor Local")
print("=" * 60)
print(f"📂 Pasta raiz: {PASTA_RAIZ}")
print(f"🌐 Endereço:   http://localhost:{PORT}/site/index.html")
print("=" * 60)
print("\nPressione Ctrl+C pra parar o servidor.\n")

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        # Abre o navegador automaticamente
        webbrowser.open(f"http://localhost:{PORT}/site/index.html")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\n✅ Servidor parado. Até logo!")
except OSError as e:
    if "Address already in use" in str(e) or "10048" in str(e):
        print(f"\n❌ Porta {PORT} já está em uso. Feche outros programas ou mude a porta no topo deste arquivo.")
    else:
        print(f"\n❌ Erro: {e}")

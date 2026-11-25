"""Aplicação didática local. Dados em memória, credenciais fictícias.
Não representa autenticação de produção. Execute python app.py.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import json, os, re, threading, time

BASE = Path(__file__).parent
CAP = threading.BoundedSemaphore(4)
LOCK = threading.Lock()
INSCRICOES = {}
NEXT_ID = 1
DATA_SIZE = int(os.environ.get('DATA_SIZE', '100'))
BOOKS = [{'id': i, 'titulo': f'Engenharia de Software {i}'} for i in range(1, DATA_SIZE+1)]
COURSES = [{'id': i, 'nome': n, 'vagas': 2} for i,n in enumerate(['Python', 'Java', 'Testes de Software'],1)]

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def send(self, code, data, kind='application/json; charset=utf-8'):
        raw = json.dumps(data,ensure_ascii=False).encode() if kind.startswith('application/json') else data
        self.send_response(code); self.send_header('Content-Type',kind)
        self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def body(self):
        return json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))) or b'{}')
    def do_GET(self):
        u=urlparse(self.path); q=parse_qs(u.query).get('q',[''])[0].casefold()
        if u.path in ('/api/livros','/api/cursos') or re.fullmatch(r'/api/cursos/[1-3]',u.path):
            if not CAP.acquire(timeout=0.10): return self.send(503,{'erro':'Capacidade didática ocupada'})
            try:
                # Latência e limite de concorrência artificiais para a demonstração.
                time.sleep(0.03)
                if u.path=='/api/livros':
                    items=[b for b in BOOKS if q in b['titulo'].casefold()]
                    return self.send(200,{'total':len(items),'itens':items[:20]})
                if u.path=='/api/cursos':
                    items=[c for c in COURSES if q in c['nome'].casefold()]
                    return self.send(200,{'total':len(items),'itens':items})
                return self.send(200,COURSES[int(u.path.rsplit('/',1)[1])-1])
            finally: CAP.release()
        if u.path=='/api/inscricoes':
            with LOCK: return self.send(200,{'itens':list(INSCRICOES.values())})
        routes={'/':'index.html','/login':'login.html','/painel':'painel.html','/inscricoes':'inscricoes.html'}
        if u.path in routes: return self.send(200,(BASE/'web'/routes[u.path]).read_bytes(),'text/html; charset=utf-8')
        self.send(404,{'erro':'Recurso inexistente'})
    def do_POST(self):
        global NEXT_ID
        path=urlparse(self.path).path
        try: data=self.body()
        except (ValueError,UnicodeDecodeError): return self.send(400,{'erro':'JSON inválido'})
        if path=='/api/login':
            if data.get('email')=='aluno@ads.local' and data.get('senha')=='Teste123!':
                return self.send(200,{'nome':'Aluno ADS'})
            return self.send(401,{'erro':'Credenciais inválidas'})
        if path=='/api/reset':
            with LOCK: INSCRICOES.clear(); NEXT_ID=1
            return self.send(200,{'mensagem':'Dados de inscrições restaurados'})
        if path=='/api/inscricoes':
            nome=str(data.get('nome','')).strip(); email=str(data.get('email','')).strip().casefold()
            curso=data.get('curso')
            if not 3<=len(nome)<=60: return self.send(422,{'erro':'Nome deve ter de 3 a 60 caracteres'})
            if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email): return self.send(422,{'erro':'E-mail inválido'})
            if type(curso) is not int or curso not in (1,2,3): return self.send(422,{'erro':'Curso obrigatório'})
            with LOCK:
                if any(x['email']==email and x['curso']==curso for x in INSCRICOES.values()):
                    return self.send(409,{'erro':'Inscrição já existente'})
                if sum(x['curso']==curso for x in INSCRICOES.values())>=2:
                    return self.send(409,{'erro':'Curso sem vagas'})
                item={'id':NEXT_ID,'nome':nome,'email':email,'curso':curso}
                INSCRICOES[NEXT_ID]=item; NEXT_ID+=1
                return self.send(201,item)
        self.send(404,{'erro':'Recurso inexistente'})
    def do_DELETE(self):
        try: key=int(urlparse(self.path).path.rsplit('/',1)[1])
        except ValueError: return self.send(404,{'erro':'Inscrição inexistente'})
        with LOCK:
            if not urlparse(self.path).path.startswith('/api/inscricoes/') or key not in INSCRICOES:
                return self.send(404,{'erro':'Inscrição inexistente'})
            del INSCRICOES[key]
        self.send(200,{'mensagem':'Inscrição cancelada'})

if __name__=='__main__':
    print('Aplicação local em http://127.0.0.1:8000', flush=True)
    ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()

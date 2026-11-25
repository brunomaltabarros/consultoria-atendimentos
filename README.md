Portal do Credenciamento
API REST para o cadastro de consultores, dos atendimentos que eles realizam e das suas especialidades, com um front-end em React que consome a API. O projeto foi inspirado no processo de credenciamento de consultores e desenvolvido como trabalho da disciplina, ao longo de três avaliações.

Funcionalidades
Cadastro, consulta, edição e remoção de consultores, atendimentos, especialidades e usuários
Relacionamento muitos-para-muitos entre consultores e especialidades
Autenticação com JWT: registro, login e rotas protegidas
Senhas armazenadas como hash bcrypt
Documentação interativa da API com Swagger
Versionamento do banco com migrations (Alembic)
Imagem Docker da API
Front-end em React com login e tela de consultores (GET, POST, PUT e DELETE)

app/
├── controllers/    rotas da API (5 controllers)
├── services/       regras de negócio
├── repositories/   acesso ao banco
├── models/         tabelas (SQLAlchemy)
├── dtos/           entrada e saída (Pydantic)
├── mappers/        conversão DTO ↔ model
├── exceptions/     exceções de domínio e handlers
├── security/       hash de senha, JWT e dependência de autenticação
├── database.py     conexão com o banco
└── main.py         criação da aplicação
alembic/            migrations do banco
frontend/           aplicação React


Como executar
Pré-requisitos
Python 3.12
Node.js 20 ou mais recente
Git
1. API
git clone https://github.com/brunomaltabarros/consultoria-atendimentos.git
cd consultoria-atendimentos

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python -m alembic upgrade head
python -m uvicorn app.main:app --reload
No Linux ou no macOS, o ambiente virtual é ativado com source .venv/bin/activate.

A API fica disponível em http://localhost:8000, e a documentação em http://localhost:8000/docs.

2. Front-end
Em outro terminal, com a API rodando:

cd frontend
npm ci
npm run dev
O front fica disponível em http://localhost:5173. O endereço da API está em frontend/.env (VITE_API_URL).

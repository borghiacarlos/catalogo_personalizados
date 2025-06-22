# Catálogo Personalizados

Este projeto é uma aplicação Django para gerenciamento de designs personalizados.

## Pré-requisitos

- Python 3.10+
- pip (gerenciador de pacotes Python)
- (Opcional) Ambiente virtual Python (recomendado)

## Passo a passo para instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/catalogo_personalizados.git
cd catalogo_personalizados
```

### 2. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente (opcional)

Crie um arquivo `.env` (ou exporte no terminal) para definir a `SECRET_KEY` se desejar.

### 5. Execute as migrações do banco de dados

```bash
python manage.py migrate
```

### 6. Crie um superusuário para acessar o admin

```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse [http://127.0.0.1:8000/](http://127.0.0.1:8000/) no navegador.

---

## Observações

- O projeto está configurado para usar SQLite por padrão.
- Para produção, ajuste as configurações de segurança e banco de dados em `config/settings.py`.
- Para servir arquivos de mídia em produção, utilize um servidor web como Nginx.

---

## Dependências principais

Veja o arquivo [`requirements.txt`](requirements.txt) para a lista completa.  
Principais pacotes utilizados:

- Django
- Whitenoise
- Pillow

Outros pacotes presentes podem ser removidos se não forem utilizados no seu projeto.  
Para manter apenas o essencial, revise e edite o `requirements.txt` conforme sua necessidade.
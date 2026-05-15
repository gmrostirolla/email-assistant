# 📬 Email Assistant

> Assistente inteligente de triagem de e-mails com LLM — classifica, resume e sugere respostas automaticamente.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?logo=streamlit)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?logo=openai)
![Gmail API](https://img.shields.io/badge/Gmail-API-EA4335?logo=gmail)

---

## 📸 Demo

<!-- Substitua pelo GIF gravado do seu app rodando -->
![demo](docs/demo.gif)

---

## ✨ Funcionalidades

- **Autenticação real com OAuth 2.0** — conecta à sua conta Gmail com segurança, sem armazenar senhas
- **Classificação automática** — cada e-mail recebe urgência (Alta / Média / Baixa) e categoria (Trabalho, Pessoal, Financeiro…)
- **Resumo em linguagem natural** — o modelo explica em uma frase o que cada e-mail trata
- **Rascunho de resposta** — gera uma sugestão de resposta adequada ao tom e urgência do e-mail
- **Resumo da caixa de entrada** — visão geral inteligente de tudo que chegou
- **Cache local** — e-mails já analisados não são reprocessados, economizando tokens
- **Interface web** — dashboard interativo com filtros por urgência e categoria

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.11 | Linguagem principal |
| Gmail API (Google) | Leitura de e-mails via OAuth 2.0 |
| OpenAI API (GPT-4o-mini) | Classificação e geração de texto |
| Streamlit | Interface web interativa |
| python-dotenv | Gerenciamento de variáveis de ambiente |

---

## 🏗️ Arquitetura

```
Gmail API
    │
    ▼
gmail_client.py      ← OAuth2, busca e parsing de e-mails
    │
    ▼
llm_processor.py     ← Classificação e geração de rascunho via LLM
    │
    ▼
cache.py             ← Cache local em JSON para evitar reprocessamento
    │
    ▼
app.py (Streamlit)   ← Interface web com filtros e métricas
```

---

## ⚙️ Como rodar localmente

### Pré-requisitos
- Python 3.11+
- Conta Google com Gmail
- Chave de API da OpenAI ([obter aqui](https://platform.openai.com/api-keys))

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/email-assistant.git
cd email-assistant
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```
OPENAI_API_KEY=sk-proj-sua-chave-aqui
```

### 5. Configure a Gmail API
- Acesse o [Google Cloud Console](https://console.cloud.google.com)
- Crie um projeto e ative a Gmail API
- Gere credenciais OAuth 2.0 (Desktop App) e salve como `credentials.json`

### 6. Rode o app
```bash
streamlit run app.py
```

Acesse `http://localhost:8501` no navegador.

---

## 🔒 Segurança

- Credenciais OAuth e chaves de API **nunca** são commitadas (ver `.gitignore`)
- O escopo Gmail usado é `readonly` — o app **não** envia, modifica ou deleta e-mails
- Cache local armazena apenas metadados de classificação, não o conteúdo dos e-mails

---

## 📁 Estrutura do projeto

```
email-assistant/
├── app.py               # Interface Streamlit
├── gmail_client.py      # Integração com Gmail API
├── llm_processor.py     # Lógica de IA (classificação + rascunho)
├── cache.py             # Cache local de classificações
├── requirements.txt     # Dependências do projeto
├── .env                 # Variáveis de ambiente (não commitado)
├── credentials.json     # Credencial OAuth Google (não commitado)
└── tests/
    ├── test_gmail.py
    └── test_llm.py
```

---

## 💡 Possíveis extensões

- [ ] Suporte a Outlook / Microsoft 365
- [ ] Envio do rascunho diretamente pelo app (Gmail API com escopo de escrita)
- [ ] Notificações para e-mails de alta urgência
- [ ] Histórico e dashboard de tendências ao longo do tempo
- [ ] Integração com ferramentas corporativas (Slack, Teams, Jira)

---

## Autor

Desenvolvido por **Gabriel M. Rostirolla** como projeto de portfólio.  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Gabriel-0077B5?logo=linkedin)](https://linkedin.com/in/gabriel-moreira-rostirolla-4aa33339b/)
[![GitHub](https://img.shields.io/badge/GitHub-gmrostirolla-181717?logo=github)](https://github.com/gmrostirolla)
```
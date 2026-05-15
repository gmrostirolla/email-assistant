import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

#response = client.chat.completions.create(
#    model ="gpt-4o-mini",
#    messages=[...],
#    temperature=0
#)
#

def classify_email(email:dict) -> dict:
    system_prompt = """Você é um classificador de e-mails corporativos.
Sua única função é analisar e-mails e retornar um JSON estruturado.
Retorne SOMENTE o JSON - sem texto antes, sem texto depois, sem markdown, sem backticks.

O JSON deve ter exatamente estas chaves:
{
    "urgency": "alta" | "media" | "baixa".
    "category": "trabalho" | "pessoal" | "financeiro" | "spam" | "outro",
    "summary": "<resumo em no máximo 20 palavras>",
    "reasoning": "<uma frase explicando por que essa urgência>"
}

Critérios de urgência:
- alta: requer ação hoje, prazos imediatos, assuntos críticos
- media: requer ação em alguns dias, follow-ups, reuniões futuras
- baixa: informativo, newsletters, sem prazo definido"""

    user_prompt = f"""De: {email['from']}
Assunto: {email['subject']}
Data: {email['date']}
Corpo:
{email['body']}"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        max_tokens=200
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:

        return {
            "urgency": "baixa",
            "category": "outro",
            "summary": "Não foi possível classificar.",
            "reasoning": "Erro no parsing da resposta do modelo."
        }
    
def generate_draft(email: dict, classification: dict) -> str:
    system_prompt = """Você é um assistente de comunicação corporativa profissional.
Escreva rascunhos de resposta de e-mail que sejam:
- Objetivos e profissionais
- Máximo de 5 linhas
- Tom adequado à urgência (urgente = direto; baixa = cordial e relaxado)
- em português, a menos que o e-mail original seja em outro idioma
Retorne SOMENTE o texto do rascunho, sem assunto, sem saudação de abertura padrão vazia."""

    user_prompt = f"""E-mail recebido:
De: {email['from']}
Assunto: {email['subject']}
Corpo: {email['body']}

Contexto da classificação:
- Urgência: {classification.get('urgency', 'media')}
- Categoria: {classification.get('category', 'trabalho')}

Escreva um rascunho da resposta adequada."""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()

def summarize_inbox(emails_with_analysis: list) -> str:
    email_summaries = []
    for i, item in enumerate(emails_with_analysis, 1):
        a = item.get('analysis', {})
        email_summaries.append(
            f"{i}. [{a.get('urgency', '?').upper()}] {item['subject']} "
            f"(de: {item['from']}) - {a.get('summary','')}"
        )

    inbox_text = "\n".join(email_summaries)

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente executivo. Resuma o estado da caixa de entrada em 3-4 frases, destacando o que requer atenção imediata e o panorama geral. Seja direto e útil."
            },
            {
                "role": "user",
                "content": f"Aqui estão os e-mails da caixa de entrada:\n\n{inbox_text}"
            }
        ],
        temperature=0.5,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()
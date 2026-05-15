from llm_processor import classify_email, generate_draft

# E-mail fictício para teste — não precisa do Gmail rodando
fake_email = {
    'id': 'test-001',
    'from': 'gerente@empresa.com',
    'subject': 'URGENTE: Apresentação para cliente amanhã às 9h',
    'date': 'Thu, 08 May 2026 14:30:00',
    'body': (
        'Preciso que você prepare os slides da proposta comercial '
        'para o cliente XYZ. A reunião é amanhã às 9h e o cliente '
        'é muito exigente. Por favor confirme que recebeu.'
    )
}

print("=== Testando classificação ===")
classification = classify_email(fake_email)
print(classification)

print("\n=== Testando geração de rascunho ===")
draft = generate_draft(fake_email, classification)
print(draft)
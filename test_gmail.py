from gmail_client import get_gmail_service, fetch_emails

service = get_gmail_service()  # Vai abrir o navegador na primeira vez
emails = fetch_emails(service, max_results=5)

for e in emails:
    print(f"De: {e['from']}")
    print(f"Assunto: {e['subject']}")
    print(f"Corpo (primeiros 200 chars): {e['body'][:200]}")
    print("---")
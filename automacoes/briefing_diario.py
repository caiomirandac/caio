#!/usr/bin/env python3
"""
Briefing Diário Jurídico com Google Calendar + Claude
=======================================================
Lê os eventos do dia do Google Calendar e gera um briefing
estruturado com prioridades, preparação e pontos de atenção.

Uso:
    python automacoes/briefing_diario.py           # briefing de hoje
    python automacoes/briefing_diario.py amanha    # briefing de amanhã
    python automacoes/briefing_diario.py semana    # resumo da semana

Requer:
    - credentials.json do Google Calendar na pasta raiz
"""

import anthropic
import os
import sys
from datetime import datetime, timedelta, timezone
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


def autenticar_google_calendar():
    """Autentica e retorna o serviço do Google Calendar."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        import pickle

        SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
        creds = None

        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif os.path.exists("credentials.json"):
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
                with open("token.pickle", "wb") as token:
                    pickle.dump(creds, token)
            else:
                return None, "credentials.json não encontrado"

        service = build("calendar", "v3", credentials=creds)
        return service, None

    except Exception as e:
        return None, str(e)


def buscar_eventos(service, data_inicio: datetime, data_fim: datetime) -> list:
    """Busca eventos do Google Calendar no período especificado."""
    time_min = data_inicio.isoformat() + "Z"
    time_max = data_fim.isoformat() + "Z"

    events_result = service.events().list(
        calendarId="primary",
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    return events_result.get("items", [])


def formatar_eventos_para_claude(eventos: list, periodo: str) -> str:
    """Formata a lista de eventos para envio ao Claude."""
    if not eventos:
        return f"Nenhum evento encontrado para {periodo}."

    texto = f"EVENTOS DO CALENDÁRIO ({periodo}):\n\n"

    for evento in eventos:
        inicio = evento.get("start", {})
        titulo = evento.get("summary", "Sem título")
        descricao = evento.get("description", "")
        local = evento.get("location", "")

        if "dateTime" in inicio:
            dt = datetime.fromisoformat(inicio["dateTime"].replace("Z", "+00:00"))
            hora = dt.strftime("%H:%M")
            texto += f"- {hora} | {titulo}"
        else:
            texto += f"- DIA TODO | {titulo}"

        if local:
            texto += f" @ {local}"
        if descricao:
            # Inclui primeiras 200 chars da descrição
            desc_curta = descricao[:200].replace("\n", " ")
            texto += f"\n  Descrição: {desc_curta}"
        texto += "\n"

    return texto


PROMPT_BRIEFING = """
Você é um assistente jurídico especializado que prepara o briefing diário de um advogado.
Analise os eventos do calendário abaixo e gere um briefing completo e prático.

O briefing deve ter as seguintes seções em Markdown:

## 🌅 BRIEFING JURÍDICO — {data_formatada}

### 📋 RESUMO DO DIA
- Total de compromissos
- Horário mais ocupado
- Avaliação geral do dia (tranquilo / moderado / intenso)

### ⚡ PRIORIDADES (ordenadas por urgência)
Para cada evento relevante:
- **HH:MM — [Nome do evento]**
  - Tipo: audiência / reunião / prazo / aula / etc.
  - Preparação necessária: o que precisa estar pronto
  - Ponto de atenção: algo a não esquecer

### ⚖️ PRAZOS E EVENTOS JURÍDICOS
Liste separadamente qualquer evento que pareça ser um prazo processual ou audiência.
Destaque com 🔴 se for crítico.

### 📚 AULAS E DOCÊNCIA
Se houver aulas ou compromissos de ensino, liste o que precisa ser preparado.

### 💼 OUTRAS OBSERVAÇÕES
- Conflitos de horário (se houver)
- Sugestão de ordem de preparação para hoje

---
Calendário fornecido:
{eventos}
"""


def gerar_briefing(eventos_texto: str, periodo: str, data_formatada: str) -> str:
    """Usa Claude para gerar o briefing."""
    client = anthropic.Anthropic()

    prompt = PROMPT_BRIEFING.format(
        data_formatada=data_formatada,
        eventos=eventos_texto,
    )

    briefing = ""
    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            briefing += text

    return briefing


def salvar_briefing(briefing: str, data_ref: datetime):
    """Salva o briefing em arquivo."""
    os.makedirs("briefings", exist_ok=True)
    filename = f"briefings/briefing_{data_ref.strftime('%Y%m%d')}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(briefing)

    return filename


def main():
    # Interpretar argumento de data
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else "hoje"

    agora = datetime.utcnow()

    if arg == "amanha" or arg == "amanhã":
        data_ref = agora + timedelta(days=1)
        data_inicio = data_ref.replace(hour=0, minute=0, second=0, microsecond=0)
        data_fim = data_ref.replace(hour=23, minute=59, second=59)
        periodo_label = "AMANHÃ"
        data_formatada = (datetime.now() + timedelta(days=1)).strftime("%A, %d de %B de %Y")
    elif arg == "semana":
        data_inicio = agora.replace(hour=0, minute=0, second=0, microsecond=0)
        data_fim = (agora + timedelta(days=7)).replace(hour=23, minute=59, second=59)
        periodo_label = "PRÓXIMOS 7 DIAS"
        data_formatada = f"Semana de {datetime.now().strftime('%d/%m')} a {(datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')}"
    else:
        data_inicio = agora.replace(hour=0, minute=0, second=0, microsecond=0)
        data_fim = agora.replace(hour=23, minute=59, second=59)
        periodo_label = "HOJE"
        data_formatada = datetime.now().strftime("%A, %d de %B de %Y")

    console.print(Panel.fit(
        f"[bold cyan]BRIEFING DIÁRIO — {periodo_label}[/bold cyan]\n"
        f"[dim]{data_formatada}[/dim]",
        border_style="cyan"
    ))

    # Autenticar Google Calendar
    console.print("\n[dim]Conectando ao Google Calendar...[/dim]")
    service, erro = autenticar_google_calendar()

    if erro:
        console.print(f"[yellow]Google Calendar indisponível: {erro}[/yellow]")
        console.print("[dim]Gerando briefing com agenda de exemplo...[/dim]\n")
        # Agenda de exemplo para demonstração
        eventos_texto = f"""
EVENTOS DO CALENDÁRIO (exemplo — {periodo_label}):

- 09:00 | Audiência de Instrução — Proc. 0001234-22.2024.5.05.0001 @ TRT 5ª Região Salvador
  Descrição: Audiência de instrução com oitiva de 3 testemunhas. Parte autora alega horas extras.
- 11:00 | Reunião com cliente João Silva
  Descrição: Discussão sobre estratégia no processo de divórcio litigioso.
- 14:00 | PRAZO: Contrarrazões de Apelação — Proc. 0009876-11.2023.8.05.0001
  Descrição: PRAZO FATAL — último dia para protocolo das contrarrazões.
- 16:00 | Aula de Direito Processual Civil — Turma 3B
  Descrição: Tema: Recursos no CPC/2015. Preparar slides sobre agravo de instrumento.
- 18:30 | Reunião família
"""
    else:
        console.print("[green]✓ Conectado ao Google Calendar[/green]")
        eventos = buscar_eventos(service, data_inicio, data_fim)
        console.print(f"[dim]Encontrados {len(eventos)} evento(s)[/dim]")
        eventos_texto = formatar_eventos_para_claude(eventos, periodo_label)

    # Gerar briefing com Claude
    console.print("\n[bold green]Gerando briefing com Claude...[/bold green]\n")

    briefing = gerar_briefing(eventos_texto, periodo_label, data_formatada)

    # Exibir briefing formatado
    console.print(Panel(
        Markdown(briefing),
        title=f"[bold cyan]Briefing — {periodo_label}[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))

    # Salvar
    data_arquivo = datetime.now() if arg != "amanha" else datetime.now() + timedelta(days=1)
    filename = salvar_briefing(briefing, data_arquivo)
    console.print(f"\n[dim]Briefing salvo em: {filename}[/dim]")


if __name__ == "__main__":
    main()

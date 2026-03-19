#!/usr/bin/env python3
"""
Calculadora de Prazos Processuais + Google Calendar
=====================================================
Calcula prazos processuais (CPC, CLT, etc.) a partir de uma data de intimação
e cria eventos com alertas automáticos no Google Calendar.

Uso:
    python automacoes/calcular_prazos.py

Requer:
    - Variável ANTHROPIC_API_KEY configurada
    - Arquivo credentials.json do Google Calendar na pasta raiz
      (baixar em: console.cloud.google.com → APIs → Calendar → Credenciais)
"""

import anthropic
import json
import os
import sys
from datetime import datetime, timedelta
from dateutil import parser as dateparser
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

console = Console()

# Regras de prazos mais comuns no processo civil e trabalhista
TIPOS_PRAZO = {
    "1": ("Contestação (CPC)", 15, "dias úteis"),
    "2": ("Recurso de Apelação (CPC)", 15, "dias úteis"),
    "3": ("Contrarrazões de Apelação", 15, "dias úteis"),
    "4": ("Embargos de Declaração", 5, "dias úteis"),
    "5": ("Agravo de Instrumento", 15, "dias úteis"),
    "6": ("Recurso Especial (STJ)", 15, "dias úteis"),
    "7": ("Recurso Ordinário Trabalhista", 8, "dias corridos"),
    "8": ("Embargos de Declaração (TST)", 5, "dias úteis"),
    "9": ("Impugnação ao Valor da Causa", 15, "dias úteis"),
    "10": ("Manifestação sobre laudo pericial", 15, "dias úteis"),
    "11": ("Personalizado", 0, ""),
}

# Feriados nacionais fixos (simplificado)
FERIADOS_NACIONAIS = {
    (1, 1): "Confraternização Universal",
    (4, 21): "Tiradentes",
    (5, 1): "Dia do Trabalho",
    (9, 7): "Independência do Brasil",
    (10, 12): "Nossa Senhora Aparecida",
    (11, 2): "Finados",
    (11, 15): "Proclamação da República",
    (12, 25): "Natal",
}


def eh_feriado(data: datetime) -> bool:
    """Verifica se é feriado nacional fixo."""
    return (data.month, data.day) in FERIADOS_NACIONAIS


def adicionar_dias_uteis(data_inicio: datetime, dias: int) -> datetime:
    """Calcula a data final considerando apenas dias úteis (exclui sáb, dom e feriados)."""
    data_atual = data_inicio
    dias_contados = 0

    while dias_contados < dias:
        data_atual += timedelta(days=1)
        # Pula finais de semana e feriados
        if data_atual.weekday() < 5 and not eh_feriado(data_atual):
            dias_contados += 1

    return data_atual


def adicionar_dias_corridos(data_inicio: datetime, dias: int) -> datetime:
    """Calcula a data final em dias corridos."""
    return data_inicio + timedelta(days=dias)


def calcular_prazo(data_intimacao: datetime, dias: int, tipo_dia: str) -> dict:
    """Calcula o prazo e retorna as datas relevantes."""
    # Início do prazo: normalmente no dia seguinte à intimação
    inicio_contagem = data_intimacao + timedelta(days=1)

    # Se o início cair em fim de semana/feriado, passa para o próximo dia útil
    while inicio_contagem.weekday() >= 5 or eh_feriado(inicio_contagem):
        inicio_contagem += timedelta(days=1)

    if tipo_dia == "dias úteis":
        data_final = adicionar_dias_uteis(inicio_contagem - timedelta(days=1), dias)
    else:
        data_final = adicionar_dias_corridos(data_intimacao, dias)

    # Se o prazo final cair em fim de semana/feriado, prorroga para o próximo dia útil
    while data_final.weekday() >= 5 or eh_feriado(data_final):
        data_final += timedelta(days=1)

    # Alertas: 3 dias antes, 1 dia antes e no dia do vencimento
    alerta_3_dias = data_final - timedelta(days=3)
    alerta_1_dia = data_final - timedelta(days=1)

    return {
        "data_intimacao": data_intimacao,
        "inicio_contagem": inicio_contagem,
        "data_final": data_final,
        "alerta_3_dias": alerta_3_dias,
        "alerta_1_dia": alerta_1_dia,
    }


def usar_claude_para_calcular(descricao_livre: str) -> dict:
    """
    Usa o Claude para interpretar uma descrição livre de prazo
    e retornar os dados estruturados.
    """
    client = anthropic.Anthropic()

    prompt = f"""
Você é um advogado especializado em processo civil e trabalhista brasileiro.
Com base na descrição abaixo, extraia e calcule as informações do prazo processual.

Responda APENAS em JSON válido com este formato:
{{
  "tipo_prazo": "nome do ato processual",
  "data_intimacao": "DD/MM/AAAA",
  "dias": número,
  "tipo_dia": "dias úteis" ou "dias corridos",
  "observacoes": "qualquer observação relevante"
}}

Descrição: {descricao_livre}

Data de referência (hoje): {datetime.now().strftime('%d/%m/%Y')}
"""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    texto = response.content[0].text.strip()
    # Remove marcadores de código se presentes
    if texto.startswith("```"):
        texto = texto.split("```")[1]
        if texto.startswith("json"):
            texto = texto[4:]
    texto = texto.strip()

    return json.loads(texto)


def criar_evento_google_calendar(titulo: str, data: datetime, descricao: str, duracao_minutos: int = 60):
    """Cria um evento no Google Calendar via API."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        import pickle

        SCOPES = ["https://www.googleapis.com/auth/calendar"]
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

        evento = {
            "summary": titulo,
            "description": descricao,
            "start": {
                "dateTime": data.strftime("%Y-%m-%dT09:00:00"),
                "timeZone": "America/Bahia",
            },
            "end": {
                "dateTime": (data + timedelta(minutes=duracao_minutos)).strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": "America/Bahia",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},    # 1 dia antes
                    {"method": "popup", "minutes": 24 * 60},    # 1 dia antes
                    {"method": "popup", "minutes": 60},         # 1 hora antes
                ],
            },
            "colorId": "11",  # vermelho = urgente
        }

        evento_criado = service.events().insert(calendarId="primary", body=evento).execute()
        return evento_criado.get("htmlLink"), None

    except Exception as e:
        return None, str(e)


def exibir_tabela_prazos(resultado: dict, nome_ato: str, dias: int, tipo_dia: str):
    """Exibe uma tabela formatada com os prazos calculados."""
    table = Table(title=f"Prazos: {nome_ato}", border_style="cyan")
    table.add_column("Evento", style="bold")
    table.add_column("Data", style="green")
    table.add_column("Dia da semana")

    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

    table.add_row(
        "Intimação",
        resultado["data_intimacao"].strftime("%d/%m/%Y"),
        dias_semana[resultado["data_intimacao"].weekday()],
    )
    table.add_row(
        "Início da contagem",
        resultado["inicio_contagem"].strftime("%d/%m/%Y"),
        dias_semana[resultado["inicio_contagem"].weekday()],
    )
    table.add_row(
        f"[bold red]PRAZO FINAL ({dias} {tipo_dia})[/bold red]",
        f"[bold red]{resultado['data_final'].strftime('%d/%m/%Y')}[/bold red]",
        f"[bold red]{dias_semana[resultado['data_final'].weekday()]}[/bold red]",
    )
    table.add_row(
        "⚠️  Alerta 3 dias antes",
        resultado["alerta_3_dias"].strftime("%d/%m/%Y"),
        dias_semana[resultado["alerta_3_dias"].weekday()],
    )
    table.add_row(
        "🔔 Alerta 1 dia antes",
        resultado["alerta_1_dia"].strftime("%d/%m/%Y"),
        dias_semana[resultado["alerta_1_dia"].weekday()],
    )

    console.print()
    console.print(table)


def main():
    console.print(Panel.fit(
        "[bold cyan]CALCULADORA DE PRAZOS PROCESSUAIS[/bold cyan]\n"
        "Com criação automática no Google Calendar",
        border_style="cyan"
    ))

    # Modo de entrada
    console.print("\n[bold]Como deseja informar o prazo?[/bold]")
    console.print("  [1] Seleção por tipo (lista)")
    console.print("  [2] Descrição livre (Claude interpreta)")

    modo = Prompt.ask("Opção", choices=["1", "2"])

    if modo == "1":
        # Modo lista
        console.print("\n[bold]Tipo de prazo:[/bold]\n")
        for key, (nome, dias, tipo) in TIPOS_PRAZO.items():
            if key != "11":
                console.print(f"  [{key}] {nome} — {dias} {tipo}")
        console.print("  [11] Personalizado")

        escolha = Prompt.ask("\nTipo", choices=list(TIPOS_PRAZO.keys()))

        if escolha == "11":
            nome_ato = Prompt.ask("Nome do ato processual")
            dias = int(Prompt.ask("Número de dias"))
            tipo_dia = Prompt.ask("Tipo de prazo", choices=["dias úteis", "dias corridos"])
        else:
            nome_ato, dias, tipo_dia = TIPOS_PRAZO[escolha]

        data_str = Prompt.ask("Data da intimação (DD/MM/AAAA)")
        data_intimacao = dateparser.parse(data_str, dayfirst=True)
        processo = Prompt.ask("Número do processo (opcional, Enter para pular)", default="")

    else:
        # Modo descrição livre com Claude
        console.print("\n[yellow]Descreva o prazo em linguagem natural.[/yellow]")
        console.print("[dim]Exemplo: 'fui intimado hoje (15/01/2025) para apresentar contestação'[/dim]\n")

        descricao = Prompt.ask("Descrição")

        console.print("\n[dim]Interpretando com Claude...[/dim]")
        dados = usar_claude_para_calcular(descricao)

        nome_ato = dados["tipo_prazo"]
        dias = dados["dias"]
        tipo_dia = dados["tipo_dia"]
        data_intimacao = dateparser.parse(dados["data_intimacao"], dayfirst=True)
        processo = ""

        if dados.get("observacoes"):
            console.print(f"\n[yellow]Observação: {dados['observacoes']}[/yellow]")

    # Calcular prazo
    resultado = calcular_prazo(data_intimacao, dias, tipo_dia)

    # Exibir tabela
    exibir_tabela_prazos(resultado, nome_ato, dias, tipo_dia)

    # Criar eventos no Google Calendar
    if Confirm.ask("\nCriar eventos no Google Calendar?", default=True):
        titulo_base = f"[PRAZO] {nome_ato}"
        if processo:
            titulo_base += f" — Proc. {processo}"

        descricao_evento = (
            f"Tipo: {nome_ato}\n"
            f"Prazo: {dias} {tipo_dia}\n"
            f"Intimação em: {resultado['data_intimacao'].strftime('%d/%m/%Y')}\n"
            f"Início da contagem: {resultado['inicio_contagem'].strftime('%d/%m/%Y')}\n"
        )
        if processo:
            descricao_evento += f"Processo: {processo}\n"

        # Evento do prazo final
        link, erro = criar_evento_google_calendar(
            titulo=f"🔴 VENCIMENTO: {nome_ato}",
            data=resultado["data_final"],
            descricao=descricao_evento + "\n⚠️ DATA LIMITE — NÃO PERDER!",
            duracao_minutos=120,
        )

        if erro:
            console.print(f"\n[yellow]Google Calendar não configurado: {erro}[/yellow]")
            console.print("[dim]Para ativar, baixe credentials.json em console.cloud.google.com[/dim]")
        else:
            console.print(f"\n[green]✓ Evento de vencimento criado: {link}[/green]")

            # Evento de alerta 3 dias antes
            criar_evento_google_calendar(
                titulo=f"⚠️  3 DIAS: {nome_ato}",
                data=resultado["alerta_3_dias"],
                descricao=descricao_evento + f"\n⚠️ Prazo vence em 3 dias ({resultado['data_final'].strftime('%d/%m/%Y')})",
                duracao_minutos=30,
            )
            console.print("[green]✓ Alerta de 3 dias criado[/green]")

            # Evento de alerta 1 dia antes
            criar_evento_google_calendar(
                titulo=f"🔔 AMANHÃ VENCE: {nome_ato}",
                data=resultado["alerta_1_dia"],
                descricao=descricao_evento + f"\n🔴 Prazo vence AMANHÃ ({resultado['data_final'].strftime('%d/%m/%Y')})",
                duracao_minutos=30,
            )
            console.print("[green]✓ Alerta de 1 dia criado[/green]")


if __name__ == "__main__":
    main()

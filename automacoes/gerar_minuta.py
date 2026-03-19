#!/usr/bin/env python3
"""
Gerador de Minutas Jurídicas com Claude
========================================
Gera rascunhos de petições iniciais, contratos e pareceres
a partir de um briefing simples fornecido pelo usuário.

Uso:
    python automacoes/gerar_minuta.py
"""

import anthropic
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

TIPOS_DOCUMENTO = {
    "1": "Petição Inicial",
    "2": "Contrato de Prestação de Serviços",
    "3": "Contrato de Locação",
    "4": "Parecer Jurídico",
    "5": "Notificação Extrajudicial",
    "6": "Recurso de Apelação",
    "7": "Contrarrazões de Apelação",
    "8": "Embargos de Declaração",
}

PROMPTS_POR_TIPO = {
    "Petição Inicial": """
Você é um advogado experiente especializado em redação de peças processuais.
Redija uma PETIÇÃO INICIAL completa e bem estruturada com base nas informações abaixo.

A petição deve conter:
- Endereçamento ao juízo competente
- Qualificação das partes (autor e réu)
- Dos fatos (narrativa clara e cronológica)
- Do direito (fundamentos legais aplicáveis)
- Do pedido (requerimentos específicos)
- Do valor da causa
- Dos requerimentos finais (provas, citação, etc.)

Informações fornecidas pelo usuário:
{briefing}

Redija a petição de forma profissional, usando linguagem jurídica adequada mas clara.
""",
    "Contrato de Prestação de Serviços": """
Você é um advogado especializado em contratos.
Redija um CONTRATO DE PRESTAÇÃO DE SERVIÇOS completo com base nas informações abaixo.

O contrato deve conter:
- Qualificação das partes (contratante e contratado)
- Objeto do contrato (descrição detalhada dos serviços)
- Obrigações das partes
- Valor e forma de pagamento
- Prazo de execução
- Confidencialidade (se aplicável)
- Propriedade intelectual (se aplicável)
- Responsabilidade por danos
- Rescisão contratual
- Foro de eleição
- Assinaturas e testemunhas

Informações fornecidas:
{briefing}
""",
    "Contrato de Locação": """
Você é um advogado especializado em direito imobiliário.
Redija um CONTRATO DE LOCAÇÃO RESIDENCIAL/COMERCIAL completo com base nas informações abaixo.

O contrato deve seguir a Lei 8.245/91 (Lei do Inquilinato) e conter:
- Qualificação das partes (locador e locatário)
- Descrição e endereço do imóvel
- Destinação (residencial ou comercial)
- Valor do aluguel e reajuste (IGPM/IPCA)
- Garantia locatícia (caução, fiança ou seguro)
- Prazo da locação
- Obrigações do locador e locatário
- Benfeitorias
- Rescisão e multa
- Foro

Informações fornecidas:
{briefing}
""",
    "Parecer Jurídico": """
Você é um advogado sênior redigindo um PARECER JURÍDICO formal.

O parecer deve conter:
- Consulta (síntese da questão posta)
- Dos fatos
- Da análise jurídica (legislação, doutrina e jurisprudência aplicáveis)
- Das conclusões
- Da resposta à consulta

Use referências legais precisas (artigos de lei, súmulas, precedentes de tribunais superiores quando relevante).

Informações fornecidas:
{briefing}
""",
    "Notificação Extrajudicial": """
Você é um advogado redigindo uma NOTIFICAÇÃO EXTRAJUDICIAL formal.

A notificação deve conter:
- Qualificação do notificante e notificado
- Exposição dos fatos que motivam a notificação
- Das exigências (o que se exige do notificado)
- Do prazo para cumprimento
- Das consequências em caso de descumprimento
- Fecho formal

Informações fornecidas:
{briefing}
""",
    "Recurso de Apelação": """
Você é um advogado especializado em recursos processuais.
Redija um RECURSO DE APELAÇÃO completo com base nas informações abaixo.

O recurso deve conter:
- Endereçamento ao tribunal
- Tempestividade e cabimento
- Dos fatos processuais
- Das razões de reforma da sentença (error in judicando e/ou error in procedendo)
- Fundamentação legal e jurisprudencial
- Do pedido de reforma total ou parcial da sentença

Informações fornecidas:
{briefing}
""",
    "Contrarrazões de Apelação": """
Você é um advogado redigindo CONTRARRAZÕES DE APELAÇÃO.

As contrarrazões devem:
- Rebater cada argumento do recorrente
- Demonstrar a correção da sentença recorrida
- Apresentar fundamentos legais e jurisprudenciais de sustentação
- Requerer o desprovimento do recurso e manutenção da sentença

Informações fornecidas:
{briefing}
""",
    "Embargos de Declaração": """
Você é um advogado redigindo EMBARGOS DE DECLARAÇÃO.

Os embargos devem:
- Identificar o vício na decisão (omissão, contradição, obscuridade ou erro material)
- Demonstrar especificamente onde o vício ocorre
- Requerer a sanação do vício com ou sem efeito modificativo

Informações fornecidas:
{briefing}
""",
}


def coletar_briefing(tipo_documento: str) -> dict:
    """Coleta as informações necessárias para o documento."""
    console.print(f"\n[bold cyan]Informações para: {tipo_documento}[/bold cyan]\n")

    campos = {
        "Petição Inicial": [
            ("autor", "Nome completo do AUTOR (com CPF/CNPJ e endereço)"),
            ("reu", "Nome completo do RÉU (com CPF/CNPJ e endereço)"),
            ("juizo", "Juízo competente (ex: 3ª Vara Cível de Salvador/BA)"),
            ("fatos", "Descreva os FATOS em ordem cronológica"),
            ("pedido", "O que você quer que o juiz decida/condene?"),
            ("valor_causa", "Valor da causa (R$)"),
        ],
        "Contrato de Prestação de Serviços": [
            ("contratante", "Nome/empresa CONTRATANTE (com CPF/CNPJ)"),
            ("contratado", "Nome/empresa CONTRATADO (com CPF/CNPJ)"),
            ("objeto", "Descreva os SERVIÇOS a serem prestados"),
            ("valor", "Valor total e forma de pagamento"),
            ("prazo", "Prazo de execução dos serviços"),
            ("observacoes", "Outras cláusulas importantes (ou Enter para pular)"),
        ],
        "Contrato de Locação": [
            ("locador", "Nome do LOCADOR (com CPF/CNPJ)"),
            ("locatario", "Nome do LOCATÁRIO (com CPF/CNPJ)"),
            ("imovel", "Endereço completo do IMÓVEL"),
            ("finalidade", "Finalidade: residencial ou comercial?"),
            ("valor_aluguel", "Valor mensal do aluguel (R$)"),
            ("prazo", "Prazo da locação (ex: 30 meses)"),
            ("garantia", "Tipo de garantia (caução/fiança/seguro-fiança)"),
        ],
        "Parecer Jurídico": [
            ("consulente", "Quem solicita o parecer?"),
            ("questao", "Qual a questão jurídica a ser analisada?"),
            ("fatos", "Descreva os fatos relevantes"),
            ("objetivo", "O que você precisa saber/definir?"),
        ],
        "Notificação Extrajudicial": [
            ("notificante", "Nome do NOTIFICANTE (com CPF/CNPJ)"),
            ("notificado", "Nome do NOTIFICADO (com CPF/CNPJ e endereço)"),
            ("motivo", "Motivo da notificação"),
            ("exigencia", "O que se exige do notificado?"),
            ("prazo", "Prazo para cumprimento (dias)"),
        ],
    }

    # Para tipos sem campos específicos, usa campos genéricos
    campos_padrao = [
        ("partes", "Identifique as partes envolvidas"),
        ("fatos", "Descreva os fatos relevantes"),
        ("objetivo", "Qual o objetivo do documento?"),
        ("detalhes", "Outros detalhes importantes"),
    ]

    campos_tipo = campos.get(tipo_documento, campos_padrao)

    briefing_parts = []
    for campo, descricao in campos_tipo:
        valor = Prompt.ask(f"[yellow]{descricao}[/yellow]")
        if valor:
            briefing_parts.append(f"{descricao}: {valor}")

    return "\n".join(briefing_parts)


def gerar_documento(tipo_documento: str, briefing: str) -> str:
    """Chama a API do Claude para gerar o documento."""
    client = anthropic.Anthropic()

    prompt_template = PROMPTS_POR_TIPO.get(tipo_documento, """
Você é um advogado experiente. Redija o documento jurídico do tipo '{tipo}'
com base nas seguintes informações: {briefing}
""")

    prompt = prompt_template.format(briefing=briefing, tipo=tipo_documento)

    console.print("\n[bold green]Gerando documento com Claude...[/bold green]")

    documento = ""
    with console.status("[bold green]Aguarde...[/bold green]"):
        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=4096,
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                documento += text

    return documento


def salvar_documento(tipo_documento: str, documento: str) -> str:
    """Salva o documento em arquivo .txt."""
    import os
    from datetime import datetime

    os.makedirs("minutas", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_tipo = tipo_documento.lower().replace(" ", "_").replace("/", "_")
    filename = f"minutas/{nome_tipo}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {tipo_documento}\n")
        f.write(f"# Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(documento)

    return filename


def main():
    console.print(Panel.fit(
        "[bold cyan]GERADOR DE MINUTAS JURÍDICAS[/bold cyan]\n"
        "Powered by Claude (Anthropic)",
        border_style="cyan"
    ))

    # Selecionar tipo de documento
    console.print("\n[bold]Selecione o tipo de documento:[/bold]\n")
    for key, nome in TIPOS_DOCUMENTO.items():
        console.print(f"  [{key}] {nome}")

    escolha = Prompt.ask("\nOpção", choices=list(TIPOS_DOCUMENTO.keys()))
    tipo_documento = TIPOS_DOCUMENTO[escolha]

    # Coletar informações
    briefing = coletar_briefing(tipo_documento)

    if not briefing.strip():
        console.print("[red]Nenhuma informação fornecida. Encerrando.[/red]")
        sys.exit(1)

    # Gerar documento
    documento = gerar_documento(tipo_documento, briefing)

    # Exibir resultado
    console.print("\n" + "=" * 60)
    console.print(Panel(Markdown(documento), title=f"[bold]{tipo_documento}[/bold]", border_style="green"))

    # Salvar
    if Confirm.ask("\nDeseja salvar o documento em arquivo?", default=True):
        filename = salvar_documento(tipo_documento, documento)
        console.print(f"[green]Documento salvo em: [bold]{filename}[/bold][/green]")

    console.print("\n[dim]Lembre-se: este é um RASCUNHO. Revise antes de usar.[/dim]")


if __name__ == "__main__":
    main()

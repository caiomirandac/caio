#!/usr/bin/env python3
"""
Analisador de Contratos com Claude
====================================
Analisa um contrato e produz um relatório de riscos,
cláusulas problemáticas e sugestões de melhoria.

Uso:
    python automacoes/analisar_contrato.py contrato.txt
    python automacoes/analisar_contrato.py  # modo interativo (colar o texto)
"""

import anthropic
import sys
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Confirm

console = Console()

PROMPT_ANALISE = """
Você é um advogado sênior especializado em revisão e análise de contratos.
Analise o contrato abaixo e produza um relatório estruturado em Markdown.

O relatório deve conter as seguintes seções:

## 1. RESUMO EXECUTIVO
- Tipo de contrato
- Partes envolvidas
- Objeto principal
- Valor (se houver)
- Prazo

## 2. PONTOS CRÍTICOS E RISCOS
Liste cada risco com:
- **[ALTO/MÉDIO/BAIXO]** Descrição do risco
- Cláusula de referência (número ou texto)
- Por que é problemático

## 3. CLÁUSULAS ABUSIVAS OU PROBLEMÁTICAS
- Identifique cláusulas que violam o CDC, Código Civil ou lei específica
- Cite o dispositivo legal violado

## 4. LACUNAS E OMISSÕES
- O que o contrato deveria ter mas não tem
- Riscos decorrentes dessas omissões

## 5. PONTOS POSITIVOS
- O que o contrato trata bem

## 6. SUGESTÕES DE MELHORIA
- Lista de alterações recomendadas, por ordem de prioridade

## 7. RECOMENDAÇÃO FINAL
- Assinar como está / Negociar alterações / Recusar
- Justificativa resumida

---
CONTRATO A ANALISAR:
{contrato}
"""


def ler_contrato_de_arquivo(caminho: str) -> str:
    """Lê o texto do contrato de um arquivo."""
    if not os.path.exists(caminho):
        console.print(f"[red]Arquivo não encontrado: {caminho}[/red]")
        sys.exit(1)

    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()


def ler_contrato_interativo() -> str:
    """Permite colar o texto do contrato diretamente no terminal."""
    console.print("[yellow]Cole o texto do contrato abaixo.[/yellow]")
    console.print("[dim]Quando terminar, pressione Enter duas vezes seguido de Ctrl+D (Linux/Mac) ou Ctrl+Z (Windows).[/dim]\n")

    linhas = []
    try:
        while True:
            linha = input()
            linhas.append(linha)
    except EOFError:
        pass

    return "\n".join(linhas)


def analisar_contrato(texto_contrato: str) -> str:
    """Chama a API do Claude para analisar o contrato."""
    if not texto_contrato.strip():
        console.print("[red]Texto do contrato vazio.[/red]")
        sys.exit(1)

    client = anthropic.Anthropic()

    prompt = PROMPT_ANALISE.format(contrato=texto_contrato)

    console.print("\n[bold green]Analisando contrato com Claude...[/bold green]")

    relatorio = ""
    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            relatorio += text
            # Mostra progresso em tempo real
            console.print(text, end="", markup=False)

    console.print()  # nova linha após streaming
    return relatorio


def salvar_relatorio(relatorio: str, nome_original: str = "contrato") -> str:
    """Salva o relatório de análise."""
    os.makedirs("analises", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(os.path.basename(nome_original))[0]
    filename = f"analises/analise_{base}_{timestamp}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Análise de Contrato\n")
        f.write(f"**Arquivo:** {nome_original}\n")
        f.write(f"**Data da análise:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        f.write("---\n\n")
        f.write(relatorio)

    return filename


def main():
    console.print(Panel.fit(
        "[bold cyan]ANALISADOR DE CONTRATOS[/bold cyan]\n"
        "Powered by Claude (Anthropic)",
        border_style="cyan"
    ))

    # Determinar fonte do contrato
    if len(sys.argv) > 1:
        caminho_arquivo = sys.argv[1]
        console.print(f"\n[dim]Lendo arquivo: {caminho_arquivo}[/dim]")
        texto_contrato = ler_contrato_de_arquivo(caminho_arquivo)
        nome_arquivo = caminho_arquivo
    else:
        console.print("\n[dim]Nenhum arquivo informado — modo interativo[/dim]")
        texto_contrato = ler_contrato_interativo()
        nome_arquivo = "contrato_colado"

    # Mostrar tamanho do contrato
    palavras = len(texto_contrato.split())
    console.print(f"\n[dim]Contrato carregado: ~{palavras} palavras[/dim]")

    # Analisar
    relatorio = analisar_contrato(texto_contrato)

    # Salvar
    if Confirm.ask("\nDeseja salvar o relatório de análise?", default=True):
        filename = salvar_relatorio(relatorio, nome_arquivo)
        console.print(f"\n[green]Relatório salvo em: [bold]{filename}[/bold][/green]")

    console.print("\n[dim]Esta análise é um auxílio e não substitui o julgamento profissional do advogado.[/dim]")


if __name__ == "__main__":
    main()

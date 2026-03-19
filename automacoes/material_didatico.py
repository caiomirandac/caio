#!/usr/bin/env python3
"""
Gerador de Material Didático Jurídico com Claude
==================================================
Gera planos de aula, casos práticos, questões de avaliação
e resumos de doutrina para docência jurídica.

Uso:
    python automacoes/material_didatico.py
"""

import anthropic
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm

console = Console()

TIPOS_MATERIAL = {
    "1": "Plano de Aula",
    "2": "Caso Prático para Discussão",
    "3": "Questões de Avaliação (com gabarito)",
    "4": "Resumo de Doutrina",
    "5": "Esquema / Mapa Conceitual",
    "6": "Simulação de Audiência",
}

NIVEIS = {
    "1": "Graduação — 1º ou 2º período (introdutório)",
    "2": "Graduação — períodos intermediários",
    "3": "Graduação — períodos finais (formandos)",
    "4": "Pós-graduação / Especialização",
    "5": "Extensão / Aperfeiçoamento para profissionais",
}

PROMPTS = {
    "Plano de Aula": """
Você é um professor de Direito experiente. Elabore um PLANO DE AULA completo e detalhado.

## Informações
- Tema: {tema}
- Nível: {nivel}
- Duração: {duracao}
- Matéria/Disciplina: {materia}

## Estrutura do plano de aula:

### 1. IDENTIFICAÇÃO
- Disciplina, tema, turma, carga horária

### 2. OBJETIVOS DE APRENDIZAGEM
- O que o aluno deverá saber/fazer ao final

### 3. COMPETÊNCIAS E HABILIDADES
- Competências desenvolvidas (BNCC / OAB se aplicável)

### 4. CONTEÚDO PROGRAMÁTICO
- Tópicos em ordem didática, com tempo estimado para cada um

### 5. METODOLOGIA
- Aula expositiva, estudo de caso, discussão, moot court, etc.
- Recursos utilizados (slides, quadro, vídeo, jurisprudência)

### 6. DESENVOLVIMENTO DA AULA
Descreva detalhadamente cada momento:
- **Introdução** (X min): como apresentar o tema, conexão com o que já foi visto
- **Desenvolvimento** (X min): como explicar os conceitos principais
- **Atividade prática** (X min): exercício ou discussão
- **Encerramento** (X min): síntese, dúvidas, próxima aula

### 7. REFERÊNCIAS BIBLIOGRÁFICAS
- 3 a 5 obras relevantes (doutrina, legislação, jurisprudência)

### 8. AVALIAÇÃO
- Como verificar se os objetivos foram atingidos
""",

    "Caso Prático para Discussão": """
Você é um professor de Direito especializado em metodologia ativa.
Elabore um CASO PRÁTICO rico e realista para discussão em sala de aula.

## Informações
- Tema jurídico: {tema}
- Nível da turma: {nivel}
- Matéria: {materia}

## O caso prático deve conter:

### CASO — [Título chamativo]

**Contexto e Fatos**
Narrativa realista com nome de personagens, datas, locais e detalhes suficientes
para gerar debate. Inclua elementos ambíguos que permitam diferentes interpretações.

**Documentos e Provas Disponíveis**
Liste os documentos que existem no caso.

**Questões para Discussão**
1. [Questão de identificação do problema jurídico]
2. [Questão de aplicação da lei]
3. [Questão de estratégia processual]
4. [Questão ética ou deontológica, se aplicável]

**Gabarito Comentado**
Para cada questão:
- Resposta esperada
- Dispositivos legais aplicáveis
- Posição da jurisprudência (STJ/STF se relevante)
- Divergências doutrinárias (se houver)

**Variações do Caso**
2 versões do caso com pequenas alterações que mudam a resposta — para aprofundar a discussão.
""",

    "Questões de Avaliação (com gabarito)": """
Você é um professor de Direito elaborando questões de avaliação.

## Informações
- Tema: {tema}
- Nível: {nivel}
- Matéria: {materia}
- Número de questões: {num_questoes}

## Elabore as questões da seguinte forma:

### QUESTÕES OBJETIVAS (múltipla escolha — padrão OAB/concurso)
Para cada questão:
- Enunciado claro com um caso ou situação
- 4 alternativas (a, b, c, d)
- Armadilhas razoáveis mas não injustas
- **Gabarito:** alternativa correta
- **Justificativa:** por que as outras estão erradas

### QUESTÕES DISSERTATIVAS
Para cada questão:
- Enunciado que exija análise e argumentação jurídica
- **Critérios de correção:** o que deve ser abordado para atingir a nota máxima
- **Resposta esperada:** modelo de resposta ideal
- **Dica ao professor:** pontos que frequentemente geram erro nos alunos
""",

    "Resumo de Doutrina": """
Você é um professor de Direito especializado em síntese doutrinária.
Elabore um RESUMO DIDÁTICO sobre o tema indicado.

## Informações
- Tema: {tema}
- Nível: {nivel}
- Matéria: {materia}

## O resumo deve conter:

### CONCEITO E DEFINIÇÃO
- Definição doutrinária predominante
- Natureza jurídica

### FUNDAMENTO LEGAL
- Dispositivos constitucionais (se aplicável)
- Lei principal e artigos relevantes
- Legislação complementar

### ELEMENTOS ESSENCIAIS
- Liste e explique cada elemento de forma clara

### CLASSIFICAÇÕES DOUTRINÁRIAS
- Principais classificações adotadas pela doutrina brasileira

### POSIÇÃO DOS TRIBUNAIS SUPERIORES
- Súmulas relevantes (STJ/STF/TST)
- Precedentes mais importantes

### QUESTÕES CONTROVERTIDAS
- Pontos de divergência entre autores e tribunais

### MAPA VISUAL / ESQUEMA
- Esquema em texto para visualização rápida do tema

### QUESTÃO PARA FIXAÇÃO
- 1 questão objetiva e 1 dissertativa sobre o tema
""",

    "Esquema / Mapa Conceitual": """
Você é um professor de Direito especializado em materiais visuais de apoio.
Elabore um ESQUEMA ESTRUTURADO do tema em formato de texto (usando indentação e símbolos).

## Informações
- Tema: {tema}
- Nível: {nivel}
- Matéria: {materia}

## O esquema deve:
- Usar hierarquia clara (tópicos e subtópicos)
- Incluir os pontos mais cobrados em provas
- Destacar as palavras-chave
- Incluir referências legais nos pontos principais
- Ser visual e fácil de memorizar
- Ter no final um quadro-resumo comparativo (se aplicável)
""",

    "Simulação de Audiência": """
Você é um professor que usa metodologias ativas no ensino jurídico.
Elabore um ROTEIRO DE SIMULAÇÃO DE AUDIÊNCIA para prática em sala de aula.

## Informações
- Tipo de audiência: {tema}
- Nível: {nivel}
- Matéria: {materia}

## O roteiro deve conter:

### CONTEXTO DO CASO
- Situação fática completa para os alunos representarem

### PAPÉIS
- Juiz: instruções e pontos a verificar
- Advogado da parte autora/reclamante: tese e argumentos
- Advogado da parte ré/reclamada: tese e argumentos
- Testemunhas (2): perfil e o que cada uma sabe
- Perito (se aplicável)

### ROTEIRO DA AUDIÊNCIA
- Abertura
- Tentativa de conciliação
- Instrução (perguntas e respostas)
- Debates orais
- Sentença (o que o juiz deve considerar)

### GUIA DO PROFESSOR
- Como conduzir a atividade
- Pontos de aprendizagem esperados
- Dicas de debriefing após a simulação
""",
}


def coletar_informacoes(tipo_material: str) -> dict:
    """Coleta as informações necessárias para o material."""
    console.print(f"\n[bold cyan]Gerando: {tipo_material}[/bold cyan]\n")

    tema = Prompt.ask("[yellow]Tema ou assunto[/yellow] (ex: Responsabilidade Civil Extracontratual)")
    materia = Prompt.ask("[yellow]Disciplina/Matéria[/yellow] (ex: Direito Civil)")

    console.print("\n[bold]Nível da turma:[/bold]")
    for key, nivel in NIVEIS.items():
        console.print(f"  [{key}] {nivel}")
    nivel_key = Prompt.ask("Nível", choices=list(NIVEIS.keys()))
    nivel = NIVEIS[nivel_key]

    info = {"tema": tema, "materia": materia, "nivel": nivel}

    if tipo_material == "Plano de Aula":
        info["duracao"] = Prompt.ask("[yellow]Duração da aula[/yellow]", default="2 horas/aula (100 minutos)")
    elif tipo_material == "Questões de Avaliação (com gabarito)":
        info["num_questoes"] = Prompt.ask("[yellow]Número de questões objetivas[/yellow]", default="5")
        info["num_questoes_diss"] = Prompt.ask("[yellow]Número de questões dissertativas[/yellow]", default="2")

    return info


def gerar_material(tipo_material: str, info: dict) -> str:
    """Chama Claude para gerar o material didático."""
    client = anthropic.Anthropic()

    prompt_template = PROMPTS[tipo_material]

    # Preenche os campos disponíveis
    prompt = prompt_template.format(**{k: v for k, v in info.items() if k in prompt_template})

    console.print("\n[bold green]Gerando material com Claude...[/bold green]\n")

    material = ""
    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            material += text
            console.print(text, end="", markup=False)

    console.print()
    return material


def salvar_material(material: str, tipo_material: str, tema: str) -> str:
    """Salva o material em arquivo."""
    os.makedirs("materiais_didaticos", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tipo_arquivo = tipo_material.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
    tema_arquivo = tema[:30].lower().replace(" ", "_")
    filename = f"materiais_didaticos/{tipo_arquivo}_{tema_arquivo}_{timestamp}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {tipo_material}: {tema}\n")
        f.write(f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        f.write("---\n\n")
        f.write(material)

    return filename


def main():
    console.print(Panel.fit(
        "[bold cyan]GERADOR DE MATERIAL DIDÁTICO JURÍDICO[/bold cyan]\n"
        "Powered by Claude (Anthropic)",
        border_style="cyan"
    ))

    console.print("\n[bold]O que deseja criar?[/bold]\n")
    for key, nome in TIPOS_MATERIAL.items():
        console.print(f"  [{key}] {nome}")

    escolha = Prompt.ask("\nOpção", choices=list(TIPOS_MATERIAL.keys()))
    tipo_material = TIPOS_MATERIAL[escolha]

    info = coletar_informacoes(tipo_material)

    material = gerar_material(tipo_material, info)

    if Confirm.ask("\nDeseja salvar o material em arquivo?", default=True):
        filename = salvar_material(material, tipo_material, info["tema"])
        console.print(f"\n[green]Material salvo em: [bold]{filename}[/bold][/green]")

    console.print("\n[dim]Material gerado com IA — revise antes de usar em sala de aula.[/dim]")


if __name__ == "__main__":
    main()

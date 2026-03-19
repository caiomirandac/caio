# Caio — Automações Jurídicas com Claude

Ferramentas práticas para integrar Claude no dia a dia jurídico e de docência.

## Automações disponíveis

| Script | O que faz |
|--------|-----------|
| `automacoes/gerar_minuta.py` | Gera minutas de petições, contratos e pareceres |
| `automacoes/analisar_contrato.py` | Analisa contratos e aponta riscos e cláusulas problemáticas |
| `automacoes/calcular_prazos.py` | Calcula prazos processuais e cria eventos no Google Calendar |
| `automacoes/briefing_diario.py` | Lê sua agenda e gera um briefing do dia |
| `automacoes/material_didatico.py` | Gera planos de aula, casos práticos e questões de avaliação |

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sua-chave-aqui"
```

## Uso rápido

```bash
# Gerar uma petição inicial
python automacoes/gerar_minuta.py

# Analisar um contrato
python automacoes/analisar_contrato.py contrato.txt

# Calcular prazos e criar no Calendar
python automacoes/calcular_prazos.py

# Ver briefing do dia
python automacoes/briefing_diario.py

# Gerar plano de aula
python automacoes/material_didatico.py
```

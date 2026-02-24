# Refatorador de nomes em Netlist Verilog e SDF

Este script **refatora nomes gerados** (principalmente nomes escapados com `\` e índices como `bus[3]`) em:

- **Netlist Verilog** (`*.v` / `*.nl.v`)
- **Arquivo SDF** (`*.sdf`)

A ideia é **normalizar** identificadores para um formato mais “limpo”, evitando caracteres/constructos que costumam causar problemas em ferramentas de simulação, anotação de atraso, parsing ou integração (por exemplo, nomes com `\`, colchetes `[]`, e pontos `.` em hierarquias/nomes gerados).

---

## O que o script faz

Quando encontra nomes escapados (linhas que contêm `\`), o script aplica substituições do tipo:

### Netlist Verilog (`.v`)
- `].` → `__`
- `]`  → `_`
- `[`  → `_`
- `a.b` → `a__b` (quando `a` e `b` são alfanuméricos)
- `\blk` → `blk`
- Remove `\` (desescapa)

### SDF (`.sdf`)
Substituições equivalentes, mas considerando as barras de escape presentes no SDF:
- `\]\.` → `__`
- `\]`   → `_`
- `\[`   → `_`
- `a\.b` → `a__b` (quando `a` e `b` são alfanuméricos)

> **Saída:** o script escreve novos arquivos com sufixo `_refactor` no mesmo diretório do arquivo de entrada.

---

## Arquivos de saída

- Para netlist: `NOME_DO_ARQUIVO_refactor.v`
- Para SDF: `NOME_DO_ARQUIVO_refactor.sdf`

Exemplo:
- Entrada: `invent_pav2.nl.v` → Saída: `invent_pav2_nl_refactor.v`
- Entrada: `top.sdf` → Saída: `top_refactor.sdf`

*(Observação: o script também substitui `.` no `stem` por `_` ao formar o nome do arquivo de saída.)*

---

## Requisitos

- Python 3.8+ (recomendado)
- Bibliotecas padrão: `pathlib` e `re` (já vêm com o Python)

---

## Como usar

### 1) Coloque o script na pasta do seu projeto

Exemplo de estrutura:
```
./refactor_names.py
./invent_pav2.nl.v
./top.sdf
```

### 2) Execução automática (sem argumentos)

No bloco `if __name__ == "__main__":` o script pode ser chamado com:
```python
path_netlist_refatorada, path_sdf_refatorado = ferramenta.refactor_generated_names(None, None)
```

Nesse modo, ele faz **auto-detecção na pasta atual**:

- **Netlist (opcional):**
  - procura primeiro `*.nl.v`
  - se não existir, procura `*.v`
  - se não existir nenhum, apenas avisa e pula

- **SDF (opcional):**
  - procura `*.sdf`
  - se não existir, avisa e pula

Execução:
```bash
python3 refactor_names.py
```

### 3) Execução informando arquivos explicitamente (opcional)

Você pode chamar passando nomes/caminhos:

```python
path_netlist_refatorada, path_sdf_refatorado = ferramenta.refactor_generated_names(
    "invent_pav2.nl.v",
    "top.sdf"
)
```

- Se o caminho informado não existir, o script tenta procurar **um arquivo com o mesmo nome na pasta atual**.
- Se ainda assim não achar, ele emite **AVISO** e pula aquele arquivo.

---

## Como o script escolhe arquivos quando há mais de um

Se existirem múltiplos arquivos candidatos na pasta atual (por exemplo, vários `*.v`), o script:

1. respeita a prioridade de padrão (`*.nl.v` antes de `*.v`)
2. escolhe o arquivo **mais recente** (maior `mtime`)
3. imprime um **AVISO** listando os outros candidatos

---

## Logs / depuração

- Para netlist: imprime linhas “before/after” quando a linha contém `\`
- Para SDF: imprime “before/after” usando `print` (como no original)

---

## Limitações e observações

- A refatoração é feita **por linha**, e só altera linhas que contenham `\`.
- O script não valida sintaxe Verilog/SDF; ele apenas aplica substituições de texto.
- Se sua netlist tiver muitos `\` em contextos não relacionados a nomes (raro), revise rapidamente o diff.

---

## Fluxo de trabalho sugerido

1. Gere netlist e SDF.
2. Rode o script para produzir `*_refactor.v` e `*_refactor.sdf`.
3. Use os arquivos refatorados na simulação/anotação.

---

## Exemplo rápido

Pasta:
```
invent_pav2.nl.v
top.sdf
refactor_names.py
```

Rodar:
```bash
python3 refactor_names.py
```

Saída esperada:
```
invent_pav2_nl_refactor.v
top_refactor.sdf
```

---

# AutoSeguro — Motor de Precificação Securitária
## Atividade Avaliativa Prática — Qualidade e Teste de Software (QTS)

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Package Manager](https://img.shields.io/badge/managed%20by-uv-blueviolet.svg)](https://github.com/astral-sh/uv)
[![Testing Framework](https://img.shields.io/badge/tested%20with-pytest-0A9EDC.svg)](https://pytest.org/)
[![Coverage](https://img.shields.io/badge/branch%20coverage-100%25-brightgreen.svg)](https://pytest-cov.readthedocs.io/)

---

### 1. Visão Geral do Projeto
O **AutoSeguro** é um motor determinístico em Python voltado para cálculo atuarial e subscrição de apólices automotivas. O projeto foi desenvolvido com foco estrito na **Engenharia de Testes de Software**:
- **Especificação de Requisitos:** Centralizada no [PRD.md](PRD.md).
- **Governança de IA:** Diretrizes em [.cursorrules](.cursorrules) e relatório em [AI_USAGE.md](AI_USAGE.md).
- **Padrão AAA (Arrange, Act, Assert):** Aplicado em todos os testes unitários.
- **Técnicas Formais:** Particionamento de Equivalência (EP), Análise do Valor Limite (BVA) e Error Guessing.
- **Estrutura Enxuta:** 2 arquivos de teste com no máximo 5 testes em cada, atingindo **100% de cobertura de código e ramificações (branch coverage)**.

---

### 2. Estrutura do Repositório

```text
ATV-QTS/
├── .cursorrules              # Diretrizes de contexto e padrões de engenharia de software
├── AI_USAGE.md               # Relatório de transparência e auditoria do uso de IA
├── PRD.md                    # Documento de Requisitos e matrizes de teste (EP, BVA, Error Guessing)
├── README.md                 # Documentação e instruções de execução
├── VIDEO_SCRIPT.md           # Roteiro cronometrado para apresentação em vídeo (até 4 min)
├── pyproject.toml            # Configuração uv, pytest e medição de cobertura
├── app/                      # Sistema Sob Teste (SUT)
│   ├── __init__.py           # Exports públicos do pacote
│   └── calculator.py         # Motor de precificação, modelos e exceções de domínio
└── tests/                    # Suíte de Testes Unitários (2 arquivos, máx. 5 testes cada)
    ├── __init__.py
    ├── conftest.py           # Fixtures compartilhadas
    ├── test_calculator.py    # 5 testes: fatores atuariais, parcelamento, piso e cotação
    └── test_validations.py   # 5 testes: validações de fronteira (BVA) e error guessing
```

---

### 3. Regras de Negócio Implementadas

| Regra | Parâmetro | Comportamento e Limites | Exceção / Efeito |
|---|---|---|---|
| **RN-01** | Idade do Condutor | • 18 a 25 anos: Fator 1.30 (Jovem)<br>• 26 a 65 anos: Fator 1.00 (Padrão)<br>• 66 a 80 anos: Fator 1.20 (Sênior) | `< 18`: `InvalidAgeError`<br>`> 80`: `AgeLimitExceededError` |
| **RN-02** | Histórico de Sinistros | • 0 sinistros: Fator 0.90 (10% de bônus)<br>• 1 ou 2 sinistros: Fator 1.20 (20% de agravo)<br>• $\ge 3$ sinistros: Alto risco recusado | `< 0`: `InvalidClaimsError`<br>`>= 3`: `HighRiskRejectedError` |
| **RN-03** | Valor do Veículo | Faixa permitida: R$ 10.000,00 a R$ 200.000,00.<br>Taxa base: 4.0% (0.04) | `ValueOutOfBoundsError` |
| **RN-04** | Piso Mínimo | Piso de R$ 500,00 (ajustado automaticamente se o cálculo for inferior) | `is_floor_applied = True` |
| **RN-05** | Parcelamento | • 1 parcela: 5% de desconto à vista<br>• 2 a 6 parcelas: Parcelamento sem juros | `< 1` ou `> 6`: `InvalidInstallmentError` |

---

### 4. Execução Local dos Testes

O projeto utiliza o gerenciador ultrarrápido **uv** e Python 3.12+.

#### Instalação do Ambiente
```powershell
uv sync
```

#### Execução da Suíte de Testes
```powershell
uv run pytest -v
```

#### Medição com 100% de Cobertura e Ramificações
```powershell
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```

---

### 5. Relatório Comprovado de Cobertura (100%)

```text
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.13.15-final-0 _______________

Name                Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------
app\calculator.py      87      0     34      0   100%
---------------------------------------------------------------
TOTAL                  87      0     34      0   100%
Required test coverage of 100.0% reached. Total coverage: 100.00%
============================= 24 passed in 0.16s ==============================
```

---

### 6. Governança e Transparência no Uso de IA
- As regras de contexto para assistentes de IA estão no arquivo [.cursorrules](.cursorrules).
- O relatório de auditoria e transparência está registrado no arquivo [AI_USAGE.md](AI_USAGE.md).
- O roteiro para o vídeo demonstrativo de até 4 minutos encontra-se em [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md).

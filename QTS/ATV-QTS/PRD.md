# PRD — Product Requirements Document
## AutoSeguro: Motor de Precificação Securitária Simplificado

---

### 1. Visão Geral do Produto
O **AutoSeguro** é um motor determinístico em Python voltado para cálculo atuarial e subscrição básica de apólices automotivas. O sistema avalia a idade do condutor, seu histórico recente de sinistros e o valor do veículo para calcular o prêmio anual da apólice e gerar opções de parcelamento financeiro.

---

### 2. Regras de Negócio (RN)

#### **RN-01: Idade do Condutor e Fator de Risco**
- A contratação é restrita a condutores de **18 a 80 anos**.
- Idade menor que 18 anos dispara `InvalidAgeError`.
- Idade superior a 80 anos dispara `AgeLimitExceededError`.
- **Faixas etárias:**
  - **18 a 25 anos (Jovem):** Fator atuarial $1.30$ (+30%).
  - **26 a 65 anos (Padrão):** Fator atuarial $1.00$ (neutro).
  - **66 a 80 anos (Sênior):** Fator atuarial $1.20$ (+20%).

#### **RN-02: Histórico de Sinistros**
- A quantidade de sinistros deve ser um inteiro $\ge 0$. Valores negativos disparam `InvalidClaimsError`.
- **0 sinistros:** Bônus de não-sinistralidade de $10\%$ de desconto (fator $0.90$).
- **1 ou 2 sinistros:** Agravo tarifário de $20\%$ (fator $1.20$).
- **$\ge 3$ sinistros:** Recusa por alto risco via `HighRiskRejectedError`.

#### **RN-03: Valor do Veículo e Taxa Base**
- O valor do veículo deve ser positivo ($> 0$). Valores $\le 0$ disparam `InvalidValueError`.
- Intervalo aceito para subscrição: **R$ 10.000,00 a R$ 200.000,00**. Valores fora dessa faixa disparam `ValueOutOfBoundsError`.
- **Taxa base:** $4.0\%$ ($0.04$) sobre o valor do veículo:
  $$\text{Prêmio Base} = \text{Valor do Veículo} \times 0.04$$

#### **RN-04: Cálculo do Prêmio Final e Piso Mínimo**
- Fórmula de precificação:
  $$\text{Prêmio Bruto} = \text{Prêmio Base} \times \text{Fator Idade} \times \text{Fator Sinistros}$$
- **Piso Mínimo de R$ 500,00:** Se $\text{Prêmio Bruto} < 500,00$, o prêmio final é ajustado para R$ 500,00 com a flag `is_floor_applied = True`. Caso contrário, mantém-se o valor calculado (`is_floor_applied = False`).

#### **RN-05: Modalidades de Parcelamento**
- Permitido parcelar de **1 a 6 vezes**. Fora desse intervalo dispara `InvalidInstallmentError`.
- **1 parcela (À vista):** Desconto de $5\%$ sobre o prêmio final (`final_premium * 0.95`).
- **2 a 6 parcelas:** Parcelamento sem juros (`final_premium / parcelas`).

---

### 3. Matrizes da Engenharia de Testes

#### 3.1. Particionamento de Equivalência (EP)

| Variável | Classes Válidas | Classes Inválidas |
|---|---|---|
| **Idade** | [18..25] (Jovem)<br>[26..65] (Padrão)<br>[66..80] (Sênior) | $[-\infty..17]$ (`InvalidAgeError`)<br>$[81..+\infty]$ (`AgeLimitExceededError`) |
| **Sinistros** | 0 (Bônus)<br>[1..2] (Agravado) | $[-\infty..-1]$ (`InvalidClaimsError`)<br>$[3..+\infty]$ (`HighRiskRejectedError`) |
| **Valor Veículo** | [10.000,00..200.000,00] | $\le 0$ (`InvalidValueError`)<br>$]0..9.999,99]$ ou $> 200.000,00$ (`ValueOutOfBoundsError`) |
| **Parcelamento** | 1 (À vista c/ desc.)<br>[2..6] (Sem juros) | $\le 0$ ou $\ge 7$ (`InvalidInstallmentError`) |

---

#### 3.2. Análise do Valor Limite (BVA)

| Parâmetro | Ponto Testado | Valor | Resultado Esperado |
|---|---|---|---|
| **Idade** | Mínimo - 1 | 17 | `InvalidAgeError` |
| **Idade** | Mínimo / Limites | 18, 25 | Fator 1.30 |
| **Idade** | Transição Padrão | 26, 65 | Fator 1.00 |
| **Idade** | Transição Sênior | 66, 80 | Fator 1.20 |
| **Idade** | Máximo + 1 | 81 | `AgeLimitExceededError` |
| **Sinistros** | Mínimo - 1 | -1 | `InvalidClaimsError` |
| **Sinistros** | Limites válidos | 0 (0.90), 1 (1.20), 2 (1.20) | Fatores corretos |
| **Sinistros** | Limiar de recusa | 3 | `HighRiskRejectedError` |
| **Valor Veículo** | Zero / Negativo | 0.00 | `InvalidValueError` |
| **Valor Veículo** | Limites e bordas | 9.999,99 / 10.000,00 / 200.000,01 | Erro / Válido / Erro |
| **Parcelas** | Limites ilegais | 0 e 7 | `InvalidInstallmentError` |

---

#### 3.3. Error Guessing
- Passagem de booleanos em campos numéricos (`age=True`, `claims=True`, `installments=True`), barrados pela tipagem defensiva estrita.
- Coerção indevida de strings em valores numéricos.
- Acionamento do piso mínimo protetivo de R$ 500,00.

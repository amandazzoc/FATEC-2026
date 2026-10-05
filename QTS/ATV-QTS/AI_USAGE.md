# Relatório de Transparência e Governança de IA (AI_USAGE.md)
## Disciplina: Qualidade e Teste de Software (QTS)

---

### 1. Ferramenta Utilizada
- **Plataforma / IDE:** Google Antigravity IDE
- **Modelo de Linguagem:** Gemini 3.8 Flash
- **Ambiente de Execução:** Python 3.13, Gerenciador `uv`, `pytest 9.1.1`, `pytest-cov 7.1.0` no Windows 11

---

### 2. Metodologia de Emprego da Inteligência Artificial

A Inteligência Artificial Generativa foi utilizada de forma controlada e orientada por especificações formais de engenharia de software nas seguintes etapas:

1. **Especificação do Domínio e PRD:**
   - Criação da especificação do motor de subscrição e tarifação securitária (*AutoSeguro*).
   - Definição estruturada das regras de negócio (RN-01 a RN-05), requisitos funcionais e mapeamento de exceções.
2. **Engenharia de Testes de Caixa-Preta e Caixa-Branca:**
   - Concepção das matrizes de **Particionamento de Equivalência (EP)** para variáveis contínuas e discretas.
   - Determinação das fronteiras críticas na **Análise do Valor Limite (BVA)** (pontos $N-1, N, N+1$).
   - Levantamento de hipóteses de falha empírica para a técnica de **Error Guessing** (como a peculiaridade do Python em tratar `bool` como subclasse de `int`).
3. **Geração Automatizada de Casos de Teste (Scaffolding):**
   - Criação de suítes de testes parametrizadas (`@pytest.mark.parametrize`) aderentes ao padrão **AAA (Arrange, Act, Assert)**.
   - Aplicação de marcadores semânticos (`@pytest.mark.unit`, `@pytest.mark.ep`, `@pytest.mark.bva`, `@pytest.mark.error_guessing`).
4. **Otimização de Cobertura de Ramificações:**
   - Apoio na identificação de ramos (*branches*) não executados para atingimento de 100% de cobertura no pacote `app`.

---

### 3. Metodologia de Auditoria Humana e Validação

Para garantir a confiabilidade, originalidade e correção do software entregue, foram executadas as seguintes etapas de auditoria humana:

| Etapa de Auditoria | Ação Realizada | Resultado da Verificação |
|---|---|---|
| **Auditoria Atuarial e Matemática** | Conferência manual dos cálculos de prêmio base, fatores de risco combinados, juros de parcelamento e regras de arredondamento (`round(..., 2)`). | Fórmulas matematicamente consistentes, sem divergências de centavos. |
| **Auditoria de Tipagem e Sintaxe** | Inspeção dos modelos dataclass com Type Hints estritos e checagem defensiva de tipos primitivos (`isinstance(val, int) and not isinstance(val, bool)`). | Impossibilidade de injeção de tipos inválidos ou booleanos mascarados. |
| **Auditoria de Conformidade AAA** | Leitura linha a linha dos arquivos de teste para certificar que cada teste unitário possui os blocos `# [Arrange]`, `# [Act]` e `# [Assert]`. | 100% dos testes seguem estritamente a convenção AAA. |
| **Auditoria de Execução Local** | Execução dos comandos `uv run pytest -v` e `uv run pytest --cov=app --cov-branch --cov-report=term-missing` diretamente no terminal da máquina de desenvolvimento. | Todos os testes aprovados com status verde e 100% de cobertura em instruções e ramificações. |

---

### 4. Conclusão de Governança
O uso da IA neste trabalho atuou como um acelerador de produtividade para a geração de código padronizado e casos de teste exaustivos, enquanto o controle de regras, as decisões de arquitetura e a validação do comportamento do sistema foram conduzidos pelo estudante sob os critérios de rigor da disciplina de QTS.

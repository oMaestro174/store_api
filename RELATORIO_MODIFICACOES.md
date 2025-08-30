# Relatório de Modificações - Desafio Store API

## Introdução

Este documento detalha as modificações e melhorias implementadas neste projeto, que é um **fork** do repositório original `digitalinnovationone/store_api`. As alterações foram realizadas como parte de um desafio final, visando aprimorar a robustez, a flexibilidade e a capacidade de consulta da API.

É importante notar que o repositório base foi estruturado para demonstrar a criação de uma API com a metodologia **TDD (Test-Driven Development)**. No entanto, as modificações aqui descritas foram implementadas de forma direta, focando na entrega funcional dos requisitos do desafio, sem a aplicação do ciclo TDD (Red-Green-Refactor) para estas alterações específicas.

As principais áreas de aprimoramento foram:
1.  **Tratamento Avançado de Exceções:** Mapeamento de erros específicos para fornecer feedback claro ao usuário.
2.  **Integridade dos Dados:** Lógica aprimorada para o rastreamento de atualizações.
3.  **Consultas Avançadas:** Implementação de filtros dinâmicos na listagem de produtos.

A seguir, cada uma dessas implementações é detalhada.

---

## 1. Tratamento Avançado de Exceções na Controller

Para melhorar a previsibilidade e a experiência do desenvolvedor que consome a API, o tratamento de erros foi centralizado na camada de `controllers`, capturando exceções do `usecase` e do banco de dados para transformá-las em respostas HTTP padronizadas.

### a) Conflito na Criação de Produtos (Chave Duplicada)

-   **O que foi feito?** A API agora impede a criação de produtos com nomes duplicados, que é uma regra de negócio comum para garantir a consistência do catálogo.
-   **Implementação:** A rota `POST /` agora captura a exceção `pymongo.errors.DuplicateKeyError`. Quando essa exceção ocorre, a API retorna um status **`HTTP 409 Conflict`** com uma mensagem amigável.
-   **Exemplo de Resposta de Erro:**
    ```json
    {
      "detail": "Product with name 'Iphone 14 Pro Max' already exists."
    }
    ```

### b) Recurso Não Encontrado (Not Found)

-   **O que foi feito?** As rotas que operam sobre um recurso específico (`GET /{id}`, `PATCH /{id}`, `DELETE /{id}`) agora retornam uma resposta clara quando o ID do produto não é encontrado.
-   **Implementação:** A exceção customizada `NotFoundException`, lançada pela camada de `usecase`, é capturada na `controller`, que retorna um status **`HTTP 404 Not Found`**.
-   **Exemplo de Resposta de Erro (ao tentar atualizar um produto inexistente):**
    ```json
    {
      "detail": "Product not found with filter: 123e4567-e89b-12d3-a456-426614174000"
    }
    ```

---

## 2. Lógica de Atualização do Campo `updated_at`

Para garantir a rastreabilidade das modificações, a lógica do campo `updated_at` foi aprimorada com um comportamento duplo.

-   **O que foi feito?**
    1.  **Atualização Automática:** Ao modificar qualquer dado de um produto através da rota `PATCH /{id}`, o campo `updated_at` é **automaticamente atualizado** para a data e hora (UTC) do momento da modificação.
    2.  **Atualização Manual:** O sistema também permite que o campo `updated_at` seja **enviado explicitamente no corpo da requisição**, oferecendo flexibilidade para cenários de migração de dados ou correções manuais.
-   **Implementação:** O schema `ProductUpdate` foi ajustado para aceitar o campo `updated_at` opcionalmente. No `product_usecase`, a data de atualização é definida para `datetime.utcnow()` antes que os dados do corpo da requisição sejam aplicados, garantindo que o valor enviado pelo usuário tenha precedência, se existir.

---

## 3. Filtragem de Produtos por Faixa de Preço

Para permitir consultas mais poderosas e específicas, a rota de listagem de produtos foi aprimorada com filtros de preço.

-   **O que foi feito?** A rota `GET /` agora aceita os *query parameters* `min_price` e `max_price` para filtrar produtos dentro de uma faixa de valor.
-   **Implementação:** Os parâmetros são recebidos na `controller` e repassados para o `product_usecase`, que constrói uma query dinâmica no MongoDB utilizando os operadores `$gt` (greater than) e `$lt` (less than).

-   **Exemplos de Uso:**
    -   **Listar produtos com preço maior que 5000:**
        ```http
        GET /?min_price=5000
        ```
    -   **Listar produtos com preço menor que 8000:**
        ```http
        GET /?max_price=8000
        ```
    -   **Listar produtos com preço entre 5000 e 8000:**
        ```http
        GET /?min_price=5000&max_price=8000
        ```

## Conclusão

As modificações implementadas tornam a **Store API** significativamente mais robusta, intuitiva e funcional. O tratamento de erros aprimorado, a lógica de atualização inteligente e as novas capacidades de filtragem fornecem uma base sólida para a evolução contínua da aplicação.

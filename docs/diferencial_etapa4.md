# Diferencial da Etapa 4: diagnóstico sintático guiado pela gramática

## Problema educacional

O estudante iniciante pode reconhecer que há um erro de sintaxe sem compreender **qual regra gramatical foi violada**. A proposta do LexLab é tornar visível a ligação entre o texto digitado, os tokens e a regra envolvida na análise.

## Contribuição implementada nesta atualização

O LexLab apresenta, em um mesmo ambiente, (a) tokens do scanner, (b) uma AST navegável quando a estrutura é válida, e (c) diagnósticos sintáticos com **localização, símbolo encontrado, símbolos esperados, regra gramatical e uma sugestão simples** para revisão do código. Os nós da AST permitem selecionar no editor o trecho associado, quando a localização está disponível. Essa é uma forma específica de apresentação e **não uma técnica inédita de parsing**.

A análise sintática usa um parser descendente recursivo com precedência de operadores, implementado no projeto. A interface não executa o código digitado. O parser não funciona como um compilador completo de Python.

## Relação com os trabalhos relacionados

Barbosa, Faria e Campano Junior (2021, *Análise de Ferramentas de Compiladores em Ambientes Virtualizados*, DOI 10.5753/rbie.2021.2302) comparam cinco ferramentas e descrevem experiências de alunos com recursos de análise sintática. Borela et al. (2025, *Uma Ferramenta Educacional de Apoio ao Ensino de Compiladores*, DOI 10.5753/wei.2025.7407) descrevem um ambiente web que apresenta tokens e árvores, com avaliação de percepção de uso. A contribuição do LexLab não está em afirmar exclusividade na visualização de tokens/árvores, mas em colocar **o diagnóstico explicativo vinculado à regra da gramática** em primeiro plano para um subconjunto didático Python-like.

## Como demonstrar

- Código válido: `resultado = 10 + 5 * 2`. A AST organiza a multiplicação como operando direito da adição; a tabela de tokens permanece visível.
- Código inválido: `if nota >= 7` seguido de `    pass`. O parser informa que faltou `:`, a regra correspondente, o elemento esperado e uma sugestão.
- Erro léxico: `resultado = 10 @ 2`. O scanner identifica `@`, e o parser não é executado.

## Como avaliar, sem pressupor resultados

Testes unitários verificam a estrutura da AST, precedência, localização e campos do erro. Testes de navegador verificam se AST e explicações aparecem. Para medir percepção/clareza, será aplicado um questionário com estudantes da área de Computação após tarefas de análise; esses resultados **não foram coletados nesta etapa**. Nenhuma melhora de aprendizagem é declarada antes de avaliação apropriada.

## Limitações

As mensagens são montadas por regras do próprio parser e podem não cobrir toda combinação malformada; o subconjunto não inclui funções definidas pelo usuário, `for`, listas, dicionários, análise semântica ou execução do programa. Não há integração com IA; o recurso opcional Ollama do enunciado foi deixado para trabalho futuro, para priorizar o parser e o diagnóstico verificável.

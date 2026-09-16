# Justificativa Técnica

## Linguagem — Python 3.11+

Python foi escolhido por ser a linguagem principal da equipe e por sua ampla
adoção em projetos de back-end, automação e ciência de dados. Sua sintaxe
expressiva e o ecossistema de bibliotecas maduras reduzem o tempo de
desenvolvimento e facilitam a manutenção do código.

## Framework — FastAPI

FastAPI foi escolhido por três razões principais:

1. **Documentação automática:** gera a interface Swagger UI em `/docs` sem
   configuração adicional, permitindo testar todos os endpoints sem ferramenta externa.
2. **Validação integrada com Pydantic:** os schemas de entrada e saída são
   validados automaticamente, lançando erros HTTP 422 com mensagens claras
   quando os dados estão incorretos.
3. **Tipagem estática:** o uso de type hints torna o código mais legível e
   facilita a identificação de erros em tempo de desenvolvimento.

## Persistência — Arquivos JSON locais

A persistência em arquivos JSON foi escolhida por simplificar o ambiente de
execução: não é necessário instalar ou configurar um banco de dados. Os arquivos
`data/laboratorios.json` e `data/reservas.json` são lidos e escritos diretamente
pela camada de repositório. Essa abordagem é adequada para o escopo acadêmico do
projeto e pode ser substituída por um banco de dados relacional sem alterar as
camadas de service ou router — graças ao padrão Repository.

## Arquitetura — Camadas

O projeto adota uma arquitetura em camadas com responsabilidades bem definidas:

| Camada       | Pasta          | Responsabilidade                                    |
|--------------|----------------|-----------------------------------------------------|
| Apresentação | `routers/`     | Receber requisições HTTP e devolver respostas       |
| Aplicação    | `services/`    | Conter as regras de negócio do sistema              |
| Persistência | `repositories/`| Ler e escrever dados nos arquivos JSON              |
| Domínio      | `models/`      | Representar as entidades do sistema                 |
| Contrato     | `schemas/`     | Definir os DTOs de entrada e saída (Pydantic)       |

Essa separação garante baixo acoplamento entre as camadas: se a persistência
mudar de JSON para SQLite, apenas os repositórios precisam ser alterados.
Se a API mudar de REST para GraphQL, apenas os routers precisam ser alterados.

## Versionamento — Git + GitHub

Git foi utilizado para controle de versão com commits semânticos
(conventional commits). O repositório está hospedado no GitHub e organizado
com branches por feature, integradas via Pull Request para a branch `main`.
# Autorizador de débito de cartão

Arquitetura de referência para autorizador de débito de cartão totalmente serverless na AWS.

## Objetivo

Montar uma arquitetura que atenda os requisitos de um sistema autorizador de débitos de cartão, que opera do lado da instituição financeira.
A intenção não é reproduzir um sistema exatamente fiel ao real, pois é um sistema complexo. A ideia é mostrar de forma macro como poderia funcionar atendendo os requisitos básicos.

## Requisitos

Um autorizador de débito possui alguns requisitos importantes, que são:
* Tempo limite para processamento de 3 segundos
* Atomicidade no débito, a fim de evitar débitos concorrentes do mesmo saldo

Existem outros requisitos funcionais para um projeto como este, mas para esse projeto vamos nos limitar a estes basicamente.

## Arquitetura

A arquitetura abaixo é a planejada para exercitar de forma macro o funcionamento da aplicação.

![](imagens/AutorizadorDebitoCartao.jpg)

Vamos exercitar o débito em conta e o processamento dele após a confirmação do débito.

### Melhorias

* Utilização de Lambda layer para a biblioteca `psycopg2` deve trazer melhoria de performance
* Utilização de RDS Proxy deve trazer melhoria de performance (principalmente pela reutilização de conexões)
* Possibilidade de criação de um cliente ISO8583 para ficar mais fiel ao projeto de autorização de débito

## Como usar?

O projeto está totalmente funcional e com todas as configurações automatizadas.
Basta realizar o deploy utilizando Serverless Framework e *voilà*.

```shell script
sls deploy
```

Para criar uma conta basta executar a seguinte requisição (usar a URL base gerada no deploy):
```shell script
curl -X POST  https://XYZ.execute-api.us-east-1.amazonaws.com/dev/conta -d '{"agencia": 1000, "numeroConta": 1234, "saldo": 1000, "numeroCartao": 1111222233334444}' -H 'Content-Type: application/json'
```

Para realizar um débito, execute o comando abaixo:
```shell script
curl -X POST https://XYZ.execute-api.us-east-1.amazonaws.com/dev/debito -d '{"numeroCartao": 1111222233334444, "valor": 50}' -H 'Content-Type: application/json'
```

### Output

Quando fizer o deploy dessa aplicação serão criados os seguintes recursos:
* VPC
* Subnet
* SecurityGroup
* Aurora Serverless (PostgreSQL)
* Lambda Function
    * Criar conta corrente: inclui no banco de dados uma nova conta corrente
    * Debitador: efetua o débito em conta corrente
    * Contabilizar: registra a contabilização da operação
    * Registrar Lançamento: registra o lançamento de débito para sensibilizar o extrato de conta corrente
    
 Ao criar uma conta corrente utilizando o endpoint REST, a função vai automaticamente criar a tabela de conta corrente.
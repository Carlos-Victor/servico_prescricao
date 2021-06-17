
# Prescrição Médica

A missão da iClinic é descomplicar a saúde no Brasil levando mais gestão a clínicas e consultórios através da tecnologia e, com isso, possibilitar que médicos e outros profissionais promovam mais saúde aos seus pacientes.


## Rode Localmente

Clone o projeto

```bash
  git clone https://github.com/Carlos-Victor/servico_prescricao
```

Entre na source do projeto

```bash
  cd source
```

Instale as dependências

```bash
  pip install -r requirements.txt
```


Entre com os valores das variaveis de ambiente

```bash
export POSTGRES_USER=''
export POSTGRES_PASSWORD=''
export POSTGRES_HOST=''
export POSTGRES_PORT='0'
export POSTGRES_DB=''
export CLINICS_BEARER=''
export PHYSICIANS_BEARER=''
export PATIENTS_BEARER=''
export METRICS_BEARER=''
export CLINICS_HOST=''
export PHYSICIANS_HOST=''
export PATIENTS_HOST=''
export METRICS_HOST=''
```

Inicie o servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

  ## Environment Váriaveis


`API_KEY`

`POSTGRES_USER`
`POSTGRES_PASSWORD`
`POSTGRES_HOST`
`POSTGRES_PORT`
`POSTGRES_DB`
`CLINICS_BEARER`
`PHYSICIANS_BEARER`
`PATIENTS_BEARER`
`METRICS_BEARER`
`CLINICS_HOST`
`PHYSICIANS_HOST`
`PATIENTS_HOST`
`METRICS_HOST`


## Instalação

O Projeto possui docker e docker-compose, para ser instalado deve seguir o compose que se encontra na raiz do projeto
Nele se encontra uma configuração do projeto em Django e um Banco de Dados em Postgres

```bash 
    docker-compose build
    docker-compose up -d
```
      
## Rotas

|Verb  |URI Pattern              
:----:|-------------------------|
| POST  | /prescriptions

## Uso/Exemplo

Realize um Post para o endpoint /prescriptions 
```bash
curl -X POST \
  http://localhost:8000/prescriptions \
  -H 'Content-Type: application/json' \
  -d '{
  "clinic": {
    "id": 1
  },
  "physician": {
    "id": 1
  },
  "patient": {
    "id": 1
  },
  "text": "Dipirona 1x ao dia"
}'
```

## BPMN

![BPMN](diagram.svg )

  
## Executar os Testes

Para executar os testes com o projeto em docker

```bash
  docker-compose run prescription python manage.py test
```

  
## Relacionado


[Página do Desafio](https://github.com/iclinic/iclinic-python-challenge)

  
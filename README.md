# PING PONG

Sistema que verifica periódicamente se o site está ativo através de uma requisição http.

> Acesse a documentação da API através do endpoint `/docs` ex: http://127.0.0.1:8000/docs#/

## Como funciona

O sistema realiza requisições a cada 5 minutos em todos os sites registrados em nossa base de dados. Todos os resultados das requisições são armazenados para que seja possível identificar possíveis falhas ocorridas no sistema.

### Como registrar um site

Para que um site seja verificado periódicamente se está ativo, é necessário registrá-lo. Para isso, basta consumir o endpoint `/site` utilizando o método POST e enviando duas informações:
 * name: nome do site;
 * url: url do seu site;

> obs: recomendamos fortemente registrar o site com um endpoint que tenha de retorno apenas um json informando "status ok" para que não haja problemas de timeout! Páginas iniciais de sites podem ter um tempo maior de carregamento, fazendo com que o sistema identifique que o site está fora por conta de timeout! Outro ponto muito importante é a parte de bloqueio de rede pela quantidade de requisição! Pode se tornar mais fácil liberar requisições do nosso sistema para o endpoint "/health" pois o intúito do endpoint é justamente identificar se o sistema está rodando. Muitas vezes, requisições em excesso para sites podem ser considerados como ataque pelas equipes de SEC, fazendo com que o nosso sistema seja bloqueado. Acesse a documentação da nossa API e veja um exemplo prático de como funciona um endpoint /health.

Exemplo de como consumir o endpoint:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/site/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Meu site",
  "url": "https://example.com/health/"
}'
```
### Como visualizar todos os sites registrados

Para visualizar todos os sites registrados, basta consumir o endpoint `/site` através do método GET. Exemplo:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/site/' \
  -H 'accept: application/json'
```

### Como visualizar os logs de monitoramento de um único site

É possível visualizar os logs de monitoramento através do endpoint `/logs` utilizando o método GET. É necessário ter o ID do site que você quer visualizar, por exemplo:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/logs/1' \
  -H 'accept: application/json'
```

## Como rodar o projeto

É possível rodar o projeto de duas maneiras: Com docker e sem docker :)

### Com docker

> Recomendo rodar o projeto via docker para fazer deploy em produção!

#### Construindo a imagem Docker

```
docker build -t ping-pong .
```

#### Rodando o container

```
docker run -d -p 8000:8000 --name ping-pong ping-pong
```

### Sem docker

É necessário ter python instalado na máquina (de preferência 3.12) ou instalado através de um gerenciador de versões do python (pyenv).

> Recomendo esse método sem docker para caso você queira ter um pouquinho mais de velocidade e praticidade para poder debbugar o código sem precisar rodar o docker attach e sem querer matar o container.

#### Instalando dependências

Crie e ative o ambiente virtual (caso já tenha criado para esse projeto, só ative):
```
python -m venv venv
source venv/bin/activate
```

Agora estamos aptos para instalar as dependências:
```
pip install -r requirements.txt
```

Caso você for contribuir para o projeto desenvolvendo, é necessário instalar as dependências dev:
```
pip install -r requirements-dev.txt
```

#### Subindo a aplicação

Com todas as dependências instaladas, basta rodar o uvicorn:

```
uvicorn src.main:app --reload
```

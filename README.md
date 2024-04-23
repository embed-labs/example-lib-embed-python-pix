# example-lib-embed-python-pix

Exemplo demonstrativo para o uso da `lib-embed` no transações com PIX.

## Instalação

### Requisitos

É necessário o Python 3 instalado em sua máquina.

Verifique a necessidade de instalar as dependências:
- PIP
- PILLOW

### Clonar

```git
git clone git@github.com:org-dev-embed/example-lib-embed-python-pix.git
```

### Configurações 

Acessar o diretório, modificar o arquivo .env.example, renomeando para .env e colocando os valores passados pelo time de integração

```
cd example-lib-embed-python-pix
mv .env.example .env
```

Feito isso, executar o programa com Python

```
python3 embed_ui.py
```

### Sobre o exemplo

Este exemplo contem três itens fundamentais:
1. embed_lib.py: carregamemento das bibliotecas 
2. embed_api.py: utilização dos métodos para transações/operações com PIX
3. embed_ui.py: interface gráfica simplificada que consome os métodos

*OBS*: em **embed_ui.py** verifique as funções **processar** de cada item, ali tem o caminho das pedras para integração

## API

### Fluxos
Vamos definir o fluxo que deve ser seguido para que sua implementação seja realizada seguindo as melhores práticas no uso da nossa API

#### Geral
```mermaid
graph TD;
    A(1 - embed_configurar) -->B(2 - embed_iniciar);    
    B --> C(3 - embed_processar);
    C --> D{4 - embed_processar};
    D --> |processando|D;
    D --> E(5 - embed_finalizar);
```

#### Transações

1. Obter Base64
```mermaid
flowchart TD;
    base1(embed_iniciar\ninput = pix) -- result.status_code ==  0 --> base2(embed_processar\ninput = get_qrcode;10000);
    base2 -- result.status_code ==  1 --> base3(embed_processar\ninput = get_status);
    base3 -- result.status_code ==  1 --> base3;
    base3 -- result.status_code ==  0 --> base4(embed_finalizar\ninput = N/A);
```

### Métodos

#### 1. Configurar 

Este método realiza a configuração do produto, para este caso PIX

##### 1.1. Assinatura

```c++
char* embed_configurar(char* input);
```

##### 1.2. Parâmetros

Aqui estão as definições para _input_ e _output_ para este método

###### 1.2.1. Input

Pode ser parametrizado de duas maneiras:

1. JSON
```javascript
{
    "configs": {
        "produto": "pos",                                        
        "sub_produto": "1",                                       
        "infos": {
            "timeout": "300",
            "api_key": "",              // gerado pelo time de integração
            "prod_id": "",              // gerado pelo time de integração
            "pid": "",                  // gerado pelo time de integração
            "conta": "",                // gerado pelo time de integração (temporário para piloto)
            "nome": "",                 // informado pelo cliente
            "email": "",                // informado pelo cliente
            "telefone": "",             // informado pelo cliente
            "documento": "",            // informado pelo cliente
        }
    }
}
```
2. Metaparâmetro (obedecendo a sequência)
```c
"pos;1;300;api_key;prod_id;pid;nome;email;telefone;documento;conta"
```

###### 1.2.2. Output

O retorno para este método consiste em um Json (sempre), no seguinte formato:

```json
{
  "codigo": 0,
  "mensagem": "Sucesso"
}
```

#### 2. Iniciar

Este método realiza a inicialização do produto, para este caso POS

##### 2.1. Assinatura

```c++
char* embed_iniciar(char* input);
```

##### 2.2. Parâmetros

Aqui estão as definições para _input_ e _output_ para este método.

###### 2.2.1. Input

Pode ser parametrizado de duas maneiras:

1. JSON
```json
{
    "iniciar": {
        "operacao": "pix"
    }
}
```
2. Metaparâmetro
```c
"pix"
```
###### 2.2.1.1 Metaparâmetro (obedecendo a sequência)
```c
"{operacao};{valor};{tid}"
```

###### 2.2.2. Output

O retorno para este método consiste em um JSON (sempre), no seguinte formato:

```json
{
    "codigo": 0,
    "mensagem": "Sucesso",
}
```

#### 3. Processar

Este método realiza o processamento de transações POS

##### 3.1. Assinatura

```c++
char* embed_processar(char* input);
```

##### 3.2. Parâmetros

Aqui estão as definições para _input_ e _output_ para este método.

###### 3.2.1. Input

Temos cinco modalidades de processamento que podem ser realizadas:
1. get_base64
2. get_chave_pix
3. get_status (transação atual)
4. get_reembolso

Estas modalidades podem ser parametrizadas de duas formas:

1. JSON
```javascript
// Get Qrcode (base64)
{
    "processar": {
        "operacao": "get_base64",       // obtém o qrcode base64 
        "valor": "",                    // em centavos (se R$ 1,00 logo 100)
    }
}
// Get Chave Pix (chave_pix)
{
    "processar": {
        "operacao": "get_chave_pix",        // obtém a chave pix
        "valor": "",                        // em centavos (se R$ 1,00 logo 100)
    }
}
// Get Status
{
    "processar": {
        "operacao": "get_status",
        "tid": "",                  // opcional, para pegar o status de uma transação específica
    }
}
// Get Reembolso
{
    "processar": {
        "operacao": "get_reembolso",
        "tid": "",                  // opcional, para fazer o reembolso de uma transação específica
    }
}
```
2. Metaparâmetro (obedecendo a sequência)
```c
// Get Qrcode (base64)
"get_base64;valor"
// Get Status
"get_status"
```
###### 3.2.2. Output

O retorno para este método consiste em um JSON (sempre), no seguinte formato:

```javascript
// Get Qrcode (base64)
{
    "codigo": 0,
    "mensagem": "Sucesso",
    "resultado": {
        "status_code": "1",
        "status_message": "1",
        "base64": "",
        "tid": "",   
    }
}
// Get Chave Pix (chave_pix)
{
    "codigo": 0,
    "mensagem": "Sucesso",
    "resultado": {
        "status_code": "1",
        "status_message": "1",
        "chave_pix": "",
        "tid": "",   
    }
}
// Get Status | Get Reembolso
{
    "codigo": 0,
    "mensagem": "Sucesso",
    "resultado": {
        "status_code": 1,
        "status_message": "processando"
    }
}
```

#### 4. Finalizar

Este método realiza a finalização de transações PIX

##### 4.1. Assinatura

```c++
char* embed_finalizar(char* input);
```

##### 4.2. Parâmetros

Aqui estão as definições para os _inputs_ e _output_ para este método.

###### 4.2.1. Input

Pode ser parametrizado de duas maneiras:

1. JSON
```json
{
    "finalizar": {
        "operacao": "",
    }
}
```
2. Metaparâmetro
```c
""
```

###### 4.2.2. Output

O retorno para este método consiste em um JSON (sempre), no seguinte formato:

```json
{
    "codigo": 0,
    "mensagem": "Sucesso",
    "resultado": {
        "status_code": 1,
        "status_message": "iniciado"
    }
}
```

#### 5. Obter Valor

Este método responsável por buscar um valor contido em uma chave ou objeto de um JSON válido. 

##### 5.1. Assinatura

```c++
char* embed_obter_valor(char* json, char* key);
```

##### 5.2. Parâmetros

Aqui estão as definições para os _inputs_ e _output_ para este método.

###### 5.2.1. Input

Deve ser informado sempre um String com conteúdo JSON.

```json
// Json
{
    "key1": "value1",
    "key2": {
        "key21": "value21",
        "key22": "value22",
        "key23": "value23",
        "key24": "value24",
        "key25": "value25"
    }
}
```
```c
// Key
"key2.key25"
```

###### 5.2.2. Output

Será um String com valor informado em _key_ se conter em _json_ 

```c
// Value
"value25"
```

### Retornos 

Os possíveis retornos para os métodos utilizando o produto PIX conforme as tabelas abaixo

| codigo | mensagem |
| - | - |
| 0 | Sucesso | 
| -1 | Erro |
| -2 | Deserialize |
| -3 | ProviderError |
| -11 | PixError |
| -12 | PixMissingParameter |
| -13 | PixInvalidOperation |
| -14 | PixInputBadFormat |

| status_code | status_message |
| - | - |
| -1 | erro |
| 0 | finalizado |
| 1 | processando |

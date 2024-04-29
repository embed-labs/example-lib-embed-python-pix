import os
import base64
import dotenv
import embed_lib as lib

STATUS_CODE = "resultado.status_code"

def configurar():
    dotenv.load_dotenv()

    PRODUTO = "pix"                         # produto de pagamento (atual pix)
    SUB_PRODUTO = os.getenv('SUB_PRODUTO')  # fornecedor/banco/parceiro (atual 1)
    TIMEOUT = "250"                         # timeout para consulta de status (para gerar qrcode ou reembolso)
    API_KEY = os.getenv('API_KEY')          # fonecido pela integração
    PROD_ID = os.getenv('PROD_ID')          # fonecido pela integração
    PID = os.getenv('PID')                  # fonecido pela integração
    CONTA = os.getenv('CONTA')              # fonecido pela integração
    NOME = os.getenv('NOME')                # dado informado pelo parceiro
    EMAIL = os.getenv('EMAIL')              # dado informado pelo parceiro
    TELEFONE = os.getenv('TELEFONE')        # dado informado pelo parceiro
    DOCUMENTO = os.getenv('DOCUMENTO')      # dado informado pelo parceiro

    input = f"{PRODUTO};{SUB_PRODUTO};{TIMEOUT};{API_KEY};{PROD_ID};{PID};{NOME};{EMAIL};{TELEFONE};{DOCUMENTO};{CONTA}"
    output = lib.configurar(input)
    print(f"configurar = {output}")

def iniciar():
    OPERACAO = "pix" # produto para processamento
    output = lib.iniciar(OPERACAO)
    print(f"iniciar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def base_64(valor):
    OPERACAO = 'get_base64' # operação para realizar pagamento pix
    VALOR = valor           # valor do pagamento em centavos

    input = f"{OPERACAO};{VALOR}"
    output = lib.processar(input)
    print(f"processar = {output}")

    data = lib.obter_valor(output, "resultado.base64")
    image_data = base64.b64decode(data)
    with open("base64.png", "wb") as image_file:
        image_file.write(image_data)

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def chave_pix(valor):
    OPERACAO = 'get_chave_pix'  # operação para realizar pagamento pix
    VALOR = valor               # valor do pagamento em centavos

    input = f"{OPERACAO};{VALOR}"
    output = lib.processar(input)
    print(f"processar = {output}")

    data = lib.obter_valor(output, "resultado.chave_pix")
    with open('chave_pix.txt', 'w') as arquivo:   
        arquivo.write(data)

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def reembolso(tid=None, valor=None):
    OPERACAO = 'get_reembolso'  # operação para realizar reembolso pix

    # realiza o reembolso de uma transação específica (tid e valor) ou realiza
    # o reembolso da última transação
    if tid != None and valor != None:
        input = f"{OPERACAO};{valor};{tid}"
    else:
        input = OPERACAO
    
    output = lib.processar(input)
    print(f"processar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def status(tid=None):
    OPERACAO = 'get_status' # obtem o status do pagamento
    TID = tid               # tid (identificador) da transação - opcional

    # verifica o tid pois é opcional
    if tid == None:
        input = OPERACAO
    else:
        input = f"{OPERACAO};{TID}"

    output = lib.processar(input)
    print(f"processar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def finalizar():
    # apaga os arquivos auxiliares para a demo
    if os.path.exists("base64.png"):
        os.remove("base64.png")    
    if os.path.exists("chave_pix.txt"):
        os.remove("chave_pix.txt")

    OPERACAO = '' # finaliza a API
    output = lib.finalizar(OPERACAO)
    print(f"finalizar = {output}")

    result = lib.obter_valor(output, "codigo")
    return result

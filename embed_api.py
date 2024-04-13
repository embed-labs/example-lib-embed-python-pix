import base64
import os
import dotenv
import embed_lib as lib

CODE = "codigo"
STATUS_CODE = "resultado.status_code"
QRCODE_BASE64 = "resultado.qrcode_base64"

def configurar():
    dotenv.load_dotenv()

    PRODUTO = "pix"                             # produto de pagamento (atual pix)
    SUB_PRODUTO = os.getenv('SUB_PRODUTO')      # fornecedor/banco/parceiro (atual 1)
    TIMEOUT = "250"                             # timeout para consulta de status (para gerar qrcode ou reembolso)
    API_KEY = os.getenv('API_KEY')              # fonecido pela integração
    PROD_ID = os.getenv('PROD_ID')              # fonecido pela integração
    PID = os.getenv('PID')                      # fonecido pela integração
    CONTA = os.getenv('CONTA')                  # fonecido pela integração
    NOME = os.getenv('NOME')                    # dado informado pelo parceiro
    EMAIL = os.getenv('EMAIL')                  # dado informado pelo parceiro
    TELEFONE = os.getenv('TELEFONE')            # dado informado pelo parceiro
    DOCUMENTO = os.getenv('DOCUMENTO')          # dado informado pelo parceiro

    input = f"{PRODUTO};{SUB_PRODUTO};{TIMEOUT};{API_KEY};{PROD_ID};{PID};{NOME};{EMAIL};{TELEFONE};{DOCUMENTO};{CONTA}"
    output = lib.configurar(input)
    print(f"configurar = {output}")

def iniciar():
    OPERACAO = "pix" # produto para processamento
    output = lib.iniciar(OPERACAO)
    print(f"iniciar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def pix(valor):
    OPERACAO = 'get_qrcode'     # operação para realizar pagamento pix
    VALOR = valor               # valor do pagamento em centavos

    input = f"{OPERACAO};{VALOR}"
    output = lib.processar(input)
    print(f"processar = {output}")

    data = lib.obter_valor(output, QRCODE_BASE64)
    image_data = base64.b64decode(data)
    with open("qrcode.png", "wb") as image_file:
        image_file.write(image_data)

    result = lib.obter_valor(output, "codigo")
    return result

def reembolso():
    OPERACAO = 'get_reembolso'     # operação para realizar reembolso pix
    output = lib.processar(OPERACAO)
    print(f"processar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def status():
    OPERACAO = 'get_status' # obtem o status do pagamento
    output = lib.processar(OPERACAO)
    print(f"processar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def finalizar():
    OPERACAO = '' # finaliza a API
    output = lib.finalizar(OPERACAO)
    print(f"finalizar = {output}")

    result = lib.obter_valor(output, CODE)
    return result
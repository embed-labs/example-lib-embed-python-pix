# python3
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# imports


import time
import json
import io
import os
import base64
from libembed import configurar, iniciar, processar, finalizar, obter_valor
from PIL import Image, ImageTk
import warnings
from dotenv import load_dotenv
from threading import Thread
from tkinter import (
    Button,
    Tk,
    Label,
    Frame,
    Text,
    StringVar,
    Scrollbar,
    VERTICAL,
    NSEW,
    NS,
    W,
    FLAT,
    SUNKEN,
    END,
    RAISED,
)

warnings.filterwarnings("ignore", category=DeprecationWarning)

# --------------------------------------------------------------------------------------------

LARGE_FONT_STYLE = ("Roboto", 12, "bold")  # brandon, musc, montserrat, coco goose
SMALL_FONT_STYLE = ("Roboto", 11, "bold")
BUTTON_FONT_STYLE = ("Roboto", 9)
COLOR_BG_FRAME = "#282a36"  # Dark purple
COLOR_BG_LABEL = "#282a36"  # Dark purple
COLOR_FG_LABEL = "#f8f8f2"  # White
COLOR_BG_ENTRY = "#44475a"  # Dark gray
COLOR_BG_BUTTON = "#6272a4"  # Light purple
COLOR_FG_BUTTON = "#f8f8f2"  # White

# =========================================
# | =========  PÁGINA PRINCIPAL ========= |
# =========================================


class PixApp:
    # =========================================
    # | ===========  BEGIN LAYOUT =========== |
    # =========================================
    def __init__(self, root):
        self.root = root
        self.root.title("Exemplo Pix")
        self.root.resizable(width=False, height=False)
        self.root.minsize(700, 400)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame = self.create_main_frame()
        self.value_frame = self.create_value_frame()
        self.operator_frame = self.create_operator_frame()
        self.logs_frame = self.create_logs_frame()
        self.labels = self.create_labels()
        self.buttons = self.create_buttons()
        self.logs_text = self.create_logs_text()
        self.buttons["canc"]["state"] = "disabled"

    def create_main_frame(self):
        frame = Frame(self.root, bg=COLOR_BG_FRAME, borderwidth=2, border=10)
        frame.grid(column=0, row=0, sticky=NSEW, padx=(5, 5), pady=(5, 5))
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        return frame

    def create_value_frame(self):
        frame = Frame(self.main_frame, bg=COLOR_BG_FRAME, borderwidth=2)
        frame.grid(column=0, row=0, sticky=NSEW, padx=(1, 1), pady=(1, 1))
        return frame

    def create_operator_frame(self):
        frame = Frame(self.main_frame, bg=COLOR_BG_FRAME, borderwidth=2)
        frame.grid(column=0, row=1, sticky=NSEW, padx=(1, 1), pady=(1, 1))
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(4, weight=1)
        return frame

    def create_logs_frame(self):
        frame = Frame(self.main_frame, bg=COLOR_BG_FRAME, borderwidth=2)
        frame.grid(column=1, row=0, rowspan=2, sticky=NS, padx=(1, 1), pady=(1, 1))
        return frame

    def create_labels(self):
        self.lbl_value_text = StringVar()
        self.lbl_value_text.set("")
        lbl_value = Label(
            self.value_frame,
            text="Pix teste",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_value.grid(column=0, row=0, sticky=W, pady=(0, 0))

        lbl_operator_title = Label(
            self.operator_frame,
            text="Operador",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_operator_title.grid(column=0, row=0, columnspan=2, sticky=W, pady=(10, 0))

        lbl_logs = Label(
            self.logs_frame,
            text="Logs Exemplos",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_logs.grid(column=0, row=0, sticky=W, pady=(10, 0))

        self.lbl_operator_text = StringVar()
        self.lbl_operator_text.set("Status")
        lbl_operator = Label(
            self.operator_frame,
            textvariable=self.lbl_operator_text,
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=SMALL_FONT_STYLE,
        )
        lbl_operator.grid(column=0, row=1, columnspan=2, sticky=W, pady=(10, 0))

        return lbl_operator

    def create_buttons(self):
        btns = {}

        btns["configs"] = Button(
            self.value_frame,
            text="Configurar",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.configurar,
        )
        btns["configs"].grid(column=0, row=1, columnspan=2, padx=5, pady=5, sticky=NSEW)

        btns["start"] = Button(
            self.value_frame,
            text="PIX",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.pagamento,
        )
        btns["start"].grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        btns["reembolso"] = Button(
            self.value_frame,
            text="Reembolso",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.reembolso,
        )
        btns["reembolso"].grid(column=2, row=2, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        btns["canc"] = Button(
            self.operator_frame,
            text="Cancelar",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.cancelamento,
        )
        btns["canc"].grid(column=1, row=4, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        return btns

    def create_logs_text(self):
        self.logs = StringVar()
        logs_entry = Text(
            self.logs_frame,
            relief=SUNKEN,
            bg=COLOR_BG_ENTRY,
            fg=COLOR_FG_LABEL,
            width=60,
        )
        logs_entry.grid(column=0, row=1, sticky=NS, padx=(10, 0), pady=(10, 20))
        logs_entry.insert(END, "")

        sb_ver = Scrollbar(self.logs_frame, orient=VERTICAL)
        sb_ver.grid(column=1, row=1, sticky=NS, pady=(10, 20))

        logs_entry.config(yscrollcommand=sb_ver.set)
        sb_ver.config(command=logs_entry.yview)
        return logs_entry

    def write_logs(self, logs: str, div=True):
        if div:
            logs = "\n=======================================\n" + logs
        self.logs_text.insert(END, logs)
        self.logs_text.yview(END)
        self.root.update()

    # =======================================
    # | ===========  END LAYOUT =========== |
    # =======================================

    # =======================================
    # | ==============  PIX  ============== |
    # =======================================
    def error(self):
        self.lbl_operator_text.set("Aconteceu algum erro na operacao")

    def configurar(self):
        result = self.e_configurar()
        self.lbl_operator_text.set(result)
        self.root.update()

    def pagamento(self):
        self.buttons["configs"]["state"] = "disabled"
        self.buttons["start"]["state"] = "disabled"
        self.buttons["reembolso"]["state"] = "disabled"
        self.buttons["canc"]["state"] = "active"
        self.running = True
        self.process_thread = Thread(target=self.pix)
        self.process_thread.start()

    def cancelamento(self):
        self.running = False
        self.buttons["configs"]["state"] = "active"
        self.buttons["start"]["state"] = "active"
        self.buttons["reembolso"]["state"] = "active"
        self.buttons["canc"]["state"] = "disabled"
        self.lbl_operator_text.set("Cancelled")
        self.tk_image = None
        self.image_label.grid_forget()

    def reembolso(self):
        if "Sucesso" not in self.e_iniciar():
            return self.error()
        
        result = self.e_reembolso()
        self.lbl_operator_text.set(result)
        self.root.update()

    def pix(self):
        if "Sucesso" not in self.e_iniciar():
            return self.error()
        
        if "Sucesso" not in self.e_qrcode():
            return self.error()
        
        while self.running:
            result = self.e_status() 
            self.lbl_operator_text.set(f"Result: {result}")
            self.root.update()
            if "-1" in result:
                self.error()
                break;
            if "0" in result:
                break
        if "Sucesso" not in finalizar(""):
            return self.error()

        self.buttons["start"]["state"] = "active"
        self.buttons["reembolso"]["state"] = "active"
        self.buttons["configs"]["state"] = "active"
        self.lbl_operator_text.set("Ready")
        self.tk_image = None
        self.image_label.grid_forget()
        self.root.update()

    def e_configurar(self):
        self.lbl_operator_text.set("configurando produto pix")
        
        load_dotenv()

        PRODUTO = "pix"     # produto de pagamento (atual pix)
        SUB_PRODUTO = "1"   # fornecedor/banco/parceiro (atual 1)
        TIMEOUT = "250"     # timeout para consulta de status (para gerar qrcode ou reembolso)
        API_KEY = os.getenv('API_KEY')
        PROD_ID = os.getenv('PROD_ID')
        PID = os.getenv('PID')
        NOME = os.getenv('NOME')
        EMAIL = os.getenv('EMAIL')
        TELEFONE = os.getenv('TELEFONE')
        DOCUMENTO = os.getenv('DOCUMENTO')

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON 
        # input_data = {
        #     "configs": {
        #         "produto": PRODUTO,                                        
        #         "sub_produto": SUB_PRODUTO,                                       
        #         "infos": {
        #             "timeout": TIMEOUT,                                    
        #             "api_key": API_KEY,                                  
        #             "prod_id": PROD_ID,                                   
        #             "pid": PID,                                       
        #             "nome": NOME,                            
        #             "email": EMAIL,               
        #             "telefone": TELEFONE,                            
        #             "documento": DOCUMENTO,  
        #         }
        #     }
        # }
        # input_json = json.dumps(input_data)
        # res = configurar(input_json)

        # META PARAMETROS
        input_data = f"{PRODUTO};{SUB_PRODUTO};{TIMEOUT};{API_KEY};{PROD_ID};{PID};{NOME};{EMAIL};{TELEFONE};{DOCUMENTO}"
        res = configurar(input_data)

        self.write_logs("CONFIGURAR")
        self.write_logs(res)

        result = obter_valor(res, "mensagem")
        return result

    def e_iniciar(self):
        self.lbl_operator_text.set("iniciando pix")

        OPERACAO = "pix" # produto que será executado (atual pix)

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON
        # input_data = {
        #     "iniciar": {
        #         "operacao": OPERACAO
        #     }
        # }
        # input_json = json.dumps(input_data)
        # res = iniciar(input_json)

        # META PARAMETROS
        res = iniciar(OPERACAO)

        self.write_logs("INICIAR")
        self.write_logs(res)

        return res

    def e_qrcode(self):
        self.lbl_operator_text.set("pedindo qrcode para 1 real")

        OPERACAO    = 'get_qrcode'  # obtem o qrcode
        VALOR       = "100"         # valor sempre em centavos

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON 
        # input_data = {
        #     "processar": {
        #         "operacao": OPERACAO,   
        #         "valor": VALOR
        #     }
        # }
        # input_json = json.dumps(input_data)
        # res = processar(input_json)

        # META PARAMETROS
        input_data = f"{OPERACAO};{VALOR}"
        res = processar(input_data)

        self.write_logs("PROCESSAR")
        self.write_logs(res)
        
        qrcode_base64 = obter_valor(res, "resultado.qrcode_base64")
        message = obter_valor(res, "mensagem")

        if qrcode_base64:
            image_data = base64.b64decode(qrcode_base64)
            with open("qrcode.png", "wb") as img_file:
                img_file.write(image_data)
            image = Image.open(io.BytesIO(image_data))
            self.tk_image = ImageTk.PhotoImage(image)
            self.image_label = Label(self.value_frame, image=self.tk_image)
            self.image_label.grid(column=0, row=3, columnspan=1, rowspan=1, pady=(10, 0))
            self.image_label.config(image=self.tk_image)

            self.lbl_operator_text.set("Pagar")
            self.root.update()
        else:
            print("no qrcode in response ")
            self.lbl_operator_text.set("Ocorreu algum erro ao obter o qrcode")
        return message

    def e_reembolso(self):
        self.lbl_operator_text.set("pedindo reembolso de 1 real")

        OPERACAO = 'get_reembolso' # obtem o reembolso

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON 
        # input_data = {
        #     "processar": {
        #         "operacao": OPERACAO
        #     }
        # }
        # input_json = json.dumps(input_data)
        # res = processar(input_json)
    
        # META PARAMETROS
        res = processar(OPERACAO)

        self.write_logs("PROCESSAR")
        self.write_logs(res)

        result = obter_valor(res, "mensagem")
        if len(result) > 45:
            return result[0:45] + '\n' + result[45:]
        return result
    
    def e_status(self):
        self.lbl_operator_text.set("consultando status")

        OPERACAO = 'get_status' # obtem o status do pagamento do qrcode

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON
        # input_data = {
        #     "processar": {
        #         "operacao": "get_status"
        #     }
        # }
        # input_json = json.dumps(input_data)
        # res = processar(input_json)
    
        # META PARAMETROS
        res = processar(OPERACAO)

        self.write_logs("PROCESSAR")
        self.write_logs(res)
        
        result = obter_valor(res, "resultado.status_code")
        return result

    # =======================================
    # | ============  END PIX  ============ |
    # =======================================

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PixApp(Tk())
    app.run()

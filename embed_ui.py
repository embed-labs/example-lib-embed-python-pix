import embed_api as api

import os
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk

class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        api.configurar()    # Configuração da API

        # Variáveis de cores
        self.cor_fundo = "black"
        self.cor_botao = "green"
        self.cor_texto = "white"

        self.title("Embed")
        self.overrideredirect(False)  # Mostra a barra de título

        # Responsividade
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)  # Ocupa 4/5 da tela
        self.grid_columnconfigure(0, weight=1)

        self.header = HeaderFrame(self, bg=self.cor_fundo)
        self.header.grid(row=0, column=0, sticky="nsew")

        self.content = ContentFrame(self, bg=self.cor_fundo)
        self.content.grid(row=1, column=0, sticky="nsew")

        self.frames = {
            "TelaQrcode": TelaQrcode, 
            "TelaChavePix": TelaChavePix, 
            "TelaReembolso": TelaReembolso, 
            "TelaPrincipal": TelaPrincipal, 
            "TelaProcessamento": TelaProcessamento,
            "TelaStatusEspecifico": TelaStatusEspecifico, 
        }
        self.mostrar_frame("TelaPrincipal")

    def mostrar_frame(self, page_name):
        frame_class = self.frames[page_name]
        self.content.mostrar_frame(frame_class)

class HeaderFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.current_logo_index = 0
        self.logos = [
            Image.open("img/logo1.png"), 
            Image.open("img/logo2.png"),
            Image.open("img/logo3.png"),
        ]

        self.logo_photo = ImageTk.PhotoImage(self.logos[self.current_logo_index])
        self.logo_label = tk.Label(self, image=self.logo_photo)
        self.logo_label.pack(pady=1)

        # Alterna entre as imagens do logo a cada segundo
        self.after(1000, self.toggle_logo)

    def toggle_logo(self):
        self.current_logo_index = (self.current_logo_index + 1) % len(self.logos)
        self.logo_photo = ImageTk.PhotoImage(self.logos[self.current_logo_index])
        self.logo_label.config(image=self.logo_photo)
        self.after(1000, self.toggle_logo)

class ContentFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.controller = None  # Será atribuído na chamada de mostrar_frame

    def mostrar_frame(self, frame_class):
        if self.controller:
            self.controller.destroy()

        self.controller = frame_class(self)
        self.controller.pack(fill="both", expand=True)

class TelaPrincipal(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent.master.cor_fundo)
        self.parent = parent
        
        api.iniciar()   # Inicialização do produto PIX

        self.label = tk.Label(self, text="Operações com Pix\n", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 32))
        self.label.pack()

        self.refund_button = tk.Button(self, text="Gerar Base64 (QR Code)", command=lambda: self.parent.master.mostrar_frame("TelaQrcode"), height=5, width=20, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 12, 'bold'))
        self.refund_button.pack(pady=10)

        self.refund_button = tk.Button(self, text="Gerar Chave Pix", command=lambda: self.parent.master.mostrar_frame("TelaChavePix"), height=5, width=20, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 12, 'bold'))
        self.refund_button.pack(pady=10)

        self.refund_button = tk.Button(self, text="Gerar Reembolso", command=lambda: self.parent.master.mostrar_frame("TelaReembolso"), height=5, width=20, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 12, 'bold'))
        self.refund_button.pack(pady=10)

        self.refund_button = tk.Button(self, text="Obter Status Especifico", command=lambda: self.parent.master.mostrar_frame("TelaStatusEspecifico"), height=5, width=20, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 12, 'bold'))
        self.refund_button.pack(pady=10) 

class TelaQrcode(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent.master.cor_fundo)
        self.parent = parent

        self.label = tk.Label(self, text="Valor do Pix:", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 26))
        self.label.pack()

        self.textbox = tk.Text(self, height=1, bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.textbox.pack(pady=10)

        self.button_frame = tk.Frame(self, bg=self.parent.master.cor_fundo)
        self.button_frame.pack(padx=30)

        self.ok_button = tk.Button(self.button_frame, text="OK", command=self.processar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.ok_button.pack(side="left", padx=10)

        self.voltar_button = tk.Button(self.button_frame, text="Voltar", command=self.voltar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.voltar_button.pack(pady=10)

    def processar(self):
        valor = self.textbox.get()
        print("Valor do Pix:", valor)

        result = api.base_64(valor)
        if result == "1":
            self.parent.master.mostrar_frame("TelaProcessamento")

    def voltar(self):
        self.parent.master.mostrar_frame("TelaPrincipal")

class TelaChavePix(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent.master.cor_fundo)
        self.parent = parent

        self.label = tk.Label(self, text="Valor do Pix:", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 26))
        self.label.pack()

        self.textbox = tk.Text(self, height=1, bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.textbox.pack(pady=10)

        self.button_frame = tk.Frame(self, bg=self.parent.master.cor_fundo)
        self.button_frame.pack(padx=30)

        self.ok_button = tk.Button(self.button_frame, text="OK", command=self.processar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.ok_button.pack(side="left", padx=10)

        self.voltar_button = tk.Button(self.button_frame, text="Voltar", command=self.voltar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.voltar_button.pack(pady=10)

    def processar(self):
        valor = self.textbox.get()
        print("Valor do Pix:", valor)

        result = api.chave_pix(valor)
        if result == "1":
            self.parent.master.mostrar_frame("TelaProcessamento")

    def voltar(self):
        self.parent.master.mostrar_frame("TelaPrincipal")

class TelaReembolso(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent.master.cor_fundo)
        self.parent = parent

        self.label = tk.Label(self, text="Digite o TID:", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 26))
        self.label.pack()

        self.tid_text = tk.Text(self, height=1, bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.tid_text.pack(pady=10)

        self.button_frame = tk.Frame(self, bg=self.parent.master.cor_fundo)
        self.button_frame.pack(padx=30)

        self.ok_button = tk.Button(self.button_frame, text="OK", command=self.processar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.ok_button.pack(side="left", padx=10)

        self.voltar_button = tk.Button(self.button_frame, text="Voltar", command=self.voltar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.voltar_button.pack(pady=10)

    def processar(self):
        tid = self.tid_text.get("1.0", tk.END)
        print("Tid:", tid)

        result = api.reembolso(tid)
        if result == "0":
            self.label.config(text="Reembolso confirmado!", font=('Helvetica', 26))
        else:
            self.label.config(text="Erro ao realizar!", font=('Helvetica', 26))
        
        time.sleep(3)  
        self.parent.master.mostrar_frame("TelaPrincipal")

    def voltar(self):
        self.parent.master.mostrar_frame("TelaPrincipal")

class TelaStatusEspecifico(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent.master.cor_fundo)
        self.parent = parent

        self.label = tk.Label(self, text="Digite o TID:", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 26))
        self.label.pack()

        self.tid_text = tk.Text(self, height=1, bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.tid_text.pack(pady=10)

        self.button_frame = tk.Frame(self, bg=self.parent.master.cor_fundo)
        self.button_frame.pack(padx=30)

        self.ok_button = tk.Button(self.button_frame, text="OK", command=self.processar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.ok_button.pack(side="left", padx=10)

        self.voltar_button = tk.Button(self.button_frame, text="Voltar", command=self.voltar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.voltar_button.pack(pady=10)

    def processar(self):
        tid = self.tid_text.get("1.0", tk.END)
        print("Tid:", tid)

        result = api.status(tid)
        if result == "1":
            self.parent.master.mostrar_frame("TelaProcessamento")

    def voltar(self):
        self.parent.master.mostrar_frame("TelaPrincipal")

class TelaProcessamento(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent.master.cor_fundo)
        self.parent = parent

        self.label = tk.Label(self, text="Realize o pagamento", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.label.pack(pady=10)

        if os.path.exists("base64.png"):        
            self.imagem = tk.PhotoImage(file="base64.png") 
            self.imagem_label = tk.Label(self, image=self.imagem, bg=self.parent.master.cor_fundo)
            self.imagem_label.pack(pady=10)
        elif os.path.exists("chave_pix.txt"):
            with open('chave_pix.txt', 'r') as arquivo:
                conteudo = arquivo.read()
            self.key_text = tk.Text(self, height=3, bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
            self.key_text.insert("1.0", conteudo)   # Insere o conteúdo do arquivo no Text
            self.key_text.config(state="disabled")  # Desativa a edição do Text
            self.key_text.pack(pady=10)
        else:
            self.label.config(text="Consultando status", font=('Helvetica', 18))

        self.spinner = ttk.Progressbar(self, mode='indeterminate', )
        self.spinner.pack(pady=10)
        self.spinner.start()

        self.status_label = tk.Label(self, text="Aguardando processamento", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.status_label.pack(pady=10)

        self.button_frame = tk.Frame(self, bg=self.parent.master.cor_fundo)
        self.button_frame.pack(padx=20)

        self.cancel_button = tk.Button(self.button_frame, text="Cancelar", command=self.cancelar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.cancel_button.pack(side="left", padx=10)

        self.voltar_button = tk.Button(self.button_frame, text="Voltar", command=self.voltar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.voltar_button.pack(pady=10)

        self.process_thread = Thread(target=self.processar)
        self.process_thread.start()    
        
    def processar(self):
        while True:
            result = api.status()
            if result == "0":
                self.label.pack_forget()
                self.spinner.pack_forget()
                self.button_frame.pack_forget()
                self.status_label.config(text="Pagamento confirmado!", font=('Helvetica', 26))

                api.finalizar()
                time.sleep(3)
                break
                
        self.parent.master.mostrar_frame("TelaPrincipal")


    def cancelar(self):
        api.finalizar()
        self.parent.master.mostrar_frame("TelaPrincipal")

    def voltar(self):
        api.finalizar()
        self.parent.master.mostrar_frame("TelaPrincipal")

if __name__ == "__main__":
    app = Main()
    app.mainloop()

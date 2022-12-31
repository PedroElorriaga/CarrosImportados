import tkinter
import customtkinter
from app import *

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")
width = 450
heigth = 500

root = customtkinter.CTk()
root.geometry(f"{width}x{heigth}+500+200")
root.wm_resizable(False, False)
root.title("Base de dados")

frame = customtkinter.CTkFrame(root)
frame.pack(pady=10, padx=50, fill="both", expand=True)
customtkinter.CTkLabel(frame, text="Carros importados", font=("Roboto",20, "bold")).pack(pady=30)
customtkinter.CTkLabel(frame, text="Qual consulta deseja realizar?", font=("Arial",14)).pack(pady=10)
customtkinter.CTkButton(frame, text="Detalhes",font=("Roboto",14), height=30, command=exibir_detalhe).pack(pady=15)
customtkinter.CTkButton(frame, text="Incluir novo",font=("Roboto",14), height=30, command=post_request).pack(pady=15)
customtkinter.CTkButton(frame, text="Atualizar",font=("Roboto",14), height=30).pack(pady=15)
customtkinter.CTkButton(frame, text="Deletar",font=("Roboto",14), height=30).pack(pady=15)

customtkinter.CTkLabel(frame, text="Direitos reservados para PedroElorriaga ©", font=("Roboto", 8)).pack(pady=40)

root.mainloop()
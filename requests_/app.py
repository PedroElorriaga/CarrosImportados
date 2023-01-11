# IMPORTAÇÕES DE LIBS
import json, requests, time
from time import sleep
from infos import dados, dadoExibicao
from datetime import datetime, timedelta
from tkinter import *
import customtkinter
import os


current = os.getcwd()
appRoaming = True
roamingType = None
log_info = ''


# BUSCA O API DO SERVER CONECTADO
def get_request():
    response = requests.get('https://basecarros-98462-default-rtdb.firebaseio.com/.json')
    return response.json()

# CRIA UM NOVO DADO NO BD
def post_request():
    if roamingType == 'DEV':
        x = '{"ano" : "c_ano", "cor" : "c_cor", "marca" : "c_marca", "modelo" : "c_modelo"}'
        info = x.replace("c_ano", input("Digite o ano do veiculo: ")).replace("c_cor", 
        input("Digite a cor do veiculo: ")).replace("c_marca", input("Digite a marca do veiculo: ")).replace("c_modelo", 
        input("Digite o modelo do veiculo: "))
        response = requests.post('https://basecarros-98462-default-rtdb.firebaseio.com/.json', data=info)
        separador()
        print('Criado com sucesso!')
        separador()
        arquivo_json()
        arquivo_log()
        return response

    # INTERFACE DE INCLUSÃO
    elif roamingType == None:
        def send_data():
            ano_entry = ano.get()
            cor_entry = cor.get()
            marca_entry = marca.get()
            modelo_entry = modelo.get()
            x = '{"ano" : "c_ano", "cor" : "c_cor", "marca" : \
            "c_marca", "modelo" : "c_modelo"}'
            info = x.replace("c_ano", ano_entry).replace("c_cor", cor_entry)\
            .replace("c_marca", marca_entry).replace("c_modelo", modelo_entry)
            response = requests.post('https://basecarros-98462-default-rtdb.firebaseio.com/.json', data=info)
            arquivo_json()
            arquivo_log('post_request()')
            customtkinter.CTkLabel(frame, text="Dados atualizados com sucesso!", text_color="green", font=("arial", 12, "bold")).pack()

            return response
            
        width = 350
        heigth = 450
        root = customtkinter.CTkToplevel()
        root.geometry(f"{width}x{heigth}+250+300")
        root.wm_resizable(False, False)
        root.title("Base de dados")

        frame = customtkinter.CTkFrame(root)
        frame.pack(pady=10, padx=50, fill="both", expand=True)
        customtkinter.CTkLabel(frame, text=" ").pack(pady=10)
        customtkinter.CTkLabel(frame, text="Informe o ano:", font=("Arial",14), width=100).pack(pady= 2)
        ano = customtkinter.CTkEntry(frame, placeholder_text="Digite o ano", font=("Roboto", 12))
        ano.pack(pady=5)
        customtkinter.CTkLabel(frame, text="Informe a cor:", font=("Arial",14)).pack(pady= 2)
        cor = customtkinter.CTkEntry(frame, placeholder_text="Digite a cor", font=("Roboto", 12))
        cor.pack(pady=5)
        customtkinter.CTkLabel(frame, text="Informe a marca:", font=("Arial",14)).pack(pady= 2)
        marca = customtkinter.CTkEntry(frame, placeholder_text="Digite a marca", font=("Roboto", 12))
        marca.pack(pady=5)
        customtkinter.CTkLabel(frame, text="Informe o modelo:", font=("Arial",14)).pack(pady= 2)
        modelo = customtkinter.CTkEntry(frame, placeholder_text="Digite o modelo", font=("Roboto", 12))
        modelo.pack(pady=5)

        customtkinter.CTkButton(frame, text="Incluir", font=("Roboto",14), command=send_data).pack(pady=15)


# EXIBE OS DADOS DO BANCO DE DADOS
def exibir_detalhe():
    arquivo_json()
    if roamingType == 'DEV':
        teste = get_request()
        for k, val in teste.items():
            print(k)
            for i, v in val.items():
                print(f'\t{i}: {v}')

    # INTERFACE DE EXIBIÇÃO
    elif roamingType == None:
        with open(current+'/ArquivoJson.json', 'r') as arqv:
            exibir = json.load(arqv)

        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("green")
        width = 350
        heigth = 400
        root = customtkinter.CTkToplevel()
        root.geometry(f"{width}x{heigth}+950+150")
        root.wm_resizable(False, False)
        root.title("Base de dados")

        frame = customtkinter.CTkFrame(root)
        frame.pack(pady=10, padx=50, fill="both", expand=True)
        customtkinter.CTkLabel(frame, text="Detalhes", font=("Roboto", 20, "bold")).pack(pady=30)
        #canvaa = customtkinter.CTkCanvas(frame)
        #canvaa.pack(padx=5, pady=3, ipadx=5)
        text = customtkinter.CTkTextbox(frame, font=("Roboto", 11))

        for chave, valor in exibir.items():
            exibirChave = f"Key: {chave}\n\n"
            text.insert(END, exibirChave)
            #customtkinter.CTkLabel(canvaa, text=exibirChave).pack()
            for k,v in valor.items():
                exibirLabel = f"   {k}: {v}\n\n"
                text.insert(END, exibirLabel)

        text.pack(padx=2, pady=5)
        customtkinter.CTkLabel(frame, text="Direitos reservados para PedroElorriaga ©", font=("Roboto", 8)).pack(pady=30)
                #customtkinter.CTkLabel(canvaa, text=exibirLabel).pack(fill="both", expand=True)
    

# ATUALIZA DO DADOS NO BD
def patch_request(link=None, key=None, value=None):
    if roamingType == 'DEV':
        tokenResponse = get_request()
        if link in tokenResponse:
            x = '{"chave" : "valor"}'
            info = x.replace("chave", f"{key}").replace("valor", f"{value}")
            response = requests.patch(f"https://basecarros-98462-default-rtdb.firebaseio.com/{link}.json", data=info)
            separador()
            print('Atualizado com sucesso!')
            separador()
            exibir_detalhe()
            arquivo_json()
            arquivo_log()
            return response
        else:
            print()
            print('Link não encontrado!')

    #INTERFACE DE ATUALIZAÇÃO
    elif roamingType == None:
        def update_data():
            tokenResponse = get_request()
            key_entry = key.get()
            if key_entry in tokenResponse:
                colum_entry = colum.get()
                valor_entry = valor.get()
                for key_tk, value_tk in tokenResponse.items():
                    if colum_entry in value_tk:
                        x = '{"chave" : "valor"}'
                        info = x.replace("chave", f"{colum_entry}").replace("valor", f"{valor_entry}")
                        response = requests.patch(f"https://basecarros-98462-default-rtdb.firebaseio.com/{key_entry}.json", data=info)
                        arquivo_json()
                        arquivo_log('patch_request()')
                        customtkinter.CTkLabel(frame, text="Dados atualizados com sucesso!", text_color="green", font=("arial", 12, "bold")).pack()
                        no_find_value = False
                        return response 
                    else:
                        no_find_value = True
                
                #Exibe mensagem de não encontrado
                if no_find_value == True:
                    def exit_buttom():
                            messagebox.destroy()
                            return messagebox

                    messagebox = customtkinter.CTkToplevel()
                    messagebox.geometry("250x150+300+400")
                    messagebox.title("Alerta")
                    customtkinter.CTkLabel(messagebox, text="Chave não encontrada").pack(pady=30)
                    customtkinter.CTkButton(messagebox, command=exit_buttom, text="Ok").pack()

            #Exibe mensagem de não encontrado
            else:
                def exit_buttom():
                            messagebox.destroy()
                            return messagebox

                messagebox = customtkinter.CTkToplevel()
                messagebox.geometry("250x150+300+400")
                messagebox.title("Alerta")
                customtkinter.CTkLabel(messagebox, text="Link não encontrado").pack(pady=30)
                customtkinter.CTkButton(messagebox, command=exit_buttom, text="Ok").pack()

                
        width = 350
        heigth = 450
        root = customtkinter.CTkToplevel()
        root.geometry(f"{width}x{heigth}+250+300")
        root.wm_resizable(False, False)
        root.title("Base de dados")

        frame = customtkinter.CTkFrame(root)
        frame.pack(pady=10, padx=50, fill="both", expand=True)
        customtkinter.CTkLabel(frame, text="Atualizar", font=("Roboto",20, "bold")).pack(pady=20)
        customtkinter.CTkLabel(frame, text="Informe a KEY:", font=("Arial",14)).pack(pady= 2)
        key = customtkinter.CTkEntry(frame, placeholder_text="Digite a key", font=("Roboto", 12))
        key.pack(pady=5)
        customtkinter.CTkLabel(frame, text="Informe a coluna:", font=("Arial",14)).pack(pady= 2)
        colum = customtkinter.CTkEntry(frame, placeholder_text="Digite a coluna", font=("Roboto", 12))
        colum.pack(pady=5)
        customtkinter.CTkLabel(frame, text="Informe o novo valor:", font=("Arial",14)).pack(pady= 2)
        valor = customtkinter.CTkEntry(frame, placeholder_text="Digite o valor", font=("Roboto", 12))
        valor.pack(pady=5)

        customtkinter.CTkButton(frame, text="Incluir", font=("Roboto",14), command=update_data).pack(pady=15)


# DELETA OS DADOS NO BD
def delete_request(link=None):
    if roamingType == 'DEV':
        if link is not None:
            tokenResponse = get_request()
            if link in tokenResponse:
                response = requests.delete(f"https://basecarros-98462-default-rtdb.firebaseio.com/{link}.json")
                separador()
                print('Deletado com sucesso!')
                separador()
                arquivo_json()
                arquivo_log()
                return response
            else:
                print()
                print('Link não encontrado!')
        else:
            print()
            print('Nenhum valor digitado!')

    #INTERFACE DE EXCLUSÃO
    elif roamingType == None:
        def del_data():
            key_entry = key.get()
            link = key_entry
            if link is not None:
                tokenResponse = get_request()
                if link in tokenResponse:
                    def delete_duo_check():
                        response = requests.delete(f"https://basecarros-98462-default-rtdb.firebaseio.com/{link}.json")
                        arquivo_json()
                        arquivo_log('delete_request()')
                        confirmbox = customtkinter.CTkToplevel()
                        confirmbox.geometry("150x100+350+400")
                        confirmbox.title("Confirmation")
                        def exit_confirm():
                            confirmbox.destroy()
                            exit_buttom()
                        customtkinter.CTkLabel(confirmbox, text="Excluido com sucesso!").pack(pady=10)
                        customtkinter.CTkButton(confirmbox, text="OK", command=exit_confirm).pack()
                        
                        return response
                    
                    def exit_buttom():
                        messagebox.destroy()
                        return messagebox

                    messagebox = customtkinter.CTkToplevel()
                    messagebox.geometry("250x150+300+400")
                    messagebox.wm_resizable(False, False)
                    messagebox.title("Duo Check")
                    customtkinter.CTkLabel(messagebox, text="Tem certeza disso?", font=("Roboto",18, "bold")).pack(pady=25)
                    customtkinter.CTkButton(messagebox, text="Sim", command=delete_duo_check, height=10, width=120).pack(side=LEFT, padx=2)
                    customtkinter.CTkButton(messagebox, text="Não", height=10, command=exit_buttom, width=120).pack(side=RIGHT, padx=2)
                
                else:
                    def exit_buttom():
                        messagebox.destroy()
                        return messagebox

                    messagebox = customtkinter.CTkToplevel()
                    messagebox.geometry("250x150+300+400")
                    messagebox.title("Alerta")
                    customtkinter.CTkLabel(messagebox, text="Link não encontrado").pack(pady=30)
                    customtkinter.CTkButton(messagebox, command=exit_buttom, text="Ok").pack()
            else:
                def exit_buttom():
                        messagebox.destroy()
                        return messagebox

                messagebox = customtkinter.CTkToplevel()
                messagebox.geometry("250x150+300+400")
                messagebox.title("Alerta")
                customtkinter.CTkLabel(messagebox, text="Campo Key em branco").pack(pady=30)
                customtkinter.CTkButton(messagebox, command=exit_buttom, text="Ok").pack()

        width = 350
        heigth = 450
        root = customtkinter.CTkToplevel()
        root.geometry(f"{width}x{heigth}+250+270")
        root.wm_resizable(False, False)
        root.title("Base de dados")

        frame = customtkinter.CTkFrame(root)
        frame.pack(pady=10, padx=50, fill="both", expand=True)
        customtkinter.CTkLabel(frame, text="Deletar", font=("Roboto", 20, "bold")).pack(pady=50)
        customtkinter.CTkLabel(frame, text="Informe a KEY:", font=("Arial",14)).pack(pady= 2)
        key = customtkinter.CTkEntry(frame, placeholder_text="Digite a key", font=("Roboto", 12))
        key.pack(pady=5)

        customtkinter.CTkButton(frame, command=del_data, text="Confirmar").pack(pady=10)
        #customtkinter.CTkLabel(frame, text="Direitos reservados para PedroElorriaga ©", font=("Roboto", 8)).pack(pady=80)


# TRANSFORMA AQRUIVO EM JSON
def arquivo_json():
    dados = get_request()
    with open(current + '/ArquivoJson.json', 'w') as arqv:
        json.dump(dados, arqv, indent=4)
        separador()
        print('JSON atualizado com sucesso!')
        separador()


# CRIA LOG DE MODIFICAÇÃO
def arquivo_log(log_info=None):
    data = datetime.now()
    dataFormat = datetime.strftime(data, '%d/%m/%Y ' '%H:%M:%S')
    if roamingType == 'DEV':
        with open(current + '/logs.txt', 'a') as arqv:
            arqv.write(f'Ultima modificação --> {dataFormat} {requisicao}\n')
    else:
        with open(current + '/logs.txt', 'a') as arqv:
            arqv.write(f'Ultima modificação --> {dataFormat} {log_info}\n')


# GERA UM SEPARADOR '-'
def separador():
    print('-' * 30)


# INICIA APP ROAMING
if __name__ == "__main__":
    while appRoaming:
        roamingType = 'DEV'
        texto = separador(),print('  BANCO DE DADOS CARROS 2023'),separador()
        print('Qual operação deseja realizar?')
        

        # EXIBE AS OPERAÇÕES PARA O USUÁRIO
        i=0
        for indice, dado in enumerate(dados):
            if indice != 0:
                print(f'\t',indice, dadoExibicao[i])
                i+=1
        print()


        # COLETA AS INFORMAÇÕES SE FOR INTEIRO
        qtd_dados = len(dadoExibicao)
        dado_user = input('--> ')
        print()
        dado_userINT = None 
        if dado_user.isdigit():
            dado_userINT = int(dado_user)
        else:
            print('Informe apenas o indice!')
            continue
        

        # VERIFICA SE O INPUT NÃO É NULL E SE O INPUT ESTÁ DENTRO DA QUANTIDADE DE OPERAÇÕES
        if dado_userINT is not None:
            if dado_userINT >= 1 and dado_userINT < qtd_dados:
                requisicao = dados[dado_userINT]
            else:
                print('Fora do indice!')
                continue
        

        # SWITCH CASE DAS CONDIÇÕES
        match requisicao:
            case 'exibir_detalhe()':
                exibir_detalhe()
            case 'post_request()':
                post_request()
            case 'patch_request()':
                exibir_detalhe()
                separador()
                link = input('Digite o link: ')
                key = input('Digite a chave: ')
                value = input('Digite o valor: ')
                patch_request(link, key, value)
            case 'delete_request()':
                exibir_detalhe()
                link = input('Digite o link: ')
                print('\nTem certeza disso?[(S)sim / (N)não]')
                tokenDelete = input('--> ')
                if tokenDelete == 'S':
                    delete_request(link)
                else:
                    print()
                    print('Não deletado!')
                    continue
            case _:
                print()
                print('Comando não encontrado!')
        
        print()
        print('Deseja efetuar mais alguma operação?')
        dado_user = input('--> ')


        # VERIFICA SE MAIS ALGUMA OPERAÇÃO SERÁ REALIZADA
        if dado_user == 'S' or dado_user == 's':
            continue
        else:
            appRoaming = False


# IMPORTAÇÕES DE LIBS
import json, requests
from time import sleep
from infos import dados, dadoExibicao
from datetime import datetime, timedelta
from tkinter import *
import customtkinter
import os


current = os.getcwd()
appRoaming = True
roamingType = None

# BUSCA O API DO SERVER CONECTADO
def get_request():
    response = requests.get('https://basecarros-98462-default-rtdb.firebaseio.com/.json')
    return response.json()


# CRIA UM NOVO DADO NO BD
def post_request():
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


# EXIBE OS DADOS DO BANCO DE DADOS
def exibir_detalhe():
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
    root = customtkinter.CTk()
    root.geometry(f"{width}x{heigth}+550+200")
    root.title("Base de dados")

    frame = customtkinter.CTkFrame(root)
    frame.pack(pady=10, padx=50, fill="both", expand=True)
    customtkinter.CTkLabel(frame, text="Detalhes", font=("Roboto", 20, "bold")).pack(pady=30)
    canvaa = customtkinter.CTkCanvas(frame)
    canvaa.pack(padx=5, pady=3, ipadx=5)
    scroll_bar = Scrollbar(canvaa, orient="vertical")
    scroll_bar.pack(side=RIGHT, fill=Y, padx=2, pady=8)
    text = Text(canvaa, yscrollcommand=scroll_bar.set, font=("Roboto", 12))

    for chave, valor in exibir.items():
        exibirChave = f"Key: {chave}\n"
        text.insert(END, exibirChave)
        #customtkinter.CTkLabel(canvaa, text=exibirChave).pack()
        for k,v in valor.items():
            exibirLabel = f"\t{k}: {v}\n"
            text.insert(END, exibirLabel)

    text.pack(padx=5, pady=5)
            #customtkinter.CTkLabel(canvaa, text=exibirLabel).pack(fill="both", expand=True)
    

# ATUALIZA DO DADOS NO BD
def patch_request(link, key, value):
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
    elif roamingType == None:
        #CRIAR CONDIÇÃO DE EXE DA INTERFACE
        if link == None:
            link = input('Digite o link: ')
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


# TRANSFORMA AQRUIVO EM JSON
def arquivo_json():
    dados = get_request()
    with open(current + '/ArquivoJson.json', 'w') as arqv:
        json.dump(dados, arqv, indent=4)
        separador()
        print('JSON atualizado com sucesso!')
        separador()


# CRIA LOG DE MODIFICAÇÃO
def arquivo_log():
    data = datetime.now()
    dataFormat = datetime.strftime(data, '%d/%m/%Y ' '%H:%M:%S')
    if roamingType == 'DEV':
        with open(current + '/logs.txt', 'a') as arqv:
            arqv.write(f'Ultima modificação --> {dataFormat} {requisicao}\n')
    else:
        with open(current + '/logs.txt', 'a') as arqv:
            arqv.write(f'Ultima modificação --> {dataFormat} TESTE\n')


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


# INTERFACE GRÁFICA

import requests 
import time
import re
import os
#import pyperclip

def gerar_header_e_sessao_php() -> dict:
    php_session_id = None
    

    ## Gerando PHP_SESSION_ID
    if not php_session_id:
        try:
            data = requests.get("https://www.minuteinbox.com/")
            # Tratando cookie recebido 
            php_session_id = f"PHPSESSID={dict(data.cookies)['PHPSESSID']}"
        except Exception as err: # Tratar no futuro
            print("Ainda precisa ser tratado ")
            
    ## Gerando Headers
    headers = {
        "Cookie": php_session_id,
        "Host": "www.minuteinbox.com",
        "Referer": "https://www.minuteinbox.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36.",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"'
    }
    
    resultado = {
        "headers": headers,
        "phpID": php_session_id
    }
    return resultado


def gerar_email(headers) -> str:
     
    data = requests.get("https://www.minuteinbox.com/index/index",headers=headers).text

    
    email = re.sub('[{|"|]|}',"",data).split(":")[1]
    
    ## Copiando para o mouse o email
    # pyperclip.copy(email)
    # pyperclip.paste() # depende do xclip

    return email

def verificar_emails_novos(headers):
    dados_bruto = requests.get("https://www.minuteinbox.com/index/refresh",headers=headers).text

    tratar_e_mostrar_emails(dados_bruto)

    return 0

def tratar_e_mostrar_emails(json_emails_bruto):
    # Regex 
    emails_bruto = re.findall(r'"predmetZkraceny".*?"id".[1-99]',json_emails_bruto)

    ## Tratando email
    for email in emails_bruto:

        # Removendo caracters ",),<,> da saida e dividindo pela virgula ,
        email_tratado = re.sub('["|)|<|>]',"",email).split(",")


        # dividindo ":" da saida Ex: (predmetZkraceny:SendTestEmail...) e pegando a parte sem ":"

        titulo = email_tratado[0].split(":")[1]
        conteudo = email_tratado[1].split(":")[1]
        email_remetente = email_tratado[2].split(":")[1]
        id = email_tratado[3].split(":")[1]

        print("#" * 40)
        print(f"Titulo: {titulo}\nConteudo: {conteudo}\nEmail: {email_remetente}\nIdEmail: {id}")
        print("#" * 40)
        
    return 0

def acessar_email(id,headers):
    headers["Referer"] = "https://www.minuteinbox.com/window/id/1"
    data = requests.get(f"https://www.minuteinbox.com/email/id/{id}",headers=headers)

    return data.text




if __name__ == "__main__":

    headers,sessao = gerar_header_e_sessao_php().values()

    email = gerar_email(headers)

    while True:
    
        os.system("clear") # Modificar no futuro
        print(f"Email: {email}")

        print("\tCaixa de Entrada {qtd_caixa_entrada}\n")
        novos_emails = verificar_emails_novos(headers)

        decisao_usr = input("\nVerificar Novos Emails:[r]| Acessar Email:[a] | Fechar:[q] ").lower()

        if decisao_usr == "r":
            continue
        elif decisao_usr == "a":
            email_id = input("Digite o ID do email: ")
            resultado = acessar_email(email_id,headers)
            print(resultado)
            time.sleep(20)
        elif decisao_usr == "q":
            break
        else:
            print("opt invalida recarregando! caixa de entrada")




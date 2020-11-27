import imaplib 
from datetime import datetime
import re


conn = imaplib.IMAP4_SSL("imap.gmail.com", 993) 
gmail_user = 'joaquin.cancino@mail.udp.cl' 
gmail_pwd = 'udp2016.3099' 

exp_reg = "[0-9a-f]{12}4[0-9a-f]{19}@373$"
adress =  "hello@sonicwall.com"
date_exp = "01/01/2016 00:00:00" #el correo mas antiguo es del 2019 y cumple con la expresion regular

conn.login(gmail_user, gmail_pwd) 

conn.select('Inbox', readonly=True)

typ, data = conn.search(None, "(FROM "+adress+")")

for num in data[0].split():

    typ, data = conn.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID DATE)])')

    info = data[0][1].decode("utf-8").split()
  

    msg_id = info[1][1:37]
    date=[]

    if (len(info) == 8):
        date = info[3:7]
        f_date = str(date[0]+'/'+date[1]+'/'+date[2]+' '+date[3])

    elif (len(info) == 10):
        date = info[3:8]
        f_date = str(date[1]+'/'+date[2]+'/'+date[3]+' '+date[4])
    #print(msg_id)
    #print(info)
    #print(len(info))
    #print (date)
    
    
    date_dt = datetime.strptime(f_date, '%d/%b/%Y %H:%M:%S')
    date_comp = datetime.strptime(date_exp, '%d/%m/%Y %H:%M:%S')
    

    pattern = re.compile(exp_reg)

    match_re = pattern.match(msg_id)

    print (msg_id , date_dt)

    #print ("MATCH: ", match_re, "DATE: ", date_dt>date_comp)

    if ((match_re is None) and (date_dt>date_comp)):
        print("ERROR en el correo con el MESSAGE-ID ",msg_id, " NO CUMPLE CON LA EXPRESION REGULAR \n")
        print("El CORREO FUE ENVIADO EL: ", date_dt)

    elif ((match_re is None) and (date_dt<date_comp)):
        print("ERROR en el correo con el MESSAGE-ID ",msg_id, " LA FECHA ESTA FUERA DEL LIMITE Y NO CUMPLE CON LA E.R \n")
        print("El CORREO FUE ENVIADO EL: ", date_dt)


    elif ((match_re is not None) and (date_dt<date_comp)):
        print("MATCH E.R ",msg_id, " LA FECHA ESTA FUERA DEL LIMITE \n")
        print("El CORREO FUE ENVIADO EL: ", date_dt)
    
    elif ((match_re is not None) and (date_dt>date_comp)):
        print("MATCH, email secure")

        

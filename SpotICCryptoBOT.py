from telethon import TelegramClient, events, sync
from binance.client import Client
from binance.enums import *
from binance.helpers import round_step_size
import time
import asyncio
import json
import win32api
import re
import threading
from datetime import datetime


"""
SpotICCCryptoBOT by Richard Libreros

"""
# Bot especifico para el canal IC Crypto signals VIP
#---------binance api ----------
API_KEY = ""
API_SECRET = ""
clientBinance = Client( API_KEY, API_SECRET, tld= "com")

#--------telegram api
api_id = 16487976
api_hash = ''
client = TelegramClient('', api_id, api_hash)

cantidadUSD = 30 #CANTIDAD de usd por operacion MINIMA deberia ser 20 para evitar errores 
Theorders = {}
PairsUsed = []


"""
channel_id = -1001440312345
for message in client.get_messages(channel_id, limit=1): #carga todo el historial de mensajes, limit = N°mensajes a cargar
    print(message.message)
"""


async def func(mesg):
    entity = await client.get_entity(-1001433974492)
    await client.send_message(entity=entity, message=mesg)




def SyncTime():
 gt = clientBinance.get_server_time()
 tt=time.gmtime(int((gt["serverTime"])/1000))
 win32api.SetSystemTime(tt[0],tt[1],0,tt[2],tt[3],tt[4],tt[5],0)   




async def engine ():
   
 global PairsUsed    
 orD = open('new_orders.json',) 
 PaiR = open('new_pairs.json',)
 Theorders.update(json.load(orD))
 PairsUsed = list(json.load(PaiR))



 fixGet = Theorders.get
 while True:
    try:        
        for v in PairsUsed:   
            orders = clientBinance.get_all_orders(symbol=v) #obtiene todas la ordenes x cada par encontrado en la lista
            print("loop alive")

            for i in orders:
                #print(i) 
                ids = str(i['orderId']) 
                status = str(i['status']) #CANCELED/FILLED 
                #print(ids)   
                #print(Theorders.get(ids))       
                if fixGet(ids) != None: #compara los id encontrados de las ordenes con las ordenes almacenadas, si hay coincidencias se ejecuta lo siguiente
                #print(status)  
                    if status == 'FILLED': 
                            SyncTime()
                            print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
                            #print(ids)
                            ordergeted = fixGet(ids) #accede a la informacion dentro de cada id en el diccionario
                            #print(status)

                            #encuentra filtra la cantidad del activo que se compro, para vender la misma cantidad
                            buyPrice = str(ordergeted['quantity']) #cuenta los caracteres despues del .
                            lotSize = str(ordergeted['stepsize']) #cuenta los caracteres despues del .
                            stepzise = buyPrice[::-1].find('.')

                            
                            pos1 = v.find("USDT")
                            asset = v[0:pos1]
                            orders = clientBinance.get_asset_balance(asset) 
                            freeprice = str(orders["free"])
                            pricefixed = freeprice[0:stepzise+2]

                            cadena = freeprice.split(".")
                            quitdecimal = cadena[1]
                            quitdecimal2 = quitdecimal[0:stepzise]
                            pricefixed2 = cadena[0] + "." + quitdecimal2

                            
   
                            ocoQuantity = float(pricefixed2) # SI ESTE METODO DA ERRORES USAR EL ANTIGUO pricefixed
                            if lotSize == "1.00000000": #CUANDO el lotsize de el pair es 1.0 y en la cuenta tenemos ejmp: 7.9 solo dejara vender 7 
                               ocoQuantity = int (ocoQuantity)
                            print(ocoQuantity)


                            #print(ordergeted['symbol'])
                            ocoSymbol = ordergeted['symbol'] 
                            #print(ordergeted['takeprofit'])
                            ocoPrice = ordergeted['takeprofit']
                            #print(ordergeted['stoploss'])
                            ocoStoploss = ordergeted['stoploss']

                            asyncio.ensure_future(func("[" +  u'\U0001F916' + "] " + u'\U00002705' +  "LA ORDEN LIMIT DEL ASSET (" + ocoSymbol + ") HA SIDO EJECUTADA.\n\nPreparando oredenes SL/TP..."))
                            await asyncio.sleep(5)  

                            try:
                                order = clientBinance.create_oco_order(
                                    symbol=ocoSymbol,
                                    side=SIDE_SELL,
                                    quantity=ocoQuantity,                
                                    price=ocoPrice,
                                    stopPrice=ocoStoploss,
                                    stopLimitPrice=ocoStoploss,
                                    stopLimitTimeInForce="GTC")

                                print("orden OCO completada del asset: " + ocoSymbol) 
                                asyncio.ensure_future(func("[" +  u'\U0001F916' + "] " + u'\U0001F6A9' +  "ORDENES TP/SL COMPLETADAS:"))
                                await asyncio.sleep(5)  

                                Theorders.pop(ids) 
                                with open('C:/Users/CaoZRich/Desktop/spotbot/json/new_orders.json', 'w') as fp: #guarda el diccionario como json 
                                    json.dump(Theorders, fp)



                                PairsUsed.remove(ocoSymbol) #elimina el simbolo de la lista .remove elminar el primer item que encuentre con ese nombre
                                with open('C:/Users/CaoZRich/Desktop/spotbot/json/new_pairs.json', 'w') as fp: #guarda los pares usados como json
                                    json.dump(PairsUsed, fp)


                            except Exception as e:
                                print("an exception occured while send OCO order - {}".format(e))
                                asyncio.ensure_future(func("[" +  u'\U0001F916' + "] " + u'\U000026D4' +  "SCRIPT ERROR, ALGO SALIO MAL MIENTRAS SE REALIZABA LA ORDEN OCO:\n\nEXEPTION: - {}".format(e)))
                                await asyncio.sleep(5)  

                    elif status == 'CANCELED' :
 
  
                                ordergeted = fixGet(ids)
                                ocoSymbol = ordergeted['symbol']  

                                Theorders.pop(str(ids)) #aqui borrar orden de el diccionario y guardarla en el archivo json
                                with open('C:/Users/CaoZRich/Desktop/spotbot/json/new_orders.json', 'w') as fp: #guarda el diccionario como json 
                                   json.dump(Theorders, fp)
                                

                                PairsUsed.remove(ocoSymbol) #elimina el simbolo de la lista .remove elminar el primer item que encuentre con ese nombre
                                with open('C:/Users/CaoZRich/Desktop/spotbot/json/new_pairs.json', 'w') as fp: #guarda los pares usados como json
                                   json.dump(PairsUsed, fp)

                                asyncio.ensure_future(func("[" +  u'\U0001F916' + "] " + u'\U000026A0' +  "LA ORDEN BUY LIMIT DEL PAR (" + ocoSymbol + ") HA SIDO CANCELADA"))
                                await asyncio.sleep(3)                                     

                                   

            
            time.sleep(3)
     
    except Exception as e:
        print(f'Whoops, we ran into the following error: {e}')
        seconds_into_current_minute = int(datetime.now().strftime("%S"))

        wait_time = (60 + 5) - seconds_into_current_minute
        time.sleep(wait_time)
 



  

_thread = threading.Thread(target=asyncio.run, args=(engine(),))
_thread.start()






def search(Tlist, confirmation):
    for i in range(len(Tlist)):
        if Tlist[i] == confirmation:
            return True
    return False


async def evento (text): #esta funcion verifica que el mesaje sea una orden y saca los valores 
 try:   
    if text[0] == u'\U000026A1': #unicode para el emoji del rayo
        print(">>-------------------------------------------------------<<")

        def remove_urls (vTEXT):
            vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
            return(vTEXT)


        text = remove_urls(text)
        text = text.replace("/", "") #quita el caracter / para que el par sea igual que en binance
        text = text.replace(" ", "") #quita los espacios para disminuir probalidad de errores
        pos1 = (text.find("#") +1) #encuentra el caracter # que fija el comienzo del par
        pos2 = text.find(u'\U000026A1',3) #el final del par
        print("Pair: " + text[pos1:pos2])
        PairF = text[pos1:pos2]

        #-----------

        entry = text.find("Entry")
        pos1b = text.find(")",entry)
        pos2b = text.find("-",pos1b)
       
        entryF = float(text[pos1b+1:pos2b])
        

        #-----------

        take = text.find("Take")
        pos1c = text.find(")",take)
        pos2c = text.find("-",pos1c)

        takeF = float(text[pos1c+1:pos2c])       

        #-----------

        stop = text.find("Stop")
        pos1d = text.find(")",stop)
        pos2d = text.find("-",pos1d)

        stopF = float(text[pos1d+1:pos2d])  


        print("Preparing order...")
        print("Entry price: " + str(entryF))    
        print("Take Profit: " + str(takeF))
        print("StopLoss: " +  str(stopF))

        await sentOrder(PairF,entryF,takeF,stopF)



    elif text[0] == u'\U0001F6A8':

        #print("es una orden de venta")
        pos = (text.find("#")+1) 
        pos2 = text.find(" ",pos)
        pair = text[pos:pos2] + "USDT"
        orders = clientBinance.get_open_orders(symbol=pair)
        asyncio.ensure_future(func("[" +  u'\U0001F6A8' + "] " + u'\U000026A0' +  "Se ha detectado una señal de venta manual para el par " + pair))
        if orders != []:

            try:
                for i in orders:
                    orderid = i['orderId']
                    clientBinance.cancel_order(
                    symbol=pair,
                    orderId=orderid)
                    time.sleep(1)
            except:
                pass        

            balance = clientBinance.get_asset_balance(text[pos:pos2])              
            freeprice = str(balance["free"])

            symbol_info =  clientBinance.get_symbol_info(pair)    #extrae el stepsize del par
            json_str = json.dumps(symbol_info, indent=2)
            resp = json.loads(json_str)
            filters = resp['filters']
    

            lotsize = filters[2]
            stepSize = lotsize['stepSize'] #cantidad minima de decimales en la cantidad del token
            revzeros = str(float(stepSize))#quita los ceros de la derecha ejemp 2.001000 --> 2.001
            lenstr = len(str(revzeros).split(".")[1]) #cuenta los ceros despues de el punto
            if stepSize == "1.00000000": #CUANDO el stepSize de el pair es 1.0 y en la cuenta tenemos ejmp: 7.9 solo dejara vender 7 
                pricefixed2 = int (float(freeprice)) #pricefiex2referenced befores assigned
            else:    
                cadena = freeprice.split(".")
                quitdecimal = cadena[1]
                quitdecimal2 = quitdecimal[0:lenstr]
                pricefixed2 = cadena[0] + "." + quitdecimal2


   

            print(pricefixed2)

            order = clientBinance.order_market_sell(
                symbol=pair,
                quantity=float(pricefixed2))   

 except Exception as e:
    print("an exception occured - {}".format(e))
    asyncio.ensure_future(func("[" +  u'\U0001F916' + "] " + u'\U000026D4' +  "SCRIPT ERROR, ALGO SALIO MAL MIENTRAS SE REALIZABA LA ORDEN:\n\nEXEPTION: - {}".format(e)))
    print("operacion cancelada")




async def sentOrder(PairF,entryF,takeF,stopF): #organiza los valores y los envia como una orden de compra

    symbolPrice = 0
    orders = clientBinance.get_open_orders(symbol=PairF) 
    
    if (len(orders) == 0): #verifica que no exista un orden con el par usado
        print(" ")
        print("Comprobando...")
        time.sleep(2)


        # get price
        list_of_tickers = clientBinance.get_all_tickers()
        for tick_2 in list_of_tickers:
            if tick_2['symbol'] == PairF:
                symbolPrice = float(tick_2['price'])
        # get price

        
        tokenammount = 1/entryF*cantidadUSD #calcula el monto de la moneda con el valor en usdt a gastar

       
        symbol_info =  clientBinance.get_symbol_info(PairF)    #extrae el stepsize del par
        json_str = json.dumps(symbol_info, indent=2)
        resp = json.loads(json_str)
        filters = resp['filters']

        lotsize = filters[2]
        stepSize = lotsize['stepSize'] #cantidad minima de decimales en la cantidad del token

        ticksizeFilter = filters[0]
        ticksize = ticksizeFilter['tickSize'] #cantidad maxima de decimales en el precio     

    
        cantidad = round_step_size(tokenammount, float(stepSize))

        fixedTP = round_step_size(takeF, float(ticksize))
        fixedSL = round_step_size(stopF, float(ticksize))

        #-------------FIX/STEP_SIZE DE 1.0------------(CUANDO EL STEPSIZE ES DE 1.0)

        
  



        print("se enviara una orden de compra limite de " + str(cantidad) + " " + PairF + " por: $" + str(cantidadUSD) + "USDT al precio de: " + str(entryF) ) #cantidad del token a comprar
        print("precio actual: $" + str(symbolPrice)) #precio actual
  

        #-------------LIMIT/BUY----------------
        SyncTime()

        order = clientBinance.order_limit_buy(
        symbol=PairF,
        quantity=cantidad,
        price=str(entryF))
 
        print(" ")
        print("orden LIMIT/BUY fue realizada con exito, ID: " + str(order["orderId"]))
        await func("[" +  u'\U0001F916' + "] " + u'\U00002714' +  " ORDEN LIMIT REALIZADA CON EXITO: \n\nAsset: " + PairF + "\nEntry: " + str(entryF) + "\nCurrentPrice: " +str(symbolPrice)) #str(symbolPrice)4

        #------------GUARDAR DATOS DE LA ORDEN-------------
        global PairsUsed 
        global Theorders

        id = str(order["orderId"]) #extrae el id de la orden
        Theorders.update({id:{"quantity":cantidad,"symbol":PairF,"takeprofit":str(fixedTP),"stoploss":str(fixedSL),"stepsize":stepSize}}) #agrega un diccionario dentro de theorders
        with open('new_orders.json', 'w') as fp: #guarda el diccionario como json 
            json.dump(Theorders, fp)
        #orD = open('json/new_orders.json',) 
        #Theorders = json.load(orD)
        


        if search(PairsUsed, PairF): #si el par no existe entro de la lista lo agrega
            pass
        else:
            PairsUsed.append(PairF)


        with open('new_pairs.json', 'w') as fp: #guarda los pares usados como json
            json.dump(PairsUsed, fp)


    else:
        print(" ")
        print("ya existe una orden con el par: " + PairF)







@client.on(events.NewMessage(chats=-1001440312345)) #1001440312345 --> iD of IC crypto chanel 
async def my_event_handler(event): #evento/llegada de un mensaje al canal
    await evento (event.raw_text) #solo se ejecuta cuando el evento ocurre   


client.start()
client.run_until_disconnected() #ejecutar el envento hasta que la sesion acabe








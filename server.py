#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def fetch_clients():
    while True:
        try:
            client, client_address = SERVER.accept()
            print("%s:%s si è collegato." % client_address)
            client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
            indirizzi[client] = client_address
            Thread(target=manage_clients, args=(client,client_address)).start()
        except:
            break

def manage_clients(client,client_address):
    try:
        nome = client.recv(BUFSIZ).decode("utf8")
        benvenuto = 'Benvenuto %s! Se vuoi lasciare la Chat, scrivi {quit} per uscire.' % nome
        client.send(bytes(benvenuto, "utf8"))
        msg = "%s si è connesso" % nome
        broadcast(bytes(msg, "utf8"))
        clients[client] = nome
        while True:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, nome+": ")
            else:
                try:
                    client.send(bytes("{quit}", "utf8"))
                    client.close()
                    del clients[client]
                    broadcast(bytes("%s si è disconnesso" % nome, "utf8"))
                    break
                except:
                    #questa clausola va aggiunta sennò se non chiudo esclusivamente digitando "{quit}" genera eccezione
                    del clients[client]
                    broadcast(bytes("%s si è disconnesso" % nome, "utf8"))
                    break
    except:
        print("%s:%s si è scollegato" % client_address)
                

def broadcast(msg, prefisso=""):
    for utente in clients:
        utente.send(bytes(prefisso, "utf8")+msg)
        
clients = {}
indirizzi = {}


HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Running...")
    ACCEPT_THREAD = Thread(target=fetch_clients)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

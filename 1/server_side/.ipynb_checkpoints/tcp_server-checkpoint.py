import socket
import logging
import json
import ssl

alldata = dict()
alldata['1']=dict(nomor=1, nama="David De Gea", posisi="GK 1")
alldata['2']=dict(nomor=2, nama="Victor Lindelof", posisi="DF 1")
alldata['3']=dict(nomor=3, nama="Eric Bailly", posisi="DF 2")
alldata['4']=dict(nomor=4, nama="Phil Jones", posisi="DF 3")
alldata['5']=dict(nomor=5, nama="Harry Maguire", posisi="DF 4")
alldata['6']=dict(nomor=6, nama="Paul Pogba", posisi="MF 1")
alldata['7']=dict(nomor=7, nama="Cristiano Ronaldo", posisi="FW 1")
alldata['8']=dict(nomor=8, nama="Juan Mata", posisi="MF 2")
alldata['9']=dict(nomor=9, nama="Anthony Martial", posisi="FW 2")
alldata['10']=dict(nomor=10, nama="Marcus Rashford", posisi="FW 3")
alldata['11']=dict(nomor=11, nama="Mason Greenwood", posisi="FW 4")
alldata['12']=dict(nomor=21, nama="Edinson Cavani", posisi="FW 5")
alldata['13']=dict(nomor=13, nama="Lee Grant", posisi="GK 2")
alldata['14']=dict(nomor=14, nama="Jesse Lingard", posisi="MF 3")
alldata['15']=dict(nomor=15, nama="Andreas Pereira", posisi="MF 4")
alldata['16']=dict(nomor=16, nama="Amad", posisi="MF 5")
alldata['17']=dict(nomor=17, nama="Fred", posisi="MF 6")
alldata['18']=dict(nomor=18, nama="Bruno Fernandes", posisi="MF 7")
alldata['19']=dict(nomor=19, nama="Raphael Varane", posisi="DF 5")
alldata['20']=dict(nomor=20, nama="Diogo Dalot", posisi="DF 6")

def versi():
    return "versi 0.0.1"


def proses_request(request_string):
    #format request
    # NAMACOMMAND spasi PARAMETER
    cstring = request_string.split(" ")
    hasil = None
    try:
        command = cstring[0].strip()
        if (command == 'getdatapemain'):
            # getdata spasi parameter1
            # parameter1 harus berupa nomor pemain
            logging.warning("getdata")
            nomorpemain = cstring[1].strip()
            try:
                logging.warning(f"data {nomorpemain} ketemu")
                hasil = alldata[nomorpemain]
            except:
                hasil = None
        elif (command == 'versi'):
            hasil = versi()
    except:
        hasil = None
    return hasil


def serialisasi(a):
    #print(a)
    #serialized = str(dicttoxml.dicttoxml(a))
    serialized =  json.dumps(a)
    logging.warning("serialized data")
    logging.warning(serialized)
    return serialized

def run_server(server_address):
    #--- INISIALISATION ---
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    logging.warning(f"starting up on {server_address}")
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1000)


    while True:
        # Wait for a connection
        logging.warning("waiting for a connection")
        connection, client_address = sock.accept()
        logging.warning(f"Incoming connection from {client_address}")
        # Receive the data in small chunks and retransmit it

        try:
            selesai=False
            data_received="" #string
            while True:
                data = connection.recv(32)
                logging.warning(f"received {data}")
                if data:
                    data_received += data.decode()
                    if "\r\n\r\n" in data_received:
                        selesai=True

                    if (selesai==True):
                        hasil = proses_request(data_received)
                        logging.warning(f"hasil proses: {hasil}")

                        #hasil bisa berupa tipe dictionary
                        #harus diserialisasi dulu sebelum dikirim via network
                        # Send data
                        # some data structure may have complex structure
                        # how to send such data structure through the network ?
                        # use serialization
                        #  example : json, xml

                        # complex structure, nested dict
                        # all data that will be sent through network has to be encoded into bytes type"
                        # in this case, the message (type: string) will be encoded to bytes by calling encode

                        hasil = serialisasi(hasil)
                        hasil += "\r\n\r\n"
                        connection.sendall(hasil.encode())
                        selesai = False
                        data_received = ""  # string
                        break

                else:
                   logging.warning(f"no more data from {client_address}")
                   break
            # Clean up the connection
        except ssl.SSLError as error_ssl:
            logging.warning(f"SSL error: {str(error_ssl)}")

if __name__=='__main__':
    try:
        run_server(('0.0.0.0', 12000))
    except KeyboardInterrupt:
        logging.warning("Control-C: Program berhenti")
        exit(0)
    finally:
        logging.warning("selesai")

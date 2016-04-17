import os
import sys
import socket
import thread
import time
import logging
import errno
from properties import property as prop

class SocketServer:
    """
    Multithreaded socket server.
    """
    __SERVER_SOCKET = None
    __HOST = None
    __PORT = None
    __TIMEOUT = prop.TIMEOUT

    def __init__(self, host=prop.HOST, port=prop.PORT):
        """
        Construct new SocketServer object.
        
        :type host: str
        :param host: Host name
        :type port: number
        :param port: Port number
        :return:
        """
        self.__HOST = host
        self.__PORT = port
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
        try:
            self.__SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__SERVER_SOCKET.settimeout(self.__TIMEOUT)
            
            if not os.path.exists(prop.TMP_DIR):
                os.makedirs(prop.TMP_DIR)
        except socket.error as error:
            logging.error("Error while create the server socket " + str(error))
            sys.exit(1)

    def __del__(self):
        """
        Free ServerSocket object.
        
        :return:
        """
        self.__SERVER_SOCKET.close()

    def run(self):
        """
        Server run method.
        Infinite multithreaded server loop.
        
        :return:
        """
        server = self.__SERVER_SOCKET
        try:
            server.bind((self.host(), self.port()))
            server.listen(5)
        except socket.error as error:
            logging.error("Server error: " +  str(error))
            sys.exit(1)
        try:
            logging.debug("Server running at port " + str(self.port()))
            print("Server running at port " + str(self.port()))
            while True:
                client, address =  server.accept()
                logging.debug("Client connected: " + str(address))
                try:
                    thread.start_new_thread(self.client_handler, (client, address))
                except socket.error as error:
                    logging.error("Server thread error: " +  str(error))
                    sys.exit()
        except socket.timeout as error:
            logging.debug("Server stop because " + str(error))
            print("Server stop because " + str(error))
            server.close()
            sys.exit(1)

    def host(self):
        """
        Return the server host name.
        
        :return: host name
        :rtype: str
        """
        return self.__HOST

    def port(self):
        """
        Return server port number.
        
        :return: port number
        :rtype: number
        """
        return self.__PORT

    def client_handler(self, client, address):
        """
        Callable method.
        Handle image receive from client.
        
        :return:
        """
        client.send("Connected to the server. Send a picture of the analysis." + os.linesep)
        filename = str(address[1]) + "_img.jpg"
        with open(prop.TMP_DIR + filename, "wb") as img:
            logging.debug(filename + " created")
            while True:
                try: 
                    data = client.recv(prop.BUFF_SIZE)
                    if not data: break
                    img.write(data)
                    client.send("Package arrived from client " + str(address[1]) + os.linesep)
                except socket.error as error:
                    if error.args[0] == errno.EAGAIN or error.args[0] == errno.EWOULDBLOCK:
                        time.sleep(0.1)
                        continue
                    else:
                        logging.error("Thread error: " +  str(error))
                        sys.exit(1)
        img.close()
        logging.debug("Client " + str(address[1]) + " close")    
        client.close()

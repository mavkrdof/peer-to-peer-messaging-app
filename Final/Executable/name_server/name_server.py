import asyncio
import logging
import json
import os


class Name_server:
    """
     Name_server the name server class deals with directing new clents to chat servers
     should be used on a static ip address
     does not require much proccessing power as only contatacted once per client
     vars:
        logger: logging object
            the error and info logger for the name server class
        save_file: str
            the path to the save file
        address_book: dict
            holds the addres of the current chat_server if any
        own_address: dict
            holds the address of the name server
        message_separator: bytes
            the message separator for communication over the network
        server_locked_in: bool
            whether or not a chat server has locked in hosting
            esures the name server can only have one chat server
    methods:
        add_address(name: str, ip: str, port: int)
            adds a new address to the address book
        read_in_address_book(save_file: str)
            reads in the address book from file
        save_address_book()
            saves the address book to file
        is_active_server()
            checks if there is an active server
        create_chat_server()
            creates a new chat server
        listner(server: asyncio.Server)
            listens for new clients
    """
    def __init__(self) -> None:
        """
        __init__ Initilizes variables for the name server
        params:
            logger: logging object
                the error and info logger for the name server class
            save_file: str
                the path to the save file
            address_book: dict
                holds the addres of the current chat_server if any
            own_address: dict
                holds the address of the name server
            message_separator: bytes
                the message separator for communication over the network
            server_locked_in: bool
                whether or not a chat server has locked in hosting
                esures the name server can only have one chat server
        returns: None
        """
        self.logger = logging.getLogger(name='{__name__}')
        logging.basicConfig(encoding='utf-8', level=logging.DEBUG, filemode='w')
        self.save_file = 'address_book.json'
        self.address_book: dict = self.read_in_address_book(self.save_file)
        self.own_address = {
            'name': 'name_server',
            'ip': '127.0.0.1',
            'port': 8888
        }
        self.message_separator: bytes = '\n'.encode()
        self.server_locked_in = False

    def add_address(self, name: str, ip: str, port: int) -> None:
        """
        add_address adds a new address to the address book

        Args:
            name (str): the name of the address
            ip (str): the ip of the address
            port (int): the port of the address
        """
        if isinstance(name, str) and isinstance(ip, str) and isinstance(port, int):
            if self.address_book.__contains__(name):
                self.logger.info(f'Address book already contains {name} replacing data')
            else:
                self.logger.info(f'Address book does not already contain {name} creating new entry')
            self.address_book[name] = {
                'name': name,
                'ip': ip,
                'port': port,
            }
            self.logger.debug(f'Successfully added address {name}')
            self.save_address_book()
        else:
            self.logger.error('Invalid address data')

    def read_in_address_book(self, save_file: str) -> dict:
        """
        read_in_address_book reads in the address book from file

        Args:
            save_file (str): the path to the save file for the address book

        Returns:
            dict: the address book as read in from file
        """
        if os.path.exists(save_file):
            with open(save_file, 'r') as file:
                address_book = json.load(file)
            return address_book
        else:
            return {}

    def is_active_server(self) -> bool:
        """
        is_active_server checks if the name server knows of an active chat server

        Returns:
            bool: whether or not the name server knows of an active chat server
        """
        if self.address_book.__contains__('chat_server'):
            self.logger.info('Chat server is active')
            return True
        elif self.server_locked_in:
            self.logger.info('Server is locked in')
            return True
        else:
            self.logger.info('No chat server established or locked in')
            return False

    async def create_name_server(self) -> None:
        """
        create_name_server hosts a new server on the network at the port and ip defined in the own_address variable
        """
        try:
            self.logger.info('Creating server...')
            server = await asyncio.start_server(self.listener, self.own_address['ip'], self.own_address['port'])
            self.logger.info('Server created')
            async with server:
                await server.serve_forever()
        except OSError as error:
            self.logger.error(error)

    def create_message(self, content, command) -> str:  # TODO finish
        """
        create_message formats a message to be sent over the network

        Args:
            content (any): the content of the message
            command (any): the command of the message

        Returns:
            str: a formatted message
        """
        if isinstance(content, str):
            content.replace(self.message_separator.decode(), '')
        message = {
            'command': command,
            'content': content,
            'sender': self.own_address['name']
        }
        message_json = json.dumps(message) + self.message_separator.decode()
        return message_json

    async def listener(self, reader, writer) -> None:
        """
        listener the listner for the name server runs on a seperate thread and listens for incoming messages

        Args:
            reader (asyncio.streams.StreamReader): reads from the network stream
            writer (asyncio.streams.StreamWriter): writes to the network stream
        """
        while True:
            try:
                message = await reader.readuntil(self.message_separator)
            except ConnectionResetError as error:
                self.logger.error(error)
                break
            except asyncio.exceptions.IncompleteReadError as error:
                self.logger.error(error)
                break
            message = message.decode()
            message = self.parse_message(message)
            self.logger.info(f'Received message: {message}')
            match message['command'].lower():
                case 'request server privileges':
                    if self.is_active_server():
                        response = self.create_message(
                            content='',
                            command='rejected'
                        )
                    else:
                        response = self.create_message(
                            content='',
                            command='accepted'
                        )
                        self.server_locked_in = True
                    writer.write(response.encode())
                    await writer.drain()
                    self.logger.info(f'Server locked in: {self.server_locked_in}')
                case 'server established':
                    self.add_address(name='chat_server', ip=message['content']['ip'], port=message['content']['port'])
                    self.logger.info(f'Added chat server to address book {message["content"]}')
                case 'server terminated':
                    self.remove_address('chat_server')
                    self.logger.info('Removed chat server from address book')
                case 'request current server ip and port':
                    if self.is_active_server():
                        response = self.create_message(
                            content=self.address_book['chat_server'],
                            command='server exists'
                        )
                        self.logger.info('Server exists, sending ip and port...')
                    else:
                        response = self.create_message(
                            content='',
                            command='no chat server'
                        )
                        self.logger.info('No chat server, sending no server...')
                    writer.write(response.encode())
                    await writer.drain()
                    self.logger.info(f'Response sent: {response}')
                case 'chat server terminated':
                    if self.ping_chat_server():
                        self.logger.info('Chat server is still alive')
                    else:
                        self.logger.info('Chat server is dead')
                        self.remove_address('chat_server')
                        self.logger.info('Removed chat server from address book')
                        self.server_locked_in = False
                        # response
                        response = self.create_message(
                            content='',
                            command='chat server dead'
                        )
                    writer.write(response.encode())
                case _:
                    self.logger.error('Invalid command')

    def ping_chat_server(self) -> bool:
        """
        ping_chat_server pings the chat server

        Returns:
            bool: whether or not the chat server is still alive
        """
        if self.address_book.__contains__('chat_server'):
            self.logger.info('Pinging chat server...')
            message = self.create_message(
                content='',
                command='ping'
            )
            response = self.send_message(
                message=message,
                address=self.address_book['chat_server']
            )
            if response is None:
                return False
            else:
                return True
        else:
            return False

    async def send_message(self, message: str, address: dict) -> dict | None:  # TODO pull from a queue
        """
        send_message sends a message to a specific address

        Args:
            message (str): the message to be sent, in json format usually
            address (dict): the name of the address to send the message to

        Returns:
            dict | None: a parsed resonse from the reciever
        """
        self.logger.info('Sending message...')
        reader, writer = await self.establish_connection(ip=address['ip'], port=address['port'])
        if reader is None or writer is None:
            self.logger.error('Connection Failed')
        else:
            writer.write(message.encode())
            await writer.drain()
            response: bytes = await reader.readuntil(separator=self.message_separator)
            self.logger.info('Successfully sent message')
            parsed_response = self.parse_message(message=response.decode())
            return parsed_response

    async def establish_connection(self, ip, port) -> tuple[asyncio.StreamReader | None, asyncio.StreamWriter | None]:
        """
        establish_connection establishes a connection to a specific address

        Args:
            ip (str): the ip of the address
            port (int): the port of the address

        Returns:
            tuple[asyncio.StreamReader | None, asyncio.StreamWriter | None]: a stream reader and writer if connection was successful else None
        """
        self.logger.info('Connecting...')
        reader, writer = None, None
        try:
            reader, writer = await asyncio.open_connection(ip, port)
            self.logger.info('Connected')
            return reader, writer
        except ConnectionRefusedError as error:
            self.logger.error(error)
        except OSError as error:
            self.logger.error(error)
        return reader, writer

    def parse_message(self, message: str) -> dict:
        """
        parse_message parses messages into a dictionary so that they can be processed

        Args:
            message (str): the message to be parsed

        Returns:
            dict: a parsed message
        """
        parsed_message = json.loads(message)
        return parsed_message

    def remove_address(self, address: str):
        """
        remove_address removes an address from the address book

        Args:
            address (str): the address to be removed
        """
        if address in self.address_book.keys():
            self.logger.info(f'Removing address {address}')
            self.address_book.pop(address)
            self.save_address_book()
        else:
            self.logger.error(f'Address {address} not found')

    def save_address_book(self):
        """
        save_address_book saves the address book to file
        """
        self.logger.info('Saving address book...')
        if os.path.exists(self.save_file):
            with open(self.save_file, 'w') as file:
                json.dump(self.address_book, file)
        else:
            with open(self.save_file, 'x') as file:
                json.dump(self.address_book, file)
        self.logger.info('Successfully saved address book')


if __name__ == '__main__':
    ns = Name_server()
    asyncio.run(ns.create_name_server())

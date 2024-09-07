import asyncio
import logging
import json
import os


class Name_server:
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
            match message['command']:
                case 'Request Server Privileges':
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
                case 'Server Established':
                    self.add_address(name='chat_server', ip=message['content']['ip'], port=message['content']['port'])
                    self.logger.info(f'Added chat server to address book {message["content"]}')
                case 'Server Terminated':
                    self.remove_address('chat_server')
                    self.logger.info('Removed chat server from address book')
                case 'Request Current Server Ip and Port':
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
                case _:
                    self.logger.error('Invalid command')

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

import asyncio
import json
import logging
import socket
import peertopeermessagingapp.RSA_encrypt as RSA_encrypt
import peertopeermessagingapp.RSA_decrypt as RSA_decrypt


# TODO chat server shuting down
class Network_manager:
    """
    Network_manager manages the network of the application
    attrs:
        app: app
            the app class
        logger: logging object
            the error and info logger for the name server class
        message_separator: bytes
            the message separator for communication over the network
        address_book: dict
            holds the address of the current chat_server if any
        own_address: dict
            holds the address of the name server
        message_queue: asyncio.Queue
            the message queue for the network manager
        chat_server_task: asyncio.Task
            the task for the chat server
        client_server_task: asyncio.Task
            the task for the client server
        message_queue_task: asyncio.Task
            the task for the message queue
    methods:
        start(self)
            starts the network manager
        add_address(self, name: str, ip: str, port: int, public_key_e: int, public_key_n: int)
            adds a new address to the address book
        load_address_book(self)
            loads the address book from file
        save_address_book(self)
            saves the address book to file
        is_active_server(self)
            checks if there is an active server
        create_chat_server(self)
            creates a new chat server
        listener(server: asyncio.Server)
            listens for new clients
        handle_chat_message(message)
            handles the receiving of a chat message
        __shutdown_network_manager(self)
            shuts down the network manager
    """
    def __init__(self, app) -> None:
        """
        __init__ initialises the network manager

        Args:
            app (_type_): the app class
        attrs:
            app: app
                the app class
            logger: logging object
                the error and info logger for the name server class
            message_separator: bytes
                the message separator for communication over the network
            address_book: dict
                holds the address of the current chat_server if any
            own_address: dict
                holds the address of the name server
            message_queue: asyncio.Queue
                the message queue for the network manager
            chat_server_task: asyncio.Task
                the task for the chat server
            client_server_task: asyncio.Task
                the task for the client server
            message_queue_task: asyncio.Task
                the task for the message queue
        """
        self.app = app
        self.logger = logging.getLogger(name='{__name__}')
        self.message_separator: bytes = '\n'.encode()  # TODO decide message sep
        self.address_book: dict = {}
        self.message_queue = asyncio.Queue()
        self.chat_server_task: asyncio.Task | None = None  # type: ignore
        self.client_server_task: asyncio.Task | None = None
        self.message_queue_task: asyncio.Task | None = None
        self.shutdown_event = asyncio.Event()
        self.main_task: asyncio.Task | None  = None

    def start(self) -> None:
        """
        start starts the network manager
        """
        self.logger.info('Starting network manager...')
        self.own_address = {
            'name': self.app.backend.user_data.username,
            'ip': socket.gethostbyname(socket.gethostname()),
            'port': 8000,
            'public_key_n': self.app.backend.user_data.get_public_key('n'),
            'public_key_e': self.app.backend.user_data.get_public_key('e')
        }
        self.add_address(
            name='name_server',
            ip='127.100.1',  # default place holder value
            port=8888,  # TODO should be loaded from constant
            public_key_e=0,  # unencrypted comms
            public_key_n=0
            )  # a small server that holds the name and address of the current active server
        self.load_address_book()
        if self.main_task is None:
            self.__boot_main_loop()
        elif not self.main_task.done():
            self.logger.debug('main task done')
            self.__boot_main_loop()

    def __boot_main_loop(self) -> None:
        if self.is_event_loop():
            self.logger.info('Starting local network with alternate method')
            self.main_task = asyncio.create_task(self.main())
        else:
            self.logger.info('Creating new event loop...')
            asyncio.run(self.main())  # TODO find whether or not their is another event loop and find fix: Error in handler: asyncio.run() cannot be called from a running event loop

    def is_main_loop_running(self) -> bool:
        """
        is_main_loop_running checks if a main loop is currently running

        Returns:
            bool: whether or not a main loop is running
        """
        if self.main_task is None:
            if self.is_event_loop():
                return False
            else:
                return True
        elif self.main_task.done():
            return True
        else:
            return False

    def is_event_loop(self) -> bool:
        """
        is_event_loop checks if an event loop is running

        Returns:
            bool: whether or not an event loop is running
        """
        try:
            asyncio.get_running_loop()
            self.logger.warning('Event loop already running')
            return True
        except RuntimeError:
            self.logger.info('No event loop running')
            return False

    async def main(self) -> None:
        """
        main starts all the main processes of the network manager
        """
        self.logger.debug('Checking for established server...')
        server_exists = await self.is_active_server()
        if server_exists:
            self.logger.info('Found established server')
        else:
            self.logger.info('Attempting to establishing server...')
            await self.create_chat_server()
        # start tasks
        self.logger.info('Starting tasks...')
        self.client_server_task = asyncio.create_task(self.create_chat_client())
        asyncio.create_task(self.get_address_book())
        self.message_queue_task = asyncio.create_task(self.send_messages_from_queue())
        self.logger.info('Tasks started')
        # update address book
        self.logger.debug('Updating address book...')
        asyncio.create_task(self.get_address_book())
        # await shutdown event
        self.logger.debug('Finished booting local network awaiting shutdown')
        await self.shutdown_event.wait()
        self.logger.info('Shutdown event triggered shutting down local network')
        await self.__shutdown_network_manager()
        self.logger.info('Shutdown complete clearing event')
        # clear shutdown event
        self.shutdown_event.clear()
        self.logger.info('Shutdown event cleared')

    def shutdown(self) -> None:
        """
        shutdown triggers the shutdown of the network manager and waits till shutdown event cleared or timeout
        """
        self.logger.info('Triggering local network shutdown')
        self.shutdown_event.set()

    async def __shutdown_network_manager(self) -> None:
        """
        shutdown_network_manager shuts down the network manager
        """
        self.save_address_book()
        await self.__shutdown_chat_server()

        if self.client_server_task is not None:
            self.logger.info('Shutting down client server')
            self.client_server_task.cancel()
            try:
                await self.client_server_task
            except asyncio.CancelledError:
                self.logger.info('Client server shutdown')
        else:
            self.logger.error('No client server to shutdown')

        if self.message_queue_task is not None:
            self.logger.info('Shutting down message queue')
            self.message_queue_task.cancel()
            try:
                await self.message_queue_task
            except asyncio.CancelledError:
                self.logger.info('Message queue shutdown')
        else:
            self.logger.error('No message queue to shutdown')

    async def __shutdown_chat_server(self):
        """
        __shutdown_chat_server shuts down the chat server if it exists
        """
        if self.chat_server_task is not None:
            self.logger.info('Shutting down chat server')
            self.chat_server_task.cancel()
            try:
                await self.chat_server_task
            except asyncio.CancelledError:
                self.logger.info('chat server terminated')
                self.logger.info('Notifying name server')
                message = self.create_message(
                    content=self.address_book['chat_server'],
                    command='chat server shutdown',
                    target='name_server'
                )
                if message is None:
                    self.logger.error('No message to send')
                else:
                    response_reader = await self.send_message(
                        address=self.address_book['name_server'],
                        message=message
                    )
                    parsed_response = await self.read_and_parse_response(response_reader)
                    self.logger.debug(f'Name server Response: {parsed_response}')
        else:
            self.logger.warning('No chat server to shutdown')

    def load_address_book(self) -> None:
        """
        load_address_book loads the address book from user_data
        """
        self.address_book = self.app.backend.user_data.address_book
        if isinstance(self.address_book, dict):
            pass
        else:
            self.address_book = {}

    def save_address_book(self) -> None:
        """
        save_address_book saves the address book to user_data
        """
        self.app.backend.user_data.address_book = self.address_book

    async def is_active_server(self) -> bool:  # TODO add the ability to get the updated server location if server is locked in but not currently active
        """
        is_active_server checks if the name server knows of an active chat server

        Returns:
            bool: whether or not the name server knows of an active chat server
        """
        reader, writer = await self.establish_connection(
            ip=self.address_book['name_server']['ip'],
            port=self.address_book['name_server']['port']
            )
        if reader is None or writer is None:
            self.logger.error('Connection to name server Failed')
            return False
        else:
            self.logger.info('connections to name_server established')
            request_chat_server_message = self.create_message(
                    target='name_server',
                    command='Request Current Server Ip and Port',
                    content=''
                    )
            if request_chat_server_message is None:
                self.logger.error('no message to send')
                return False
            else:
                writer.write(
                    request_chat_server_message.encode()
                    )  # request the current server ip and port from the established peer
                await writer.drain()
                self.logger.info('requested server ip and port from name server awaiting response...')
                parsed_response = await self.read_and_parse_response(reader)
                if parsed_response is None:
                    self.logger.warning('invalid response')
                    return False
                else:
                    self.logger.info(f'Response: {parsed_response}')
                    try:
                        if parsed_response['sender'] == self.address_book['name_server']['name']:
                            if parsed_response['content'] == 'no chat server':
                                self.logger.info('No chat server established')
                                return False
                            elif parsed_response['command'] == 'server exists':
                                self.logger.info('found established chat server')
                                self.add_address(
                                    name='chat_server',
                                    ip=parsed_response['content']['ip'],
                                    port=parsed_response['content']['port'],
                                    public_key_e=0,  # unencrypted comms
                                    public_key_n=0
                                )
                                return True
                            else:
                                self.logger.error('Establish peer returned invalid Response')
                                return False
                        else:
                            self.logger.error('Establish peer returned invalid Response')
                            return False
                    except ValueError:
                        self.logger.error('Establish peer returned invalid Response')
                        return False

    async def read_and_parse_response(self, reader) -> dict | None:
        """
        read_and_parse_response reads the response to a message and parses it

        Args:
            reader (asyncio.StreamReader): allows reading from the network stream

        Returns:
            dict | None: the parsed response
        """
        try:
            response = await reader.readuntil(self.message_separator)
            parsed_response = self.parse_message(message=response)
            return parsed_response
        except ConnectionResetError as error:
            self.logger.error(error)
        except asyncio.exceptions.IncompleteReadError as error:
            self.logger.error(error)

    def add_address(self, name: str, ip: str, port: int, public_key_n: int, public_key_e: int) -> None:
        """
        add_address adds an address to the address book

        Args:
            name (str): the name of the address
            ip (str): the ip of the address
            port (int): the port of the address
            public_key_n (int): the n value of the public key of the address
            public_key_e (int): the e value of the public key of the address
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
                'public_key_n': public_key_n,
                'public_key_e': public_key_e
            }
            self.logger.debug(f'Successfully added address {name}')
            self.logger.debug('Saving address book...')
            self.save_address_book()
            self.logger.debug('saved address book')
            # sync contact data from chat server
            self.logger.debug('Syncing contact data...')
            self.add_message_to_queue('update address book', 'chat_server')
        else:
            self.logger.error('Invalid address data')

    def parse_message(self, message) -> dict:
        """
        parse_message parses messages into a dictionary so that they can be processed

        Args:
            message (str): the message to be parsed

        Returns:
            dict: the parsed message
        """
        parsed_message = json.loads(message)
        encrypted_message_content = parsed_message['content']
        if [isinstance(i, int) for i in encrypted_message_content].count(False) > 0:
            self.logger.info('Message unencrypted')
            message_content = encrypted_message_content
        else:
            message_content = self.decrypt_message_content(
                private_key_d=self.app.backend.user_data.get_private_key('d'),
                private_key_n=self.app.backend.user_data.get_private_key('n'),
                content=encrypted_message_content
                )
        parsed_message['content'] = message_content
        return parsed_message

    async def report_dead_chat_server(self) -> None:
        """
        report_dead_chat_server reports that the chat server is dead
        """
        self.logger.info('Reporting dead chat server...')
        message = self.create_message(
            content=self.address_book['chat_server'],
            command='chat server shutdown',
            target='name_server'
        )
        if message is None:
            self.logger.error('No message to send')
        else:
            response_reader = await self.send_message(
                address=self.address_book['name_server'],
                message=message
            )
            parsed_response = await self.read_and_parse_response(response_reader)
            if parsed_response is None:
                self.logger.warning('Invalid response')
            else:
                if parsed_response['command'] == 'chat server dead':
                    self.logger.info('Chat server dead')
                    self.logger.debug('Removing chat server from address book')
                    self.address_book.pop('chat_server')
                    self.logger.debug('Chat server removed from address book')
                    self.logger.debug('Saving address book...')
                    self.save_address_book()
                    self.logger.debug('saved address book')
                    self.logger.info('Attempting to creat new chat server...')
                    await self.create_chat_server()
                else:
                    self.logger.info('Chat server not dead')

    def add_message_to_queue(self, content, target) -> None:  # TODO Remove async as means cant be called from outside
        """
        add_message_to_queue adds a message to the message queue

        Args:
            content (str): the content of the message
            target (str): the target of the message
        """
        self.logger.info('Adding message to queue...')
        if content == 'update address book':
            self.message_queue.put_nowait(content)
        message = self.create_message(
            target=target,
            content=content,
            command='message'
            )
        queue_item = {
            'message': message,
            'target': target
        }
        self.message_queue.put_nowait(queue_item)
        self.logger.info('Message added to queue')

    async def send_messages_from_queue(self) -> None:
        """
        send_messages_from_queue sends messages from the message queue
        runs on a separate thread to allow separation between the asynchronous network manager and the rest of the application
        """
        running = True
        while running:
            try:
                self.logger.info('Awaiting message from queue...')
                message = await self.message_queue.get()
            except Exception as e:
                self.logger.error(f'Failed to get message from queue {e}')
            try:
                if message == 'update address book':
                    await self.get_address_book()
                    continue
                else:
                    self.logger.info('Found message in queue...')
                    acknowledgement = await self.send_message(
                        message=message['message'],
                        address=self.address_book[message['target']]
                        )
                    parsed_acknowledgement = self.parse_message(message=acknowledgement)
                    if isinstance(parsed_acknowledgement, dict):
                        if parsed_acknowledgement['command'] == 'message sent':
                            self.logger.info('Message sent')
                            continue  # skips message failure
                    # message failure
                    self.add_message_to_queue(
                        content=message['message'],
                        target=message['target']
                        )
                    self.app.GUI.chat_screen.failed_to_send_message()
                    self.logger.error('Failed to send message')
            except Exception as e:
                self.logger.error(f'Encountered error: {e}')
                # TODO determine if the above code is necessary
                self.app.GUI.chat_screen.failed_to_send_message()
                self.logger.error('Failed to send message')

    async def send_message(self, message: str, address: dict) -> dict | None:  # TODO pull from a queue
        """
        send_message sends a message to a specific address

        Args:
            message (str): the message to be sent, in json format usually
            address (dict): the name of the address to send the message to

        Returns:
            dict | None: a parsed response from the receiver
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
            parsed_response = self.parse_message(message=response)
            return parsed_response

    async def get_address_book(self) -> None:
        """
        get_address_book updates the address book from the chat server
        """
        self.logger.info('Updating address book...')
        message = self.create_message(
                target='chat_server',
                command='requesting address book',
                content=''
                )
        if message is None:
            self.logger.error('no message to send')
        else:
            response = await self.send_message(
                message=message,
                address=self.address_book['chat_server']
            )
            parsed_message = self.parse_message(message=response)
            if parsed_message is None:
                self.logger.error('Failed to get address book')
                self.logger.debug('Assuming that the chat server is dead')
                await self.report_dead_chat_server()
            elif isinstance(parsed_message, dict):
                for key in parsed_message['content']:
                    self.add_address(
                        name=key,
                        ip=parsed_message['content'][key]['ip'],
                        port=parsed_message['content'][key]['port'],
                        public_key_e=parsed_message['content'][key]['public_key_e'],
                        public_key_n=parsed_message['content'][key]['public_key_n']
                        )
            self.logger.info('Address book updated')

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

    def create_message(self, content, command: str, target: str) -> str | None:  # TODO finish
        """
        create_message formats a message to be sent over the network

        Args:
            content (any): the content of the message
            command (str): the command of the message
            target (str): the name of the address to send the message to

        Returns:
            str | None: a formatted message
        """
        if self.address_book.__contains__(target):
            self.logger.debug('address found')
            target_address = self.address_book[target]
            content = json.dumps(content)
            if target_address['public_key_e'] == 0 and target_address['public_key_n'] == 0:
                self.logger.info('Not Encrypting message')
            else:
                content = self.encrypt_message_content(
                    public_key_e=target_address['public_key_e'],
                    public_key_n=target_address['public_key_n'],
                    content=content
                    )
            content.replace(self.message_separator.decode(), '')
            message = {
                'command': command,
                'content': content,
                'sender': self.own_address['name']
            }
            message_json = json.dumps(message) + self.message_separator.decode()
            return message_json
        else:
            self.logger.debug('address not found')
            return None

    def handle_chat_message(self, message: dict) -> None:
        """
        handle_chat_message handles the receiving of a chat message

        Args:
            message (dict): the message to be added to the queue
        """
        if message.__contains__('content') and message.__contains__('sender'):
            self.app.backend.message_received(
                content=message['content'],
                sender=message['sender'],
                target=message['target']
                )
        else:
            self.logger.error('Invalid message')

    def encrypt_message_content(self, public_key_n: int, public_key_e: int, content: str) -> str:
        """
        encrypt_message_content encrypts the content of the message if public key is not 0

        Args:
            public_key_n (int): the public key n of the address
            public_key_e (int): the public key e of the address
            content (str): the content to be encrypted

        Returns:
            str: the encrypted content converted to a json formatted string
        """
        encrypted = RSA_encrypt.encrypt_data(
            public_key_e=public_key_e,
            public_key_n=public_key_n,
            plain_text=content
            )
        str_encrypted = json.dumps(encrypted)
        return str_encrypted

    def decrypt_message_content(self, private_key_n: int, private_key_d: int, content: str):
        """
        decrypt_message_content decrypts the content of the message the content is a json formatted string

        Args:
            private_key_n (int): own private key n
            private_key_d (int): own private key d
            content (str): the content to be decrypted

        Returns:
            any: the decrypted content
        """
        parsed_content = json.loads(content)
        if parsed_content is None:
            return ''
        if isinstance(parsed_content, list):
            decrypted = RSA_decrypt.decrypt_data(
                private_key_d=private_key_d,
                private_key_n=private_key_n,
                encrypted=parsed_content
                )
            return decrypted
        else:
            return parsed_content

    async def create_chat_client(self) -> None:
        """
        create_chat_client creates a client server at the port and ip defined in the own_address variable
        """
        self.logger.info('Creating client...')
        try:
            server = await asyncio.start_server(self.client_listener, self.own_address['ip'], self.own_address['port'])
            async with server:
                await server.serve_forever()
        except OSError as error:
            self.logger.error(error)

    async def create_chat_server(self) -> None:
        """
        create_chat_server requests the name server to create a chat server
        if the name server accepts the request, it creates the chat server
        at the port 8888 and a ip that is the ip of the machine
        """
        ip = socket.gethostbyname(socket.gethostname())
        port = 8888
        self.logger.info('Creating server...')
        server_address = {
            'name': f'{self.own_address["name"]}-server',
            'ip': ip,
            'port': port
        }
        try:
            self.logger.info('Requesting server privileges')
            request_server_message = self.create_message(
                    target='name_server',
                    command='Request Server Privileges',
                    content=server_address
                    )
            if request_server_message is None:
                self.logger.error('no message to send')
            else:
                response = await self.send_message(
                    message=request_server_message,
                    address=self.address_book['name_server']
                    )
                if response is None:
                    self.logger.error('Established Peer response invalid')
                else:
                    match response['command']:
                        case 'accepted':
                            server = await asyncio.start_server(self.server_listener, ip, port)
                            self.logger.info('Server created')
                            server_established_message = self.create_message(
                                    target='name_server',
                                    content=server_address,
                                    command='Server Established',
                                    )
                            if server_established_message is None:
                                self.logger.error('no message to send')
                            else:
                                await self.send_message(
                                    message=server_established_message,
                                    address=self.address_book['name_server']
                                    )
                                self.add_address(
                                    name='chat_server',
                                    ip=ip,
                                    port=port,
                                    public_key_e=0,  # unencrypted comms
                                    public_key_n=0
                                    )
                            self.chat_server_task: asyncio.Task = asyncio.create_task(self.init_server(server))
                        case 'rejected':
                            self.logger.warn('Established peer rejected server privileges')
                            await self.is_active_server()
                        case _:
                            self.logger.error('Established Peer response invalid')
        except OSError as error:
            self.logger.error(error)

    async def init_server(self, server):
        """
        init_server initializes the server

        Args:
            server (asyncio.Server): the server to be initialized
        """
        async with server:
            await server.serve_forever()

    async def client_listener(self, reader, writer) -> None:
        """
        client_listener the listener for the client

        Args:
            reader (asyncio.streams.StreamReader): allows reading from the network stream
            writer (asyncio.streams.StreamWriter): allows writing to the network stream
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
                case 'message':
                    self.handle_chat_message(message)
                case _:
                    self.logger.error('Invalid command')

    async def server_listener(self, reader, writer) -> None:
        """
        server_listener the listener for the server

        Args:
            reader (asyncio.streams.StreamReader): allows reading from the network stream
            writer (asyncio.streams.StreamWriter): allows writing to the network stream
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
                case 'update address book':
                    if isinstance(message['content'], dict):
                        updated_client_address_book = {
                            key: self.address_book.get(key, message['content'][key])
                            for key in message['content']
                        }
                        response = self.create_message(
                            target=message['sender'],
                            content=updated_client_address_book,
                            command='address book data'
                            )
                    if response is None:
                        self.logger.error('no message to send')
                    else:
                        writer.write(response.encode())
                        await writer.drain()
                case 'new client':
                    if isinstance(message['content'], dict):
                        if message.__contains__('ip') and message.__contains__('port') and message.__contains__('name'):
                            self.add_address(
                                name=message['content']['name'],
                                ip=message['content']['ip'],
                                port=message['content']['port'],
                                public_key_e=message['content']['public_key_e'],
                                public_key_n=message['content']['public_key_n']
                                )
                case _:
                    self.logger.error('Invalid command')


if __name__ == '__main__':
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, filemode='w')
    nm = Network_manager(app='test')
    nm.start()

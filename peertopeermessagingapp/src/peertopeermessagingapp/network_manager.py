import asyncio
import json
import logging
import socket
import peertopeermessagingapp.src.peertopeermessagingapp.RSA_encrypt as RSA_encrypt
import peertopeermessagingapp.src.peertopeermessagingapp.RSA_decrypt as RSA_decrypt


# TODO must add the ability to manage an address book of all connected users (holding: ip, port and username(figure out how to deal with dupilicate usernames)) and pass that book onto new server when this server shuts down
class Network_manager:  # TODO Server maintenance instance should be on a different port, define a message Structure eg need type, destination, content, make sure to check that their is not already a server running before creating your own
    def __init__(self, app) -> None:
        self.app = app
        self.logger = logging.getLogger(name='{__name__}')
        self.message_separator: bytes = '\n'.encode()  # TODO decide message sep
        self.address_book: dict = {}
        self.own_address = {  # TODO Finish
            'name': '',
            'ip': '',
            'port': 0,
            'public_key_n': 0,
            'public_key_e': 0
        }
        self.message_queue = asyncio.Queue()

    def start(self) -> None:
        self.add_address(
            name='name_server',
            ip='127.100.1',  # default place holder value
            port=8888,  # TODO should be loaded from constant
            public_key_e=0,  # unencrypted comms
            public_key_n=0
            )  # a small server that holds the name and address of the current active server
        self.load_address_book()
        asyncio.run(self.main())

    async def main(self) -> None:
        server_exists = await self.is_active_server()
        if server_exists:
            self.logger.info('Found established server')
        else:
            await self.create_chat_server()
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.create_chat_client())
            tg.create_task(self.get_address_book())
            tg.create_task(self.send_messages_from_queue())
        # update address book
        message = self.create_message(
            content=self.address_book,
            command='update address book',
            target='chat_server'
        )
        if message is None:
            self.logger.error('No message to send')
        else:
            await self.send_message(
                address=self.address_book['chat_server'],
                message=message
            )

    def load_address_book(self) -> None:
        self.address_book = self.app.backend.user_data.address_book
        if isinstance(self.address_book, dict):
            pass
        else:
            self.address_book = {}

    def save_address_book(self) -> None:
        self.app.backend.user_data.address_book = self.address_book

    async def is_active_server(self) -> bool:
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
        try:
            response = await reader.readuntil(self.message_separator)
            parsed_response = self.parse_message(message=response)
            return parsed_response
        except ConnectionResetError as error:
            self.logger.error(error)
        except asyncio.exceptions.IncompleteReadError as error:
            self.logger.error(error)

    def add_address(self, name: str, ip: str, port: int, public_key_n: int, public_key_e: int) -> None:
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
        else:
            self.logger.error('Invalid address data')

    def parse_message(self, message) -> dict:
        parsed_message = json.loads(message)
        encrypted_message_content = parsed_message['content']
        message_content = self.decrypt_message_content(
            private_key_d=self.app.backend.user_data.get_private_key('d'),
            private_key_n=self.app.backend.user_data.get_private_key('n'),
            content=encrypted_message_content
            )
        parsed_message['content'] = message_content
        return parsed_message

    async def add_message_to_queue(self, content, target) -> None:  # TODO Remove async as means cant be called from outside
        self.logger.info('Adding message to queue...')
        if content == 'update address book':
            await self.message_queue.put(content)
        message = self.create_message(
            target=target,
            content=content,
            command='send message'
            )
        queue_item = {
            'message': message,
            'target': target
        }
        await self.message_queue.put(queue_item)
        self.logger.info('Message added to queue')

    async def send_messages_from_queue(self) -> None:
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
                    await self.add_message_to_queue(
                        content=message['message'],
                        target=message['target']
                        )
                    self.app.GUI_manager.chat_screen.failed_to_send_message()
                    self.logger.error('Failed to send message')
            except Exception as e:
                self.logger.error(f'Encountered error: {e}')
                # TODO determine if the above code is necessary
                self.app.GUI_manager.chat_screen.failed_to_send_message()
                self.logger.error('Failed to send message')

    async def send_message(self, message: str, address: dict) -> dict | None:  # TODO pull from a queue
        self.logger.info('Sending message...')
        reader, writer = await self.establish_connection(ip=address['ip'], port=address['port'])
        if reader is None or writer is None:
            self.logger.error('Connection Failed')
        else:
            writer.write(message.encode())
            await writer.drain()
            response: bytes = await reader.readuntil(separator=self.message_separator)
            self.logger.info('Successfully sent message')
            parsed_message = self.parse_message(message=response)
            return parsed_message

    async def get_address_book(self) -> None:
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
        if self.address_book.__contains__(target):
            target_address = self.address_book['target']
            content = json.dumps(content)
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

    def encrypt_message_content(self, public_key_n: int, public_key_e: int, content: str) -> str:
        encrypted = RSA_encrypt.encrypt_data(
            public_key_e=public_key_e,
            public_key_n=public_key_n,
            plain_text=content
            )
        str_encrypted = json.dumps(encrypted)
        return str_encrypted

    def decrypt_message_content(self, private_key_n: int, private_key_d: int, content: str):
        parsed_content = json.loads(content)
        if parsed_content is None:
            return ''
        if isinstance(parsed_content, list):
            if [isinstance(i, int) for i in parsed_content].count(False) > 0:
                return parsed_content
            else:
                decrypted = RSA_decrypt.decrypt_data(
                    private_key_d=private_key_d,
                    private_key_n=private_key_n,
                    encrypted=parsed_content
                    )
                return decrypted
        else:
            return parsed_content

    async def create_chat_client(self) -> None:
        self.logger.info('Creating client...')
        try:
            server = await asyncio.start_server(self.client_listener, self.own_address['ip'], self.own_address['port'])
            async with server:
                await server.serve_forever()
        except OSError as error:
            self.logger.error(error)

    async def create_chat_server(self) -> None:
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
                            async with asyncio.TaskGroup() as tg:
                                tg.create_task(self.init_server(server))
                        case 'rejected':
                            self.logger.warn('Established peer rejected server privileges')
                        case _:
                            self.logger.error('Established Peer response invalid')
        except OSError as error:
            self.logger.error(error)

    async def init_server(self, server):
        async with server:
            await server.serve_forever()

    async def client_listener(self, reader, writer) -> None:
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
                case _:
                    self.logger.error('Invalid command')

    async def server_listener(self, reader, writer) -> None:
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
                        if message.includes('ip') and message.includes('port') and message.includes('name'):
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

import asyncio
import json
import logging


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
            'port': 0
        }
        self.add_address(name='name_server', ip='127.0.0.1', port=8888)  # a small server that holds the name and address of the current active server

    async def main(self, ip, port) -> None:
        server_exists = await self.is_active_server()
        if server_exists:
            self.logger.info('Found established server')
        else:
            await self.create_chat_server(
                ip=ip, port=port
                )
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.create_chat_client())
            tg.create_task(self.get_address_book())
            tg.create_task(
                self.send_message(
                    message='Hello, I am connected!',
                    address=self.address_book['chat_server']
                    )
                )

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
            writer.write(self.create_message(command='Request Current Server Ip and Port', content='').encode())  # request the current server ip and port from the established peer
            await writer.drain()
            self.logger.info('requested server ip and port from name server awaiting response...')
            parsed_response = await self.read_and_parse_response(reader)
            if parsed_response is None:
                self.logger.warning('invalid resonse')
                return False
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
                            port=parsed_response['content']['port']
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

    def add_address(self, name: str, ip: str, port: int) -> None:
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
        else:
            self.logger.error('Invalid address data')

    def parse_message(self, message):
        message = json.loads(message)
        return message

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
        response = await self.send_message(
            message=self.create_message(
                command='requesting address book',
                content=''
                ),
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
                    port=parsed_message['content'][key]['port']
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

    def create_message(self, content, command) -> str:  # TODO finish
        if isinstance(content, str):
            content.replace(self.message_separator.decode(), '')
        message = {
            'command': command,
            'content': content,
            'sender': self.own_address['name']
        }
        message_json = json.dumps(message) + self.message_separator.decode()
        return message_json

    async def create_chat_client(self) -> None:
        self.logger.info('Creating client...')
        try:
            server = await asyncio.start_server(self.client_listener, self.own_address['ip'], self.own_address['port'])
            async with server:
                await server.serve_forever()
        except OSError as error:
            self.logger.error(error)

    async def create_chat_server(self, ip, port) -> None:
        self.logger.info('Creating server...')
        server_address = {
            'name': f'{self.own_address["name"]}-server',
            'ip': ip,
            'port': port
        }
        try:
            self.logger.info('Requesting server privileges')
            response = await self.send_message(
                message=self.create_message(
                    command='Request Server Privileges',
                    content=server_address
                    ),
                address=self.address_book['name_server']
                )
            if response is None:
                self.logger.error('Established Peer response invalid')
            else:
                match response['command']:
                    case 'accepted':
                        server = await asyncio.start_server(self.server_listener, ip, port)
                        self.logger.info('Server created')
                        await self.send_message(
                            message=self.create_message(
                                content=server_address,
                                command='Server Established', 
                                ),
                            address=self.address_book['name_server']
                            )
                        self.add_address(name='chat_server', ip=ip, port=port)
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
        try:
            while True:
                data: bytes = await reader.read(1024)
                self.logger.info(f'Received: {data.decode()}')
        except ConnectionResetError as error:
            self.logger.error(error)
        finally:
            self.logger.info('Closing connection')
            writer.close()

    async def server_listener(self, reader, writer) -> None:
        try:
            while True:
                data: bytes = await reader.read(1024)
                self.logger.info(f'Received: {data.decode()}')
        except ConnectionResetError as error:
            self.logger.error(error)
        finally:
            self.logger.info('Closing connection')
            writer.close()


if __name__ == '__main__':
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, filemode='w')
    nm = Network_manager(app='test')
    asyncio.run(nm.main(ip='127.0.0.1', port=4444))  # TODO move into create chat serve func dont define ip and port here

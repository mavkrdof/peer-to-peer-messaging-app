import asyncio
import logging


# TODO must add the ability to manage an address book of all connected users (holding: ip, port and username(figure out how to deal with dupilicate usernames)) and pass that book onto new server when this server shuts down
class Network_manager:  # TODO Server maintainance instance should be on a different port, define a message Structure eg need type, destination, content, make sure to check that their is not already a server running before creating your own
    def __init__(self, app) -> None:
        self.app = app
        self.logger = logging.getLogger(name='{__name__}')
        self.message_separator: bytes = ''.encode()
        self.address_book: dict = {}
        self.add_address(name='established_peer', ip='', port=0)  # a small server that holds the name and address of the current active server

    async def main(self, ip, port) -> None:
        async with asyncio.TaskGroup() as tg:
            if await self.is_active_server():
                self.logger.info('Found established server')
            else:
                tg.create_task(
                    self.create_server(
                        ip=ip, port=port
                        )
                    )
            tg.create_task(
                self.send_message(
                    message='Hello, I am connected!',
                    ip=self.address_book['server']['ip'],
                    port=self.address_book['server']['port']
                    )
                )

    async def is_active_server(self) -> bool:
        connection = await self.establish_connection(
            ip=self.address_book['established_peer']['ip'],
            port=self.address_book['established_peer']['port']
            )
        if connection is None:
            self.logger.error('Connection to established peer Failed')
            return False
        else:
            reader, writer = connection
            writer.write('Current Server Ip and Port'.encode())  # request the current server ip and port from the established peer
            await writer.drain()
            response = await reader.readuntil(self.message_separator)
            parsed_response = self.parse_message(message=response)
            try:
                if parsed_response['sender'] == self.address_book['established_peer']['name']:
                    if parsed_response['content'] == 'No Server':
                        return False
                    elif isinstance(parsed_response['content'], dict):
                        self.add_address(
                            name=parsed_response['content']['name'],
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

    def add_address(self, name: str, ip: str, port: int) -> None:
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

    def parse_message(self, message) -> dict:
        return message

    async def send_message(self, message, ip, port) -> None:  # TODO pull from a queue
        self.logger.info('Sending message...')
        connection = await self.establish_connection(ip, port)
        if connection is None:
            self.logger.error('Connection Failed')
        else:
            reader, writer = connection
            writer.write(message.encode())
            await writer.drain()
            self.logger.info('Successfully sent message')

    async def establish_connection(self, ip, port) -> tuple[asyncio.StreamReader, asyncio.StreamWriter] | None:
        self.logger.info('Connecting...')
        try:
            reader, writer = await asyncio.open_connection(ip, port)
            self.logger.info('Connected')
            return reader, writer
        except ConnectionRefusedError as error:
            self.logger.error(error)
        except OSError as error:
            self.logger.error(error)

    async def create_server(self, ip, port) -> None:
        self.logger.info('Creating server...')
        try:
            server = await asyncio.start_server(self.listener, ip, port)
            self.logger.info('Server created')
            async with server:
                await server.serve_forever()
        except OSError as error:
            self.logger.error(error)

    async def listener(self, reader, writer) -> None:
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
    asyncio.run(nm.main(ip='127.0.0.1', port=8888))

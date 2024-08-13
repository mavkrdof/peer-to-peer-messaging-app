import asyncio
import logging


# TODO must add the ability to manage an address book of all connected users (holding: ip, port and username(figure out how to deal with dupilicate usernames)) and pass that book onto new server when this server shuts down
class Network_manager:  # TODO Server maintainance instance should be on a different port, define a message Structure eg need type, destination, content, make sure to check that their is not already a server running before creating your own
    def __init__(self, app) -> None:
        self.app = app
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self.logger = logging.getLogger(name='{__name__}')

    async def main(self, ip, port) -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.create_server(ip, port))
            tg.create_task(self.send_message('Hello, I am connected!', ip, port))

    async def send_message(self, message, ip, port) -> None:  # TODO pull from a queue
        self.logger.info('Sending message...')
        await self.establish_connection(ip, port)
        if self.writer is None:
            self.logger.error('Connection not established')
        else:
            self.writer.write(message.encode())
            await self.writer.drain()
            self.logger.info('Successfully sent message')

    async def establish_connection(self, ip, port):
        self.logger.info('Connecting...')
        try:
            self.reader, self.writer = await asyncio.open_connection(ip, port)
            self.logger.info('Connected')
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

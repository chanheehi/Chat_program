from twisted.internet import protocol, reactor
import names

from Management_data import Log, Login
server_start_time_log = Log('./Log/Server_start_time/start')  # 서버 시작 시간 로그
server_shutdown_time_log = Log('./Log/Server_shutdown_time/shutdown')    # 서버 종료 시간 로그
server_start_time_log.debug("==========Server start==========")

transports = set()
users = set()


class Chat(protocol.Protocol):
    def connectionMade(self):
        name = names.get_first_name()
        users.add(name)
        transports.add(self.transport)

        self.transport.write(name.encode())

    def dataReceived(self, data):
        for t in transports:
            if self.transport is not t:
                t.write(data)

class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

print('Server started!')
reactor.listenTCP(8000, ChatFactory())
reactor.run()

server_shutdown_time_log.debug("==========Server shutdown==========")
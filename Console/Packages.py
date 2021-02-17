class NetworkDiscoverFlag(object):
    ConsoleFlag = 1
    ClientFlag = 2


class ClassBroadcastFlag(object):
    PublicMessage = 1
    PrivateMessage = 2
    StartScreenBroadcast = 3
    StopScreenBroadcast = 4
    ConsoleQuit = 5


class PrivateMessageFlag(object):
    ClientLogin = 1
    ClientLogout = 2
    ClientMessage = 3
    ClientScreen = 4
    ClientFile = 5

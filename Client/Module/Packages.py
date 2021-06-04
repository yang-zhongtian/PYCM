class NetworkDiscoverFlag(object):
    ConsoleFlag = 1
    ClientFlag = 2


class ClassBroadcastFlag(object):
    PublicMessage = 1
    PrivateMessage = 2
    StartScreenBroadcast = 3
    StopScreenBroadcast = 4
    ConsoleQuit = 5
    PrivateCommand = 6
    PublicCommand = 7


class PrivateMessageFlag(object):
    ClientLogin = 1
    ClientLogout = 2
    ClientMessage = 3
    ClientScreen = 4
    ClientFile = 5
    ClientNotify = 6
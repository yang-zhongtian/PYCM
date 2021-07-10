class NetworkDiscoverFlag(object):
    ConsoleFlag = 1
    ClientFlag = 2


class ClassBroadcastFlag(object):
    Message = 1
    StartScreenBroadcast = 2
    StopScreenBroadcast = 3
    ConsoleQuit = 4
    Command = 5
    RemoteSpyStart = 6


class PrivateMessageFlag(object):
    ClientLogin = 1
    ClientLogout = 2
    ClientMessage = 3
    ClientScreen = 4
    ClientFile = 5
    ClientNotify = 6


class RemoteSpyFlag(object):
    PackInfo = 1
    RemoteSpyStop = 2

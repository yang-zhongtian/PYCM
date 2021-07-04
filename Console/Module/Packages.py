class NetworkDiscoverFlag(object):
    ConsoleFlag = 1
    ClientFlag = 2


class ClassBroadcastFlag(object):
    Message = 1
    StartScreenBroadcast = 2
    StopScreenBroadcast = 3
    ConsoleQuit = 4
    Command = 5
    RemoteControlStart = 6


class PrivateMessageFlag(object):
    ClientLogin = 1
    ClientLogout = 2
    ClientMessage = 3
    ClientScreen = 4
    ClientFile = 5
    ClientNotify = 6


class RemoteControlFlag(object):
    PackInfo = 1
    ControlCommmand = 2
    RemoteControlStop = 3

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
    RemoteQuit = 7
    ClientFileRecieved = 8


class PrivateMessageFlag(object):
    ClientLogin = 1
    ClientLogout = 2
    ClientMessage = 3
    ClientScreen = 4
    ClientFileInfo = 5
    ClientFileData = 6
    ClientNotify = 7


class RemoteSpyFlag(object):
    PackInfo = 1
    RemoteSpyStop = 2


class ScreenBroadcastFlag(object):
    PackInfo = 1
    PackData = 2


class FileServerFlag(object):
    ListDir = 1
    DownloadFile = 2


class FileClientFlag(object):
    ListDir = 1
    DownloadFile = 2

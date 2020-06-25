from .nc import NC, NCParameter, ExperienceParameter


class NCPVParameter(NCParameter):
    RATE_LIMIT= "pvRateLimit"
    G        = "pvG" #patched version of pv
    Z        = "pvZ"
    CHANGE_PV   = "changePv"
    CHANGE_PV_AT = "changePvAt"

    def __init__(self, experience_parameter_filename):
        super(NCPVParameter, self).__init__(experience_parameter_filename)
        self.default_parameters.update({
            NCPVParameter.RATE_LIMIT: "400k",
            NCPVParameter.G: "10000",
            NCPVParameter.Z: "10000",
            NCPVParameter.CHANGE_PV: "no",
        })


class MpPvAt(object):
    def __init__(self, at, cmd):
        self.at = at
        self.cmd = cmd
        self.delta = 0

    def __str__(self):
        return "Pv... at " + str(self.at) + "(" + str(self.delta) + \
                ") will be " + self.cmd


class NCPV(NC):
    """
    NC PV : NetCat and Pipe Viewer
    """
    NAME = "ncpv"
    PARAMETER_CLASS = NCPVParameter

    SERVER_NC_LOG = "netcat_server"
    CLIENT_NC_LOG = "netcat_client"
    NC_BIN = "/usr/local/bin/nc"
    PV_BIN = "/usr/local/bin/pv"
    PING_OUTPUT = "ping.log"

    def __init__(self, experience_parameter_filename, topo, topo_config):
        super(NCPV, self).__init__(experience_parameter_filename, topo, topo_config)
        self.load_parameters()
        self.ping()

    def ping(self):
        self.topo.command_to(self.topo_config.client, "rm " + \
                NCPV.PING_OUTPUT )
        count = self.experience_parameter.get(ExperienceParameter.PINGCOUNT)
        for i in range(0, self.topo_config.getClientInterfaceCount()):
             cmd = self.pingCommand(self.topo_config.getClientIP(i),
                 self.topo_config.getServerIP(), n = count)
             self.topo.command_to(self.topo_config.client, cmd)

    def pingCommand(self, fromIP, toIP, n=5):
        s = "ping -c " + str(n) + " -I " + fromIP + " " + toIP + \
                  " >> " + NCPV.PING_OUTPUT
        print(s)
        return s

    def load_parameters(self):
        super(NCPV, self).load_parameters()
        self.pvg = self.experience_parameter.get(ExperienceParameter.PVG)
        self.pvz = self.experience_parameter.get(ExperienceParameter.PVZ)
        self.pvRateLimit = self.experience_parameter.get(ExperienceParameter.PVRATELIMIT)
        self.loadPvAt()

    def loadPvAt(self):
        self.changePvAt = []
        self.changePv = self.experience_parameter.get(ExperienceParameter.CHANGEPV)
        if self.changePv != "yes":
            print("Don't change pv rate...")
            return
        changePvAt = self.experience_parameter.get(ExperienceParameter.CHANGEPVAT)
        if not isinstance(changePvAt, list):
            changePvAt = [changePvAt]
        for p in changePvAt:
            tab = p.split(",")
            if len(tab)==2:
                o = MpPvAt(float(tab[0]), tab[1])
                self.addPvAt(o)
            else:
                print("pv wrong line : " + p)

    def addPvAt(self, p):
        if len(self.changePvAt) == 0 :
            p.delta = p.at
        else:
            if p.at > self.changePvAt[-1].at:
                p.delta = p.at - self.changePvAt[-1].at
            else:
                print("Do not take into account " + p.__str__() + \
                        "because ooo !")
                return

        self.changePvAt.append(p)

    def getPvChangeCmd(self):
        cmd = ""
        for p in self.changePvAt:
            cmd = cmd + "sleep " + str(p.delta)
            cmd = cmd + " && "
            cmd = cmd + NCPV.PV_BIN + " -R " + self.pvPid
            cmd = cmd + " " + p.cmd + " && "
        cmd = cmd + " true &"
        return cmd

    def prepare(self):
        super(NCPV, self).prepare()

    def getNCServerCmd(self, id):
        s = NC.NC_BIN + " -d  " + \
                " -l " + self.ncServerPort  + \
                " 1>/dev/null 2>" + NC.SERVER_NC_LOG + \
                "_" + str(id) + ".log &"
        print(s)
        return s

    def getNCClientCmd(self, id):
        s = "dd if=/dev/urandom ibs=" + self.ddibs + \
                " obs=" + self.ddobs + \
                " count=" + self.ddcount + \
                " | " + NC.PV_BIN + \
                " -g " + self.pvg + " -z " + self.pvz + \
                " -q --rate-limit " + self.pvRateLimit + \
                " | " + NC.NC_BIN + " " + \
                "  -p " + self.ncClientPort[id] + " " + \
                self.topo_config.getServerIP() + " " + \
                self.ncServerPort + " " + \
                "&>" + NCPV.CLIENT_NC_LOG + \
                "_" + str(id) + ".log"
        print(s)
        return s

    def getPvPidCmd(self):
        s = "pgrep -n pv"
        return s

    def clean(self):
        super(NCPV, self).clean()

    def run(self):
        for i in range(0, len(self.ncClientPort)):
            cmd = self.getNCServerCmd(i)
            self.topo.command_to(self.topo_config.server, cmd)

            cmd = self.getNCClientCmd(i)
            self.topo_config.client.sendCmd(cmd)

            cmd = self.getPvPidCmd()
            self.pvPid = None
            while self.pvPid == None or self.pvPid == "": 
                self.pvPid = self.topo.command_to(self.topo_config.server, cmd)[:-1]
                print("guessing pv pid ... :" + str(self.pvPid))

            cmd = self.getPvChangeCmd()
            print(cmd)
            self.topo.command_to(self.topo_config.server, cmd)


            self.topo_config.client.waitOutput()

            self.topo.command_to(self.topo_config.client, "sleep 1")


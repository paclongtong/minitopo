from core.experiment import ExperimentParameter, RandomFileExperiment, RandomFileParameter
import os

class HTTP(RandomFileExperiment):
    NAME = "http"

    SERVER_LOG = "http_server.log"
    CLIENT_LOG = "http_client.log"
    WGET_BIN = "wget"
    PING_OUTPUT = "ping.log"

    def __init__(self, experiment_parameter_filename, topo, topo_config):
        # Just rely on RandomFileExperiment
        super(HTTP, self).__init__(experiment_parameter_filename, topo, topo_config)

    def ping(self):
        self.topo.command_to(self.topo_config.client, "rm " + \
                HTTP.PING_OUTPUT )
        count = self.experiment_parameter.get(ExperimentParameter.PING_COUNT)
        for i in range(0, self.topo_config.client_interface_count()):
             cmd = self.pingCommand(self.topo_config.getClientIP(i),
                 self.topo_config.getServerIP(), n = count)
             self.topo.command_to(self.topo_config.client, cmd)

    def pingCommand(self, fromIP, toIP, n=5):
        s = "ping -c " + str(n) + " -I " + fromIP + " " + toIP + \
                  " >> " + HTTP.PING_OUTPUT
        print(s)
        return s

    def load_parameters(self):
        # Just rely on RandomFileExperiment
        super(HTTP, self).load_parameters()

    def prepare(self):
        super(HTTP, self).prepare()
        self.topo.command_to(self.topo_config.client, "rm " + \
                HTTP.CLIENT_LOG )
        self.topo.command_to(self.topo_config.server, "rm " + \
                HTTP.SERVER_LOG )

    def getHTTPServerCmd(self):
        s = "/etc/init.d/apache2 restart &> {}&".format(HTTP.SERVER_LOG)
        print(s)
        return s

    def getHTTPClientCmd(self):
        s = "(time {} http://{}/{} --no-check-certificate) &> {}".format(HTTP.WGET_BIN,
            self.topo_config.getServerIP(), self.file, HTTP.CLIENT_LOG)
        print(s)
        return s

    def clean(self):
        super(HTTP, self).clean()

    def run(self):
        cmd = self.getHTTPServerCmd()
        self.topo.command_to(self.topo_config.server, "netstat -sn > netstat_server_before")
        self.topo.command_to(self.topo_config.server, cmd)

        self.topo.command_to(self.topo_config.client, "sleep 2")
        cmd = self.getHTTPClientCmd()
        self.topo.command_to(self.topo_config.client, "netstat -sn > netstat_client_before")
        self.topo.command_to(self.topo_config.client, cmd)
        self.topo.command_to(self.topo_config.server, "netstat -sn > netstat_server_after")
        self.topo.command_to(self.topo_config.client, "netstat -sn > netstat_client_after")
        self.topo.command_to(self.topo_config.client, "sleep 2")

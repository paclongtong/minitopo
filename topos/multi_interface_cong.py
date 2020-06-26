from core.topo import TopoConfig, Topo, TopoParameter


class MultiInterfaceCongTopo(Topo):
    NAME = "MultiIfCong"

    congClientName = "CCli"
    congServerName = "CSer"

    def __init__(self, topoBuilder, parameterFile):
        super(MultiInterfaceCongTopo, self).__init__(topoBuilder, parameterFile)
        print("Hello from topo multi if")
        self.client = self.addHost(Topo.clientName)
        self.server = self.addHost(Topo.serverName)
        self.router = self.addHost(Topo.routerName)
        self.cong_clients = []
        self.cong_servers = []
        self.switch = []
        for l in self.topoParam.linkCharacteristics:
            self.switch.append(self.addOneSwitchPerLink(l))
            self.addLink(self.client,self.switch[-1])
            self.cong_clients.append(self.addHost(MultiInterfaceCongTopo.congClientName + str(len(self.cong_clients))))
            self.addLink(self.cong_clients[-1], self.switch[-1])
            self.addLink(self.switch[-1],self.router, **l.asDict())
        self.addLink(self.router, self.server)
        for i in range(len(self.cong_clients)):
            self.cong_servers.append(self.addHost(MultiInterfaceCongTopo.congServerName + str(len(self.cong_servers))))
            self.addLink(self.router, self.cong_servers[-1])

    def getCongClients(self):
        return self.cong_clients

    def getCongServers(self):
        return self.cong_servers

    def addOneSwitchPerLink(self, link):
        return self.addSwitch(MultiInterfaceCongTopo.switchNamePrefix +
                str(link.id))

    def __str__(self):
        s = "Simple multiple interface topology with congestion \n"
        i = 0
        n = len(self.topoParam.linkCharacteristics)
        for p in self.topoParam.linkCharacteristics:
            if i == n // 2:
                if n % 2 == 0:
                    s = s + "c            r-----s\n"
                    s = s + "|-----sw-----|\n"
                else:
                    s = s + "c-----sw-----r-----s\n"
            else:
                s = s + "|-----sw-----|\n"

            i = i + 1
        return s


class MultiInterfaceCongConfig(TopoConfig):
    NAME = "MultiIfCong"

    def __init__(self, topo, param):
        super(MultiInterfaceCongConfig, self).__init__(topo, param)

    def configureRoute(self):
        i = 0
        for l in self.topo.switch:
            cmd = self.addRouteTableCommand(self.getClientIP(i), i)
            self.topo.command_to(self.client, cmd)

            # Congestion client
            cmd = self.addRouteTableCommand(self.getCongClientIP(i), i)
            self.topo.command_to(self.cong_clients[i], cmd)

            cmd = self.addRouteScopeLinkCommand(
                    self.getClientSubnet(i),
                    self.get_client_interface(i), i)
            self.topo.command_to(self.client, cmd)

            # Congestion client
            cmd = self.addRouteScopeLinkCommand(
                    self.getClientSubnet(i),
                    self.getCongClientInterface(i), i)
            self.topo.command_to(self.cong_clients[i], cmd)

            cmd = self.addRouteDefaultCommand(self.getRouterIPSwitch(i),
                    i)
            self.topo.command_to(self.client, cmd)

            # Congestion client
            # Keep the same command
            self.topo.command_to(self.cong_clients[i], cmd)

            # Congestion client
            cmd = self.addRouteDefaultGlobalCommand(self.getRouterIPSwitch(i),
                    self.getCongClientInterface(i))
            i = i + 1

        cmd = self.addRouteDefaultGlobalCommand(self.getRouterIPSwitch(0),
                self.get_client_interface(0))
        self.topo.command_to(self.client, cmd)

        # Congestion Client
        i = 0
        for c in self.cong_clients:
            cmd = self.addRouteDefaultGlobalCommand(self.getRouterIPSwitch(i),
                self.getCongClientInterface(i))
            self.topo.command_to(c, cmd)
            i = i + 1

        cmd = self.addRouteDefaultSimple(self.getRouterIPServer())
        self.topo.command_to(self.server, cmd)
        # Congestion servers
        i = 0
        for s in self.cong_servers:
            cmd = self.addRouteDefaultSimple(self.getRouterIPCongServer(i))
            self.topo.command_to(s, cmd)
            i += 1


    def configureInterfaces(self):
        print("Configure interfaces for multi inf")
        self.client = self.topo.get_host(Topo.clientName)
        self.server = self.topo.get_host(Topo.serverName)
        self.router = self.topo.get_host(Topo.routerName)
        cong_client_names = self.topo.getCongClients()
        self.cong_clients = []
        for cn in cong_client_names:
            self.cong_clients.append(self.topo.get_host(cn))

        cong_server_names = self.topo.getCongServers()
        self.cong_servers = []
        for sn in cong_server_names:
            self.cong_servers.append(self.topo.get_host(sn))

        i = 0
        netmask = "255.255.255.0"
        links = self.topo.getLinkCharacteristics()
        for l in self.topo.switch:
            cmd = self.interfaceUpCommand(
                    self.get_client_interface(i),
                    self.getClientIP(i), netmask)
            self.topo.command_to(self.client, cmd)
            clientIntfMac = self.client.intf(self.get_client_interface(i)).MAC()
            self.topo.command_to(self.router, "arp -s " + self.getClientIP(i) + " " + clientIntfMac)

            if(links[i].back_up):
                cmd = self.interface_backup_command(
                        self.get_client_interface(i))
                self.topo.command_to(self.client, cmd)

            # Congestion client
            cmd = self.interfaceUpCommand(
                    self.getCongClientInterface(i),
                    self.getCongClientIP(i), netmask)
            self.topo.command_to(self.cong_clients[i], cmd)
            congClientIntfMac = self.cong_clients[i].intf(self.getCongClientInterface(i)).MAC()
            self.topo.command_to(self.router, "arp -s " + self.getCongClientIP(i) + " " + congClientIntfMac)

            cmd = self.interfaceUpCommand(
                    self.get_router_interface_to_switch(i),
                    self.getRouterIPSwitch(i), netmask)
            self.topo.command_to(self.router, cmd)
            routerIntfMac = self.router.intf(self.get_router_interface_to_switch(i)).MAC()
            self.topo.command_to(self.client, "arp -s " + self.getRouterIPSwitch(i) + " " + routerIntfMac)
            # Don't forget the congestion client
            self.topo.command_to(self.cong_clients[i], "arp -s " + self.getRouterIPSwitch(i) + " " + routerIntfMac)
            print(str(links[i]))
            i = i + 1

        cmd = self.interfaceUpCommand(self.getRouterInterfaceServer(),
                self.getRouterIPServer(), netmask)
        self.topo.command_to(self.router, cmd)
        routerIntfMac = self.router.intf(self.getRouterInterfaceServer()).MAC()
        self.topo.command_to(self.server, "arp -s " + self.getRouterIPServer() + " " + routerIntfMac)

        cmd = self.interfaceUpCommand(self.getServerInterface(),
                self.getServerIP(), netmask)
        self.topo.command_to(self.server, cmd)
        serverIntfMac = self.server.intf(self.getServerInterface()).MAC()
        self.topo.command_to(self.router, "arp -s " + self.getServerIP() + " " + serverIntfMac)

        # Congestion servers
        i = 0
        for s in self.cong_servers:
            cmd = self.interfaceUpCommand(self.getRouterInterfaceCongServer(i),
                self.getRouterIPCongServer(i), netmask)
            self.topo.command_to(self.router, cmd)
            routerIntfMac = self.router.intf(self.getRouterInterfaceCongServer(i)).MAC()
            self.topo.command_to(s, "arp -s " + self.getRouterIPCongServer(i) + " " + routerIntfMac)

            cmd = self.interfaceUpCommand(self.getCongServerInterface(i),
                self.getCongServerIP(i), netmask)
            self.topo.command_to(s, cmd)
            congServerIntfMac = s.intf(self.getCongServerInterface(i)).MAC()
            self.topo.command_to(self.router, "arp -s " + self.getCongServerIP(i) + " " + congServerIntfMac)
            i = i + 1

    def getClientIP(self, interfaceID):
        lSubnet = self.param.get(TopoParameter.LSUBNET)
        clientIP = lSubnet + str(interfaceID) + ".1"
        return clientIP

    def getCongClientIP(self, interfaceID):
        lSubnet = self.param.get(TopoParameter.LSUBNET)
        congClientIP = lSubnet + str(interfaceID) + ".127"
        return congClientIP

    def getClientSubnet(self, interfaceID):
        lSubnet = self.param.get(TopoParameter.LSUBNET)
        clientSubnet = lSubnet + str(interfaceID) + ".0/24"
        return clientSubnet

    def getRouterIPSwitch(self, interfaceID):
        lSubnet = self.param.get(TopoParameter.LSUBNET)
        routerIP = lSubnet + str(interfaceID) + ".2"
        return routerIP

    def getRouterIPServer(self):
        rSubnet = self.param.get(TopoParameter.RSUBNET)
        routerIP = rSubnet + "0.2"
        return routerIP

    def getRouterIPCongServer(self, congID):
        rSubnet = self.param.get(TopoParameter.RSUBNET)
        routerIP = rSubnet + str(1 + congID) + ".2"
        return routerIP

    def getServerIP(self):
        rSubnet = self.param.get(TopoParameter.RSUBNET)
        serverIP = rSubnet + "0.1"
        return serverIP

    def getCongServerIP(self, congID):
        rSubnet = self.param.get(TopoParameter.RSUBNET)
        serverIP = rSubnet + str(1 + congID) + ".1"
        return serverIP

    def client_interface_count(self):
        return len(self.topo.switch)

    def getRouterInterfaceServer(self):
        return self.get_router_interface_to_switch(len(self.topo.switch))

    def getRouterInterfaceCongServer(self, congID):
        return self.get_router_interface_to_switch(len(self.topo.switch) + 1 + congID)

    def get_client_interface(self, interfaceID):
        return  Topo.clientName + "-eth" + str(interfaceID)

    def getCongClientInterface(self, interfaceID):
        return MultiInterfaceCongConfig.congClientName + str(interfaceID) + "-eth0"

    def get_router_interface_to_switch(self, interfaceID):
        return  Topo.routerName + "-eth" + str(interfaceID)

    def getServerInterface(self):
        return  Topo.serverName + "-eth0"

    def getCongServerInterface(self, interfaceID):
        return MultiInterfaceCongConfig.congServerName + str(interfaceID) + "-eth0"

    def getMidLeftName(self, id):
        return Topo.switchNamePrefix + str(id)

    def getMidRightName(self, id):
        return Topo.routerName

    def getMidL2RInterface(self, id):
        return self.getMidLeftName(id) + "-eth2"

    def getMidR2LInterface(self, id):
        return self.getMidRightName(id) + "-eth" + str(id)

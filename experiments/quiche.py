import sys
import os
sys.path.append(os.path.abspath("/home/bolong/minitopo"))
from core.experiment import Experiment, ExperimentParameter, RandomFileParameter, RandomFileExperiment
import logging



class QuicheParameter(RandomFileParameter):
    SIZE = "quicheSize"
    CLIENT_FLAGS = "clientFlags"
    SERVER_FLAGS = "serverFlags"
    ENV = "env"

    # Server-specific parameters
    CERT_PATH = "serverCertPath"
    KEY_PATH = "serverKeyPath"
    LISTEN_ADDR = "serverListenAddr"
    ROOT_DIR = "serverRootDir"
    INDEX_FILE = "serverIndexFile"
    NAME = "serverName"
    MAX_DATA = "serverMaxData"
    MAX_WINDOW = "serverMaxWindow"
    MAX_STREAM_DATA = "serverMaxStreamData"
    MAX_STREAM_WINDOW = "serverMaxStreamWindow"
    MAX_STREAMS_BIDI = "serverMaxStreamsBidi"
    MAX_STREAMS_UNI = "serverMaxStreamsUni"
    IDLE_TIMEOUT = "serverIdleTimeout"
    CC_ALGORITHM = "serverCcAlgorithm"
    ENABLE_EARLY_DATA = "serverEnableEarlyData"
    ENABLE_RETRY = "serverEnableRetry"
    DISABLE_GREASE = "serverDisableGrease"
    HTTP_VERSION = "serverHttpVersion"

    # Client-specific parameters
    METHOD = "clientMethod"
    BODY = "clientBody"
    MAX_DATA_CLIENT = "clientMaxData"
    MAX_WINDOW_CLIENT = "clientMaxWindow"
    MAX_STREAM_DATA_CLIENT = "clientMaxStreamData"
    MAX_STREAM_WINDOW_CLIENT = "clientMaxStreamWindow"
    MAX_STREAMS_BIDI_CLIENT = "clientMaxStreamsBidi"
    MAX_STREAMS_UNI_CLIENT = "clientMaxStreamsUni"
    IDLE_TIMEOUT_CLIENT = "clientIdleTimeout"
    WIRE_VERSION = "clientWireVersion"
    DGRAM_PROTO = "clientDgramProto"
    DGRAM_COUNT = "clientDgramCount"
    DGRAM_DATA = "clientDgramData"
    DUMP_PACKETS = "clientDumpPackets"
    DUMP_RESPONSES = "clientDumpResponses"
    DUMP_JSON = "clientDumpJson"
    MAX_JSON_PAYLOAD = "clientMaxJsonPayload"
    CONNECT_TO = "clientConnectTo"
    TRUST_CA = "clientTrustCA"
    CC_ALGORITHM_CLIENT = "clientCcAlgorithm"
    MAX_ACTIVE_CIDS = "clientMaxActiveCIDs"
    PERFORM_MIGRATION = "clientPerformMigration"
    SOURCE_PORT = "clientSourcePort"
    INITIAL_CWND_PACKETS = "clientInitialCwndPackets"
    SESSION_FILE = "clientSessionFile"
    INITIAL_MAX_PATH_ID_SERVER = "initialMaxPathIdServer"
    INITIAL_MAX_PATH_ID_CLIENT = "initialMaxPathIdClient"


    def __init__(self, experiment_parameter_filename):
        super(QuicheParameter, self).__init__(experiment_parameter_filename)


        self.default_parameters.update({
            QuicheParameter.SIZE: 1024,
            QuicheParameter.CLIENT_FLAGS: "",
            QuicheParameter.SERVER_FLAGS: "",
            QuicheParameter.ENV: "",

            # Server-specific
            QuicheParameter.CERT_PATH: "src/bin/cert.crt",
            QuicheParameter.KEY_PATH: "src/bin/cert.key",
            QuicheParameter.LISTEN_ADDR: "10.1.0.1:4433",
            QuicheParameter.ROOT_DIR: "src/bin/root/",
            QuicheParameter.INDEX_FILE: "index.html",
            QuicheParameter.NAME: "quic.tech",
            QuicheParameter.MAX_DATA: "10000000",
            QuicheParameter.MAX_WINDOW: "25165824",
            QuicheParameter.MAX_STREAM_DATA: "1000000",
            QuicheParameter.MAX_STREAM_WINDOW: "16777216",
            QuicheParameter.MAX_STREAMS_BIDI: "50",
            QuicheParameter.MAX_STREAMS_UNI: "50",
            QuicheParameter.IDLE_TIMEOUT: "30000",
            QuicheParameter.CC_ALGORITHM: "cubic",
            QuicheParameter.ENABLE_EARLY_DATA: "false",
            QuicheParameter.ENABLE_RETRY: "false",
            QuicheParameter.DISABLE_GREASE: "false",
            QuicheParameter.HTTP_VERSION: "HTTP/0.9",
            QuicheParameter.INITIAL_MAX_PATH_ID_SERVER:"50",

            # Client-specific
            QuicheParameter.METHOD: "GET",
            QuicheParameter.BODY: "",
            QuicheParameter.MAX_DATA_CLIENT: "10000000",
            QuicheParameter.MAX_WINDOW_CLIENT: "25165824",
            QuicheParameter.MAX_STREAM_DATA_CLIENT: "1000000",
            QuicheParameter.MAX_STREAM_WINDOW_CLIENT: "16777216",
            QuicheParameter.MAX_STREAMS_BIDI_CLIENT: "50",
            QuicheParameter.MAX_STREAMS_UNI_CLIENT: "50",
            QuicheParameter.IDLE_TIMEOUT_CLIENT: "30000",
            QuicheParameter.WIRE_VERSION: "babababa",
            QuicheParameter.DGRAM_PROTO: "none",
            QuicheParameter.DGRAM_COUNT: "0",
            QuicheParameter.DGRAM_DATA: "quack",
            QuicheParameter.DUMP_PACKETS: "",
            QuicheParameter.DUMP_RESPONSES: "",
            QuicheParameter.DUMP_JSON: "false",
            QuicheParameter.MAX_JSON_PAYLOAD: "10000",
            QuicheParameter.CONNECT_TO: "",
            QuicheParameter.TRUST_CA: "",
            QuicheParameter.CC_ALGORITHM_CLIENT:"cubic",
            QuicheParameter.MAX_ACTIVE_CIDS: "2",
            QuicheParameter.PERFORM_MIGRATION: "false",
            QuicheParameter.SOURCE_PORT: "0",
            QuicheParameter.INITIAL_CWND_PACKETS: "10",
            QuicheParameter.SESSION_FILE: "",
        })


class Quiche(RandomFileExperiment):
    NAME = "quiche"
    PARAMETER_CLASS = QuicheParameter

    CLIENT = "/home/bolong/quiche-multipath/quiche/apps/src/bin/send_different/quiche-client"
    SERVER = "/home/bolong/quiche-multipath/quiche/apps/src/bin/send_different/quiche-server"
    SERVER_LOG = "/dev/shm/minitopo_experiences/quiche_server.log"
    CLIENT_LOG = "/dev/shm/minitopo_experiences/quiche_client.log"

    def __init__(self, experiment_parameter_filename, topo, topo_config):
        super(Quiche, self).__init__(experiment_parameter_filename, topo, topo_config)

        # Server parameters
        self.cert_path = self.experiment_parameter.get(QuicheParameter.CERT_PATH)
        self.key_path = self.experiment_parameter.get(QuicheParameter.KEY_PATH)
        self.listen_addr = self.experiment_parameter.get(QuicheParameter.LISTEN_ADDR)
        self.root_dir = self.experiment_parameter.get(QuicheParameter.ROOT_DIR)
        self.index_file = self.experiment_parameter.get(QuicheParameter.INDEX_FILE)
        self.server_name = self.experiment_parameter.get(QuicheParameter.NAME)
        self.max_data = self.experiment_parameter.get(QuicheParameter.MAX_DATA)
        self.max_window = self.experiment_parameter.get(QuicheParameter.MAX_WINDOW)
        self.max_stream_data = self.experiment_parameter.get(QuicheParameter.MAX_STREAM_DATA)
        self.max_stream_window = self.experiment_parameter.get(QuicheParameter.MAX_STREAM_WINDOW)
        self.max_streams_bidi = self.experiment_parameter.get(QuicheParameter.MAX_STREAMS_BIDI)
        self.max_streams_uni = self.experiment_parameter.get(QuicheParameter.MAX_STREAMS_UNI)
        self.idle_timeout = self.experiment_parameter.get(QuicheParameter.IDLE_TIMEOUT)
        self.cc_algorithm = self.experiment_parameter.get(QuicheParameter.CC_ALGORITHM)
        self.enable_early_data = self.experiment_parameter.get(QuicheParameter.ENABLE_EARLY_DATA)
        self.enable_retry = self.experiment_parameter.get(QuicheParameter.ENABLE_RETRY)
        self.disable_grease = self.experiment_parameter.get(QuicheParameter.DISABLE_GREASE)
        self.http_version = self.experiment_parameter.get(QuicheParameter.HTTP_VERSION)

        # Client parameters
        self.method = self.experiment_parameter.get(QuicheParameter.METHOD)
        self.body = self.experiment_parameter.get(QuicheParameter.BODY)
        self.max_data_client = self.experiment_parameter.get(QuicheParameter.MAX_DATA_CLIENT)
        self.max_window_client = self.experiment_parameter.get(QuicheParameter.MAX_WINDOW_CLIENT)
        self.max_stream_data_client = self.experiment_parameter.get(QuicheParameter.MAX_STREAM_DATA_CLIENT)
        self.max_stream_window_client = self.experiment_parameter.get(QuicheParameter.MAX_STREAM_WINDOW_CLIENT)
        self.max_streams_bidi_client = self.experiment_parameter.get(QuicheParameter.MAX_STREAMS_BIDI_CLIENT)
        self.max_streams_uni_client = self.experiment_parameter.get(QuicheParameter.MAX_STREAMS_UNI_CLIENT)
        self.idle_timeout_client = self.experiment_parameter.get(QuicheParameter.IDLE_TIMEOUT_CLIENT)
        self.wire_version = self.experiment_parameter.get(QuicheParameter.WIRE_VERSION)
        self.dgram_proto = self.experiment_parameter.get(QuicheParameter.DGRAM_PROTO)
        self.dgram_count = self.experiment_parameter.get(QuicheParameter.DGRAM_COUNT)
        self.dgram_data = self.experiment_parameter.get(QuicheParameter.DGRAM_DATA)
        self.dump_packets = self.experiment_parameter.get(QuicheParameter.DUMP_PACKETS)
        self.dump_responses = self.experiment_parameter.get(QuicheParameter.DUMP_RESPONSES)
        self.dump_json = self.experiment_parameter.get(QuicheParameter.DUMP_JSON)
        self.max_json_payload = self.experiment_parameter.get(QuicheParameter.MAX_JSON_PAYLOAD)
        self.connect_to = self.experiment_parameter.get(QuicheParameter.CONNECT_TO)
        self.trust_ca = self.experiment_parameter.get(QuicheParameter.TRUST_CA)
        self.cc_algorithm_client = self.experiment_parameter.get(QuicheParameter.CC_ALGORITHM_CLIENT)
        self.max_active_cids = self.experiment_parameter.get(QuicheParameter.MAX_ACTIVE_CIDS)
        self.perform_migration = self.experiment_parameter.get(QuicheParameter.PERFORM_MIGRATION)
        self.source_port = self.experiment_parameter.get(QuicheParameter.SOURCE_PORT)
        self.initial_cwnd_packets = self.experiment_parameter.get(QuicheParameter.INITIAL_CWND_PACKETS)
        self.session_file = self.experiment_parameter.get(QuicheParameter.SESSION_FILE)
        # logging.debug(f"self.size before assigning a value: {self.size}")
        self.size = self.experiment_parameter.get(QuicheParameter.SIZE)
        self.initial_max_path_id_server = self.experiment_parameter.get(QuicheParameter.INITIAL_MAX_PATH_ID_SERVER)
        self.initial_max_path_id_client = self.experiment_parameter.get(QuicheParameter.INITIAL_MAX_PATH_ID_CLIENT)
        # self.addr_client = self.experiment_parameter.get(QuicheParameter.A)
        #
        if isinstance(self.size, list):
            logging.warning("Multiple size values found.")
            logging.info(f"The length of the self.size list = {len(self.size)}")
            for index, each_size in enumerate(self.size):
                print(f"size[{index}] = {each_size}")
            self.size = int(self.size[1])
            logging.info("The value of SIZE is {}".format(self.size))
        self.load_parameters()
        self.ping()

    def load_parameters(self):
        super(Quiche, self).load_parameters()

        self.client_flags = self.experiment_parameter.get(QuicheParameter.CLIENT_FLAGS)
        self.server_flags = self.experiment_parameter.get(QuicheParameter.SERVER_FLAGS)
        self.env = self.experiment_parameter.get(QuicheParameter.ENV)

    def prepare(self):
        super(Quiche, self).prepare()
        self.topo.command_to(self.topo_config.client, "rm {}".format(Quiche.CLIENT_LOG))
        self.topo.command_to(self.topo_config.server, "rm {}".format(Quiche.SERVER_LOG))
        self.topo.command_to(self.topo_config.server, "dd if=/dev/random of={}/{} bs=1024 count={}".format(self.root_dir, self.size, int(self.size) // 1024))

    def get_quiche_server_cmd(self):
        """
         Constructs the command for starting the Quiche server using the loaded parameters.
         """

        '''
        certs = "--cert /home/bolong/quiche-multipath/quiche/apps/src/bin/cert.crt --key /home//bolong/quiche-multipath/quiche/apps/src/bin/cert.key --listen 0.0.0.0:4433 --root ."
        s = "{} {} {} {} &> {} &".format(self.env, Quiche.SERVER, certs, self.server_flags,
            Quiche.SERVER_LOG)
        logging.info(s)
        '''

        # Server-specific command options
        certs = f"--cert {self.cert_path} --key {self.key_path}"
        listen = f"--listen {self.listen_addr}"
        root = f"--root {self.root_dir}"
        index = f"--index {self.index_file}"
        server_name = f"--name {self.server_name}"
        max_data = f"--max-data {self.max_data}"
        max_window = f"--max-window {self.max_window}"
        max_stream_data = f"--max-stream-data {self.max_stream_data}"
        max_stream_window = f"--max-stream-window {self.max_stream_window}"
        max_streams_bidi = f"--max-streams-bidi {self.max_streams_bidi}"
        max_streams_uni = f"--max-streams-uni {self.max_streams_uni}"
        idle_timeout = f"--idle-timeout {self.idle_timeout}"
        cc_algorithm = f"--cc-algorithm {self.cc_algorithm}"
        early_data = "--early-data" if self.enable_early_data == "true" else ""
        retry = "" if self.enable_retry == "false" else "--no-retry"
        grease = "--no-grease" if self.disable_grease == "true" else ""
        http_version = f"--http-version {self.http_version}"
        initial_max_path_id_server = f"--initial-max-path-id {self.initial_max_path_id_server}" if self.initial_max_path_id_server else "30"

        # Construct the full command for starting the server
        cmd = f"{self.env} {Quiche.SERVER} {certs} {listen} {root} {index} {server_name} " \
              f"{max_data} {max_window} {max_stream_data} {max_stream_window} " \
              f"{max_streams_bidi} {max_streams_uni} {idle_timeout} {cc_algorithm} {initial_max_path_id_server} " \
              f"{early_data} {retry} {grease} {http_version} {self.server_flags} " \
              f"&> {Quiche.SERVER_LOG} &"

        logging.info(f"Server command: {cmd}")
        return cmd

    def get_quiche_client_cmd(self):
        """
        Constructs the command for starting the Quiche client using the loaded parameters.
        """

        '''
        s = "{} {} {} {} https://{}:4433/{} &> {} > /dev/null".format(self.env, Quiche.CLIENT, no_verify, self.client_flags,
            self.topo_config.get_server_ip(), self.size, Quiche.CLIENT_LOG)
        logging.info(s)
        '''

        # Client-specific command options
        method_flag = f"--method {self.method}"
        body_flag = f"--body {self.body}" if self.body else ""
        max_data = f"--max-data {self.max_data}"
        max_window = f"--max-window {self.max_window}"
        max_stream_data = f"--max-stream-data {self.max_stream_data}"
        max_stream_window = f"--max-stream-window {self.max_stream_window}"
        max_streams_bidi = f"--max-streams-bidi {self.max_streams_bidi}"
        max_streams_uni = f"--max-streams-uni {self.max_streams_uni}"
        idle_timeout = f"--idle-timeout {self.idle_timeout}"
        wire_version = f"--wire-version {self.wire_version}"
        http_version = f"--http-version {self.http_version}"
        dgram_proto = f"--dgram-proto {self.dgram_proto}" if self.dgram_proto != "none" else ""
        dgram_count = f"--dgram-count {self.dgram_count}" if int(self.dgram_count) > 0 else ""
        dgram_data = f"--dgram-data {self.dgram_data}" if self.dgram_data else ""
        dump_packets = f"--dump-packets {self.dump_packets}" if self.dump_packets else ""
        dump_responses = f"--dump-responses {self.dump_responses}" if self.dump_responses else ""
        dump_json = "--dump-json" if self.dump_json == "true" else ""
        max_json_payload = f"--max-json-payload {self.max_json_payload}"
        connect_to = f"--connect-to {self.connect_to}" if self.connect_to else ""
        trust_ca = f"--trust-origin-ca-pem {self.trust_ca}" if self.trust_ca else ""
        cc_algorithm = f"--cc-algorithm {self.cc_algorithm_client}"
        max_active_cids = f"--max-active-cids {self.max_active_cids}"
        perform_migration = "--perform-migration" if self.perform_migration == "true" else ""
        source_port = f"--source-port {self.source_port}" if self.source_port != "0" else ""
        session_file = f"--session-file {self.session_file}" if self.session_file else ""
        initial_max_path_id_client = f"--initial-max-path-id {self.initial_max_path_id_client}" if self.initial_max_path_id_client else "30"
        addr_client = f"-A 10.0.0.1:4433 -A 10.0.0.1:14434"  # Hardcoded 2-path

        # Construct the full command for starting the client
        cmd = f"{self.env} {Quiche.CLIENT} {method_flag} {body_flag} {max_data} {max_window} " \
              f"{max_stream_data} {max_stream_window} {max_streams_bidi} {max_streams_uni} " \
              f"{idle_timeout} {wire_version} {http_version} {dgram_proto} {dgram_count} {dgram_data} " \
              f"{dump_packets} {dump_responses} {dump_json} {max_json_payload} {connect_to} {trust_ca} {cc_algorithm} " \
              f"{max_active_cids} {perform_migration} {source_port} {session_file} {initial_max_path_id_client} {addr_client} {self.client_flags} "\
              f"https://{self.topo_config.get_server_ip()}:4433/{self.size} &> {Quiche.CLIENT_LOG} > /dev/null"

        logging.info(f"Client command: {cmd}")
        return cmd

    def clean(self):
        # super(Quiche, self).clean()
        self.topo.command_to(self.topo_config.server, "rm {}/{}".format(self.root_dir, self.size))
        logging.info("Cleaning up experiment. Skipping sysctl restoration.")

    def run(self):
        cmd = self.get_quiche_server_cmd()
        self.topo.command_to(self.topo_config.server, cmd)

        self.topo.command_to(self.topo_config.client, "sleep 2")

        cmd = self.get_quiche_client_cmd()
        self.topo.command_to(self.topo_config.client, cmd)

        self.topo.command_to(self.topo_config.client, "sleep 2")

        # self.topo.get_cli()


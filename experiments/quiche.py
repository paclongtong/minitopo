import sys
import os
sys.path.append(os.path.abspath("/home/paul/minitopo"))
from core.experiment import Experiment, ExperimentParameter, RandomFileParameter, RandomFileExperiment
import logging
import time
import subprocess

IPERF_LOG = "/tmp/minitopo_experiences/iperf_client.log"
IPERF_SERVER_LOG = "/tmp/minitopo_experiences/iperf_server.log"
IPERF_BIN = "iperf3"

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

    HTTP_VERSION = "httpVersion"

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
    PUT = "put"


    def __init__(self, experiment_parameter_filename):
        super(QuicheParameter, self).__init__(experiment_parameter_filename)


        self.default_parameters.update({
            QuicheParameter.SIZE: 102400000,
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
            QuicheParameter.CC_ALGORITHM_CLIENT:"bbr",
            QuicheParameter.MAX_ACTIVE_CIDS: "2",
            QuicheParameter.PERFORM_MIGRATION: "false",
            QuicheParameter.SOURCE_PORT: "0",
            QuicheParameter.INITIAL_CWND_PACKETS: "10",
            QuicheParameter.SESSION_FILE: "",
        })

# sudo /usr/bin/python /home/paul/minitopo/runner.py -x config/xp/quiche -t config/topo/topo_8
class Quiche(RandomFileExperiment):
    NAME = "quiche"
    PARAMETER_CLASS = QuicheParameter

    # CLIENT = "/home/paul/multipath-quiche/target/release/separate_stream_ack/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/release/separate_stream_ack/quiche-server"

    # CLIENT = "/home/paul/multipath-quiche/target/debug/separate-cca-logging/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/debug/separate-cca-logging/quiche-server"
    # CLIENT = "/home/paul/multipath-quiche/target/release/separate-two-streams/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/release/separate-two-streams/quiche-server"

    # CLIENT = "/home/paul/multipath-quiche/target/release/original-two-streams/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/release/original-two-streams/quiche-server"

    # CLIENT = "/home/paul/multipath-quiche/target/debug/original_log_server_path/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/debug/original_log_server_path/quiche-server"

    # CLIENT = "/home/paul/multipath-quiche/target/debug/server_path_scheduling/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/debug/server_path_scheduling/quiche-server"

    # CLIENT = "/home/paul/multipath-quiche/target/debug/test_server/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/debug/test_server/quiche-server"

    CLIENT = "/home/paul/multipath-quiche/target/release/separate-cca-logging/quiche-client"
    SERVER = "/home/paul/multipath-quiche/target/release/separate-cca-logging/quiche-server"

    # CLIENT = "/home/paul/multipath-quiche/target/debug/simplified_server/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/debug/simplified_server/quiche-server"

    # CLIENT = "/home/paul/multipath-quiche/target/debug/separate-untouched_server/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/debug/separate-untouched_server/quiche-server"
    # 
    # CLIENT = "/home/paul/multipath-quiche/target/debug/original_two_method/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/debug/original_two_method/quiche-server"

    # CLIENT = "/home/paul/multipath-quiche/target/debug/server_fixed/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/debug/server_fixed/quiche-server"
    # CLIENT = "quiche-client"

    # CLIENT = "/home/paul/multipath-quiche/target/debug/server_stack_test/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/debug/server_stack_test/quiche-server"

    # CLIENT = "/home/paul/multipath-quiche/target/release/original-two-streams/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/release/original-two-streams/quiche-server"

    # CLIENT = "/home/paul/multipath-quiche/target/release/original/quiche-client"
    # SERVER = "/home/paul/multipath-quiche/target/release/original/quiche-server"
    SERVER_LOG = "/tmp/minitopo_experiences/quiche_server.log"
    CLIENT_LOG = "/tmp/minitopo_experiences/quiche_client.log"
    
    PING_OUTPUT = "/tmp/minitopo_experiences/ping.log"

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
        self.put = self.experiment_parameter.get(QuicheParameter.PUT)
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
        self.topo.command_to(self.topo_config.client, "dd if=/dev/random of={}/{} bs=1024 count={}".format(self.body, self.size+"_put", int(self.size) // 1024))

    def get_iperf_server_cmd(self):
        cmd = f"iperf3 -s -p 5201 &> {IPERF_SERVER_LOG} &"
        self.topo.command_to(self.topo_config.server, cmd)
    
    def get_iperf_client_cmd(self):
        """
        Generate the iperf client command with variable log file, server IP, test duration, and parallel streams.
        """
        cmd = f"iperf3 -c 10.1.0.1 -p 5201 -u " \
              f"-t 30 -P 1 -b 100M -B 10.0.1.1 -i 1 &> {IPERF_LOG}"
        logging.info(f"Client Command: {cmd}")
        return cmd

    def get_quiche_server_cmd(self):
        """
         Constructs the command for starting the Quiche server using the loaded parameters.
         """

        '''
        certs = "--cert /home/paul/quiche-multipath/quiche/apps/src/bin/cert.crt --key /home//paul/quiche-multipath/quiche/apps/src/bin/cert.key --listen 0.0.0.0:4433 --root ."
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
        # QLOGDIR=/tmp/minitopo_experiences/ 
        cmd = f"QLOGDIR=/tmp/minitopo_experiences/ {self.env} {Quiche.SERVER} {certs} {listen} {root} {index} {server_name} " \
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
        body_flag = f"--body {self.body}/{self.size}_put" if self.put == 'true' else ""
        max_data = f"--max-data {self.max_data}"
        max_window = f"--max-window {self.max_window_client}"
        max_stream_data = f"--max-stream-data {self.max_stream_data_client}"
        max_stream_window = f"--max-stream-window {self.max_stream_window_client}"
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
        addr_client = f"-A 10.0.0.1:4433 -A 10.0.1.1:14434"  # Hardcoded 2-path
        put = f"PUT:https://{self.topo_config.get_server_ip()}:4433/{self.size}_put" if self.put == 'true' else ''
        # Construct the full command for starting the client 
        # QLOGDIR=/tmp/minitopo_experiences/ 
        cmd = f"QLOGDIR=/tmp/minitopo_experiences/ {self.env} {Quiche.CLIENT} {method_flag} {body_flag} {max_data} {max_window} " \
              f"{max_stream_data} {max_stream_window} {max_streams_bidi} {max_streams_uni} " \
              f"{idle_timeout} {wire_version} {http_version} {dgram_proto} {dgram_count} {dgram_data} " \
              f"{dump_packets} {dump_responses} {dump_json} {max_json_payload} {connect_to} {trust_ca} {cc_algorithm} " \
              f"{max_active_cids} {perform_migration} {source_port} {session_file} {initial_max_path_id_client} {addr_client} {self.client_flags} "\
              f"GET:https://{self.topo_config.get_server_ip()}:4433/{self.size} {put} &> {Quiche.CLIENT_LOG} > /dev/null "
                # "PUT:https://{self.topo_config.get_server_ip()}:4433/{self.size}"\.
                # " &> {Quiche.CLIENT_LOG} > /dev/null "
            #   f"--method GET https://{self.topo_config.get_server_ip()}:4433/{self.size}"

        logging.info(f"Client command: {cmd}")
        return cmd

    def run_post_experiment_analysis(self):
        """
        Enhanced automated post-experiment analysis with transfer time extraction,
        metadata collection, and detailed file output
        """
        import datetime
        import re
        
        logging.info("Starting enhanced post-experiment analysis...")
        
        # Extract implementation name from SERVER path
        implementation_raw = None
        if hasattr(self, 'SERVER') and self.SERVER:
            # Extract from path like "/home/paul/multipath-quiche/target/release/separate-cca-logging/quiche-server"
            import os
            server_path = self.SERVER
            path_parts = server_path.split('/')
            # Find the part that comes before 'quiche-server'
            for i, part in enumerate(path_parts):
                if part == 'quiche-server' and i > 0:
                    implementation_raw = path_parts[i-1]
                    break
        
        # Apply implementation name conversions
        implementation_mapping = {
            'separate-cca-logging': 'separate_rigid',
            'original-two-streams': 'original'
        }
        
        implementation = implementation_mapping.get(implementation_raw, implementation_raw) if implementation_raw else 'unknown'
        
        logging.info(f"Detected implementation: {implementation_raw} -> {implementation}")
        print(f"Using implementation: {implementation}")
        
        # Generate timestamp and transfer type for filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        transfer_type = "bidi" if self.put == 'true' else "uni"
        
        # We'll set the final results_filename after creating the directory
        temp_results_filename = f"/tmp/minitopo_experiences/{timestamp}-{transfer_type}-{implementation}.txt"
        
        # Determine expected response count based on PUT parameter
        expected_responses = "2/2" if self.put == 'true' else "1/1"
        
        # Check for expected responses in client log and extract transfer time
        grep_cmd = f"grep '{expected_responses}' {Quiche.CLIENT_LOG}"
        logging.info(f"Checking for {expected_responses} responses in client log...")
        response_check = self.topo.command_to(self.topo_config.client, grep_cmd)
        
        transfer_time = None
        if response_check:
            logging.info(f"Found expected {expected_responses} responses")
            print(f"\n{expected_responses} responses received successfully")
            
            # Extract transfer time from the response line
            # Looking for pattern like "in 12.889255462s"
            time_match = re.search(r'in\s+([\d.]+)s', response_check)
            if time_match:
                transfer_time = time_match.group(1)
                print(f"Transfer time: {transfer_time}s")
                logging.info(f"Extracted transfer time: {transfer_time}s")
        else:
            logging.warning(f"Expected {expected_responses} responses not found in client log")
            print(f"\nWarning: {expected_responses} responses not found")
        
        # Find qlog files
        logging.info("Finding qlog files...")
        server_qlog_cmd = "ls -lth /tmp/minitopo_experiences/ | grep server- | head -n 1 | awk '{print $9}'"
        client_qlog_cmd = "ls -lth /tmp/minitopo_experiences/ | grep client- | head -n 1 | awk '{print $9}'"
        
        server_qlog = self.topo.command_to(self.topo_config.client, server_qlog_cmd).strip()
        client_qlog = self.topo.command_to(self.topo_config.client, client_qlog_cmd).strip()
        
        # Get experiment metadata
        server_cmd = self.get_quiche_server_cmd()
        client_cmd = self.get_quiche_client_cmd()
        
        # Read topology file content
        topo_content = ""
        try:
            # Extract topology filename from topo_parameter if available
            # if hasattr(self.topo, 'topo_parameter') and hasattr(self.topo.topo_parameter, 'parameter_filename'):
            #     topo_file_path = self.topo.topo_parameter.parameter_filename
            #     # Read file directly from host filesystem
            #     with open(topo_file_path, 'r') as f:
            #         topo_content = f.read()
            topo_content = self.topo.topo_parameter.format_parameters()
        except Exception as e:
            logging.warning(f"Could not read topology file: {e}")
            topo_content = "Topology content could not be retrieved"
        
        # Prepare results data
        results_data = []
        results_data.append("=" * 80)
        results_data.append(f"QUICHE EXPERIMENT RESULTS - {timestamp}")
        results_data.append(f"Transfer Type: {transfer_type.upper()}")
        results_data.append(f"Implementation: {implementation}")
        results_data.append("=" * 80)
        results_data.append("")
        
        # Transfer summary
        results_data.append("TRANSFER SUMMARY:")
        results_data.append(f"Expected responses: {expected_responses}")
        if transfer_time:
            results_data.append(f"Transfer time: {transfer_time}s")
        else:
            results_data.append("Transfer time: Not available")
        results_data.append("")
        
        # Response check details
        results_data.append("RESPONSE CHECK:")
        if response_check:
            results_data.append(response_check.strip())
        else:
            results_data.append("No matching responses found")
        results_data.append("")
        
        # Qlog files
        results_data.append("QLOG FILES:")
        results_data.append(f"Server qlog: {server_qlog if server_qlog else 'Not found'}")
        results_data.append(f"Client qlog: {client_qlog if client_qlog else 'Not found'}")
        results_data.append("")
        
        if transfer_time:
            logging.info(f"Found server qlog: {server_qlog}")
            logging.info(f"Found client qlog: {client_qlog}")
            
            # Extract loss statistics
            logging.info("Extracting loss statistics...")
            server_loss_cmd = f"grep 'lost=' {Quiche.SERVER_LOG} | tail -n 1"
            client_loss_cmd = f"grep 'lost=' {Quiche.CLIENT_LOG} | tail -n 1"
            
            server_loss = self.topo.command_to(self.topo_config.server, server_loss_cmd)
            client_loss = self.topo.command_to(self.topo_config.client, client_loss_cmd)
            
            # Add loss statistics to results
            results_data.append("TRANSFER END STATISTICS:")
            if server_loss:
                results_data.append(f"Server: {server_loss.strip()}")
                print(f"\nServer loss stats: {server_loss.strip()}")
            if client_loss:
                results_data.append(f"Client: {client_loss.strip()}")
                print(f"Client loss stats: {client_loss.strip()}")
            results_data.append("")
            
            # Create results directory
            results_dir_name = f"{timestamp}-{transfer_type}-{implementation}"
            results_dir_path = f"/home/paul/data_quiche/qlog/{results_dir_name}"
            
            # Create the directory in normal terminal environment
            import subprocess
            import os
            os.makedirs(results_dir_path, exist_ok=True)
            logging.info(f"Created results directory: {results_dir_path}")
            
            # Run qlog comparison script with implementation name and output to results directory
            qlog_script_path = "/home/paul/data_quiche/logging-script/qlog_compare_pathwise.py"
            server_qlog_full = f"/tmp/minitopo_experiences/{server_qlog}"
            client_qlog_full = f"/tmp/minitopo_experiences/{client_qlog}"
            
            # Construct qlog command to run in normal terminal (not Mininet namespace)
            # Try to find a Python interpreter that has pandas
            import subprocess
            python_candidates = ["python3", "python", "/usr/bin/python3", "/usr/bin/python"]
            working_python = None
            
            for py_cmd in python_candidates:
                try:
                    result = subprocess.run([py_cmd, "-c", "import pandas"], capture_output=True, timeout=10)
                    if result.returncode == 0:
                        working_python = py_cmd
                        logging.info(f"Found working Python with pandas: {py_cmd}")
                        break
                except:
                    continue
            
            if not working_python:
                working_python = "python3"  # fallback
                logging.warning("Could not find Python with pandas, using python3 as fallback")
            
            qlog_cmd_args = [
                working_python, qlog_script_path,
                "--qlogs", f"{server_qlog_full},server-{implementation}",
                f"{client_qlog_full},client-{implementation}",
                "--paths", "0", "1",
                "--output-suffix",f"{transfer_time}_{implementation}"
            ]
            
            logging.info(f"Running qlog comparison in normal terminal: {' '.join(qlog_cmd_args)}")
            print(f"\nRunning qlog comparison script in {results_dir_path}...")
            
            # Execute the qlog comparison script in normal terminal environment
            import subprocess
            try:
                qlog_process = subprocess.run(
                    qlog_cmd_args,
                    cwd=results_dir_path,  # Change working directory to results_dir_path
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                if qlog_process.returncode == 0:
                    qlog_result = qlog_process.stdout
                    if qlog_process.stderr:
                        qlog_result += f"\nSTDERR:\n{qlog_process.stderr}"
                else:
                    qlog_result = f"Script failed with return code {qlog_process.returncode}\nSTDOUT:\n{qlog_process.stdout}\nSTDERR:\n{qlog_process.stderr}"
                    
            except subprocess.TimeoutExpired:
                qlog_result = "Qlog comparison script timed out after 5 minutes"
                logging.error("Qlog comparison script timed out")
            except Exception as e:
                qlog_result = f"Error running qlog comparison script: {str(e)}"
                logging.error(f"Error running qlog comparison script: {e}")
            if qlog_result:
                results_data.append("QLOG COMPARISON OUTPUT:")
                results_data.append(qlog_result.strip())
                print(f"Qlog comparison output:\n{qlog_result}")
            else:
                results_data.append("QLOG COMPARISON: Failed or no output")
                logging.warning("Qlog comparison script produced no output or failed")
                print("Warning: Qlog comparison script execution failed or produced no output")
                
        else:
            results_data.append("TRANSFER END STATISTICS: Could not retrieve (qlog files not found)")
            results_data.append("QLOG COMPARISON: Skipped (qlog files not found)")
            logging.error("Could not find qlog files")
            print("\nError: Could not find qlog files for analysis")
            
            # Create results directory even if qlog files not found
            results_dir_name = f"{timestamp}-{transfer_type}-{implementation}"
            results_dir_path = f"/home/paul/data_quiche/qlog/{results_dir_name}"
            import os
            os.makedirs(results_dir_path, exist_ok=True)
            logging.info(f"Created results directory: {results_dir_path}")
        
        results_data.append("")
        results_data.append("=" * 80)
        results_data.append("EXPERIMENT METADATA")
        results_data.append("=" * 80)
        results_data.append("")
        
        # Add experiment metadata
        results_data.append("SERVER COMMAND:")
        results_data.append(server_cmd)
        results_data.append("")
        
        results_data.append("CLIENT COMMAND:")
        results_data.append(client_cmd)
        results_data.append("")
        
        results_data.append("TOPOLOGY CONFIGURATION:")
        results_data.append(topo_content.strip() if topo_content else "Not available")
        results_data.append("")
        
        results_data.append("EXPERIMENT PARAMETERS:")
        results_data.append(f"Implementation: {implementation} (raw: {implementation_raw})")
        results_data.append(f"File size: {self.size}")
        results_data.append(f"PUT enabled: {self.put}")
        results_data.append(f"Server CC algorithm: {self.cc_algorithm}")
        results_data.append(f"Client CC algorithm: {self.cc_algorithm_client}")
        results_data.append(f"Client flags: {self.client_flags}")
        results_data.append(f"Server flags: {self.server_flags}")
        results_data.append("")
        
        # Determine final file paths - always use the organized directory structure
        results_dir_name = f"{timestamp}-{transfer_type}-{implementation}"
        results_dir_path = f"/home/paul/data_quiche/qlog/{results_dir_name}"
        final_results_filename = f"{results_dir_path}/{timestamp}-{transfer_type}-{implementation}.txt"
        
        # Write results to file in the organized directory using normal Python file operations
        results_content = "\n".join(results_data)
        
        try:
            with open(final_results_filename, 'w') as f:
                f.write(results_content)
            logging.info(f"Successfully wrote results to {final_results_filename}")
        except Exception as e:
            logging.error(f"Failed to write results file: {e}")
            print(f"Error writing results file: {e}")
        
        # Also create a copy in the original location for backwards compatibility
        try:
            import shutil
            shutil.copy2(final_results_filename, temp_results_filename)
            logging.info(f"Created backup copy at {temp_results_filename}")
        except Exception as e:
            logging.warning(f"Failed to create backup copy: {e}")
        
        # Change ownership from root to paul for direct user access
        try:
            import subprocess
            chown_cmd = ["chown", "-R", "paul:paul", results_dir_path]
            subprocess.run(chown_cmd, check=True)
            logging.info(f"Changed ownership of {results_dir_path} to paul:paul")
            
            # Also change ownership of the backup file
            if os.path.exists(temp_results_filename):
                chown_backup_cmd = ["chown", "paul:paul", temp_results_filename]
                subprocess.run(chown_backup_cmd, check=True)
                logging.info(f"Changed ownership of {temp_results_filename} to paul:paul")
                
        except subprocess.CalledProcessError as e:
            logging.warning(f"Failed to change ownership: {e}")
            print(f"Warning: Could not change file ownership to paul:paul")
        except Exception as e:
            logging.warning(f"Error changing ownership: {e}")

        print(f"\nDetailed results saved to: {final_results_filename}")
        print(f"Results directory: {results_dir_path}")
        print(f"Files ownership changed to paul:paul for direct access")
        logging.info(f"Results saved to: {final_results_filename}")
        logging.info(f"Results directory created: {results_dir_path}")
        logging.info("Enhanced post-experiment analysis completed")

    def clean(self):
        # super(Quiche, self).clean()
        self.topo.command_to(self.topo_config.server, "rm {}/{}".format(self.root_dir, self.size))
        self.topo.command_to(self.topo_config.client, "rm {}/{}".format(self.body, self.size+'_put'))
        logging.info("Cleaning up experiment. Skipping sysctl restoration.")

    def run(self):
        # cmd = self.get_iperf_server_cmd()      # start iperf server
        # self.topo.command_to(self.topo_config.server, cmd)

        # cmd = self.get_iperf_client_cmd()       # start iperf client 
        # self.topo.command_to(self.topo_config.client, cmd)

        # self.topo.command_to(self.topo_config.client, "sleep 30")
        # self.topo.command_to(self.topo_config.server, "pkill iperf")
        # self.topo.get_cli()
        # time.sleep(12000)``
        # server = 'Server_0'
        # client = 'Client_0'

        '''
        # Interfaces for path0 and path1
        iface0 = 'Client_0-eth0'
        iface1 = 'Client_0-eth1'
        pcap_dir = '/tmp/minitopo_experiences'
        # PCAP files
        pcap0 = '/tmp/minitopo_experiences/quic-path0.pcap'
        pcap1 = '/tmp/minitopo_experiences/quic-path1.pcap'

        # Clean up any existing files
        self.topo.command_to(self.topo_config.client, f'rm -f {pcap0} {pcap1}')
        self.topo.command_to(self.topo_config.client, 'rm -f /tmp/tshark*.pid')

        # Debug: Check if interfaces exist
        print("Checking interfaces...")
        self.topo.command_to(self.topo_config.client, f'ip link show {iface0}')
        self.topo.command_to(self.topo_config.client, f'ip link show {iface1}')

        # Debug: Check if tshark is available
        print("Checking tshark availability...")
        self.topo.command_to(self.topo_config.client, 'which tshark')

        # 1. Start tshark on path0 (improved command)
        tshark_cmd0 = (
            f'tshark -i {iface0} -f "udp port 4433" '
            f'-w {pcap0} '
            f'> /tmp/tshark0.log 2>&1 & echo $! > /tmp/tshark0.pid'
        )
        print(f"Starting tshark on {iface0}...")
        self.topo.command_to(self.topo_config.client, tshark_cmd0)
        
        # 2. Start tshark on path1 (improved command)
        tshark_cmd1 = (
            f'tshark -i {iface1} -f "udp port 4433" '
            f'-w {pcap1} '
            f'> /tmp/tshark1.log 2>&1 & echo $! > /tmp/tshark1.pid'
        )
        print(f"Starting tshark on {iface1}...")
        self.topo.command_to(self.topo_config.client, tshark_cmd1)
        
        # Give tshark time to start
        time.sleep(2)

        # Debug: Check if tshark processes are running
        print("Checking tshark processes...")
        self.topo.command_to(self.topo_config.client, 'ps aux | grep tshark')

        # Debug: Check if PID files were created
        self.topo.command_to(self.topo_config.client, 'ls -la /tmp/tshark*.pid')
        '''
        # Start the QUIC server
        print("Starting QUIC server...")

        cmd = self.get_quiche_server_cmd()
        self.topo.command_to(self.topo_config.server, cmd)

        self.topo.command_to(self.topo_config.client, "sleep 2")

        cmd = self.get_quiche_client_cmd()
        # time.sleep(200)
        self.topo.command_to(self.topo_config.client, cmd)

        self.topo.command_to(self.topo_config.client, "sleep 2")

        # Automated post-experiment analysis
        self.run_post_experiment_analysis()

        '''
        # Wait for the transfer to complete (adjust timing as needed)
        print("Waiting for transfer to complete...")
        time.sleep(10)  # Increased wait time
        
        # Debug: Check if PCAP files exist before stopping tshark
        print("Checking PCAP files before stopping capture...")
        self.topo.command_to(self.topo_config.client, f'ls -la {pcap_dir}/')
        
        # Stop tshark captures with better error handling
        print("Stopping tshark captures...")
        
        # Check if PID files exist before trying to kill
        pid_check0 = self.topo.command_to(self.topo_config.client, 'test -f /tmp/tshark0.pid && echo "exists" || echo "missing"')
        pid_check1 = self.topo.command_to(self.topo_config.client, 'test -f /tmp/tshark1.pid && echo "exists" || echo "missing"')
        
        # Kill tshark processes
        self.topo.command_to(self.topo_config.client, 'if [ -f /tmp/tshark0.pid ]; then kill $(cat /tmp/tshark0.pid) 2>/dev/null; fi')
        self.topo.command_to(self.topo_config.client, 'if [ -f /tmp/tshark1.pid ]; then kill $(cat /tmp/tshark1.pid) 2>/dev/null; fi')
        
        # Alternative: kill all tshark processes
        self.topo.command_to(self.topo_config.client, 'pkill -f tshark')
        
        # Give time for files to be written
        time.sleep(2)
        
        # Final check of PCAP files
        print("Final check of PCAP files...")
        self.topo.command_to(self.topo_config.client, f'ls -la {pcap_dir}/')
        self.topo.command_to(self.topo_config.client, f'file {pcap0} {pcap1}')
        
        # Check tshark logs for errors
        print("Checking tshark logs...")
        self.topo.command_to(self.topo_config.client, 'cat /tmp/tshark0.log')
        self.topo.command_to(self.topo_config.client, 'cat /tmp/tshark1.log')
        
        print("PCAP capture completed!")
        '''
        # # 8. Count QUIC losses on each path inside client namespace
        # loss0_output = self.topo.command_to(
        #     self.topo_config.client,
        #     f"tshark -r {pcap0} "
        #     f"-Y \"ip.src==10.0.0.1 && quic.analysis.lost_packet\" "
        #     "-q -z io,stat,0,COUNT(quic.analysis.lost_packet)"
        # )
        # loss1_output = self.topo.command_to(
        #     self.topo_config.client,
        #     f"tshark -r {pcap1} "
        #     f"-Y \"ip.src==10.0.1.1 && quic.analysis.lost_packet\" "
        #     "-q -z io,stat,0,COUNT(quic.analysis.lost_packet)"
        # )

        # # Helper to parse the numeric count
        # def parse_count(output):
        #     try:
        #         return int(output.strip().split()[-1])
        #     except Exception:
        #         return 0

        # loss0 = parse_count(loss0_output)
        # loss1 = parse_count(loss1_output)

        # print(f"QUIC Path0 ({iface0}) losses: {loss0}")
        # print(f"QUIC Path1 ({iface1}) losses: {loss1}")

        


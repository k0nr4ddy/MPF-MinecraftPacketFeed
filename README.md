Minecraft Packet Feed
Minecraft Packet Feed is a tool designed for stress testing Minecraft servers by sending a large number of packets to the target server. This tool can help server administrators evaluate their server's resilience to network attacks and optimize their infrastructure accordingly.

Features
Stress test Minecraft servers by sending packets at a specified rate and duration.
Monitor system resources including CPU usage, memory usage, disk usage, and simulated TPS (ticks per second) data.
Fetch player data from the database for analysis.
Backup the server's database for security purposes.
Prerequisites

Python 3.x installed on your system.
Required Python packages:
pyfiglet
psutil
matplotlib
numpy
Usage
Clone the repository to your local machine:

bash
Copy code
git clone https://github.com/your-username/minecraft-packet-feed.git
Navigate to the project directory:

bash
Copy code
cd minecraft-packet-feed
Run the minecraft_packet_feed.py script:

Copy code
python minecraft_packet_feed.py
Follow the prompts to enter the target IP address, port number, test duration, packets per second, and packet size.

Use the available commands to monitor system resources, print packet statistics, fetch player data, backup the database, or exit the program.

Commands
/print cpu: Print CPU usage.
/print memory: Print memory usage.
/print packets: Print total packets sent.
/overall send packets: Print overall packets sent during the test session.
/getinfo: Get specifications of the physical server's PC.
/get database: Download the server's database.
/exit: Exit the program.
License
This project is licensed under the MIT License - see the LICENSE file for details.

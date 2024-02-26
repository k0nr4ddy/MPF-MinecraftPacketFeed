# MPF - MinecraftPacketFeed

MPF (MinecraftPacketFeed) is a tool designed to stress test Minecraft servers by sending packets to measure their performance. It also provides basic server monitoring capabilities.

## Disclaimer

MPF is intended for educational and testing purposes only. Do not use MPF to harm, disrupt, or perform any unauthorized actions on Minecraft servers or any other systems. The author(s) of MPF are not responsible for any misuse of this tool.

## Features

- Stress tests Minecraft servers by sending packets.
- Measures server performance metrics such as packets per second, CPU usage, memory usage, etc.
- Provides a command-line interface for interacting with the tool.

## Usage

1. Clone or download the MPF repository to your local machine.
2. Install the required dependencies (`pyfiglet`, `psutil`).
3. Run the `main.py` script.
4. Follow the prompts to input the Minecraft server details and desired test parameters.
5. Use the command-line interface to interact with the tool and retrieve server metrics.

## Commands

- `/help`: Displays available commands.
- `/print cpu`: Prints CPU usage of the local system.
- `/print memory`: Prints memory usage of the local system.
- `/print packets`: Prints total packets sent to the Minecraft server.
- `/overall send packets`: Prints overall packets sent to the Minecraft server during the test session.
- `/exit`: Exits the program.

## Contributing

Contributions to MPF are welcome! If you find bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License

MPF is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

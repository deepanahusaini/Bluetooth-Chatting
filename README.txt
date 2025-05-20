Step 1: Install Visual Studio
Download and install Visual Studio Community Edition (free) from https://visualstudio.microsoft.com/downloads/
Step 2: Create a New Console Application
Open Visual Studio.
Click Create a new project.
Choose Console App (.NET Framework) (or Console App (.NET Core) if you prefer but check compatibility).
Click Next.
Enter the project name, e.g., BluetoothChatApp.
Choose a folder location.
Click Create.
Step 3: Add the Bluetooth Library (32feet.NET)
Go to Tools > NuGet Package Manager > Package Manager Console.
In the console, type the command to install the Bluetooth library:
Run
Copy code
Install-Package 32feet.NET -Version 3.5.0
Press Enter and wait for installation to complete.
Step 4: Replace the Program.cs File
In Solution Explorer on the right, find Program.cs and open it.
Delete all the existing code inside Program.cs.
Copy and paste the complete code from the Bluetooth chat app I provided earlier into Program.cs.
Step 5: Build the Project
Click Build > Build Solution (or press Ctrl + Shift + B).
Ensure there are no errors in the output window.
If errors appear, check the code pasted or NuGet package installed correctly.
Step 6: Prepare Your Bluetooth Devices
On both Windows machines (or one machine and another paired Bluetooth device), turn on Bluetooth.
Pair the two devices:
Open Settings > Devices > Bluetooth & other devices.
Scan for devices and pair the other device you want to chat with.
Step 7: Run the Program on Both Devices
Run the program on both devices (press F5 or click Start in Visual Studio).
The console will prompt:
Run
Copy code
Choose mode:
1. Host (Accept connection)
2. Client (Connect to a device)
Enter choice (1 or 2):
Step 8: Start the Host (Server)
On the device that will wait for the connection (Host), type 1 and press Enter.
You will see a message like:
Run
Copy code
Starting in Host mode, waiting for incoming Bluetooth connection...
Step 9: Start the Client
On the other device (Client), type 2 and press Enter.
The client will search for paired devices, for example:
Run
Copy code
Paired devices:
1: DeviceName1 [xx:xx:xx:xx:xx:xx]
2: DeviceName2 [yy:yy:yy:yy:yy:yy]
Enter device number to connect:
Type the number corresponding to the host device.
The client will connect to the host.
Step 10: Chatting
After the connection is established, the console will show:
Run
Copy code
You can start chatting now! Type 'exit' to quit.
Type your messages and press Enter to send.
Messages from the other device are displayed prefixed with Friend:.
To quit the chat, type exit and press Enter.
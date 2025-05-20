// This is a minimal Windows console Bluetooth chat app using 32feet.NET library.
// It supports chatting with a paired device over Bluetooth RFCOMM without internet.

// To run this app:
// 1. Create a new C# Console Application project in Visual Studio.
// 2. Open NuGet Package Manager and install the 32feet.NET package:
//      Install-Package 32feet.NET -Version 3.5.0
// 3. Replace the Program.cs contents with this code.
// 4. Build and run the app on two Windows devices with Bluetooth enabled and paired with each other.

using System;
using InTheHand.Net.Sockets;
using InTheHand.Net.Bluetooth;
using System.Text;
using System.Threading;
using System.IO;

namespace BluetoothChatApp
{
    class Program
    {
        // Bluetooth service GUID for chat app (custom UUID for RFCOMM)
        static readonly Guid chatServiceUuid = new Guid("00001101-0000-1000-8000-00805F9B34FB"); // standard SerialPortServiceClass_UUID

        static void Main(string[] args)
        {
            Console.WriteLine("Bluetooth Chat Application");
            Console.WriteLine("==========================");

            Console.WriteLine("Choose mode:");
            Console.WriteLine("1. Host (Accept connection)");
            Console.WriteLine("2. Client (Connect to a device)");
            Console.Write("Enter choice (1 or 2): ");
            var choice = Console.ReadLine();

            if (choice == "1")
            {
                RunHost();
            }
            else if (choice == "2")
            {
                RunClient();
            }
            else
            {
                Console.WriteLine("Invalid choice. Exiting.");
            }
        }

        static void RunHost()
        {
            Console.WriteLine("Starting in Host mode, waiting for incoming Bluetooth connection...");

            BluetoothListener listener = new BluetoothListener(chatServiceUuid);
            listener.Start();

            BluetoothClient client = listener.AcceptBluetoothClient();
            Console.WriteLine("Client connected: " + client.RemoteEndPoint.Address);

            using (var stream = client.GetStream())
            {
                ChatLoop(stream);
            }

            listener.Stop();
        }

        static void RunClient()
        {
            Console.WriteLine("Discovering paired Bluetooth devices...");

            BluetoothClient client = new BluetoothClient();
            var devices = client.DiscoverDevices(255, true, false, false);

            if (devices.Length == 0)
            {
                Console.WriteLine("No paired devices found. Please pair devices first.");
                return;
            }

            Console.WriteLine("Paired devices:");
            for (int i = 0; i < devices.Length; i++)
            {
                Console.WriteLine($"{i + 1}: {devices[i].DeviceName} [{devices[i].DeviceAddress}]");
            }

            Console.Write("Enter device number to connect: ");
            if (!int.TryParse(Console.ReadLine(), out int deviceIndex) || deviceIndex < 1 || deviceIndex > devices.Length)
            {
                Console.WriteLine("Invalid device selection.");
                return;
            }

            var device = devices[deviceIndex - 1];
            Console.WriteLine($"Connecting to {device.DeviceName}...");

            client.Connect(device.DeviceAddress, chatServiceUuid);
            Console.WriteLine("Connected to server.");

            using (var stream = client.GetStream())
            {
                ChatLoop(stream);
            }
        }

        static void ChatLoop(Stream stream)
        {
            var reader = new StreamReader(stream, Encoding.UTF8);
            var writer = new StreamWriter(stream, Encoding.UTF8) { AutoFlush = true };

            bool running = true;

            // Start receiver thread
            Thread receiverThread = new Thread(() =>
            {
                try
                {
                    while (running)
                    {
                        string incomingMessage = reader.ReadLine();
                        if (incomingMessage == null)
                        {
                            Console.WriteLine("Connection closed by remote device.");
                            running = false;
                            break;
                        }
                        Console.WriteLine("\nFriend: " + incomingMessage);
                        Console.Write("You: ");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Receiver error: " + ex.Message);
                    running = false;
                }
            });
            receiverThread.Start();

            Console.WriteLine("You can start chatting now! Type 'exit' to quit.");
            while (running)
            {
                Console.Write("You: ");
                string text = Console.ReadLine();
                if (text == null || text.ToLower() == "exit")
                {
                    running = false;
                    break;
                }

                try
                {
                    writer.WriteLine(text);
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Send error: " + ex.Message);
                    running = false;
                    break;
                }
            }

            try
            {
                stream.Close();
            }
            catch { }

            Console.WriteLine("Chat ended.");
        }
    }
}


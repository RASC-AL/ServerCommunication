using System;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace Server1
{
    class Program
    {
        static byte[] Buffer { get; set; }
        static Socket sck;
     
        static void Main(string[] args)
        {
            // Create an instance of the TcpListener class.
            TcpListener tcpListener = null;
            IPAddress ipAddress = new IPEndPoint(0, 5000).Address;
            try
            {
                // Set the listener on the local IP address 
                // and specify the port.
                tcpListener = new TcpListener(ipAddress, 5000);
                tcpListener.Start();
                Console.WriteLine("Waiting for a connection...");
            }
            catch (Exception e)
            {
                Console.WriteLine("Error: " + e.StackTrace);
                
            }
            while (true)
            {
                // Always use a Sleep call in a while(true) loop 
                // to avoid locking up your CPU.
                Thread.Sleep(10);
                // Create a TCP socket. 
                // If you ran this server on the desktop, you could use 
                // Socket socket = tcpListener.AcceptSocket() 
                // for greater flexibility.
                TcpClient tcpClient = tcpListener.AcceptTcpClient();
                // Read the data stream from the client. 
                byte[] bytes = new byte[256];
                NetworkStream stream = tcpClient.GetStream();
                stream.Read(bytes, 0, bytes.Length);
                var mstrMessage = Encoding.ASCII.GetString(bytes, 0, bytes.Length);
                Console.WriteLine(mstrMessage);
            }
        }
        
    }
}

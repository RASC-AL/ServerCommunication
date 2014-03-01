using System;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Net.Sockets;
namespace Client1
{
    class Program
    {
        static Socket sck;
        static void Main(string[] args)
        {
            sck = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            IPEndPoint localEndPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 1234);
            //Attempt a connection
            try
            {
                sck.Connect(localEndPoint);
            }
            catch
            {
                //if connections fails 
                Console.Write("Unable to connect to remote end point!\r\n");
                Main(args);
            }
            Console.Write("Enter Text: ");
            String text = Console.ReadLine();
            byte[] data = Encoding.ASCII.GetBytes(text);

            sck.Send(data);
            Console.Write("Data Sent. \r\n");
            Console.Write("Press any key to continue.. \r\n");
            Console.Read();
            sck.Close();
        }
    }
}

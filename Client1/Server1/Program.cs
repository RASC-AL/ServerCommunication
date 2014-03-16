using System;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Net.Sockets;

namespace Server1
{
    class Program
    {
        static byte[] Buffer { get; set; }
        static Socket sck;
        static void Main(string[] args)
        {
            sck = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            sck.Bind(new IPEndPoint(0, 5000));
            sck.Listen(100);

            while (true)
            {
                try
                {
                    Socket accepted = sck.Accept();
                    Buffer = new byte[accepted.SendBufferSize];    //Default Buffer Size is 8192
                    int bytesRead = accepted.Receive(Buffer);
                    byte[] formatted = new byte[bytesRead];
                    for (int i = 0; i < bytesRead; i++)
                    {
                        formatted[i] = Buffer[i];
                    }
                    String strData = Encoding.ASCII.GetString(formatted);
                    Console.Write(strData + "\r\n");
                    Console.Read();

                    accepted.Close();
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.StackTrace);
                }
            }
            sck.Close();
        }
    }
}

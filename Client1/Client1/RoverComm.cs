using System;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Net.Sockets;

namespace RoboOps.HomeClient
{
    public class RoverComm
    {
        string ip;
        int port;
        static Socket sck;
        

        public RoverComm(string ip, int port)
        {
            //this.ip = "128.205.54.5";
            //this.port = 5000;
            //TODO: remove the hardcoding
            this.ip = ip;
            this.port = port;
        }

        public bool send(string msg)
        {
            sck = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            IPEndPoint localEndPoint = new IPEndPoint(IPAddress.Parse(ip), port);
            //Attempt a connection
            try
            {
                sck.Connect(localEndPoint);

                byte[] data = Encoding.ASCII.GetBytes(msg.Trim());
                sck.Send(data);

            }
            catch (Exception e)
            {
                //if connections fails 
                Console.Write("Unable to connect to remote end point!\r\n");
                return false;
            }
            finally
            {
                sck.Close();
            }
            return true;
        }

        public bool send(string[] msgs)
        {
            sck = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            IPEndPoint localEndPoint = new IPEndPoint(IPAddress.Parse(ip), port);
            //Attempt a connection
            try
            {
                sck.Connect(localEndPoint);
                foreach (var msg in msgs)
                {
                    byte[] data = Encoding.ASCII.GetBytes(msg);
                    sck.Send(data);
                }
            }
            catch (Exception e)
            {
                //if connections fails 
                Console.Write("Unable to connect to remote end point!\r\n");
                return false;
            }
            finally
            {
                sck.Close();
            }
            return true;
        }

        public bool MoveRover(int leftSpeed, int rightSpeed)
        {
            return send("drv " + leftSpeed.ToString() + "," + rightSpeed.ToString());
        }

        public bool MoveArm(int baseRotation, int baseLift, int elbowRotation, int yaw)
        {
            return send("arm " + baseRotation.ToString() + "," + baseLift.ToString() + "," + elbowRotation.ToString() + "," + yaw.ToString());
        }

        public bool ChangeCamera(int cam)
        {

            return send("cam " + (cam - 1).ToString()+ ",5,1024,768");
        }

        static void Main(string[] args)
        {
            Console.WriteLine("Enter 5 msgs");
            String[] s = new String[2];
            for (int i = 0; i < s.Length; i++)
            {
                s[i] = Console.ReadLine();
            }

            RoverComm p = new RoverComm("128.205.54.5", 5000);
            p.send(s);
        }
    }
}

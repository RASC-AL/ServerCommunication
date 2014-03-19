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

        public bool MoveForward(double r, double theta)
        {
            return send("F " + r.ToString() + " " + theta );
        }

        public bool MoveBackward(double r, double theta)
        {
            return send("B " + r.ToString() + " " + theta );
        }

        public bool MoveArm(int theta1, int theta2, int theta3)
        {
            return send("arm:" + theta1.ToString() + "," + theta2.ToString() + "," + theta3.ToString());
        }

        public bool ChangeCamera(int cam)
        {
            if (cam > Constants.noOfCameras)
                return false;
            string cams = "cam ";
            for (int i = 1; i <= Constants.noOfCameras; i++)
            {
                if (cam == i)
                    cams += "1,";
                else
                    cams += "0,";
            }
            //cams = cams.Substring(0, cams.Length - 1);
            cams = cams + "15,640,480";
            return send(cams);
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

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
                Console.WriteLine(e.GetBaseException());
                Console.WriteLine(e.Message);
                return false;
            }
            finally
            {
                sck.Close();
            }
            return true;
        }

        public String reading()
        {
            sck = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            IPEndPoint localEndPoint = new IPEndPoint(IPAddress.Parse(ip), port);
            //Attempt a connection
            String ret = String.Empty;
            try
            {
                sck.Connect(localEndPoint);

                byte[] data = Encoding.ASCII.GetBytes("get");
                sck.Send(data);
                sck.Receive(data);
                ret = Encoding.UTF8.GetString(data);
            }
            catch (Exception e)
            {
                //if connections fails 
                Console.Write("Unable to connect to remote end point!\r\n");
                Console.WriteLine(e.GetBaseException());
                Console.WriteLine(e.Message);
            }
            finally
            {
                sck.Close();
            }
            return ret;
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

                Console.WriteLine("Unable to connect to remote end point!\r\n");
                Console.WriteLine(e.GetBaseException());
                Console.WriteLine(e.Message);
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
            return send("DRV " + leftSpeed.ToString() + "," + rightSpeed.ToString());
        }

        public bool ChangeRelay(bool mast, bool arm)
        {
            return send("RLY " + (mast?"1":"0") + "," + (arm?"1":"0"));
        }

        public bool ChangeCameras(string cameras)
        {
            return send("CCM " + cameras);
        }

        public bool MoveArm(int baseRotation, int baseLift, int elbowRotation, int yaw, string scoop)
        {
            return send("ARM " + baseRotation.ToString() + "," + baseLift.ToString() + "," + elbowRotation.ToString() + "," + yaw.ToString() + "," + scoop);
        }

        public bool ChangeCamera(int cam, int fps, int width, int height)
        {

            return send("CAM " + (cam - 1).ToString()+ ","+fps.ToString()+","+width.ToString()+","+height.ToString());
        }

        public bool PTZ(int pan, int tilt, int zoom, int focus, int brightness, int iris, bool autofocus)
        {

            return send("PTZ " + pan.ToString() + "," + tilt.ToString() + "," + zoom.ToString() + "," + focus.ToString() + "," + brightness.ToString() + "," + iris.ToString() + "," + (autofocus ? "true" : "false"));
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

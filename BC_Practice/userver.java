import java.io.*;
import java.net.*;

public class userver{
    public static void main(String[] args) throws Exception {
        DatagramSocket socket = new DatagramSocket(10000);
        byte[] buffer = new byte[1024];
        while (true) {
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
            socket.receive(packet);
            String message = new String(packet.getData(), 0, packet.getLength());
            System.out.println("Received: " + message);
            String response = "Echo: " + message;
            BufferedReader in=new BufferedReader(new InputStreamReader(System.in));
            String m=in.readLine();
            InetAddress address = packet.getAddress();
            int port = packet.getPort();
            DatagramPacket sendPacket = new DatagramPacket(response.getBytes(), response.length(), address, port);
            socket.send(sendPacket);
            if(m.equalsIgnoreCase("exit")) break;
        }
        socket.close();
    }
}
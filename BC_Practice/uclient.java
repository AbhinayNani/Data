import java.io.*;
import java.net.*;

public class uclient{
    public static void main(String[] args) throws IOException {
        Datagram Socket=new DatagramSocket();
        InetAddress addr=InetAddress.getByName("localhost");
        BufferedReader reader=new BufferedReader(new InputStreamReader(System.in));
        byte[] buf=new byte[1024];  
        int port=8080;
        while(true){
            String line=reader.readLine();
            if(line.equalsIgnoreCase("bye")) break;
            DatagramPacket msg=new DatagramPacket(line.getBytes(),line.length(),addr,10000);
            Socket.send(msg);
            DatagramPacket reply=new DatagramPacket(buf,buf.length);
            Socket.receive(reply);
            System.out.println(new String(reply.getData(),0,reply.getLength()));
        }
}
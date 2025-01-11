import java.io.*;
import java.net.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;

public class Ntpserver {
    private static final SimpleDateFormat sDateFormat = new SimpleDateFormat("hh:mm:ss.SSS");
    static{
        sDateFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
    }
    public static void main(String[] args) throws Exception {
        DatagramSocket socket = new DatagramSocket(10000);
        try {
            System.out.println("NTP server started on port 10000");
            while (true) {
                byte[] receiveData = new byte[1024];
                DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
                socket.receive(receivePacket);
                DataInputStream in=new DataInputStream(new ByteArrayInputStream(receivePacket.getData()));
                InetAddress IPAddress = receivePacket.getAddress();
                int port = receivePacket.getPort();
                byte[] sendData = new byte[48];
                long currentTimeMillis = System.currentTimeMillis();
                
import java.io.*;
import java.net.*;

public class server{
    public static void main(String args[] )throws IOException{
        try(ServerSocket socket = new ServerSocket(10000)){
            System.out.println("Server started on port 10000");
            try(Socket Clisocket=socket.accept()){
                BufferedReader in=new BufferedReader(new InputStreamReader(Clisocket.getInputStream()));
                PrintWriter out=new PrintWriter(Clisocket.getOutputStream(),true);
                String message=in.readLine();
                System.out.println("Client: "+message);
                BufferedReader sin=new BufferedReader(new InputStreamReader(System.in));
                while(true){
                    String s,s1;
                    while ((s=in.readLine())!=null){
                        System.out.println("Client: "+s);
                        s1=sin.readLine();
                        if(s1.equalsIgnoreCase("bye")) break;
                        out.println("Server: "+s1);
                        out.flush();
                }}
                out.println("Server: Hello Client!");
            }
        }
        socket.close();
        Clisocket.close();
        in.close();
        out.close();
        sin.close();
        System.exit(0);
}
}
import java.io.*;
import java.net.*;

public class client{
    public static void main(String args[]) throws Exception{
        Socket socket=new Socket("localhost",10000);
        BufferedReader in=new BufferedReader(new InputStreamReader(socket.getInputStream()));
        DataOuputStream out=new DataOuputStream(socket.getOutputStream());
        
        BufferedReader br=new BufferedReader(new InputStreamReader(System.in));
        String s,s1;
        while(!(s=br.readLine()).equals("bye")){
            out.writeBytes(s);
            out.flush();
            s1=in.readLine();
            System.out.println("Server: "+s1);
        }
        
        socket.close();
}
}
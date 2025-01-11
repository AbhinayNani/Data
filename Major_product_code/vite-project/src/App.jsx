import { useEffect } from "react";
import { Html5QrcodeScanner } from "html5-qrcode";

const App = () => {
  useEffect(() => {
    const scanner = new Html5QrcodeScanner(
      "reader",
      { fps: 10, qrbox: 250 },
      false
    );
    scanner.render(
      (decodedText) => {
        console.log("Scanned result:", decodedText);
        alert(`Scanned Data: ${decodedText}`);
      },
      (error) => {
        console.error("Error scanning QR code:", error);
      }
    );

    return () => {
      scanner.clear();
    };
  }, []);

  return <div id="reader" style={{ width: "300px" }}></div>;
};

export default App;

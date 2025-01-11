import "./App.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Error from "./Error";
import Login from "./Login";
import Home from "./Home";

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <Login />,
      errorElement: <Error/>,
    },
    {
      path: "/Home",
      element: <Home />,
      errorElement: <Error/>,
    },
  ]);
  return (
    <div className="app">
      <RouterProvider router={router}></RouterProvider>
    </div>
  );
}

export default App;
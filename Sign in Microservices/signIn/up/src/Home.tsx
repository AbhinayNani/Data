import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { VscAccount } from "react-icons/vsc";
import { GiEvilWings } from "react-icons/gi";

import "./Home.css";

function Home() {
  const [user, setUser] = useState<{ _id: string; email: string; password: string; name: string } | null>(null);
  const [dropdownVisible, setDropdownVisible] = useState(false);
  const navigate = useNavigate();

  async function login(email: string) {
    const response = await fetch(`http://localhost:9200/Home?email=${email}`, {
      method: "GET",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch user data");
    } else {
      const data = await response.json();
      setUser(data);
    }
  }

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (!storedUser) {
      navigate("/");
    } else {
      try {
        const parsedUser = JSON.parse(storedUser);
        login(parsedUser.email);
        setUser(parsedUser);
      } catch (error) {
        console.error("Failed to parse user data:", error);
        navigate("/");
      }
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("user"); 
    navigate("/"); 
  };

  if (!user) return null;

  return (
    <>
      <div className="menu">
        <div className="logo">
            <span>
                <GiEvilWings />
            </span>
        </div>
        <ol className="menu-list">
          <li>Home</li>
          <li>About us</li>
          <li>Contact us</li>
          <li
            className="user-menu"
            onMouseEnter={() => setDropdownVisible(true)}  // Show dropdown on hover
            onMouseLeave={() => setDropdownVisible(false)} // Hide dropdown when not hovering
          >
            <div className="user-info">
              <span>
                <i>
                  <VscAccount />
                </i>
              </span>
              {user.name && <span>{user.name}</span>}
            </div>
            {dropdownVisible && (
              <ul className="dropdown">
                <li onClick={() => navigate("/home")}>Home</li>
                <li onClick={handleLogout}>Logout</li>
              </ul>
            )}
          </li>
        </ol>
      </div>
    </>
  );
}

export default Home;

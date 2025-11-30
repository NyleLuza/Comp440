import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import SearchBar from "./SearchBar";

function Profile() {
  const { username } = useParams();
  const [data, setData] = useState();
  const [clicked, setClick] = useState(false);

  const handleSearch = async (searchTerm) => {
    const lowerCaseSearchTerm = searchTerm.toLowerCase();
    try {
      const response = await fetch(
        `http://localhost:8000/api/${username}/search/${lowerCaseSearchTerm}`
      );
      if (!response.ok) throw new Error("Network response was not ok");
      const accounts = await response.json();
      setData(accounts.users);
      console.log("accounts worked", accounts.status);
      console.log(data);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <nav className="d-flex flex-column">
      <div>
        <SearchBar onSearch={handleSearch} />
        {clicked ? (
          <ul>
            {data.map((item) => (
              <li key={item.id}>{item.username}</li>
            ))}
          </ul>
        ) : (
          <p></p>
        )}
      </div>
      <h2 className="d-flex justify-content-center">{username}</h2>
      <main className="d-flex flex-grow-1">
        <div className="d-flex flex-grow-1 flex-column align-items-center">
          Posts
          <h3>12</h3>
        </div>
        <div className="d-flex flex-grow-1 flex-column align-items-center">
          Followers
          <h3>10</h3>
        </div>
        <div className="d-flex flex-grow-1 flex-column align-items-center">
          Following
          <h3>12</h3>
        </div>
      </main>
      <p>Biography</p>
    </nav>
  );
}
export default Profile;

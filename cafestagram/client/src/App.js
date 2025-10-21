import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home.js";
import SignUpMenu from "./pages/SignUpMenu";
import LoginMenu from "./pages/LoginMenu.js";
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<SignUpMenu />} />
        <Route path="/login" element={<LoginMenu />} />
      </Routes>
    </Router>
  );
}

export default App;
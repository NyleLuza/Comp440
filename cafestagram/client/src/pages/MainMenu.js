import { useState } from "react";
import Post from "../components/Post.js"
import MainFeed from "../components/MainFeed.js";
function MainMenu(){
    const [showPost, setShowPost] = useState(false)
    return(
        <main className="d-flex flex-column" style={{
            height: '100%',
            width: '100%'
        }}>
            <nav className="d-flex flex-row justify-content-between align-items-center" style={{
                height: '15%',
                borderBottom: '2px solid black'
            }}>
                <button onClick={()=>setShowPost(true)} className="d-flex justify-content-center" style={{
                    width: '8%'
                }}>post</button>
                <h2 className="d-flex ">Cafestagram</h2>
                <button className="d-flex justify-content-center" style={{
                    width: '8%',
                    fontSize: '15px'
                }}>profile</button>
            </nav>
            {showPost ? (<Post postClickedOut={()=>setShowPost(false)}/>):
            (<MainFeed />)
            }
        </main>
    );
}
export default MainMenu;
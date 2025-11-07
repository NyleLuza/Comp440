function Post({postClickedOut}){
    return(
        <nav className="d-flex ">
            <button style={
                {width:'5%'}
            } onClick={postClickedOut}></button>
            <h2 className="d-flex flex-grow-1 justify-content-center">Post</h2>
        </nav>
    )
}
export default Post;
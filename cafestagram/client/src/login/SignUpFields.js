import './signUp.css'
function SignUpFields(){
    return(
        <section className="d-flex flex-column flex-grow-1">
            {/* Header  */}
            <h1>Sign Up</h1>

            {/* Form section for logging in sign up information */}
            <form className="d-flex flex-column flex-grow-1" style={{
                height: "50vh"
            }} method="post">
                <div class="signUp"
                >
                    <label for="firstName">First Name: </label>
                    <input type="text" id="firstName"></input>
                </div>
                <div class="signUp"
                >
                    <label for="lastName">Last Name: </label>
                    <input type="text" id="lastName"></input>
                </div>
                <div class="signUp"
                >
                    <label for="username">Username: </label>
                    <input type="text" id="username"></input>
                </div>
                <div class="signUp"
                >
                    <label for="email">Email Address: </label>
                    <input type="text" id="email"></input>
                </div>
                <div class="signUp"
                >
                    <label for="phoneNumber">Phone Number: </label>
                    <input type="text" id="phoneNumber"></input>
                </div>
                <div class="signUp"
                >
                    <label for="password">Password: </label>
                    <input type="password" id="password"></input>
                </div>
            </form>
        </section>
    );
}

export default SignUpFields;
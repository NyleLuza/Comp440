import SignUpFields from "./SignUpFields.js";
function MainMenu() {
  return (
    <main className='d-flex flex-column' style={{
      height: '100%',
      width: '100%'
    }}>
      <SignUpFields />
    </main>
  );
}

export default MainMenu;

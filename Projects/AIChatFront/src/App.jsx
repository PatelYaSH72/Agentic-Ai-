import { useState } from "react";
import Navbar from "./components/Navbar";
import IntroScreen from "./components/IntroScreen";
import Home from "./pages/Home";

function App() {
  const [showIntro, setShowIntro] = useState(true);

  return (
    <>
      {showIntro ? (
        <IntroScreen onFinish={() => setShowIntro(false)} />
      ) : (
        <>
          <Navbar/>
          <Home/>
          
        </>
      )}
    </>
  );
}

export default App;
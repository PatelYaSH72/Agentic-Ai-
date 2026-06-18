import { useState } from "react";
import Navbar from "./components/Navbar";
import IntroScreen from "./components/IntroScreen";

function App() {
  const [showIntro, setShowIntro] = useState(true);

  return (
    <>
      {showIntro ? (
        <IntroScreen onFinish={() => setShowIntro(false)} />
      ) : (
        <>
          <Navbar/>

          <div className="h-[calc(100vh-72px)] flex items-center justify-center">
            <h1 className="text-4xl font-bold">
              Welcome to AIChat
            </h1>
          </div>
        </>
      )}
    </>
  );
}

export default App;
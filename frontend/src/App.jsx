import { useState, useEffect } from "react";
import { FaPaperclip, FaArrowRight } from 'react-icons/fa';
import "./App.css";
import logo from './logo.jpg';

function App() {
  const [message, setMessage] = useState("");
  const [chats, setChats] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [image, setImage] = useState(null);
  const [userId, setUserId] = useState(null);

  const sendInitialBotMessage = () => {
    const initialMessage = {
      role: "bot",
      content: "I am Stone Canyon bot, how may I help you?",
      image: null
    };
    setChats([initialMessage]);
  };

  useEffect(() => {
    const startSession = async () => {
      try {
        // Make sure to use HTTP since you want to avoid mixed content errors
        const sessionResponse = await fetch("https://what-do-you-need.onrender.com/start_session", {
          method: "POST",
          // 'no-cors' mode can be used to avoid CORS issues, but it limits response access
          mode: 'no-cors',
        });

        // Since 'no-cors' mode is used, you cannot access the sessionData directly
        // However, in a real scenario, you would want to remove 'no-cors' and switch to HTTPS to handle it securely
        // const sessionData = await sessionResponse.json();
        // setUserId(sessionData.user_id);

        // Placeholder for now due to 'no-cors'
        const dummyUserId = '12345';
        setUserId(dummyUserId);

        await fetch(`https://what-do-you-need.onrender.com/reset/${dummyUserId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });
      } catch (error) {
        console.error("Session initiation failed:", error);
      }
    };

    startSession();
    setMessage("");
    setChats([]);
    setImage(null);
    setTimeout(() => {
      sendInitialBotMessage();
    }, 1000); // 1000 milliseconds = 1 second
  }, []);

  const chat = async (e) => {
    e.preventDefault();
    if (!message && !image) return;
    setIsTyping(true);
    let msgs = chats;

    if (image) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result.split(",")[1];
        const userMsg = { role: "user", content: message, image: reader.result };
        msgs.push(userMsg);
        setChats([...msgs]);
        const payload = {
          query: message,
          image_url: base64String,
        };
        sendRequest(payload);
      };
      reader.readAsDataURL(image);
    } else {
      const userMsg = { role: "user", content: message, image: null };
      msgs.push(userMsg);
      setChats([...msgs]);
      const payload = {
        query: message,
        image_url: null,
      };
      sendRequest(payload);
    }
    setMessage("");
    setImage(null);
  };

  const sendRequest = (payload) => {
    fetch(`https://what-do-you-need.onrender.com/ai/${userId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        let msgs = chats;
        const botMsg = { role: "bot", content: data.content, image: null };
        msgs.push(botMsg);
        setChats([...msgs]);
        setIsTyping(false);
      })
      .catch((error) => {
        console.log("Fetch error:", error);
        setIsTyping(false);
      });
  };

  const resetChat = async () => {
    await fetch(`https://what-do-you-need.onrender.com/reset/${userId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    setMessage("");
    setChats([]);
    setImage(null);
    setTimeout(() => {
      sendInitialBotMessage();
    }, 500); // 500 milliseconds = 0.5 seconds
  };

  return (
    <main>
      <header>
        <img src={logo} alt="Stone Canyon Logo" className="logo" />
        <h1>Welcome to Stone Canyon Support</h1>
      </header>
      <section>
        {chats && chats.length
          ? chats.map((chat, index) => (
              <div key={index} className={`chat-bubble ${chat.role}`}>
                <div className="chat-content">
                  <span>
                    <b>{chat.role.toUpperCase()}</b>
                  </span>
                  <span>:</span>
                  <span>{chat.content}</span>
                  {chat.image && <img src={chat.image} alt="User provided" className="chat-image" />}
                </div>
              </div>
            ))
          : ""}
      </section>
      <div className={isTyping ? "" : "hide"}>
        <p>
          <i>{isTyping ? "Typing..." : ""}</i>
        </p>
      </div>
      <form onSubmit={chat} className="chat-form">
        <label htmlFor="file-input" className="file-input-label">
          <FaPaperclip />
        </label>
        <input
          id="file-input"
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
          style={{ display: 'none' }}
        />
        <div className="text-input-container">
          <input
            type="text"
            name="message"
            value={message}
            placeholder="Type a message here and hit Enter..."
            onChange={(e) => setMessage(e.target.value)}
          />
          {image && (
            <div className="image-preview">
              <img src={URL.createObjectURL(image)} alt="Preview" className="preview-image" />
            </div>
          )}
        </div>
        <button type="submit">
          <FaArrowRight />
        </button>
      </form>
      <button className="clear-chat" onClick={resetChat}>Clear Chat</button>
    </main>
  );
}

export default App;

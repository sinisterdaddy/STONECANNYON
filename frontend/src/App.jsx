import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [chats, setChats] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [image, setImage] = useState(null);

  const chat = async (e) => {
    e.preventDefault();

    if (!message && !image) return;
    setIsTyping(true);

    let msgs = chats;
    msgs.push({ role: "user", content: message });
    setChats([...msgs]);

    const sendRequest = (payload) => {
      fetch("http://localhost:8080/ai", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
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
          msgs.push({ role: "bot", content: data.content });
          setChats([...msgs]);
          setIsTyping(false);
        })
        .catch((error) => {
          console.log("Fetch error:", error);
          setIsTyping(false);
        });
    };

    if (image) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result.split(",")[1];
        const payload = {
          query: message,
          image_url: base64String
        };
        sendRequest(payload);
      };
      reader.readAsDataURL(image);
    } else {
      const payload = {
        query: message,
        image_url: null
      };
      sendRequest(payload);
    }

    setMessage("");
    setImage(null);
  };

  return (
    <main>
      <h1>What do you need?</h1>

      <section>
        {chats && chats.length
          ? chats.map((chat, index) => (
              <p key={index} className={chat.role === "user" ? "user_msg" : "bot_msg"}>
                <span>
                  <b>{chat.role.toUpperCase()}</b>
                </span>
                <span>:</span>
                <span>{chat.content}</span>
              </p>
            ))
          : ""}
      </section>

      <div className={isTyping ? "" : "hide"}>
        <p>
          <i>{isTyping ? "Typing..." : ""}</i>
        </p>
      </div>

      <form onSubmit={chat}>
        <input
          type="text"
          name="message"
          value={message}
          placeholder="Type a message here and hit Enter..."
          onChange={(e) => setMessage(e.target.value)}
        />
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
        />
        <button type="submit">Send</button>
      </form>
    </main>
  );
}

export default App;

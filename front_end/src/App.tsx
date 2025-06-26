import { useState } from "react";
import type { ChatMessage } from "./types";
import { ChatInput, ChatMessageComponent } from "./components";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [responses, setResponses] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const userMessage = input;
    setInput("");
    // Immediately add the user's message with a placeholder response
    setResponses((prev) => [
      ...prev,
      {
        user: userMessage,
        response: {
          loading: true,
          chart_type: "",
          result: [],
        },
      },
    ]);

    try {
      const res = await fetch(
        `http://localhost:3000/analyze?text=${encodeURIComponent(userMessage)}`
      );

      if (!res.ok) {
        // Handle 400 status code by extracting error message from response
        if (res.status === 400) {
          const errorData = await res.json();
          const errorMessage = errorData.error || "Bad request";
          setResponses((prev) => {
            // Update the last message with the error response
            const updated = [...prev];
            updated[updated.length - 1] = {
              ...updated[updated.length - 1],
              response: {
                chart_type: "error",
                result: [errorMessage],
                loading: false,
              },
            };
            return updated;
          });
        } else {
          throw new Error("API error");
        }
      } else {
        const apiData = await res.json();
        setResponses((prev) => {
          // Update the last message with the API response
          const updated = [...prev];
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            response: { ...apiData, loading: false },
          };
          return updated;
        });
      }
    } catch {
      setResponses((prev) => {
        // Update the last message with a generic error
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          response: {
            chart_type: "error",
            result: ["Internal error, try again."],
            loading: false,
          },
        };
        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
        height: "100%",
        justifyContent: "space-between",
        margin: "0 auto",
        position: "relative",
      }}
    >
      <h1 style={{ margin: "16px 0 0 0" }}>
        Nivii<span style={{ fontSize: 8 }}>(mini)</span>
      </h1>
      <div
        style={{
          display: "flex",
          justifyContent: "flex-end",
          flexDirection: "column",
          height: "100%",
        }}
      >
        <div style={{ width: "100%", maxWidth: 800, margin: "0 auto" }}>
          <div
            style={{
              flex: 1,
              padding: "16px 0 0 0",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
              {responses.length === 0 && (
                <div
                  style={{ color: "#888", textAlign: "center", marginTop: 32 }}
                >
                  Start a conversation by typing a prompt below.
                </div>
              )}
              {responses.map((message, idx) => (
                <ChatMessageComponent key={idx} message={message} />
              ))}
            </div>
          </div>
          <ChatInput
            input={input}
            setInput={setInput}
            onSubmit={handleSubmit}
            loading={loading}
          />
        </div>
        <p
          style={{
            color: "#888",
            fontSize: 12,
            textAlign: "center",
            zIndex: 100,
            margin: 0,
            marginTop: 50,
            padding: "8px 0",
          }}
        >
          Made with ❤️ by Tomas
        </p>
      </div>
    </div>
  );
}

export default App;

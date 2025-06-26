import type { ChatMessage as ChatMessageType } from "../types";
import { UserMessage } from "./UserMessage";
import { ChartMessage } from "./ChartMessage";

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage = ({ message }: ChatMessageProps) => (
  <div style={{ marginBottom: 8 }}>
    <UserMessage message={message.user} />
    <div
      style={{
        background: "#f3f4f6",
        borderRadius: 16,
        borderTopLeftRadius: 0,
        padding: 16,
        maxWidth: "fit-content",
        margin: "0 auto 0 0",
        boxShadow: "0 1px 4px rgba(0,0,0,0.04)",
      }}
    >
      <ChartMessage response={message.response}/>
    </div>
  </div>
); 
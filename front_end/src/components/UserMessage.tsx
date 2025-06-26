interface UserMessageProps {
  message: string;
}

export const UserMessage = ({ message }: UserMessageProps) => (
  <div
    style={{
      background: "#e0e7ff",
      color: "#3730a3",
      alignSelf: "flex-end",
      borderRadius: 16,
      borderTopRightRadius: 0,
      padding: "8px 16px",
      maxWidth: "fit-content",
      margin: "0 0 8px auto",
      fontWeight: 500,
    }}
  >
    {message}
  </div>
); 
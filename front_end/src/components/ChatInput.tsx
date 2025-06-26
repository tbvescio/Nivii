interface ChatInputProps {
  input: string;
  setInput: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  loading: boolean;
}

export const ChatInput = ({
  input,
  setInput,
  onSubmit,
  loading,
}: ChatInputProps) => (
  <form
    onSubmit={onSubmit}
    style={{ padding: "16px 0", display: "flex", gap: 8 }}
  >
    <input
      type="text"
      value={input}
      onChange={(e) => setInput(e.target.value)}
      placeholder="Enter your prompt..."
      style={{
        flex: 1,
        padding: 12,
        fontSize: 16,
        borderWidth: 0,
        borderRadius: 8,
      }}
      required
      disabled={loading}
    />
    <button
      type="submit"
      disabled={loading || !input.trim()}
      style={{ padding: "8px 16px" }}
    >
      {loading ? "Analyzing..." : "Send"}
    </button>
  </form>
);

export interface ApiResponse {
  loading?: boolean;
  chart_type: string;
  result: unknown[];
  analysis?: string;
  error?: string;
  [key: string]: unknown;
}

export interface PieEntry {
  name: string;
  value: number;
}

export interface ChatMessage {
  user: string;
  response: ApiResponse;
}

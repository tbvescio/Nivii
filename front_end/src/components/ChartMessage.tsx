import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { ApiResponse, PieEntry } from "../types";

interface ChartMessageProps {
  response: ApiResponse;
}

// Utility to format numbers with K/M/B suffixes
const formatNumber = (num: number): string => {
  if (Math.abs(num) >= 1_000_000_000)
    return (num / 1_000_000_000).toFixed(1).replace(/\.0$/, "") + "B";
  if (Math.abs(num) >= 1_000_000)
    return (num / 1_000_000).toFixed(1).replace(/\.0$/, "") + "M";
  if (Math.abs(num) >= 1_000)
    return (num / 1_000).toFixed(1).replace(/\.0$/, "") + "K";
  return num.toString();
};

// Utility to format dates from 'Sat, 21 Sep 2024 00:00:00 GMT' to '21 Sep 2024'
const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) return dateStr;
  return date.toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
};

export const ChartMessage = ({ response }: ChartMessageProps) => {
  if (response?.loading) {
    return <div className="loader"></div>;
  }
  if (!response || !response.chart_type || !response.result) return null;

  const chartType = response.chart_type.toLowerCase();
  const data = response.result;
  const analysis = response.analysis;

  if (chartType === "error") {
    return (
      <div style={{ color: "#333", fontWeight: 500 }}>
        {Array.isArray(data) ? String(data[0]) : String(data)}
      </div>
    );
  }

  if (!Array.isArray(data) || data.length === 0)
    return <div style={{ color: "#333" }}>No data</div>;

  // Convert list of lists to array of objects for recharts
  let chartData: { x: number | string; value: number }[] = [];
  if (Array.isArray(data) && Array.isArray(data[0])) {
    chartData = (data as unknown[]).map((row) => {
      if (Array.isArray(row) && row.length >= 2) {
        return { x: row[0], value: Number(row[1]) };
      }
      return { x: "", value: 0 };
    });
  } else {
    chartData = data as { x: number | string; value: number }[];
  }

  // For pie chart, recharts expects name/value
  let pieData: PieEntry[];
  if (chartType === "pie") {
    pieData = chartData.map((d, i) => ({
      name: String(d.x ?? `Value ${i + 1}`),
      value: d.value,
    }));
  } else {
    pieData = [];
  }

  const renderChart = () => {
    switch (chartType) {
      case "line":
        return (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <XAxis
                dataKey="x"
                tickFormatter={(tick) => {
                  // Try to format as date, fallback to string
                  if (typeof tick === "string" && /\w{3},/.test(tick)) {
                    return formatDate(tick);
                  }
                  return tick;
                }}
              />
              <YAxis tickFormatter={formatNumber} />
              <Tooltip
                formatter={(value: number) => [formatNumber(value), "value"]}
                labelFormatter={(label: string | number) => {
                  if (typeof label === "string" && /\w{3},/.test(label)) {
                    return formatDate(label);
                  }
                  return label;
                }}
              />
              <Legend formatter={() => "value"} />
              <Line type="monotone" dataKey="value" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        );
      case "bar":
        return (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <XAxis
                dataKey="x"
                tickFormatter={(tick) => {
                  if (typeof tick === "string" && /\w{3},/.test(tick)) {
                    return formatDate(tick);
                  }
                  return tick;
                }}
              />
              <YAxis tickFormatter={formatNumber} />
              <Tooltip
                formatter={(value: number) => [formatNumber(value), "value"]}
                labelFormatter={(label: string | number) => {
                  if (typeof label === "string" && /\w{3},/.test(label)) {
                    return formatDate(label);
                  }
                  return label;
                }}
              />
              <Legend formatter={() => "value"} />
              <Bar dataKey="value" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        );
      case "pie":
        return (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                fill="#8884d8"
                label={({ name, value }) =>
                  `${name}: ${formatNumber(value ?? 0)}`
                }
              >
                {pieData.map((_entry: PieEntry, index: number) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={
                      ["#8884d8", "#82ca9d", "#ffc658", "#ff8042"][index % 4]
                    }
                  />
                ))}
              </Pie>
              <Tooltip
                formatter={(value: number) => [formatNumber(value), "value"]}
                labelFormatter={(label: string | number) => label}
              />
              <Legend formatter={(value: string) => value} />
            </PieChart>
          </ResponsiveContainer>
        );
      case "table":
        return (
          <div
            style={{
              overflowX: "auto",
              maxWidth: "100%",
              border: "1px solid #e1e5e9",
              borderRadius: 8,
              backgroundColor: "white",
            }}
          >
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                fontSize: 14,
              }}
            >
              <tbody>
                {data.map((row: unknown, rowIndex: number) => (
                  <tr
                    key={rowIndex}
                    style={{
                      borderBottom: "1px solid #f3f4f6",
                      backgroundColor: rowIndex % 2 === 0 ? "white" : "#f9fafb",
                    }}
                  >
                    {Array.isArray(row) &&
                      row.map((cell: unknown, cellIndex: number) => (
                        <td
                          key={cellIndex}
                          style={{
                            padding: "12px 16px",
                            textAlign: "left",
                            color: "#374151",
                          }}
                        >
                          {String(cell)}
                        </td>
                      ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      default:
        return <div>Unknown chart type: {chartType}</div>;
    }
  };

  return (
    <div>
      {renderChart()}
      {analysis && (
        <div
          style={{
            marginTop: 16,
            padding: 20,
            fontSize: 14,
            color: "#333",
            textAlign: "left",
          }}
        >
          {analysis}
        </div>
      )}
    </div>
  );
};

"use client";
import React, { useEffect, useState, useRef } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

export interface DiagramInfo {
  type: "graph" | "flowchart" | "svg_library" | "svg_generated" | "none";
  title?: string;
  data?: any;
  library_key?: string;
  note?: string;
}

/**
 * Sanitizes Mermaid syntax:
 * - Strips any ```mermaid or ``` fences
 * - Wraps every node label in double quotes (e.g. B["Follicular (Proliferative) Phase"])
 *   because unquoted parentheses break Mermaid parsing.
 */
export function sanitizeMermaidCode(raw: string): string {
  if (!raw || typeof raw !== "string") return "";
  let code = raw.trim();

  // 1. Strip markdown fences like ```mermaid ... ``` or ``` ... ```
  code = code.replace(/```mermaid\s*/gi, "");
  code = code.replace(/```\s*$/g, "");
  code = code.replace(/^```\s*/g, "");
  code = code.trim();

  // Ensure diagram type header if missing
  if (!/^(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|erDiagram|gantt|pie|gitGraph)\b/i.test(code)) {
    code = "graph TD\n" + code;
  }

  // 2. Wrap node labels in double quotes for rectangular nodes: nodeId[content]
  code = code.replace(/([a-zA-Z0-9_-]+)\[([^\]\r\n]+)\]/g, (match, id, label) => {
    const trimmed = label.trim();
    if (trimmed.startsWith('"') && trimmed.endsWith('"')) {
      return `${id}[${trimmed}]`;
    }
    const safe = trimmed.replace(/"/g, "'");
    return `${id}["${safe}"]`;
  });

  // 3. Wrap node labels in double quotes for rounded nodes: nodeId(content)
  code = code.replace(/([a-zA-Z0-9_-]+)\((?!\()([^\)\r\n]+)\)/g, (match, id, label) => {
    const trimmed = label.trim();
    if (trimmed.startsWith('"') && trimmed.endsWith('"')) {
      return `${id}("${trimmed}")`;
    }
    const safe = trimmed.replace(/"/g, "'");
    return `${id}("${safe}")`;
  });

  // 4. Wrap edge labels if they contain parentheses: |label|
  code = code.replace(/\|([^\|\r\n]+)\|/g, (match, label) => {
    const trimmed = label.trim();
    if (trimmed.startsWith('"') && trimmed.endsWith('"')) {
      return `|${trimmed}|`;
    }
    if (trimmed.includes("(") || trimmed.includes(")") || trimmed.includes("/")) {
      const safe = trimmed.replace(/"/g, "'");
      return `|"${safe}"|`;
    }
    return `|${trimmed}|`;
  });

  return code;
}

export function DiagramRenderer({ diagram }: { diagram?: DiagramInfo | null }) {
  const [mounted, setMounted] = useState(false);
  const [mermaidSvg, setMermaidSvg] = useState<string>("");
  const [mermaidError, setMermaidError] = useState<string>("");
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Handle Mermaid Flowcharts (Client-Only dynamic import with strict configuration)
  useEffect(() => {
    if (!mounted || !diagram || diagram.type !== "flowchart" || typeof diagram.data !== "string") {
      return;
    }

    let isMounted = true;
    const rawCode = diagram.data.trim();
    const sanitizedCode = sanitizeMermaidCode(rawCode);
    const uniqueId = "mermaid-" + Math.random().toString(36).substring(2, 9) + "-" + Date.now().toString(36);

    import("mermaid")
      .then(async (m) => {
        if (!isMounted) return;
        const mermaid = m.default;
        mermaid.initialize({
          startOnLoad: false,
          securityLevel: "strict",
          theme: "neutral",
        });

        const { svg } = await mermaid.render(uniqueId, sanitizedCode);
        if (isMounted) {
          setMermaidSvg(svg);
          setMermaidError("");
        }
      })
      .catch((err) => {
        if (isMounted) {
          console.error("Mermaid diagram rendering error:", err);
          // Remove any stray error elements created in document body
          const stray = document.getElementById(uniqueId) || document.getElementById("d" + uniqueId);
          if (stray) stray.remove();
          setMermaidError(String(err?.message || err || "Syntax error in flowchart definition"));
          setMermaidSvg("");
        }
      });

    return () => {
      isMounted = false;
      const stray = document.getElementById(uniqueId) || document.getElementById("d" + uniqueId);
      if (stray) stray.remove();
    };
  }, [diagram, mounted]);

  if (!diagram || diagram.type === "none") {
    return null;
  }

  // Download Handler (SVG & PNG using the rendered SVG element)
  const downloadDiagram = (format: "svg" | "png") => {
    if (!containerRef.current) return;
    const svgEl = containerRef.current.querySelector("svg");
    if (!svgEl) {
      alert("Diagram not ready for download yet.");
      return;
    }

    const bbox = svgEl.getBoundingClientRect();
    const width = Math.max(bbox.width || 0, 800);
    const height = Math.max(bbox.height || 0, 500);

    // Clone SVG to inject namespace and dimensions safely
    const svgClone = svgEl.cloneNode(true) as SVGSVGElement;
    if (!svgClone.getAttribute("xmlns")) {
      svgClone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    }
    if (!svgClone.getAttribute("width")) {
      svgClone.setAttribute("width", String(width));
    }
    if (!svgClone.getAttribute("height")) {
      svgClone.setAttribute("height", String(height));
    }

    const svgData = new XMLSerializer().serializeToString(svgClone);
    const filename = (diagram.title || "diagram").toLowerCase().replace(/[^a-z0-9]+/g, "-") + "." + format;

    if (format === "svg") {
      const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } else {
      // PNG Export via Canvas (2x scale for high resolution)
      const canvas = document.createElement("canvas");
      canvas.width = width * 2;
      canvas.height = height * 2;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      const img = new Image();
      const svgBlob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(svgBlob);
      img.onload = () => {
        ctx.fillStyle = "#FFFFFF";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        URL.revokeObjectURL(url);

        const a = document.createElement("a");
        a.href = canvas.toDataURL("image/png");
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      };
      img.onerror = () => {
        URL.revokeObjectURL(url);
        // Fallback to SVG download if canvas loading fails
        const fallbackBlob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
        const fallbackUrl = URL.createObjectURL(fallbackBlob);
        const a = document.createElement("a");
        a.href = fallbackUrl;
        a.download = filename.replace(/\.png$/, ".svg");
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(fallbackUrl);
      };
      img.src = url;
    }
  };

  return (
    <div className="mt-4 p-5 rounded-2xl bg-[#FAF8F5] border border-[#EBE4D8] shadow-xs space-y-3">
      {/* Header with Title and Download Buttons */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#EAE3D6]">
        <div className="flex items-center gap-2">
          <span className="text-base">📊</span>
          <span className="font-semibold text-sm text-[#29221C]">
            {diagram.title || "Visual Diagram"}
          </span>
          <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full bg-[#E5EDE3] text-[#3D6649]">
            {diagram.type === "graph" ? "Plot / Graph" :
             diagram.type === "flowchart" ? "Flowchart" :
             diagram.type === "svg_library" ? "Curriculum Diagram" : "AI Schematic"}
          </span>
        </div>

        {/* Download Buttons using rendered SVG */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => downloadDiagram("png")}
            className="px-2.5 py-1 text-[11px] font-medium rounded-lg border border-[#D5CCC0] bg-white text-[#4A433B] hover:bg-[#F4EFE6] transition-colors cursor-pointer flex items-center gap-1 shadow-xs"
            title="Download PNG image"
          >
            <span>📥</span> PNG
          </button>
          <button
            onClick={() => downloadDiagram("svg")}
            className="px-2.5 py-1 text-[11px] font-medium rounded-lg border border-[#D5CCC0] bg-white text-[#4A433B] hover:bg-[#F4EFE6] transition-colors cursor-pointer flex items-center gap-1 shadow-xs"
            title="Download vector SVG"
          >
            <span>📥</span> SVG
          </button>
        </div>
      </div>

      {/* Main Diagram Canvas */}
      <div ref={containerRef} className="w-full flex items-center justify-center min-h-[220px] overflow-x-auto py-2">
        {/* 1. RECHARTS GRAPH */}
        {diagram.type === "graph" && diagram.data && mounted && (
          <div className="w-full max-w-2xl h-72">
            {(() => {
              const graphData = diagram.data;
              const xKey = graphData.x_label || "x";
              const seriesList = graphData.series || [];

              // Combine points into tabular rows
              const rowsMap: Record<number, any> = {};
              seriesList.forEach((s: any) => {
                (s.points || []).forEach(([x, y]: [number, number]) => {
                  if (!rowsMap[x]) rowsMap[x] = { [xKey]: x };
                  rowsMap[x][s.name || "Value"] = y;
                });
              });
              const formattedData = Object.values(rowsMap).sort((a: any, b: any) => a[xKey] - b[xKey]);

              const colors = ["#0284c7", "#ec4899", "#16a34a", "#f59e0b"];

              return (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={formattedData} margin={{ top: 10, right: 30, left: 10, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                    <XAxis
                      dataKey={xKey}
                      stroke="#64748b"
                      label={{ value: xKey, position: "insideBottom", offset: -15, fill: "#475569", fontSize: 12 }}
                    />
                    <YAxis
                      stroke="#64748b"
                      label={{ value: graphData.y_label || "Value", angle: -90, position: "insideLeft", fill: "#475569", fontSize: 12 }}
                    />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#1e293b", borderColor: "#475569", borderRadius: "8px", color: "#f8fafc", fontSize: 12 }}
                    />
                    <Legend verticalAlign="top" height={36} />
                    {seriesList.map((s: any, idx: number) => (
                      <Line
                        key={idx}
                        type="monotone"
                        dataKey={s.name || "Value"}
                        stroke={colors[idx % colors.length]}
                        strokeWidth={3}
                        dot={{ r: 5, fill: colors[idx % colors.length] }}
                        activeDot={{ r: 8 }}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              );
            })()}
          </div>
        )}

        {/* 2. MERMAID FLOWCHART */}
        {diagram.type === "flowchart" && (
          <div className="w-full flex flex-col items-center justify-center">
            {mermaidSvg ? (
              <div
                className="w-full max-w-2xl flex justify-center [&>svg]:max-w-full [&>svg]:h-auto shadow-2xs rounded-xl overflow-hidden bg-white p-4 border border-[#F0EBE3]"
                dangerouslySetInnerHTML={{ __html: mermaidSvg }}
              />
            ) : mermaidError ? (
              <div className="w-full max-w-xl space-y-2 p-4 rounded-xl bg-[#FAF5EE] border border-[#E8DEC8] text-center">
                <div className="text-xs font-semibold text-[#A84234] flex items-center justify-center gap-1.5">
                  <span>⚠️</span>
                  <span>Diagram could not be drawn</span>
                </div>
                <pre className="text-left font-mono text-[11px] bg-white border border-[#E4DDD0] p-3 rounded-lg text-[#5C5346] whitespace-pre-wrap overflow-x-auto">
                  {diagram.data}
                </pre>
              </div>
            ) : (
              <div className="text-xs text-[#8C8377] animate-pulse py-6">Rendering flowchart...</div>
            )}
          </div>
        )}

        {/* 3. SVG LIBRARY / GENERATED SVG */}
        {(diagram.type === "svg_library" || diagram.type === "svg_generated") && (
          <div className="w-full max-w-2xl flex justify-center">
            {diagram.data ? (
              <div
                className="w-full [&>svg]:w-full [&>svg]:h-auto [&>svg]:rounded-xl shadow-xs"
                dangerouslySetInnerHTML={{ __html: diagram.data }}
              />
            ) : (
              <div className="text-xs text-[#8C8377]">Diagram not available.</div>
            )}
          </div>
        )}
      </div>

      {/* Note / Disclaimer */}
      {diagram.note && (
        <div className="text-[11px] text-[#8C8377] italic text-center pt-2 border-t border-[#EDE7DF]">
          {diagram.note}
        </div>
      )}
    </div>
  );
}

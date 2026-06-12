import { useState, useEffect, useRef } from "react";
import "./App.css";

const API = "http://localhost:8000";

export default function App() {
  const [documents, setDocuments] = useState([]);
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    fetchDocuments();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const fetchDocuments = async () => {
    try {
      const res = await fetch(`${API}/documents`);
      const data = await res.json();
      setDocuments(data.documents || []);
    } catch {
      setDocuments([]);
    }
  };

  const uploadFile = async (file) => {
    const allowed = [".pdf", ".docx", ".md", ".txt"];
    const ext = "." + file.name.split(".").pop().toLowerCase();
    if (!allowed.includes(ext)) {
      alert(`Unsupported file type. Allowed: ${allowed.join(", ")}`);
      return;
    }
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch(`${API}/upload`, { method: "POST", body: formData });
      const data = await res.json();
      if (res.ok) {
        setMessages((prev) => [...prev, {
          role: "system",
          text: `✅ "${data.filename}" uploaded and indexed successfully.`
        }]);
        fetchDocuments();
      } else {
        setMessages((prev) => [...prev, {
          role: "system",
          text: `❌ Upload failed: ${data.detail}`
        }]);
      }
    } catch {
      setMessages((prev) => [...prev, { role: "system", text: "❌ Upload failed — is the backend running?" }]);
    }
    setUploading(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) uploadFile(file);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) uploadFile(file);
  };

  const askQuestion = async () => {
    if (!question.trim() || loading) return;
    const q = question.trim();
    setQuestion("");
    setMessages((prev) => [...prev, { role: "user", text: q }]);
    setLoading(true);
    try {
      const res = await fetch(`${API}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, {
        role: "assistant",
        text: data.answer,
        sources: data.sources || []
      }]);
    } catch {
      setMessages((prev) => [...prev, {
        role: "assistant",
        text: "❌ Error — is the backend running?",
        sources: []
      }]);
    }
    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo">📄 Papermind</div>
          <div className="tagline">Research Paper Q&A</div>
        </div>

        <div
          className={`upload-zone ${dragOver ? "drag-over" : ""} ${uploading ? "uploading" : ""}`}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input ref={fileInputRef} type="file" accept=".pdf,.docx,.md,.txt" onChange={handleFileSelect} hidden />
          {uploading ? (
            <div className="upload-text">⏳ Indexing...</div>
          ) : (
            <>
              <div className="upload-icon">⬆️</div>
              <div className="upload-text">Drop a file or click to upload</div>
              <div className="upload-hint">PDF, DOCX, MD, TXT</div>
            </>
          )}
        </div>

        <div className="doc-section">
          <div className="doc-section-title">Indexed Documents</div>
          {documents.length === 0 ? (
            <div className="no-docs">No documents yet</div>
          ) : (
            documents.map((doc, i) => (
              <div key={i} className="doc-item">
                <span className="doc-icon">📄</span>
                <span className="doc-name">{doc}</span>
              </div>
            ))
          )}
        </div>
      </aside>

      <main className="chat">
        <div className="chat-messages">
          {messages.length === 0 && (
            <div className="empty-state">
              <div className="empty-icon">🔬</div>
              <div className="empty-title">Ask anything about your papers</div>
              <div className="empty-sub">Upload a document on the left, then ask a question</div>
            </div>
          )}
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              {msg.role === "user" && <div className="msg-label">You</div>}
              {msg.role === "assistant" && <div className="msg-label">Papermind</div>}
              <div className="msg-text">{msg.text}</div>
              {msg.sources && msg.sources.length > 0 && (
                <div className="sources">
                  {msg.sources.map((s, j) => (
                    <div key={j} className="source-chip">
                      [{s.index}] {s.filename} — Page {s.page}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <div className="msg-label">Papermind</div>
              <div className="msg-text typing">Thinking<span>...</span></div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <div className="input-bar">
          <textarea
            className="input-box"
            placeholder="Ask a question about your documents..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
          />
          <button className="send-btn" onClick={askQuestion} disabled={loading || !question.trim()}>
            {loading ? "⏳" : "➤"}
          </button>
        </div>
      </main>
    </div>
  );
}
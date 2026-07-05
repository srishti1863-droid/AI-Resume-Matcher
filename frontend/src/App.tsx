import { useState } from "react";
import axios from "axios";
import jsPDF from "jspdf";
import "./App.css";

interface MatchResult {
  ats_score: number;
  match_percentage: number;
  matched_skills: string[];
  missing_skills: string[];
  suggestions: string[];
  ai_feedback: string;
}

function App() {
  const [resume, setResume] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState<MatchResult | null>(null);
  const [loading, setLoading] = useState(false);

  // ✅ Your deployed backend
  const API_URL = "https://ai-resume-matcher-dmqb.onrender.com";

  const handleAnalyze = async () => {
    if (!resume) {
      alert("Please upload a resume.");
      return;
    }

    if (!jobDescription.trim()) {
      alert("Please enter a job description.");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", resume);

      await axios.post(
        `${API_URL}/upload-resume`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const response = await axios.post(
        `${API_URL}/match-resume`,
        {
          description: jobDescription,
        }
      );

      setResult(response.data);
    } catch (error: any) {
      console.error(error);

      if (error.response) {
        alert(JSON.stringify(error.response.data));
      } else {
        alert("Unable to connect to backend.");
      }
    }

    setLoading(false);
  };

  const downloadReport = () => {
    if (!result) return;

    const doc = new jsPDF();

    doc.setFontSize(20);
    doc.text("AI Resume Matcher Report", 20, 20);

    doc.setFontSize(14);
    doc.text(`ATS Score: ${result.ats_score}/100`, 20, 40);
    doc.text(`Job Match: ${result.match_percentage}%`, 20, 50);

    let y = 70;

    doc.text("Matched Skills:", 20, y);
    y += 10;

    result.matched_skills.forEach((skill) => {
      doc.text("• " + skill, 25, y);
      y += 8;
    });

    y += 5;

    doc.text("Missing Skills:", 20, y);
    y += 10;

    result.missing_skills.forEach((skill) => {
      doc.text("• " + skill, 25, y);
      y += 8;
    });

    y += 5;

    doc.text("Resume Feedback:", 20, y);
    y += 10;

    result.suggestions.forEach((item) => {
      doc.text("• " + item, 25, y);
      y += 8;
    });

    y += 5;

    doc.text("AI Review:", 20, y);
    y += 10;

    const lines = doc.splitTextToSize(result.ai_feedback, 170);
    doc.text(lines, 20, y);

    doc.save("AI_Resume_Report.pdf");
  };

  return (
    <div className="container">
      <h1>🤖 AI Resume Matcher</h1>

      <p className="subtitle">
        Upload your resume and compare it with any job description using AI.
      </p>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => {
          if (e.target.files) {
            setResume(e.target.files[0]);
          }
        }}
      />

      <textarea
        rows={8}
        placeholder="Paste Job Description Here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />

      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? "⏳ Analyzing..." : "🚀 Analyze Resume"}
      </button>

      {result && (
        <div className="dashboard">
          <div className="score-section">
            <div className="score-card">
              <h2>🎯 ATS Score</h2>

              <div
                className="circle"
                style={{
                  background: `conic-gradient(
                    #2563eb ${result.ats_score * 3.6}deg,
                    #d1d5db 0deg
                  )`,
                }}
              >
                <div className="circle-inner">
                  <span>{result.ats_score}</span>
                </div>
              </div>
            </div>

            <div className="score-card">
              <h2>📈 Job Match</h2>

              <div className="score green">
                {result.match_percentage}%
              </div>

              <div className="progress">
                <div
                  className="progress-fill green-fill"
                  style={{
                    width: `${result.match_percentage}%`,
                  }}
                ></div>
              </div>
            </div>
          </div>

          <div className="cards">
            <div className="card">
              <h3>✅ Matched Skills</h3>

              <ul>
                {result.matched_skills.map((skill, index) => (
                  <li key={index}>{skill}</li>
                ))}
              </ul>
            </div>

            <div className="card">
              <h3>❌ Missing Skills</h3>

              <ul>
                {result.missing_skills.map((skill, index) => (
                  <li key={index}>{skill}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="card feedback-card">
            <h3>💡 Resume Feedback</h3>

            <ul>
              {result.suggestions.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>

          <div className="card feedback-card">
            <h3>🤖 AI Resume Review</h3>

            <div className="ai-review">
              {result.ai_feedback}
            </div>
          </div>

          <button
            onClick={downloadReport}
            style={{ marginTop: "25px" }}
          >
            📄 Download PDF Report
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
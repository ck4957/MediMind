"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

// Types
type WebSocketMessage = {
  type: string;
  data: any;
};

// Components (Placeholders for now, will implement shortly)
// import RiskGauge from './components/RiskGauge';
// import LiveFeed from './components/LiveFeed';
// import PatientDetails from './components/PatientDetails';

export default function Home() {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const [currentPatient, setCurrentPatient] = useState<any>(null);
  const [riskScore, setRiskScore] = useState(0);

  useEffect(() => {
    // Connect to WebSocket
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => {
      console.log("Connected to WebSocket");
    };

    ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        setMessages((prev) => [message, ...prev].slice(0, 50)); // Keep last 50

        // Simple logic to update state based on message type
        if (message.type === "patient-profiles-stream") {
          setCurrentPatient(message.data);
        }

        // Mock risk calculation update - purely for demo visualization
        // In real app, this comes from 'risk-predictions-stream'
        if (message.type === "risk-predictions-stream") {
          // setRiskScore(message.data.score);
        }
      } catch (e) {
        console.error("Error parsing message", e);
      }
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  return (
    <main className={styles.main}>
      <header className={styles.header}>
        <div className={styles.logo}>
          <span className={styles.logoIcon}>⚕️</span>
          <h1>
            MediMind <span className={styles.subTitle}>Oncology Real-Time</span>
          </h1>
        </div>
        <div className={styles.status}>
          <span
            className={`${styles.indicator} ${
              socket?.readyState === 1 ? styles.online : styles.offline
            }`}
          ></span>
          {socket?.readyState === 1 ? "System Online" : "Connecting..."}
        </div>
      </header>

      <div className={styles.grid}>
        {/* Left Column: Patient Profile & Vitals */}
        <div className={styles.colLeft}>
          <div className={styles.card}>
            <h2>Patient Profile</h2>
            {currentPatient ? (
              <div className={styles.patientInfo}>
                <div className={styles.row}>
                  <label>ID</label>
                  <span>{currentPatient.patient_id}</span>
                </div>
                <div className={styles.row}>
                  <label>Age/Sex</label>
                  <span>
                    {currentPatient.demographics.age} /{" "}
                    {currentPatient.demographics.gender}
                  </span>
                </div>
                <div className={styles.row}>
                  <label>Smoking Status</label>
                  <span
                    className={
                      currentPatient.lifestyle_factors.active_smoker
                        ? styles.alert
                        : styles.normal
                    }
                  >
                    {currentPatient.lifestyle_factors.smoking_history}
                  </span>
                </div>
              </div>
            ) : (
              <div className={styles.loading}>Waiting for patient data...</div>
            )}
          </div>

          <div className={styles.card}>
            <h2>Risk Assessment</h2>
            <div className={styles.gaugePlaceholder}>
              <div
                className={styles.riskCircle}
                style={{
                  borderColor: currentPatient?.lifestyle_factors?.active_smoker
                    ? "var(--risk-high)"
                    : "var(--risk-low)",
                }}
              >
                <span className={styles.riskValue}>
                  {currentPatient?.lifestyle_factors?.active_smoker
                    ? "HIGH"
                    : "LOW"}
                </span>
                <span className={styles.riskLabel}>Predicted Risk</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Live Data Feed */}
        <div className={styles.colRight}>
          <div className={styles.cardFull}>
            <h2>Live Clinical Event Stream</h2>
            <div className={styles.feed}>
              {messages.map((msg, i) => (
                <div key={i} className={styles.feedItem} data-type={msg.type}>
                  <div className={styles.feedHeader}>
                    <span className={styles.feedType}>
                      {msg.type
                        .replace("-stream", "")
                        .replace("_", " ")
                        .toUpperCase()}
                    </span>
                    <span className={styles.feedTime}>
                      {new Date().toLocaleTimeString()}
                    </span>
                  </div>
                  <pre className={styles.feedContent}>
                    {JSON.stringify(msg.data, null, 2)}
                  </pre>
                </div>
              ))}
              {messages.length === 0 && (
                <div className={styles.emptyFeed}>
                  Waiting for Kafka streams...
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

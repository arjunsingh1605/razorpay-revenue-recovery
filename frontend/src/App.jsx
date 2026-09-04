import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const payments = [
  {
    id: "TEST001",
    amount: 2499,
    reason: "Network Error",
    attempts: 1,
    successes: 6,
  },
  {
    id: "TEST002",
    amount: 8999,
    reason: "Card Declined",
    attempts: 2,
    successes: 4,
  },
  {
    id: "TEST003",
    amount: 75000,
    reason: "Multiple Failures",
    attempts: 3,
    successes: 1,
  },
  {
    id: "TEST004",
    amount: 1499,
    reason: "Timeout",
    attempts: 1,
    successes: 8,
  },
  {
    id: "TEST005",
    amount: 4999,
    reason: "Insufficient Funds",
    attempts: 1,
    successes: 3,
  },
];

function App() {
  const [paymentId, setPaymentId] = useState("TEST001");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzePayment = async () => {
    if (!paymentId.trim()) {
      setError("Please enter a payment ID.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `${API_URL}/api/recovery/analyze`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            payment_id: paymentId.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to analyze payment."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message || "Could not connect to the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const verifyPayment = async () => {
    if (!result?.razorpay_payment_link_id) {
      setError("No Razorpay payment link found.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/api/recovery/verify/${result.razorpay_payment_link_id}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to verify payment."
        );
      }

      setResult((prev) => ({
        ...prev,
        status:
          data.status === "paid"
            ? "RECOVERED"
            : data.status,
        recovered_amount: data.amount_paid || 0,
      }));
    } catch (err) {
      setError(
        err.message || "Could not verify payment."
      );
    } finally {
      setLoading(false);
    }
  };

  const getActionClass = (action) => {
    if (action === "RETRY") return "action retry";

    if (action === "PAYMENT_LINK") {
      return "action payment-link";
    }

    if (action === "ESCALATE") {
      return "action escalate";
    }

    return "action";
  };

  return (
    <div className="app">

      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-title">
          Revenue Recovery
        </div>
      </aside>

      {/* MAIN */}
      <main className="main">

        {/* HEADER */}
        <header className="topbar">
          <div>
            <h1>Revenue Recovery</h1>

            <p>
              Review failed payments and initiate recovery
            </p>
          </div>
        </header>

        {/* PAYMENT ANALYSIS */}
        <section className="panel analyzer">

          <div className="panel-title">
            <div>
              <h2>Payment Analysis</h2>

              <p>
                Review a failed payment and determine the appropriate recovery action.
              </p>
            </div>
          </div>

          <div className="search-row">

            <input
              type="text"
              value={paymentId}
              onChange={(e) =>
                setPaymentId(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  analyzePayment();
                }
              }}
              placeholder="Enter payment ID"
            />

            <button
              onClick={analyzePayment}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                <>
                  Analyze Payment
                  <span>→</span>
                </>
              )}
            </button>

          </div>

          {error && (
            <div className="error-box">
              <strong>Error:</strong> {error}
            </div>
          )}

        </section>

        {/* FAILED PAYMENTS */}
        <section className="panel">

          <div className="panel-title">

            <div>
              <h2>Failed Payments</h2>

              <p>
                Select a payment to analyze
              </p>
            </div>

            <span className="count">
              {payments.length} payments
            </span>

          </div>

          <div className="table-wrapper">

            <table>

              <thead>
                <tr>
                  <th>Payment ID</th>
                  <th>Amount</th>
                  <th>Failure Reason</th>
                  <th>Attempts</th>
                  <th>AI Action</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>

                {payments.map((payment) => (

                  <tr
                    key={payment.id}
                    onClick={() => {
                      setPaymentId(payment.id);
                    }}
                    style={{ cursor: "pointer" }}
                  >

                    <td>
                      <strong>
                        {payment.id}
                      </strong>
                    </td>

                    <td>
                      ₹
                      {payment.amount.toLocaleString(
                        "en-IN"
                      )}
                    </td>

                    <td>
                      <span className="failure">
                        {payment.reason}
                      </span>
                    </td>

                    <td>
                      {payment.attempts}
                    </td>

                    <td>

                      <span
                        className={getActionClass(
                          result?.payment_id === payment.id
                            ? result.action
                            : ""
                        )}
                      >
                        {result?.payment_id === payment.id
                          ? result.action
                          : "—"}
                      </span>

                    </td>

                    <td>

                      {result?.payment_id === payment.id ? (

                        <span className="success-badge">
                          <span></span>
                          {result.status}
                        </span>

                      ) : (

                        <span>
                          Pending
                        </span>

                      )}

                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        </section>

        {/* RECOVERY RESULT */}
        {result && !result.error && (

          <section className="panel decision-panel">

            <div className="panel-title">

              <div>
                <h2>Recovery Decision</h2>

                <p>
                  Recommended action for this payment
                </p>
              </div>

              <span
                className={getActionClass(result.action)}
              >
                {result.action}
              </span>

            </div>

            <div className="decision-grid">

              <div className="detail">
                <span>Payment ID</span>

                <strong>
                  {result.payment_id || paymentId}
                </strong>
              </div>

              <div className="detail">
                <span>Action</span>

                <strong>
                  {result.action}
                </strong>
              </div>

              <div className="detail">
                <span>Confidence</span>

                <strong>
                  {result.confidence !== undefined
                    ? `${Math.round(
                        result.confidence * 100
                      )}%`
                    : "N/A"}
                </strong>
              </div>

              <div className="detail">
                <span>Status</span>

                <strong className="green-text">
                  {result.status || "SUCCESS"}
                </strong>
              </div>

              <div className="detail wide">

                <span>
                  Reason
                </span>

                <strong className="reason">
                  {result.reason ||
                    "Recovery action selected based on payment history and failure reason."}
                </strong>

              </div>

              <div className="detail">

                <span>
                  Recovered Amount
                </span>

                <strong className="amount">
                  ₹
                  {(result.recovered_amount || 0)
                    .toLocaleString("en-IN")}
                </strong>

              </div>

              {/* RAZORPAY */}
              {result.payment_link && (

                <div className="detail wide">

                  <span>
                    Razorpay Recovery
                  </span>

                  <div>

                    <a
                      href={result.payment_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="payment-link-button"
                    >
                      Open Payment Link →
                    </a>

                    <button
                      onClick={verifyPayment}
                      disabled={loading}
                      className="payment-link-button"
                    >
                      {loading
                        ? "Verifying..."
                        : "Verify Payment ✓"}
                    </button>

                  </div>

                </div>

              )}

            </div>

          </section>

        )}

        {/* FOOTER */}
        <footer>
          <span>
            Razorpay Revenue Recovery
          </span>

          <span>
            AI Agent • Guardrails • Audit Logging
          </span>
        </footer>

      </main>

    </div>
  );
}

export default App;
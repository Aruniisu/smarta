import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [user, setUser] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await fetch('http://localhost:5000/api/user');
        const data = await res.json();
        if(data) {
          setUser(data);
          const histRes = await fetch('http://localhost:5000/api/history');
          const histData = await histRes.json();
          setHistory(histData);
        }
      } catch (e) { console.log("Not logged in"); }
    };
    fetchUser();
  }, []);

  const handleDeploy = async () => {
    if(!url) return alert("Please paste a URL first!");
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch('http://localhost:5000/api/deploy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      const data = await res.json();
      setResult(data.link);
    } catch (err) {
      alert("Deployment failed!");
    }
    setLoading(false);
  };

  return (
    <div className="aegis-app">
      <nav className="aegis-nav">
        <div className="nav-logo">🤖 Smart Devops <span>Assistant</span></div>
        <div className="nav-actions">
          {user ? (
            <div className="user-pill">
              <img src={user.picture} alt="profile" />
              <span>{user.name}</span>
              <button className="logout-btn" onClick={() => window.location.href='http://localhost:5000/api/logout'}>Logout</button>
            </div>
          ) : (
            <button className="login-btn" onClick={() => window.location.href='http://localhost:5000/api/login'}>
              Sign in with Google
            </button>
          )}
        </div>
      </nav>

      <div className="aegis-content">
        <div className="glass-card">
          <div className="hero-text">
            <h2>Smart Deployment Hub</h2>
            <p>Deploy your GitHub projects to the cloud in seconds with AI automation.</p>
          </div>

          <div className="input-container">
            <input 
              type="text" 
              placeholder="Paste GitHub Repo URL here..." 
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <button className="deploy-btn" onClick={handleDeploy} disabled={loading}>
              {loading ? "Working..." : "Deploy Now"}
            </button>
          </div>

          {loading && (
            <div className="loader-overlay">
              <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbmZ6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6JmFjdD1n/3o7TKMGpxx66B6pDsk/giphy.gif" alt="Robot working" />
              <p>Devops Agent is building your environment...</p>
            </div>
          )}

          {result && (
            <div className="success-banner">
              <div className="confetti">🎉</div>
              <div>
                <h3>Your App is Live!</h3>
                <a href={result} target="_blank" rel="noreferrer">{result}</a>
              </div>
            </div>
          )}
        </div>

        {user && history.length > 0 && (
          <div className="history-drawer">
            <h3>Recent Deployments</h3>
            <div className="history-grid">
              {history.map((item, i) => (
                <div key={i} className="history-card">
                  <div className="hist-meta">
                    <span className="type-tag">{item.type || 'Web'}</span>
                    <p>{item.url.split('/').pop()}</p>
                  </div>
                  <a href={item.live_link} target="_blank" rel="noreferrer" className="visit-link">Open App</a>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
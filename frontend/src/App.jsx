import { useState } from "react";
import { getRecommendations } from "./services/api";
import "./App.css";

function App() {
  const [userName, setUserName] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);

  async function handleRecommend() {
    if (!userName.trim()) {
      setError("Please enter a user name.");
      return;
    }

    setLoading(true);
    setError("");
    setHasSearched(true);

    try {
      const data = await getRecommendations(userName.trim());
      setRecommendations(data.recommendations);
    } catch (err) {
      setRecommendations([]);
      setError(
        "Unable to load recommendations. Please check that the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <p className="eyebrow">GRAPH-POWERED DISCOVERY</p>

          <h1>CineGraph AI</h1>

          <p className="subtitle">
            Discover movies through your watch history and shared genres.
          </p>
        </div>
      </header>

      <main className="container">
        <section className="search-panel">
          <label htmlFor="userName">Who are you?</label>

          <div className="search-row">
            <input
              id="userName"
              value={userName}
              onChange={(event) => setUserName(event.target.value)}
              placeholder="Enter your name"
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  handleRecommend();
                }
              }}
            />

            <button
              onClick={handleRecommend}
              disabled={loading}
            >
              {loading ? "Finding..." : "Recommend →"}
            </button>
          </div>
        </section>

        {/* Error */}
        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="state">
            Finding movies for you...
          </div>
        )}

        {/* Initial state */}
        {!loading && !error && !hasSearched && (
          <div className="empty-state">
            <h2>Ready to discover?</h2>

            <p>
              Enter a user name and we'll find movies based on shared genres.
            </p>
          </div>
        )}

        {/* No recommendations */}
        {!loading &&
          !error &&
          hasSearched &&
          recommendations.length === 0 && (
            <div className="empty-state">
              <h2>No recommendations found</h2>

              <p>
                We couldn't find any recommendations for "{userName}".
                Try another user.
              </p>
            </div>
          )}

        {/* Recommendations */}
        {!loading && recommendations.length > 0 && (
          <section className="results">
            <div className="results-header">
              <div>
                <p className="eyebrow">PERSONALIZED FOR</p>

                <h2>{userName}</h2>
              </div>

              <span className="result-count">
                {recommendations.length} recommendation
                {recommendations.length !== 1 ? "s" : ""}
              </span>
            </div>

            <div className="recommendation-grid">
              {recommendations.map((movie) => (
                <article
                  className="recommendation-card"
                  key={movie.recommendation}
                >
                  <div className="movie-icon">
                    🎬
                  </div>

                  <div className="movie-content">
                    <h3>{movie.recommendation}</h3>

                    <div className="score">
                      <span>Match score</span>

                      <strong>
                        {movie.match_count}
                      </strong>
                    </div>

                    <div className="genres">
                      {movie.matching_genres.map((genre) => (
                        <span key={genre}>
                          {genre}
                        </span>
                      ))}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
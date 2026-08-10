const API_BASE_URL = "https://cinegraph-ai-5.onrender.com";

export async function getRecommendations(userName) {
  const response = await fetch(
    `${API_BASE_URL}/recommendations/${encodeURIComponent(userName)}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch recommendations");
  }

  return response.json();
}
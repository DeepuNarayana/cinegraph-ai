const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function getRecommendations(userName) {
  const response = await fetch(
    `${API_BASE_URL}/recommendations/${encodeURIComponent(userName)}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch recommendations");
  }

  return response.json();
}
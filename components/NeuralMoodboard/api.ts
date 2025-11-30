// API function for NeuralMoodboard
// Replace the URL with your actual backend endpoint

export async function generateMoodboard(text: string, mood: string, file: File | null): Promise<any> {
  const formData = new FormData();
  formData.append("text", text);
  formData.append("mood", mood);
  if (file) {
    formData.append("file", file);
  }

  const response = await fetch("/api/moodboard/generate", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to generate moodboard");
  }

  return await response.json();
}

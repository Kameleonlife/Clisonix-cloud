export async function generateMoodboard(text: string, mood: string, file: File | null) {
  const form = new FormData();
  form.append("text", text);
  form.append("mood", mood);
  if (file) form.append("file", file);

  const res = await fetch("http://localhost:8000/moodboard/generate", {
    method: "POST",
    body: form,
  });

  if (!res.ok) throw new Error("Moodboard generation failed");
  return await res.json();
}

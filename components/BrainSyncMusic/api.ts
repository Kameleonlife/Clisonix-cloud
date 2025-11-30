// API function for BrainSyncMusic
// Replace the URL with your actual backend endpoint

export async function generateBrainSync(file: File, mode: string): Promise<Blob> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("mode", mode);

  const response = await fetch("/api/music/brainsync", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to generate BrainSync music");
  }

  return await response.blob();
}

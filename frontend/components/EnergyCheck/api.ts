export async function runEnergyCheck(audioBlob: Blob) {
  const file = new File([audioBlob], "recording.webm", {
    type: "audio/webm",
  });
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch("http://localhost:8000/energy/check", {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Energy check failed");
  return await res.json();
}

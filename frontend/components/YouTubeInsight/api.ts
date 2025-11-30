export async function fetchYouTubeInsight(videoId: string) {
  const res = await fetch(
    "http://localhost:8000/youtube/insight?video_id=" + videoId,
    { method: "GET" }
  );
  if (!res.ok) throw new Error("YouTube insight error");
  return await res.json();
}

type Run = { run_id: string; created_at?: string; schema_version?: string }

async function getRuns(): Promise<Run[]> {
  const r = await fetch("/api/runs", { headers: { accept: "application/json" } })
  if (!r.ok) throw new Error(String(r.status))
  return await r.json()
}

async function boot(): Promise<void> {
  const root = document.getElementById("app")
  if (!root) return
  const runs = await getRuns().catch(() => [])
  root.textContent = runs.length ? `runs:${runs.length}` : "no runs"
}

boot()

import React, { useMemo, useState } from "react"

type Artifact = {
  relpath: string
  sha256: string
  role: string
  size_bytes: number
}

type Manifest = {
  run_id: string
  created_utc: string
  artifacts: {
    root_hash: string
    items: Artifact[]
  }
}

function humanBytes(n: number): string {
  const units = ["B", "KB", "MB", "GB"]
  let v = n
  let i = 0
  while (v >= 1024 && i < units.length - 1) {
    v = v / 1024
    i += 1
  }
  return `${v.toFixed(i === 0 ? 0 : 1)} ${units[i]}`
}

export default function App(): JSX.Element {
  const [manifest, setManifest] = useState<Manifest | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [filter, setFilter] = useState<string>("")

  const onFile = async (f: File | null) => {
    setError(null)
    setManifest(null)
    if (!f) return
    try {
      const txt = await f.text()
      const j = JSON.parse(txt) as Manifest
      if (!j.artifacts || !j.artifacts.items) throw new Error("Not a run_manifest.json")
      setManifest(j)
    } catch (e) {
      setError(String(e))
    }
  }

  const rows = useMemo(() => {
    if (!manifest) return []
    const q = filter.trim().toLowerCase()
    const base = manifest.artifacts.items
    if (!q) return base
    return base.filter(a => a.relpath.toLowerCase().includes(q) || a.role.toLowerCase().includes(q))
  }, [manifest, filter])

  const totals = useMemo(() => {
    if (!manifest) return { count: 0, bytes: 0 }
    const bytes = manifest.artifacts.items.reduce((acc, a) => acc + (a.size_bytes || 0), 0)
    return { count: manifest.artifacts.items.length, bytes }
  }, [manifest])

  return (
    <div style={{ fontFamily: "system-ui", margin: "24px", maxWidth: 1100 }}>
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between" }}>
        <div>
          <div style={{ fontSize: 22, fontWeight: 700 }}>omphalOS run inspector</div>
          <div style={{ opacity: 0.7, marginTop: 4 }}>Load a run_manifest.json and inspect declared artifacts</div>
        </div>
        <div>
          <input
            type="file"
            accept="application/json"
            onChange={e => onFile(e.target.files?.[0] ?? null)}
          />
        </div>
      </div>

      {error ? (
        <div style={{ marginTop: 18, padding: 12, border: "1px solid #ddd" }}>
          <div style={{ fontWeight: 700 }}>Error</div>
          <div style={{ marginTop: 8, whiteSpace: "pre-wrap" }}>{error}</div>
        </div>
      ) : null}

      {manifest ? (
        <div style={{ marginTop: 18, padding: 12, border: "1px solid #ddd" }}>
          <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
            <div><span style={{ opacity: 0.7 }}>Run</span> <span style={{ fontWeight: 700 }}>{manifest.run_id}</span></div>
            <div><span style={{ opacity: 0.7 }}>Created</span> <span style={{ fontWeight: 700 }}>{manifest.created_utc}</span></div>
            <div><span style={{ opacity: 0.7 }}>Payload root</span> <span style={{ fontFamily: "ui-monospace", fontWeight: 700 }}>{manifest.artifacts.root_hash}</span></div>
            <div><span style={{ opacity: 0.7 }}>Artifacts</span> <span style={{ fontWeight: 700 }}>{totals.count}</span></div>
            <div><span style={{ opacity: 0.7 }}>Bytes</span> <span style={{ fontWeight: 700 }}>{humanBytes(totals.bytes)}</span></div>
          </div>

          <div style={{ marginTop: 12, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <input
              value={filter}
              onChange={e => setFilter(e.target.value)}
              placeholder="Filter by path or role"
              style={{ width: "55%", padding: 8 }}
            />
            <div style={{ opacity: 0.7, fontSize: 13 }}>Showing {rows.length} rows</div>
          </div>

          <div style={{ marginTop: 12, overflowX: "auto" }}>
            <table style={{ borderCollapse: "collapse", width: "100%" }}>
              <thead>
                <tr>
                  <th style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: 8 }}>relpath</th>
                  <th style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: 8 }}>role</th>
                  <th style={{ textAlign: "right", borderBottom: "1px solid #ddd", padding: 8 }}>size</th>
                  <th style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: 8 }}>sha256</th>
                </tr>
              </thead>
              <tbody>
                {rows.map(a => (
                  <tr key={a.relpath}>
                    <td style={{ padding: 8, borderBottom: "1px solid #f0f0f0", fontFamily: "ui-monospace" }}>{a.relpath}</td>
                    <td style={{ padding: 8, borderBottom: "1px solid #f0f0f0" }}>{a.role}</td>
                    <td style={{ padding: 8, borderBottom: "1px solid #f0f0f0", textAlign: "right" }}>{humanBytes(a.size_bytes)}</td>
                    <td style={{ padding: 8, borderBottom: "1px solid #f0f0f0", fontFamily: "ui-monospace" }}>{a.sha256}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div style={{ marginTop: 18, padding: 12, border: "1px solid #ddd" }}>
          <div style={{ fontWeight: 700 }}>Load a manifest</div>
          <div style={{ marginTop: 8, opacity: 0.8 }}>
            Select a run_manifest.json from a run directory.
          </div>
        </div>
      )}
    </div>
  )
}

package main

import (
  "crypto/sha256"
  "encoding/hex"
  "encoding/json"
  "fmt"
  "io"
  "os"
  "path/filepath"
)

type ArtifactFile struct {
  Path string `json:"path"`
  Sha256 string `json:"sha256"`
}

type Manifest struct {
  Artifacts struct {
    Files []ArtifactFile `json:"files"`
    ControlFiles []ArtifactFile `json:"control_files"`
  } `json:"artifacts"`
}

func fileHash(p string) (string, error) {
  f, err := os.Open(p)
  if err != nil { return "", err }
  defer f.Close()
  h := sha256.New()
  if _, err := io.Copy(h, f); err != nil { return "", err }
  return hex.EncodeToString(h.Sum(nil)), nil
}

func main() {
  if len(os.Args) < 2 {
    fmt.Println("usage: omphalos-verify <run_dir>")
    os.Exit(2)
  }
  runDir := os.Args[1]
  mfPath := filepath.Join(runDir, "run_manifest.json")
  b, err := os.ReadFile(mfPath)
  if err != nil { panic(err) }
  var m Manifest
  if err := json.Unmarshal(b, &m); err != nil { panic(err) }

  files := append([]ArtifactFile{}, m.Artifacts.Files...)
  files = append(files, m.Artifacts.ControlFiles...)
  bad := 0
  for _, af := range files {
    fp := filepath.Join(runDir, af.Path)
    got, err := fileHash(fp)
    if err != nil {
      fmt.Printf("missing %s
", af.Path)
      bad++
      continue
    }
    if got != af.Sha256 {
      fmt.Printf("mismatch %s
", af.Path)
      bad++
    }
  }
  if bad > 0 {
    fmt.Printf("fail %d
", bad)
    os.Exit(1)
  }
  fmt.Println("pass")
}

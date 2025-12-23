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

type Artifact struct {
	Relpath   string `json:"relpath"`
	Sha256    string `json:"sha256"`
	Role      string `json:"role"`
	SizeBytes int64  `json:"size_bytes"`
}

type Artifacts struct {
	RootHash string     `json:"root_hash"`
	Items    []Artifact `json:"items"`
}

type Manifest struct {
	RunID     string    `json:"run_id"`
	CreatedUTC string   `json:"created_utc"`
	Artifacts Artifacts `json:"artifacts"`
}

func fileSHA256(path string) (string, int64, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", 0, err
	}
	defer f.Close()
	h := sha256.New()
	n, err := io.Copy(h, f)
	if err != nil {
		return "", 0, err
	}
	sum := hex.EncodeToString(h.Sum(nil))
	return sum, n, nil
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("usage: verify <run_dir>")
		os.Exit(2)
	}
	runDir := os.Args[1]
	manifestPath := filepath.Join(runDir, "run_manifest.json")
	b, err := os.ReadFile(manifestPath)
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
	}
	var m Manifest
	if err := json.Unmarshal(b, &m); err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
	}
	fail := 0
	for _, a := range m.Artifacts.Items {
		p := filepath.Join(runDir, a.Relpath)
		sum, n, err := fileSHA256(p)
		if err != nil {
			fmt.Printf("missing %s %s
", a.Role, a.Relpath)
			fail += 1
			continue
		}
		if a.SizeBytes != 0 && n != a.SizeBytes {
			fmt.Printf("size_mismatch %s %s expected=%d got=%d
", a.Role, a.Relpath, a.SizeBytes, n)
			fail += 1
		}
		if a.Sha256 != "" && sum != a.Sha256 {
			fmt.Printf("sha_mismatch %s %s expected=%s got=%s
", a.Role, a.Relpath, a.Sha256, sum)
			fail += 1
		}
	}
	if fail > 0 {
		fmt.Printf("status FAIL mismatches=%d
", fail)
		os.Exit(1)
	}
	fmt.Println("status PASS")
}

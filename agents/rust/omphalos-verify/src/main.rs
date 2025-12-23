use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::fs::File;
use std::io::Read;
use std::path::Path;

#[derive(Deserialize)]
struct ArtifactFile {
    path: String,
    sha256: String,
}

#[derive(Deserialize)]
struct Artifacts {
    files: Vec<ArtifactFile>,
    control_files: Vec<ArtifactFile>,
}

#[derive(Deserialize)]
struct Manifest {
    artifacts: Artifacts,
}

fn hash_file(p: &Path) -> Result<String, String> {
    let mut f = File::open(p).map_err(|_| "open_failed".to_string())?;
    let mut h = Sha256::new();
    let mut buf = [0u8; 8192];
    loop {
        let n = f.read(&mut buf).map_err(|_| "read_failed".to_string())?;
        if n == 0 { break; }
        h.update(&buf[..n]);
    }
    Ok(format!("{:x}", h.finalize()))
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("usage: omphalos-verify <run_dir>");
        std::process::exit(2);
    }
    let run_dir = Path::new(&args[1]);
    let mf_path = run_dir.join("run_manifest.json");
    let mf_text = std::fs::read_to_string(&mf_path).expect("manifest_read");
    let mf: Manifest = serde_json::from_str(&mf_text).expect("manifest_parse");

    let mut files = Vec::new();
    for f in mf.artifacts.files.iter() { files.push(f); }
    for f in mf.artifacts.control_files.iter() { files.push(f); }

    let mut bad = 0;
    for af in files {
        let fp = run_dir.join(&af.path);
        match hash_file(&fp) {
            Ok(got) => {
                if got != af.sha256 {
                    eprintln!("mismatch {}", af.path);
                    bad += 1;
                }
            }
            Err(_) => {
                eprintln!("missing {}", af.path);
                bad += 1;
            }
        }
    }
    if bad > 0 {
        eprintln!("fail {}", bad);
        std::process::exit(1);
    }
    println!("pass");
}

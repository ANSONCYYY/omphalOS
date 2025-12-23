use std::env;
use std::fs::File;
use std::io::{Read};
use std::path::PathBuf;

use serde::Deserialize;
use sha2::{Sha256, Digest};

#[derive(Deserialize)]
struct Artifact {
    relpath: String,
    sha256: String,
    role: String,
    size_bytes: u64,
}

#[derive(Deserialize)]
struct Artifacts {
    root_hash: String,
    items: Vec<Artifact>,
}

#[derive(Deserialize)]
struct Manifest {
    run_id: String,
    created_utc: String,
    artifacts: Artifacts,
}

fn sha256_file(path: &PathBuf) -> Result<(String, u64), String> {
    let mut f = File::open(path).map_err(|e| e.to_string())?;
    let mut hasher = Sha256::new();
    let mut buf = [0u8; 8192];
    let mut n: u64 = 0;
    loop {
        let k = f.read(&mut buf).map_err(|e| e.to_string())?;
        if k == 0 {
            break;
        }
        hasher.update(&buf[..k]);
        n += k as u64;
    }
    let sum = hasher.finalize();
    Ok((hex::encode(sum), n))
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("usage: omphalos-verify <run_dir>");
        std::process::exit(2);
    }
    let run_dir = PathBuf::from(&args[1]);
    let manifest_path = run_dir.join("run_manifest.json");
    let mut f = File::open(&manifest_path).unwrap();
    let mut s = String::new();
    f.read_to_string(&mut s).unwrap();
    let m: Manifest = serde_json::from_str(&s).unwrap();

    let mut fail: u64 = 0;
    for a in m.artifacts.items.iter() {
        let p = run_dir.join(&a.relpath);
        let res = sha256_file(&p);
        if res.is_err() {
            println!("missing {} {}", a.role, a.relpath);
            fail += 1;
            continue;
        }
        let (sum, n) = res.unwrap();
        if a.size_bytes != 0 && n != a.size_bytes {
            println!("size_mismatch {} {} expected={} got={}", a.role, a.relpath, a.size_bytes, n);
            fail += 1;
        }
        if !a.sha256.is_empty() && sum != a.sha256 {
            println!("sha_mismatch {} {} expected={} got={}", a.role, a.relpath, a.sha256, sum);
            fail += 1;
        }
    }
    if fail > 0 {
        println!("status FAIL mismatches={}", fail);
        std::process::exit(1);
    }
    println!("status PASS");
}

package omphalos.publishability

default allow = true

deny[msg] {
  some p
  input.files[p].path == path
  endswith(lower(path), ".env")
  msg := sprintf("forbidden_file:%s", [path])
}

deny[msg] {
  some p
  f := input.files[p]
  contains(lower(f.path), "secrets")
  msg := sprintf("forbidden_path:%s", [f.path])
}

allow {
  count(deny) == 0
}

package omphalos.release_gate

default pass = false

required_reports := {
  "reports/quality_report.json",
  "reports/determinism_report.json",
  "reports/publishability_report.json",
  "reports/sbom_manifest.json"
}

missing[path] {
  path := required_reports[_]
  not input.present[path]
}

pass {
  count(missing) == 0
}

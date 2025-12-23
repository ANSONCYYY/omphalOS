package omphalos.release_gate_test

import data.omphalos.release_gate

test_pass_when_reports_present {
  release_gate.pass with input as {"present": {
    "reports/quality_report.json": true,
    "reports/determinism_report.json": true,
    "reports/publishability_report.json": true,
    "reports/sbom_manifest.json": true
  }}
}

test_fail_when_missing {
  not release_gate.pass with input as {"present": {"reports/quality_report.json": true}}
}

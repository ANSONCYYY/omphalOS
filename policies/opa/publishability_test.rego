package omphalos.publishability

test_deny_secret_filename {
  deny with input as {"path": "secrets.txt", "content": ""}
}

test_allow_safe {
  allow with input as {"path": "exports/table.csv", "content": "ok"}
}

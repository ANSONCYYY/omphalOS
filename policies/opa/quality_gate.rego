package omphalos.quality

default pass = false

pass {
  input.status == "PASS"
  count(input.failures) == 0
}

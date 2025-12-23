package omphalos.publishability

default allow = true

deny[msg] {
  input.path != ""
  endswith(lower(input.path), ".env")
  msg := "dotenv file detected"
}

deny[msg] {
  input.path != ""
  contains(lower(input.path), "id_rsa")
  msg := "private key filename pattern detected"
}

deny[msg] {
  input.path != ""
  contains(lower(input.path), "secret")
  msg := "secret token filename pattern detected"
}

deny[msg] {
  input.content != ""
  re_match("AKIA[0-9A-Z]{16}", input.content)
  msg := "aws access key id pattern detected"
}

deny[msg] {
  input.content != ""
  re_match("-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----", input.content)
  msg := "private key material detected"
}

allow {
  count(deny) == 0
}

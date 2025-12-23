package omphalos.spark

final case class ParsedArgs(tradeCsv: String = "", out: String = "")

object Args {
  def parse(args: Array[String]): ParsedArgs = {
    val pairs = args.toList.grouped(2).collect { case List(k, v) => (k, v) }.toMap
    val tradeCsv = pairs.getOrElse("--trade-csv", "")
    val out = pairs.getOrElse("--out", "")
    ParsedArgs(tradeCsv = tradeCsv, out = out)
  }
}

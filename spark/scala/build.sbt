ThisBuild / scalaVersion := "2.13.14"
ThisBuild / organization := "omphalos"

lazy val root = (project in file("."))
  .settings(
    name := "omphalos-spark",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-sql" % "3.5.1" % "provided"
    )
  )

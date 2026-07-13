#!/bin/bash
DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd);
cd "$DIR"
java -Xmx16384m -classpath "$DIR:$DIR/jars/log4j-1.2.12.jar:$DIR/jars/commons-io-1.2.jar:$DIR/jars/commons-cli-1.0.jar:$DIR/jars/commons-logging-1.1.jar" org.katlas.JavaKh.JavaKh

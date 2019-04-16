#!/bin/bash
mkdir -p /tmp/bash
cp BashLexer.g4 BashParser.g4 /tmp/bash
cp tests.txt /tmp/bash
cd /tmp/bash
export CLASSPATH=".:/usr/local/lib/antlr-4.7.2-complete.jar:$CLASSPATH"
antlr4='java -jar /usr/local/lib/antlr-4.7.2-complete.jar'
$antlr4 BashLexer.g4 BashParser.g4
javac Bash*.java
#grun Bash cmd -gui

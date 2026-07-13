#!/bin/bash
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_FOLDER=$(dirname "$SCRIPT_PATH")
pushd "$SCRIPT_FOLDER" > /dev/null

CPP=g++
SRC=*.cpp
OBJ=knot-pdcode
OPT=-lm

echo -e "\033[1;34mINFO\033[0m: building knot-pdcode with g++." 1>&2
pushd ./knot-pdcode_src > /dev/null
$CPP $SRC -o $OBJ $OPT
popd > /dev/null
mv "./knot-pdcode_src/$OBJ" "./$OBJ"

popd > /dev/null

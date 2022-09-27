#!/bin/sh
cat 1.bin | curl 'http://localhost:8123/?format_schema=test:CapnProto&query=INSERT%20INTO%20capnproto_input%20FORMAT%20CapnProto' --data-binary @-

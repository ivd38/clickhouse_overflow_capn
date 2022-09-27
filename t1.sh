#!/usr/bin/env bash

./clickhouse-client -q "DROP TABLE IF EXISTS capnproto_input"
./clickhouse-client -q "CREATE TABLE capnproto_input
(
    number UInt64,
    string String,
    nestedone_nestednumber UInt64,
    nestedone_nestednestedone_nestednestednumber UInt64,
    nestedone_nestednestedtwo_nestednestedtext String,
    nestedtwo_nestednestedtwo_nestednestedtext String,
    nestedtwo_nestednestedone_nestednestednumber UInt64,
    nestedtwo_nestedtext String
) ENGINE = Memory"

# uncomment to repro with clickhouse-client
#cat 1.bin | ./clickhouse-client --stacktrace --format_schema="./test:CapnProto" --query="INSERT INTO capnproto_input FORMAT CapnProto";

#./programs/clickhouse-client -q "SELECT * FROM capnproto_input"

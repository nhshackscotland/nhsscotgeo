#!/usr/bin/env bash
# Export all tables in a MDB file to individual CSV files
# Requires MDB Tools http://mdbtools.sourceforge.net/

OUTDIR="exported"
MDB="Website content.mdb"

TABLES=`mdb-tables -1 "$MDB"`
IFS=$'\n'

mkdir -p "$OUTDIR"

for t in $TABLES; do
	CSV="$OUTDIR/$t.csv"
	echo Exporting "$t" to "$CSV"
	mdb-export "$MDB" "$t" > "$CSV"
done


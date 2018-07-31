#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER bitcoinmonitor PASSWORD 'bitcoinmonitor'; 
    CREATE DATABASE bitcoinmonitor;
    GRANT ALL PRIVILEGES ON DATABASE bitcoinmonitor TO bitcoinmonitor;
    ALTER USER bitcoinmonitor CREATEDB;
EOSQL


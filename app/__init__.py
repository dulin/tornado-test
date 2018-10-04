#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-

import aiopg
import psycopg2
import tornado.locks
from tornado.options import define, options
from tornado.web import Application

from app.application import Application

define('port', default=8080, help="listening port")
define('bind_address', default="", help="bind address")
define("db_host", default="127.0.0.1", help="database host")
define("db_port", default=5432, help="database port")
define("db_database", default="tornado", help="database name")
define("db_user", default="tornado", help="database user")
define("db_password", default="tornado", help="database password")


async def maybe_create_tables(db):
    try:
        with (await db.cursor()) as cur:
            await cur.execute("SELECT COUNT(*) FROM schema LIMIT 1")
            await cur.fetchone()
    except psycopg2.ProgrammingError:
        print("Database error!")


async def main():
    options.parse_command_line()

    async with aiopg.create_pool(
            host=options.db_host,
            port=options.db_port,
            user=options.db_user,
            password=options.db_password,
            dbname=options.db_database) as db:
        await maybe_create_tables(db)
        app = Application(db)
        app.listen(options.port, options.bind_address)
        print("Listening on http://%s:%i" % (options.bind_address, options.port))
        shutdown_event = tornado.locks.Event()
        await shutdown_event.wait()

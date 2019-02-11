# -*- coding: utf-8 -*-



META_TABLE = """
CREATE TABLE IF NOT EXISTS {}(
        core_id       text PRIMARY KEY,
        external_id   text NOT NULL,
        source        text NOT NULL,
        the_geom      geometry(Geometry, 4326),
        the_geom_webmercator geometry(Geometry, 3857),
        name_from     text,
        name_to       text,
        distance      integer,
        type          integer,
        enabled       boolean NOT NULL DEFAULT TRUE,
        updated_at    timestamp without time zone default (now() at time zone 'utc'),
        server_updated_at    timestamp without time zone default (now() at time zone 'utc')
);
""".format(meta_table_name)


META_INSERT = """
INSERT INTO {0} (
    core_id, source, external_id, the_geom,
    the_geom_webmercator, name_from, name_to,
    distance, updated_at, type, enabled, server_updated_at
)
VALUES (
%(core_id)s, %(source)s, %(external_id)s,
ST_GeomFromText(%(line)s,4326),
ST_Transform(ST_GeomFromText(%(line)s,4326),3857),
%(name_from)s, %(name_to)s, %(distance)s,
(now() at time zone 'utc'), %(type)s, TRUE,
(now() at time zone 'utc')
);
""".format(meta_table_name)

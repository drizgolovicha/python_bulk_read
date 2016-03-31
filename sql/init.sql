DROP TABLE IF EXISTS big_data;
CREATE TABLE big_data
(
  id integer,
  title character varying(255),
  fname character varying(255),
  lname character varying(255),
  price numeric,
  added date
)
WITH (
  OIDS=FALSE
);

insert into big_data
SELECT
	generate_series(1, 1000000),
	md5(random()::text),
	md5(random()::text),
	md5(random()::text),
	random()::FLOAT,
	CURRENT_DATE;
DROP TABLE IF EXISTS sample_table;

CREATE TABLE sample_table (
  id SERIAL,
  text VARCHAR(50),
  value FLOAT,
  PRIMARY KEY (id)
);

--csv struktura
/*
text,value
a,1
b,5
c,4
e,6
f,7 
*/

COPY sample_table(text, value) FROM '/tmp/postgres/example_file.csv' DELIMITER ',' CSV HEADER;
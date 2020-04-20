--
-- Up
--
CREATE TABLE table1 (
    id int(11) NOT NULL AUTO_INCREMENT,
    name varchar(255),
    created_at TIMESTAMP,
    PRIMARY KEY (id));
--
-- Down
--
DROP TABLE table1;

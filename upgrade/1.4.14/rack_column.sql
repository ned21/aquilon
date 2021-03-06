create table rack_save as select * from rack;

ALTER TABLE RACK ADD (NEW_RACK_COLUMN VARCHAR2(4));

UPDATE RACK SET NEW_RACK_COLUMN=(to_char(RACK_COLUMN));

UPDATE RACK SET RACK_ROW=NULL where RACK_ROW='none';

COMMIT;

ALTER TABLE RACK RENAME COLUMN RACK_COLUMN TO OLD_RACK_COLUMN;

ALTER TABLE RACK RENAME COLUMN NEW_RACK_COLUMN TO RACK_COLUMN;

ALTER TABLE RACK DROP COLUMN OLD_RACK_COLUMN;

COMMIT;

PURGE RECYCLEBIN;


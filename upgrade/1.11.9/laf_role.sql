INSERT INTO role (id, name, creation_date, comments)
	VALUES (role_id_seq.nextval, 'laf', SYSDATE,
		'used for self service role');

QUIT;

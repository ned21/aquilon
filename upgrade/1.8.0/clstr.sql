ALTER TABLE clstr ADD down_hosts_threshold NUMBER(*,0);
ALTER TABLE clstr ADD down_hosts_percent NUMBER(*,0);
ALTER TABLE clstr ADD down_maint_threshold NUMBER(*,0);
ALTER TABLE clstr ADD down_maint_percent NUMBER(*,0);

UPDATE clstr SET down_hosts_threshold = (SELECT down_hosts_threshold FROM esx_cluster WHERE esx_cluster_id = clstr.id);

ALTER TABLE esx_cluster drop constraint "ESX_CLSTR_THRSH_NN";
ALTER TABLE esx_cluster drop column down_hosts_threshold;

UPDATE clstr SET down_hosts_percent = 0, down_maint_percent = 0;

ALTER TABLE clstr ADD CONSTRAINT "CLSTR_DOWN_HOSTS_CK" CHECK (down_hosts_percent IN (0, 1)) ENABLE;
alter table clstr add CONSTRAINT "CLSTR_MAINT_HOSTS_CK" CHECK (down_maint_percent IN (0, 1)) ENABLE;
ALTER TABLE clstr MODIFY (down_hosts_percent CONSTRAINT "CLSTR_DOWN_HOSTS_NN" NOT NULL ENABLE);


CREATE TABLE "CLSTR_ALLOW_PER"
 (   "CLUSTER_ID" NUMBER(*,0) CONSTRAINT "CLSTR_ALLOW_PER_CLUSTER_ID_NN" NOT NULL ENABLE,
     "CREATION_DATE" DATE CONSTRAINT "CLSTR_ALLOW_PER_CR_DATE_NN" NOT NULL ENABLE,
     "PERSONALITY_ID" NUMBER(*,0) CONSTRAINT "CLSTR_ALLOW_PER_PRSNLTY_ID_NN" NOT NULL ENABLE,
      CONSTRAINT "CLSTR_ALLOWED_PERS_C_FK" FOREIGN KEY ("CLUSTER_ID") REFERENCES "CLSTR" ("ID") ON DELETE CASCADE ENABLE,
      CONSTRAINT "CLSTR_ALLOWED_PERS_P_FK" FOREIGN KEY ("PERSONALITY_ID") REFERENCES "PERSONALITY" ("ID") ON DELETE CASCADE ENABLE,
      CONSTRAINT "CLSTR_ALLOW_PER_PK" PRIMARY KEY ("CLUSTER_ID", "PERSONALITY_ID") ENABLE
 );


CREATE TABLE "COMPUTE_CLUSTER"
 (   "ID" NUMBER(*,0) CONSTRAINT "COMPUTE_CLUSTER_ID_NN" NOT NULL ENABLE,
      CONSTRAINT "COMPUTE_CLUSTER_FK" FOREIGN KEY ("ID") REFERENCES "CLSTR" ("ID") ON DELETE CASCADE ENABLE,
      CONSTRAINT "COMPUTE_CLUSTER_PK" PRIMARY KEY ("ID") ENABLE
 );


CREATE TABLE "STORAGE_CLUSTER"
 (   "ID" NUMBER(*,0) CONSTRAINT "STORAGE_CLUSTER_ID_NN" NOT NULL ENABLE,
      CONSTRAINT "STORAGE_CLUSTER_FK" FOREIGN KEY ("ID") REFERENCES "CLSTR" ("ID") ON DELETE CASCADE ENABLE,
      CONSTRAINT "STORAGE_CLUSTER_PK" PRIMARY KEY ("ID") ENABLE
 );

COMMIT;

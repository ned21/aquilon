--------------------------------------------------------
--  FIX for service_instance
--------------------------------------------------------

ALTER TABLE SERVICE_INSTANCE ADD CONSTRAINT SVC_INST_UK UNIQUE (
    "SERVICE_ID", "NAME") ENABLE;

--------------------------------------------------------
--  CHANGES FOR delete_quattor_server
--------------------------------------------------------

ALTER TABLE "DOMAIN" DROP COLUMN "SERVER_ID";
commit;

DROP TABLE "QUATTOR_SERVER" CASCADE CONSTRAINTS;
commit;

DELETE FROM system WHERE system_type = 'quattor_server';
commit;

--------------------------------------------------------
-- CHANGES FOR virtualization
--------------------------------------------------------

--------------------------------------------------------
--  OLD_MACHINE_SPECS
--------------------------------------------------------
ALTER TABLE "MACHINE_SPECS" DROP CONSTRAINT "MACHINE_SPECS_CPU_ID_NN";
ALTER TABLE "MACHINE_SPECS" DROP CONSTRAINT "MACHINE_SPECS_CPU_QUANTITY_NN";
ALTER TABLE "MACHINE_SPECS" DROP CONSTRAINT "MACHINE_SPECS_DISK_CAPACITY_NN";
ALTER TABLE "MACHINE_SPECS" DROP CONSTRAINT "MACHINE_SPECS_DISK_TYPE_ID_NN";
ALTER TABLE "MACHINE_SPECS" DROP CONSTRAINT "MACHINE_SPECS_ID_NN";
ALTER TABLE "MACHINE_SPECS" DROP CONSTRAINT "MACHINE_SPECS_MEMORY_NN";
ALTER TABLE "MACHINE_SPECS" DROP CONSTRAINT "MACHINE_SPECS_MODEL_ID_NN";
ALTER TABLE "MACHINE_SPECS" DROP CONSTRAINT "MACHINE_SPECS_NIC_COUNT_NN";
ALTER TABLE "MACHINE_SPECS" DROP CONSTRAINT "MACHINE_SPEC_MODEL_ID_UK";
ALTER TABLE "MACHINE_SPECS" DROP CONSTRAINT "MACH_SPEC_CPU_FK";
ALTER TABLE "MACHINE_SPECS" DROP CONSTRAINT "MACH_SPEC_DISK_TYP_FK";
ALTER TABLE "MACHINE_SPECS" DROP CONSTRAINT "MACH_SPEC_MODEL_FK";
DROP INDEX "MACHINE_SPEC_MODEL_ID_UK";
ALTER TABLE "MACHINE_SPECS" drop constraint "MACHINE_SPECS_PK";
DROP INDEX "MACHINE_SPECS_PK";
ALTER TABLE "MACHINE_SPECS" RENAME TO "OLD_MACHINE_SPECS";
commit;

--------------------------------------------------------
--  MACHINE_SPECS
--------------------------------------------------------
CREATE TABLE "MACHINE_SPECS" (
    "ID" NUMBER(*,0),
    "MODEL_ID" NUMBER(*,0),
    "CPU_ID" NUMBER(*,0),
    "CPU_QUANTITY" NUMBER(*,0),
    "MEMORY" NUMBER(*,0),
    "DISK_TYPE" VARCHAR2(5),
    "DISK_CAPACITY" NUMBER(*,0),
    "CONTROLLER_TYPE" VARCHAR2(5),
    "NIC_COUNT" NUMBER(*,0),
    "CREATION_DATE" DATE,
    "COMMENTS" VARCHAR2(255)
);
commit;

ALTER TABLE "MACHINE_SPECS" ADD CONSTRAINT MACHINE_SPECS_PK PRIMARY KEY ("ID") ENABLE;
ALTER TABLE "MACHINE_SPECS" ADD CONSTRAINT "MACHINE_SPECS_MODEL_UK" UNIQUE ("MODEL_ID") ENABLE;
ALTER TABLE "MACHINE_SPECS" MODIFY ("CONTROLLER_TYPE" CONSTRAINT "MCHN_SPECS_CNTRLR_TYPE_NN" NOT NULL ENABLE);
ALTER TABLE "MACHINE_SPECS" MODIFY ("CPU_ID" CONSTRAINT "MCHN_SPECS_CPU_ID_NN" NOT NULL ENABLE);
ALTER TABLE "MACHINE_SPECS" MODIFY ("CPU_QUANTITY" CONSTRAINT "MCHN_SPECS_CPU_QUANTITY_NN" NOT NULL ENABLE);
ALTER TABLE "MACHINE_SPECS" MODIFY ("DISK_CAPACITY" CONSTRAINT "MCHN_SPECS_DISK_CAPACITY_NN" NOT NULL ENABLE);
ALTER TABLE "MACHINE_SPECS" MODIFY ("DISK_TYPE" CONSTRAINT "MCHN_SPECS_DISK_TYPE_NN" NOT NULL ENABLE);
ALTER TABLE "MACHINE_SPECS" MODIFY ("ID" CONSTRAINT "MCHN_SPECS_ID_NN" NOT NULL ENABLE);
ALTER TABLE "MACHINE_SPECS" MODIFY ("MEMORY" CONSTRAINT "MCHN_SPECS_MEMORY_NN" NOT NULL ENABLE);
ALTER TABLE "MACHINE_SPECS" MODIFY ("MODEL_ID" CONSTRAINT "MCHN_SPECS_MODEL_ID_NN" NOT NULL ENABLE);
ALTER TABLE "MACHINE_SPECS" MODIFY ("NIC_COUNT" CONSTRAINT "MCHN_SPECS_NIC_COUNT_NN" NOT NULL ENABLE);

ALTER TABLE "MACHINE_SPECS" ADD CONSTRAINT "MACH_SPEC_CPU_FK" FOREIGN KEY ("CPU_ID")
 REFERENCES "CPU" ("ID") ENABLE;

ALTER TABLE "MACHINE_SPECS" ADD CONSTRAINT "MACH_SPEC_MODEL_FK" FOREIGN KEY ("MODEL_ID")
 REFERENCES "MODEL" ("ID") ENABLE;

commit;

--------------------------------------------------------
-- POPULATE MACHINE_SPECS
--------------------------------------------------------

insert into MACHINE_SPECS (ID, MODEL_ID, CPU_ID, CPU_QUANTITY, MEMORY, DISK_TYPE,
                           DISK_CAPACITY, CONTROLLER_TYPE, NIC_COUNT, CREATION_DATE, COMMENTS)
(SELECT A.ID, A.MODEL_ID, A.CPU_ID, A.CPU_QUANTITY, A.MEMORY, 'local', A.DISK_CAPACITY,
        B.TYPE, A.NIC_COUNT, A.CREATION_DATE, A.COMMENTS
FROM OLD_MACHINE_SPECS A, DISK_TYPE B
WHERE A.disk_type_id = B.id);

commit;

--------------------------------------------------------
--  OLD DISK
--------------------------------------------------------

ALTER TABLE "DISK" DROP CONSTRAINT "DISK_MACH_DEV_NAME_UK";
commit;

ALTER TABLE "DISK" RENAME CONSTRAINT "DISK_PK" TO "OLD_DISK_PK";
ALTER TABLE "DISK" DROP CONSTRAINT "DISK_MACHINE_FK";
ALTER TABLE "DISK" DROP CONSTRAINT "DISK_CR_DATE_NN";
ALTER TABLE "DISK" DROP CONSTRAINT "DISK_CAPACITY_NN";
ALTER TABLE "DISK" DROP CONSTRAINT "DISK_MACHINE_ID_NN";
ALTER TABLE "DISK" DROP CONSTRAINT "DISK_ID_NN";
ALTER TABLE "DISK" DROP CONSTRAINT "DISK_DEVICE_NAME_NN";
ALTER TABLE "DISK" DROP CONSTRAINT "DISK_DISK_TYPE_FK";
ALTER TABLE "DISK" DROP CONSTRAINT "DISK_DISK_TYPE_ID_NN";
DROP INDEX  "DISK_MACH_DEV_NAME_UK";
ALTER INDEX "DISK_PK" RENAME TO "OLD_DISK_PK";
commit;

ALTER TABLE "DISK" RENAME TO "OLD_DISK";
commit;

ALTER TABLE "DISK_TYPE" RENAME TO "OLD_DISK_TYPE";
commit;
--------------------------------------------------------
--  DISK
--------------------------------------------------------
CREATE TABLE "DISK" (
    "ID" NUMBER(*,0),
    "DISK_TYPE" VARCHAR2(64),
    "CAPACITY" NUMBER(*,0),
    "DEVICE_NAME" VARCHAR2(128),
    "CONTROLLER_TYPE" VARCHAR2(64),
    "MACHINE_ID" NUMBER(*,0),
    "CREATION_DATE" DATE,
    "COMMENTS" VARCHAR2(255),
    "ADDRESS" VARCHAR2(128),
    "SERVICE_INSTANCE_ID" NUMBER(*,0)
);
commit;

ALTER TABLE "DISK" MODIFY ("CAPACITY" CONSTRAINT "DISK_CAPACITY_NN" NOT NULL ENABLE);
ALTER TABLE "DISK" MODIFY ("CONTROLLER_TYPE" CONSTRAINT "DISK_CNTRLR_TYPE_NN" NOT NULL ENABLE);
ALTER TABLE "DISK" MODIFY ("CREATION_DATE" CONSTRAINT "DISK_CR_DATE_NN" NOT NULL ENABLE);
ALTER TABLE "DISK" MODIFY ("DEVICE_NAME" CONSTRAINT "DISK_DEVICE_NAME_NN" NOT NULL ENABLE);
ALTER TABLE "DISK" MODIFY ("DISK_TYPE" CONSTRAINT "DISK_DISK_TYPE_NN" NOT NULL ENABLE);
ALTER TABLE "DISK" MODIFY ("ID" CONSTRAINT "DISK_ID_NN" NOT NULL ENABLE);
ALTER TABLE "DISK" MODIFY ("MACHINE_ID" CONSTRAINT "DISK_MACHINE_ID_NN" NOT NULL ENABLE);
ALTER TABLE "DISK" ADD CONSTRAINT "DISK_MACH_DEV_NAME_UK" UNIQUE ("MACHINE_ID", "DEVICE_NAME") ENABLE;
ALTER TABLE "DISK" ADD CONSTRAINT "DISK_PK" PRIMARY KEY ("ID") ENABLE;

ALTER TABLE "DISK" ADD CONSTRAINT "DISK_MACHINE_FK" FOREIGN KEY ("MACHINE_ID")
    REFERENCES "MACHINE" ("MACHINE_ID") ON DELETE CASCADE ENABLE;

ALTER TABLE "DISK" ADD CONSTRAINT "NAS_DISK_SRV_INST_FK" FOREIGN KEY ("SERVICE_INSTANCE_ID")
    REFERENCES "SERVICE_INSTANCE" ("ID") ENABLE;
commit;

--------------------------------------------------------
--  POPULATE DISK
--------------------------------------------------------
INSERT INTO DISK (ID, DISK_TYPE, CAPACITY, DEVICE_NAME, CONTROLLER_TYPE,
                  MACHINE_ID, CREATION_DATE, SERVICE_INSTANCE_ID)
(SELECT A.id, 'local', A.capacity, A.DEVICE_NAME, B.TYPE, A.machine_id,
        A.creation_date, NULL
FROM OLD_DISK A, OLD_DISK_TYPE B
WHERE A.disk_type_id = B.id);

commit;

--------------------------------------------------------
--  CLSTR
--------------------------------------------------------

CREATE SEQUENCE "CLSTR_SEQ" MINVALUE 1 MAXVALUE 999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 2 NOORDER NOCYCLE;

CREATE TABLE "CLSTR" (
    "ID" NUMBER(*,0),
    "CLUSTER_TYPE" VARCHAR2(16),
    "NAME" VARCHAR2(64),
    "PERSONALITY_ID" NUMBER(*,0),
    "DOMAIN_ID" NUMBER(*,0),
    "LOCATION_CONSTRAINT_ID" NUMBER(*,0),
    "MAX_HOSTS" NUMBER(*,0),
    "CREATION_DATE" DATE,
    "COMMENTS" VARCHAR2(255)
);
commit;

ALTER TABLE "CLSTR" MODIFY ("CLUSTER_TYPE" CONSTRAINT "CLSTR_CLSTR_TYP_NN" NOT NULL ENABLE);
ALTER TABLE "CLSTR" MODIFY ("CREATION_DATE" CONSTRAINT "CLSTR_CR_DATE_NN" NOT NULL ENABLE);
ALTER TABLE "CLSTR" MODIFY ("DOMAIN_ID" CONSTRAINT "CLSTR_DOMAIN_ID_NN" NOT NULL ENABLE);
ALTER TABLE "CLSTR" MODIFY ("ID" CONSTRAINT "CLSTR_ID_NN" NOT NULL ENABLE);
ALTER TABLE "CLSTR" MODIFY ("NAME" CONSTRAINT "CLSTR_NAME_NN" NOT NULL ENABLE);
ALTER TABLE "CLSTR" MODIFY ("PERSONALITY_ID" CONSTRAINT "CLSTR_PRSNLTY_ID_NN" NOT NULL ENABLE);
ALTER TABLE "CLSTR" ADD CONSTRAINT "CLUSTER_PK" PRIMARY KEY ("ID") ENABLE;
ALTER TABLE "CLSTR" ADD CONSTRAINT "CLUSTER_UK" UNIQUE ("NAME") ENABLE;

ALTER TABLE "CLSTR" ADD CONSTRAINT "CLUSTER_DOMAIN_FK" FOREIGN KEY ("DOMAIN_ID")
    REFERENCES "DOMAIN" ("ID") ENABLE;

ALTER TABLE "CLSTR" ADD CONSTRAINT "CLUSTER_LOCATION_FK" FOREIGN KEY ("LOCATION_CONSTRAINT_ID")
    REFERENCES "LOCATION" ("ID") ENABLE;

ALTER TABLE "CLSTR" ADD CONSTRAINT "CLUSTER_PRSNLTY_FK" FOREIGN KEY ("PERSONALITY_ID")
    REFERENCES "PERSONALITY" ("ID") ENABLE;
commit;

--------------------------------------------------------
-- CLUSTER_ALIGNED_SERVICE
--------------------------------------------------------
CREATE TABLE "CLUSTER_ALIGNED_SERVICE" (
    "SERVICE_ID" NUMBER(*,0),
    "CLUSTER_TYPE" VARCHAR2(16),
    "CREATION_DATE" DATE,
    "COMMENTS" VARCHAR2(255)
);
commit;

ALTER TABLE "CLUSTER_ALIGNED_SERVICE" MODIFY ("CLUSTER_TYPE" CONSTRAINT "CLSTR_ALND_SVC_CLSTR_TYP_NN" NOT NULL ENABLE);
ALTER TABLE "CLUSTER_ALIGNED_SERVICE" MODIFY ("CREATION_DATE" CONSTRAINT "CLSTR_ALND_SVC_CR_DATE_NN" NOT NULL ENABLE);
ALTER TABLE "CLUSTER_ALIGNED_SERVICE" ADD CONSTRAINT "CLSTR_ALND_SVC_PK" PRIMARY KEY ("SERVICE_ID", "CLUSTER_TYPE") ENABLE;
ALTER TABLE "CLUSTER_ALIGNED_SERVICE" MODIFY ("SERVICE_ID" CONSTRAINT "CLSTR_ALND_SVC_SVC_ID_NN" NOT NULL ENABLE);

ALTER TABLE "CLUSTER_ALIGNED_SERVICE" ADD CONSTRAINT "CLSTR_ALND_SVC_SVC_FK" FOREIGN KEY ("SERVICE_ID")
    REFERENCES "SERVICE" ("ID") ON DELETE CASCADE ENABLE;

commit;
--------------------------------------------------------
-- CLUSTER_SERVICE_BINDING
--------------------------------------------------------
CREATE TABLE "CLUSTER_SERVICE_BINDING" (
    "CLUSTER_ID" NUMBER(*,0),
    "SERVICE_INSTANCE_ID" NUMBER(*,0),
    "CREATION_DATE" DATE,
    "COMMENTS" VARCHAR2(255)
);
commit;

ALTER TABLE "CLUSTER_SERVICE_BINDING" MODIFY ("CLUSTER_ID" CONSTRAINT "CLSTR_SVC_BNDG_CLUSTER_ID_NN" NOT NULL ENABLE);
ALTER TABLE "CLUSTER_SERVICE_BINDING" MODIFY ("CREATION_DATE" CONSTRAINT "CLSTR_SVC_BNDG_CR_DATE_NN" NOT NULL ENABLE);
ALTER TABLE "CLUSTER_SERVICE_BINDING" MODIFY ("SERVICE_INSTANCE_ID" CONSTRAINT "CLSTR_SVC_BNDG_SVC_INST_ID_NN" NOT NULL ENABLE);
ALTER TABLE "CLUSTER_SERVICE_BINDING" ADD CONSTRAINT "CLUSTER_SERVICE_BINDING_PK" PRIMARY KEY ("CLUSTER_ID", "SERVICE_INSTANCE_ID") ENABLE;

ALTER TABLE "CLUSTER_SERVICE_BINDING" ADD CONSTRAINT "CLSTR_SVC_BNDG_CLUSTER_FK" FOREIGN KEY ("CLUSTER_ID")
    REFERENCES "CLSTR" ("ID") ON DELETE CASCADE ENABLE;

ALTER TABLE "CLUSTER_SERVICE_BINDING" ADD CONSTRAINT "CLSTR_SVC_BNDG_SRV_INST_FK" FOREIGN KEY ("SERVICE_INSTANCE_ID")
    REFERENCES "SERVICE_INSTANCE" ("ID") ENABLE;

commit;

--------------------------------------------------------
--  DYNAMIC_STUB
--------------------------------------------------------
CREATE TABLE "DYNAMIC_STUB" (
    "SYSTEM_ID" NUMBER(*,0)
);
commit;

ALTER TABLE "DYNAMIC_STUB" ADD CONSTRAINT "DYNAMIC_STUB_PK" PRIMARY KEY ("SYSTEM_ID") ENABLE;
ALTER TABLE "DYNAMIC_STUB" MODIFY ("SYSTEM_ID" CONSTRAINT "DYNAMIC_STUB_SYSTEM_ID_NN" NOT NULL ENABLE);

ALTER TABLE "DYNAMIC_STUB" ADD CONSTRAINT "DYNAMIC_STUB_SYSTEM_FK" FOREIGN KEY ("SYSTEM_ID")
    REFERENCES "SYSTEM" ("ID") ON DELETE CASCADE ENABLE;

commit;

--------------------------------------------------------
--  ESX_CLUSTER
--------------------------------------------------------
CREATE TABLE "ESX_CLUSTER" (
    "ESX_CLUSTER_ID" NUMBER(*,0),
    "VM_TO_HOST_RATIO" NUMBER(*,0)
);
commit;

ALTER TABLE "ESX_CLUSTER" MODIFY ("ESX_CLUSTER_ID" CONSTRAINT "ESX_CLSTR_ESX_CLSTR_ID_NN" NOT NULL ENABLE);
ALTER TABLE "ESX_CLUSTER" ADD CONSTRAINT "ESX_CLUSTER_PK" PRIMARY KEY ("ESX_CLUSTER_ID") ENABLE;

ALTER TABLE "ESX_CLUSTER" ADD CONSTRAINT "ESX_CLUSTER_FK" FOREIGN KEY ("ESX_CLUSTER_ID")
    REFERENCES "CLSTR" ("ID") ON DELETE CASCADE ENABLE;

commit;

--------------------------------------------------------
--  HOST_CLUSTER_MEMBER
--------------------------------------------------------
CREATE TABLE "HOST_CLUSTER_MEMBER" (
    "CLUSTER_ID" NUMBER(*,0),
    "HOST_ID" NUMBER(*,0),
    "CREATION_DATE" DATE
);
commit;

ALTER TABLE "HOST_CLUSTER_MEMBER" MODIFY ("CLUSTER_ID" CONSTRAINT "HOST_CLSTR_MMBR_CLUSTER_ID_NN" NOT NULL ENABLE);
ALTER TABLE "HOST_CLUSTER_MEMBER" MODIFY ("CREATION_DATE" CONSTRAINT "HOST_CLSTR_MMBR_CR_DATE_NN" NOT NULL ENABLE);
ALTER TABLE "HOST_CLUSTER_MEMBER" MODIFY ("HOST_ID" CONSTRAINT "HOST_CLSTR_MMBR_HOST_ID_NN" NOT NULL ENABLE);
ALTER TABLE "HOST_CLUSTER_MEMBER" ADD CONSTRAINT "HOST_CLUSTER_MEMBER_HOST_UK" UNIQUE ("HOST_ID") ENABLE;
ALTER TABLE "HOST_CLUSTER_MEMBER" ADD CONSTRAINT "HOST_CLUSTER_MEMBER_PK" PRIMARY KEY ("CLUSTER_ID", "HOST_ID") ENABLE;

ALTER TABLE "HOST_CLUSTER_MEMBER" ADD CONSTRAINT "HST_CLSTR_MMBR_CLSTR_FK" FOREIGN KEY ("CLUSTER_ID")
    REFERENCES "CLSTR" ("ID") ON DELETE CASCADE ENABLE;

ALTER TABLE "HOST_CLUSTER_MEMBER" ADD CONSTRAINT "HST_CLSTR_MMBR_HST_FK" FOREIGN KEY ("HOST_ID")
    REFERENCES "HOST" ("ID") ON DELETE CASCADE ENABLE;

commit;

--------------------------------------------------------
--  MACHINE_CLUSTER_MEMBER
--------------------------------------------------------
CREATE TABLE "MACHINE_CLUSTER_MEMBER"(
    "CLUSTER_ID" NUMBER(*,0),
    "MACHINE_ID" NUMBER(*,0),
    "CREATION_DATE" DATE
);
commit;

ALTER TABLE "MACHINE_CLUSTER_MEMBER" ADD CONSTRAINT "MACHINE_CLUSTER_MEMBER_PK" PRIMARY KEY ("CLUSTER_ID", "MACHINE_ID") ENABLE;
ALTER TABLE "MACHINE_CLUSTER_MEMBER" ADD CONSTRAINT "MACHINE_CLUSTER_MEMBER_UK" UNIQUE ("MACHINE_ID") ENABLE;
ALTER TABLE "MACHINE_CLUSTER_MEMBER" MODIFY ("CLUSTER_ID" CONSTRAINT "MCHN_CLSTR_MMBR_CLUSTER_ID_NN" NOT NULL ENABLE);
ALTER TABLE "MACHINE_CLUSTER_MEMBER" MODIFY ("CREATION_DATE" CONSTRAINT "MCHN_CLSTR_MMBR_CR_DATE_NN" NOT NULL ENABLE);
ALTER TABLE "MACHINE_CLUSTER_MEMBER" MODIFY ("MACHINE_ID" CONSTRAINT "MCHN_CLSTR_MMBR_MACHINE_ID_NN" NOT NULL ENABLE);

ALTER TABLE "MACHINE_CLUSTER_MEMBER" ADD CONSTRAINT "MCHN_CLSTR_MMBR_CLSTR_FK" FOREIGN KEY ("CLUSTER_ID")
    REFERENCES "CLSTR" ("ID") ON DELETE CASCADE ENABLE;

ALTER TABLE "MACHINE_CLUSTER_MEMBER" ADD CONSTRAINT "MCHN_CLSTR_MMBR_MCHN_FK" FOREIGN KEY ("MACHINE_ID")
    REFERENCES "MACHINE" ("MACHINE_ID") ON DELETE CASCADE ENABLE;

commit;

--------------------------------------------------------
--  METACLUSTER
--------------------------------------------------------
CREATE SEQUENCE "METACLUSTER_SEQ" MINVALUE 1 MAXVALUE 999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 2 NOORDER NOCYCLE ;

CREATE TABLE "METACLUSTER" (
    "ID" NUMBER(*,0),
    "NAME" VARCHAR2(64),
    "MAX_CLUSTERS" NUMBER(*,0),
    "MAX_SHARES" NUMBER(*,0),
    "CREATION_DATE" DATE,
    "COMMENTS" VARCHAR2(255)
);
commit;

ALTER TABLE "METACLUSTER" MODIFY ("CREATION_DATE" CONSTRAINT "METACLUSTER_CR_DATE_NN" NOT NULL ENABLE);
ALTER TABLE "METACLUSTER" MODIFY ("ID" CONSTRAINT "METACLUSTER_ID_NN" NOT NULL ENABLE);
ALTER TABLE "METACLUSTER" MODIFY ("MAX_CLUSTERS" CONSTRAINT "METACLUSTER_MAX_CLUSTERS_NN" NOT NULL ENABLE);
ALTER TABLE "METACLUSTER" MODIFY ("MAX_SHARES" CONSTRAINT "METACLUSTER_MAX_SHARES_NN" NOT NULL ENABLE);
ALTER TABLE "METACLUSTER" MODIFY ("NAME" CONSTRAINT "METACLUSTER_NAME_NN" NOT NULL ENABLE);
ALTER TABLE "METACLUSTER" ADD CONSTRAINT "METACLUSTER_PK" PRIMARY KEY ("ID") ENABLE;
ALTER TABLE "METACLUSTER" ADD CONSTRAINT "METACLUSTER_UK" UNIQUE ("NAME") ENABLE;
commit;

--------------------------------------------------------
--  METACLUSTER_MEMBER
--------------------------------------------------------
CREATE TABLE "METACLUSTER_MEMBER" (
    "METACLUSTER_ID" NUMBER(*,0),
    "CLUSTER_ID" NUMBER(*,0),
    "CREATION_DATE" DATE
);
commit;

ALTER TABLE "METACLUSTER_MEMBER" ADD CONSTRAINT "METACLUSTER_MEMBER_PK" PRIMARY KEY ("METACLUSTER_ID", "CLUSTER_ID") ENABLE;
ALTER TABLE "METACLUSTER_MEMBER" ADD CONSTRAINT "METACLUSTER_MEMBER_UK" UNIQUE ("CLUSTER_ID") ENABLE;
ALTER TABLE "METACLUSTER_MEMBER" MODIFY ("CLUSTER_ID" CONSTRAINT "MTACLSTR_MBR_CLUSTER_ID_NN" NOT NULL ENABLE);
ALTER TABLE "METACLUSTER_MEMBER" MODIFY ("CREATION_DATE" CONSTRAINT "MTACLSTR_MBR_CR_DATE_NN" NOT NULL ENABLE);
ALTER TABLE "METACLUSTER_MEMBER" MODIFY ("METACLUSTER_ID" CONSTRAINT "MTACLSTR_MBR_MTACLSTR_ID_NN" NOT NULL ENABLE);

ALTER TABLE "METACLUSTER_MEMBER" ADD CONSTRAINT "METACLUSTER_MEMBER_CLSTR_FK" FOREIGN KEY ("CLUSTER_ID")
    REFERENCES "CLSTR" ("ID") ON DELETE CASCADE ENABLE;

ALTER TABLE "METACLUSTER_MEMBER" ADD CONSTRAINT "METACLUSTER_MEMBER_META_FK" FOREIGN KEY ("METACLUSTER_ID")
    REFERENCES "METACLUSTER" ("ID") ON DELETE CASCADE ENABLE;

commit;

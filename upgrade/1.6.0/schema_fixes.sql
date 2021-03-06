-- Add additional vlan constraints
ALTER TABLE observed_vlan
	ADD CONSTRAINT "OBSERVED_VLAN_MIN_VLAN_ID" CHECK ("VLAN_ID" >= 0);
ALTER TABLE vlan_info
	ADD CONSTRAINT "VLAN_INFO_MIN_VLAN_ID" CHECK ("VLAN_ID" >= 0);

-- Convert from CHECK to NOT NULL
ALTER TABLE archetype DROP CONSTRAINT "ARCHETYPE_IS_COMPILEABLE_NN";
ALTER TABLE archetype
	MODIFY (is_compileable CONSTRAINT "ARCHETYPE_IS_COMPILEABLE_NN" NOT NULL);
-- Missing CHECK
ALTER TABLE archetype
	MODIFY (is_compileable CHECK (is_compileable IN (0, 1)));

-- Missing CHECK
ALTER TABLE branch
	MODIFY (autosync CHECK (autosync IN (0, 1)));
ALTER TABLE branch
	MODIFY (is_sync_valid CHECK (is_sync_valid IN (0, 1)));

-- Missing NOT NULL
ALTER TABLE build_item
	MODIFY (service_instance_id CONSTRAINT "BUILD_ITEM_SVC_INST_ID_NN" NOT NULL);

-- Wrong name
ALTER TABLE clstr RENAME CONSTRAINT "CLSTR_DOMAIN_ID_NN" TO "CLSTR_BRANCH_ID_NN";
ALTER TABLE clstr MODIFY (status_id NULL);
ALTER TABLE clstr MODIFY (status_id CONSTRAINT "CLSTR_STATUS_ID_NN" NOT NULL);

-- Wrong name
ALTER TABLE clusterlifecycle MODIFY (name NULL);
ALTER TABLE clusterlifecycle MODIFY (name CONSTRAINT "CLUSTERLIFECYCLE_NAME_NN" NOT NULL);
ALTER TABLE clusterlifecycle MODIFY (creation_date NULL);
ALTER TABLE clusterlifecycle MODIFY (creation_date CONSTRAINT "CLUSTERLIFECYCLE_CR_DATE_NN" NOT NULL);
DECLARE
	name user_constraints.constraint_name%TYPE;
	target VARCHAR2(32) := 'CLUSTERLIFECYCLE_ID_NN';
BEGIN
	SELECT user_constraints.constraint_name INTO name
		FROM user_constraints
		WHERE table_name = 'CLUSTERLIFECYCLE' AND generated = 'GENERATED NAME';
	EXECUTE IMMEDIATE 'ALTER TABLE clusterlifecycle RENAME CONSTRAINT ' || name || ' TO ' || target;
END;
/

-- Convert from CHECK to NOT NULL
ALTER TABLE esx_cluster DROP CONSTRAINT "ESX_CLSTR_THRSH_NN";
ALTER TABLE esx_cluster
	MODIFY (down_hosts_threshold CONSTRAINT "ESX_CLSTR_THRSH_NN" NOT NULL);

-- Wrong name
ALTER TABLE future_a_record MODIFY (system_id NULL);
ALTER TABLE future_a_record MODIFY (system_id CONSTRAINT "FUTURE_A_RECORD_SYSTEM_ID_NN" NOT NULL);

-- Wrong name
ALTER TABLE host RENAME CONSTRAINT "HOST_DOMAIN_ID_NN" TO "HOST_BRANCH_ID_NN";
ALTER TABLE host RENAME CONSTRAINT "HOST_MACHINE_DOMAIN_UK" TO "HOST_MACHINE_BRANCH_UK";
-- Convert CHECK to NOT NULL
ALTER TABLE host DROP CONSTRAINT "HOST_PRSNLTY_ID_NN";
ALTER TABLE host
	MODIFY (personality_id CONSTRAINT "HOST_PRSNLTY_ID_NN" NOT NULL);
ALTER TABLE host DROP CONSTRAINT "HOST_OS_ID_NN";
ALTER TABLE host
	MODIFY (operating_system_id CONSTRAINT "HOST_OPERATING_SYSTEM_ID_NN" NOT NULL);
-- Wrong index name
ALTER INDEX "HOST_MACHINE_DOMAIN_UK" RENAME TO "HOST_MACHINE_BRANCH_UK";

-- Wrong name
ALTER TABLE hostlifecycle MODIFY (name NULL);
ALTER TABLE hostlifecycle MODIFY (name CONSTRAINT "HOSTLIFECYCLE_NAME_NN" NOT NULL);
ALTER TABLE hostlifecycle MODIFY (creation_date NULL);
ALTER TABLE hostlifecycle MODIFY (creation_date CONSTRAINT "HOSTLIFECYCLE_CR_DATE_NN" NOT NULL);
DECLARE
	name user_constraints.constraint_name%TYPE;
	target VARCHAR2(32) := 'HOSTLIFECYCLE_ID_NN';
BEGIN
	SELECT user_constraints.constraint_name INTO name
		FROM user_constraints
		WHERE table_name = 'HOSTLIFECYCLE' AND generated = 'GENERATED NAME';
	EXECUTE IMMEDIATE 'ALTER TABLE hostlifecycle RENAME CONSTRAINT ' || name || ' TO ' || target;
END;
/

-- Wrong name
ALTER TABLE interface RENAME CONSTRAINT "IFACE_HARDWARE_ENTITY_ID_NN" TO "IFACE_HW_ENT_ID_NN";
-- Missing CHECK
ALTER TABLE interface
	MODIFY (bootable CHECK (bootable IN (0, 1)));

-- Wrong name
ALTER TABLE machine RENAME CONSTRAINT "MACHINE_ID_NN" TO "MACHINE_MACHINE_ID_NN";
-- Missing ON DELETE CASCADE
ALTER TABLE machine DROP CONSTRAINT "MACHINE_HW_ENT_FK";
ALTER TABLE machine
	ADD CONSTRAINT "MACHINE_HW_ENT_FK" FOREIGN KEY (machine_id) REFERENCES hardware_entity(id) ON DELETE CASCADE;

-- Missing NOT NULL
ALTER TABLE model
	MODIFY (name CONSTRAINT "MODEL_NAME_NN" NOT NULL);
-- Wrong name
ALTER TABLE model RENAME CONSTRAINT "MODEL_VENDOR_NAME_UK" TO "MODEL_NAME_VENDOR_UK";
-- Wrong index name
ALTER INDEX "MODEL_VENDOR_NAME_UK" RENAME TO "MODEL_NAME_VENDOR_UK";

-- Missing CHECK
ALTER TABLE network
	MODIFY (is_discoverable CHECK (is_discoverable IN (0, 1)));
ALTER TABLE network
	MODIFY (is_discovered CHECK (is_discovered IN (0, 1)));

-- Convert CHECK to NOT NULL
ALTER TABLE observed_vlan DROP CONSTRAINT "OBSERVED_VLAN_NETWORK_ID_NN";
ALTER TABLE observed_vlan
	MODIFY (network_id CONSTRAINT "OBSERVED_VLAN_NETWORK_ID_NN" NOT NULL);
ALTER TABLE observed_vlan DROP CONSTRAINT "OBSERVED_VLAN_VLAN_ID_NN";
ALTER TABLE observed_vlan
	MODIFY (vlan_id CONSTRAINT "OBSERVED_VLAN_VLAN_ID_NN" NOT NULL);
ALTER TABLE observed_vlan DROP CONSTRAINT "OBSERVED_VLAN_CR_DATE_NN";
ALTER TABLE observed_vlan
	MODIFY (creation_date CONSTRAINT "OBSERVED_VLAN_CR_DATE_NN" NOT NULL);

-- Wrong name
ALTER TABLE personality_service_list_item RENAME CONSTRAINT "PRSNLTY_SLI_SERVICE_ID_NN" TO "PRSNLTY_SLI_SVC_ID_NN";
ALTER TABLE personality_service_list_item RENAME CONSTRAINT "PRSNLTY_SLI_PERSONALITY_ID_NN" TO "PRSNLTY_SLI_PRSNLTY_ID_NN";

-- Wrong name
ALTER TABLE personality_service_map RENAME CONSTRAINT "PRSNLTY_SVC_MAP_SVC_INST_NN" TO "PRSNLTY_SVC_MAP_SVC_INST_ID_NN";
ALTER TABLE personality_service_map RENAME CONSTRAINT "PRSNLTY_SVC_MAP_LOC_ID_NN" TO "PRSNLTY_SVC_MAP_LOCATION_ID_NN";

-- Wrong name
ALTER TABLE service_instance RENAME CONSTRAINT "SVC_INST_SERVICE_ID_NN" TO "SVC_INST_SVC_ID_NN";

-- Wrong name
ALTER TABLE service_instance_server RENAME CONSTRAINT "SIS_SERVICE_INSTANCE_ID_NN" TO "SIS_SVC_INST_ID_NN";

-- Wrong name
ALTER TABLE service_list_item RENAME CONSTRAINT "SVC_LI_SERVICE_ID_NN" TO "SVC_LI_SVC_ID_NN";

-- Wrong name
ALTER TABLE service_map RENAME CONSTRAINT "SVC_MAP_SERVICE_INSTANCE_ID_NN" TO "SVC_MAP_SVC_INST_ID_NN";

-- Convert CHECK to NOT NULL
ALTER TABLE vlan_info DROP CONSTRAINT "VLAN_INFO_VLAN_ID_NN";
ALTER TABLE vlan_info
	MODIFY (vlan_id CONSTRAINT "VLAN_INFO_VLAN_ID_NN" NOT NULL);
ALTER TABLE vlan_info DROP CONSTRAINT "VLAN_INFO_PORT_GROUP_NN";
ALTER TABLE vlan_info
	MODIFY (port_group CONSTRAINT "VLAN_INFO_PORT_GROUP_NN" NOT NULL);
ALTER TABLE vlan_info DROP CONSTRAINT "VLAN_INFO_VLAN_TYPE_NN";
ALTER TABLE vlan_info
	 MODIFY (vlan_type CONSTRAINT "VLAN_INFO_VLAN_TYPE_NN" NOT NULL);

-- Drop outdated defaults. Oracle has no "ALTER TABLE ... DROP DEFAULT"
ALTER TABLE clstr MODIFY (status_id DEFAULT NULL);
ALTER TABLE network MODIFY (is_discoverable DEFAULT NULL);
ALTER TABLE network MODIFY (is_discovered DEFAULT NULL);
ALTER TABLE switch MODIFY (last_poll DEFAULT NULL);

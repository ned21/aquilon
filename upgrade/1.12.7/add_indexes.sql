CREATE INDEX branch_owner_idx ON branch (owner_id);
CREATE INDEX clstr_sandbox_author_idx ON clstr (sandbox_author_id);
CREATE INDEX host_sandbox_author_idx ON host (sandbox_author_id);
CREATE INDEX interface_port_group_idx ON interface (port_group_id);
CREATE INDEX location_dns_domain_idx ON location (default_dns_domain_id);
CREATE INDEX machine_cpu_idx ON machine (cpu_id);
CREATE INDEX machine_specs_cpu_idx ON machine_specs (cpu_id);
CREATE INDEX machine_specs_nic_model_idx ON machine_specs (nic_model_id);
CREATE INDEX network_net_comp_idx ON network (network_compartment_id);
CREATE INDEX net_env_location_idx ON network_environment (location_id);
CREATE INDEX personality_rootuser_user_idx ON personality_rootuser (user_id);
CREATE INDEX pers_rootng_netgroup_idx ON personality_rootnetgroup (netgroup_id);

QUIT;

ALTER TABLE resholder ADD personality_id INTEGER;
ALTER TABLE resholder ADD archetype_id INTEGER;
ALTER TABLE resholder ADD eon_id INTEGER;
ALTER TABLE resholder ADD location_id INTEGER;
ALTER TABLE resholder ADD host_environment_id INTEGER;

ALTER TABLE resholder ADD CONSTRAINT resholder_personality_fk FOREIGN KEY (personality_id) REFERENCES personality (id) ON DELETE CASCADE;
ALTER TABLE resholder ADD CONSTRAINT resholder_archetype_fk FOREIGN KEY (archetype_id) REFERENCES archetype (id) ON DELETE CASCADE;
ALTER TABLE resholder ADD CONSTRAINT resholder_grn_fk FOREIGN KEY (eon_id) REFERENCES grn (eon_id) ON DELETE CASCADE;
ALTER TABLE resholder ADD CONSTRAINT resholder_location_fk FOREIGN KEY (location_id) REFERENCES location (id) ON DELETE CASCADE;
ALTER TABLE resholder ADD CONSTRAINT resholder_host_environment_fk FOREIGN KEY (host_environment_id) REFERENCES host_environment (id) ON DELETE CASCADE;

ALTER TABLE resholder ADD CONSTRAINT resholder_holder_uk UNIQUE (host_id, cluster_id, personality_id, archetype_id, eon_id, host_environment_id, location_id);

ALTER TABLE resholder ADD CONSTRAINT resholder_personality_ck CHECK (holder_type != 'personality' OR location_id IS NOT NULL);
ALTER TABLE resholder ADD CONSTRAINT resholder_archetype_ck CHECK (holder_type != 'archetype' OR (host_environment_id IS NOT NULL AND location_id IS NOT NULL));
ALTER TABLE resholder ADD CONSTRAINT resholder_grn_ck CHECK (holder_type != 'grn' OR (host_environment_id IS NOT NULL AND location_id IS NOT NULL));


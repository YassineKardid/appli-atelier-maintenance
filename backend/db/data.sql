INSERT INTO `appli_maintenance`.`role` (`id`, `name`) VALUES ('1', 'Directeur de Production');
INSERT INTO `appli_maintenance`.`role` (`id`, `name`) VALUES ('2', 'Chef d\'Atelier');
INSERT INTO `appli_maintenance`.`role` (`id`, `name`) VALUES ('3', 'Chef d\'Equipe');
INSERT INTO `appli_maintenance`.`role` (`id`, `name`) VALUES ('4', 'Opérateur');

INSERT INTO `appli_maintenance`.`stade` (`id`, `name`) VALUES ('1', 'Dragline');
INSERT INTO `appli_maintenance`.`stade` (`id`, `name`) VALUES ('2', 'Bull & Camion');

INSERT INTO `appli_maintenance`.`section` (`id`, `name`) VALUES ('1', 'Mécanique');
INSERT INTO `appli_maintenance`.`section` (`id`, `name`) VALUES ('2', 'Electrique');
INSERT INTO `appli_maintenance`.`section` (`id`, `name`) VALUES ('3', 'Electronique');
INSERT INTO `appli_maintenance`.`section` (`id`, `name`) VALUES ('4', 'Entretien');
INSERT INTO `appli_maintenance`.`section` (`id`, `name`) VALUES ('5', 'Pneumatique');
INSERT INTO `appli_maintenance`.`section` (`id`, `name`) VALUES ('6', 'Mouvement de câble');

INSERT INTO `appli_maintenance`.`stade_section` (`stade_id`, `section_id`) VALUES ('1', '1');
INSERT INTO `appli_maintenance`.`stade_section` (`stade_id`, `section_id`) VALUES ('1', '2');
INSERT INTO `appli_maintenance`.`stade_section` (`stade_id`, `section_id`) VALUES ('1', '3');
INSERT INTO `appli_maintenance`.`stade_section` (`stade_id`, `section_id`) VALUES ('1', '4');
INSERT INTO `appli_maintenance`.`stade_section` (`stade_id`, `section_id`) VALUES ('1', '5');
INSERT INTO `appli_maintenance`.`stade_section` (`stade_id`, `section_id`) VALUES ('1', '6');
INSERT INTO `appli_maintenance`.`stade_section` (`stade_id`, `section_id`) VALUES ('2', '1');
INSERT INTO `appli_maintenance`.`stade_section` (`stade_id`, `section_id`) VALUES ('2', '2');
INSERT INTO `appli_maintenance`.`stade_section` (`stade_id`, `section_id`) VALUES ('2', '3');
INSERT INTO `appli_maintenance`.`stade_section` (`stade_id`, `section_id`) VALUES ('2', '4');

INSERT INTO `appli_maintenance`.`equipment` (`id`, `name`, `section_id`, `stade_id`) VALUES ('1', 'Camion KOM1', '1', '2');
INSERT INTO `appli_maintenance`.`equipment` (`id`, `name`, `section_id`, `stade_id`) VALUES ('2', 'Camion KOM2', '1', '2');
INSERT INTO `appli_maintenance`.`equipment` (`id`, `name`, `section_id`, `stade_id`) VALUES ('3', 'Camion Terex 1', '1', '2');
INSERT INTO `appli_maintenance`.`equipment` (`id`, `name`, `section_id`, `stade_id`) VALUES ('4', 'Camion Terex 2', '1', '2');
INSERT INTO `appli_maintenance`.`equipment` (`id`, `name`, `section_id`, `stade_id`) VALUES ('5', 'Dragline M1', '1', '1');
INSERT INTO `appli_maintenance`.`equipment` (`id`, `name`, `section_id`, `stade_id`) VALUES ('6', 'Dragline M2', '1', '1');
INSERT INTO `appli_maintenance`.`equipment` (`id`, `name`, `section_id`, `stade_id`) VALUES ('7', 'Dragline PH1', '1', '1');
INSERT INTO `appli_maintenance`.`equipment` (`id`, `name`, `section_id`, `stade_id`) VALUES ('8', 'Dragline PH2', '1', '1');
INSERT INTO `appli_maintenance`.`equipment` (`id`, `name`, `section_id`, `stade_id`) VALUES ('9', 'Bulldozer D11', '1', '2');
INSERT INTO `appli_maintenance`.`equipment` (`id`, `name`, `section_id`, `stade_id`) VALUES ('10', 'Bulldozer D9', '1', '2');
INSERT INTO `appli_maintenance`.`equipment` (`id`, `name`, `section_id`, `stade_id`) VALUES ('11', 'Chargeuse F1', '1', '2');
INSERT INTO `appli_maintenance`.`equipment` (`id`, `name`, `section_id`, `stade_id`) VALUES ('12', 'Chargeuse F2', '1', '2');
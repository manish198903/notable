CREATE TABLE IF NOT EXISTS `notable`.`doctors` (
    `id`                                bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    `first_name`                        varchar(64)         NOT NULL,
    `last_name`                         varchar(64)         NOT NULL,
    `created_at`                        timestamp(3)        NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `updated_at`                        timestamp(3)        NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`)

) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `notable`.`appointments` (
    `id`                                bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    `doctor_id`                         bigint(20) unsigned NOT NULL,
    `patient_first_name`                varchar(64)         NOT NULL,
    `patient_last_name`                 varchar(64)         NOT NULL,
    `time`                              timestamp(3)        NOT NULL,
    `kind`                              varchar(64)         NOT NULL,
    `created_at`                        timestamp(3)        NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `updated_at`                        timestamp(3)        NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`),
    INDEX `doctor_appointment` (`doctor_id`, `id`),
    FOREIGN KEY (`doctor_id`) REFERENCES `notable`.`doctors`(id) ON DELETE CASCADE

) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

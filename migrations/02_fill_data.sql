--
-- Up
--

SET FOREIGN_KEY_CHECKS = 0;
START TRANSACTION;
-- ----------------------------
-- Records of problem
-- ----------------------------
INSERT INTO `problem` (problem_id, description)
VALUES
    (1, 'No such file or directory'),
    (2, 'Permission denied'),
    (3, 'command not found'),
    (4, 'user sit is currently used by process'),
    (5, 'Operation not permitted'),
    (6, 'Cannot get exclusive access to /dev/md0:Perhaps a running process, mounted filesystem or active volume group?'),
    (7, 'Can''t initialize physical volume'),
    (8, 'not mounted'),
    (9, 'special device /dev/mapper/truecrypt1 does not exist');

-- ----------------------------
-- Records of recommendation
-- ----------------------------
INSERT INTO `recommendation` (recommendation_id, recommendation)
VALUES
    (1, 'Проверьте правильность введенного названия папки/файла'),
    (2, 'Проверьте правильность введенного пути. Если путь относительный, проверьте его относительно текущей директории (используйте команду pwd, чтобы узнать ее)'),
    (3, 'Отредактируйте права на файл/папку с помощью команды chmod. Проверить права можно командой ls -l'),
    (4, 'Добавьте sudo в начало команды и попробуйте снова'),
    (5, 'Проверьте правильность введенной команды'),
    (6, 'Необходимо разлогинить удаляемого пользователя'),
    (7, 'Добавьте флаг -f к команде (это может быть опасно)'),
    (8, 'Завершите указанный процесс (с помощью команды kill -9 <pid>, где pid - номер процесса)'),
    (9, 'Отмонтируйте указанный диск с помощью команды umount'),
    (10, 'Проверьте, что работаете с нужным диском'),
    (11, 'Попробуйте следующие команды (они удалят таблицу разделов): ''sudo dd if=/dev/zero of=/dev/sd* bs=1k count=1'', ''sudo blockdev --rereadpt /dev/sd*'''),
    (12, 'Примонтируйте диск с помошью команды mount'),
    (13, 'Попробуйте команду (вместо mount) sudo truecrypt -k <путь к файлу-ключу> /dev/sd* <точка монтирования>');

-- ----------------------------
-- Records of problem_recommendation
-- ----------------------------
INSERT INTO `problem_recommendation`
VALUES
    (1, 1, 1),
    (1, 2, 2),
    (2, 3, 1),
    (2, 4, 2),
    (3, 5, 2),
    (4, 6, 3),
    (4, 7, 2),
    (4, 8, 1),
    (3, 4, 1),
    (5, 4, 2),
    (6, 9, 2),
    (6, 8, 1),
    (7, 10, 2),
    (7, 11, 1),
    (8, 12, 2),
    (9, 13, 2),
    (9, 1, 1);

COMMIT;
SET FOREIGN_KEY_CHECKS = 1;
--
-- Down
--
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE `problem_recommendation`;
TRUNCATE TABLE `problem`;
TRUNCATE TABLE `recommendation`;
SET FOREIGN_KEY_CHECKS = 1;
INSERT INTO problem VALUES
    (NULL, 'No such file or directory'),
    (NULL, 'Permission denied'),
    (NULL, 'command not found'),
    (NULL, 'user sit is currently used by process'),
    (NULL, 'Operation not permitted'),
    (NULL, 'Cannot get exclusive access to /dev/md0:Perhaps a running process, mounted filesystem or active volume group?'),
    (NULL, 'Can''t initialize physical volume'),
    (NULL, 'not mounted'),
    (NULL, 'special device /dev/mapper/truecrypt1 does not exist');

INSERT INTO recommendation VALUES
    (NULL, 'Проверьте правильность введенного названия папки/файла'),
    (NULL, 'Проверьте правильность введенного пути. Если путь относительный, проверьте его относительно текущей директории (используйте команду pwd, чтобы узнать ее)'),
    (NULL, 'Отредактируйте права на файл/папку с помощью команды chmod. Проверить права можно командой ls -l'),
    (NULL, 'Добавьте sudo в начало команды и попробуйте снова'),
    (NULL, 'Проверьте правильность введенной команды'),
    (NULL, 'Необходимо разлогинить удаляемого пользователя'),
    (NULL, 'Добавьте флаг -f к команде (это может быть опасно)'),
    (NULL, 'Завершите указанный процесс (с помощью команды kill -9 <pid>, где pid - номер процесса)'),
    (NULL, 'Отмонтируйте указанный диск с помощью команды umount'),
    (NULL, 'Проверьте, что работаете с нужным диском'),
    (NULL, 'Попробуйте следующие команды (они удалят таблицу разделов): ''sudo dd if=/dev/zero of=/dev/sd* bs=1k count=1'', ''sudo blockdev --rereadpt /dev/sd*'''),
    (NULL, 'Примонтируйте диск с помошью команды mount'),
    (NULL, 'Попробуйте команду (вместо mount) sudo truecrypt -k <путь к файлу-ключу> /dev/sd* <точка монтирования>');

INSERT INTO problem_recommendation VALUES
    (1, 1, 1),
    (1, 2, 2),
    (2, 3, 1),
    (2,	4, 2),
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
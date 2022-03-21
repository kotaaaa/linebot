use linebot;
CREATE TABLE if not exists `testTable`(
    `id` int(11),
    `name` varchar(30)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE if not exists `itemTable`(
    `main_key` int(11) AUTO_INCREMENT NOT NULL,
    `user_id` varchar(50),
    `item` varchar(50),
    `todo_flg` int(11),
    PRIMARY KEY (`main_key`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;


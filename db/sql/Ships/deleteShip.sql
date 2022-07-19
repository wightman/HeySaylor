DROP PROCEDURE deleteShip;
DELIMITER //
CREATE PROCEDURE deleteShip(
    sId INT
) 
BEGIN 
    DELETE
        FROM Ships
        WHERE shipId = sId;
    IF(ROW_COUNT() = 0) THEN
        SIGNAL SQLSTATE '51104'
            SET MESSAGE_TEXT = 'Ship not removed.';
  END IF;
END//
DELIMITER ;
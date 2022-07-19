DROP PROCEDURE updateShip;
DELIMITER //
CREATE PROCEDURE updateShip(
    sId INT,
    sName VARCHAR(45),
    sYear SMALLINT,
    eYear SMALLINT,
    note TEXT,
    uID INT
) 
BEGIN 
    UPDATE Ships
        SET shipName = sName,
            startYear =sYear,
            endYear = eYear,
            notes = note
        WHERE shipId = sId;
    IF(ROW_COUNT() = 0) THEN
        SIGNAL SQLSTATE '51103'
            SET MESSAGE_TEXT = 'Ship not updated.';
  END IF;
END//
DELIMITER ;
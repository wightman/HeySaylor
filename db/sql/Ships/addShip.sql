DROP PROCEDURE addShip;
DELIMITER //
CREATE PROCEDURE addShip(
    sName VARCHAR(45),
    sYear SMALLINT,
    eYear SMALLINT,
    note TEXT,
    uID INT
) 
BEGIN 
    INSERT INTO Ships (shipName, startYear, endYear, notes, createdBy) 
        VALUES (sName, sYear, eYear, note, uID); 
    IF(ROW_COUNT() = 0) THEN
    SIGNAL SQLSTATE '51101'
    SET MESSAGE_TEXT = 'Ship not added.';
  END IF;
END//
DELIMITER ;

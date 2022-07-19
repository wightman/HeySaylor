DROP PROCEDURE addSaylor;
DELIMITER //
CREATE PROCEDURE addSaylor(
    sRef VARCHAR(45),
    sCourt CHAR(1),
    sFName VARCHAR(45),
    sLName VARCHAR(45),
    sShipName VARCHAR(45),
    sDoW DATE,
    sDoP DATE,
    sRole VARCHAR(45),
    sMarried TINYINT(4),
    sNote TEXT,
    uID INT
) 
BEGIN 
    INSERT INTO Saylors (reference, court, nameFirst, nameLast, shipName, dateOfWill, 
        dateOfProbate, role, married, notes, createdBy) 
        VALUES (sRef, sCourt, sFName, sLName, sShipName, sDoW, sDoP, sRole, sMarried, sNote, uID); 
    IF(ROW_COUNT() = 0) THEN
    SIGNAL SQLSTATE '51501'
    SET MESSAGE_TEXT = 'Saylor not added.';
  END IF;
END//
DELIMITER ;

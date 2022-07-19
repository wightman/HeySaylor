DROP PROCEDURE IF EXISTS addWill;
DELIMITER //
CREATE PROCEDURE addWill(
    sayId INT,
    wNum INT,
    docName VARCHAR(60),
    doP DATE,
    note TEXT,
    creator INT
) 
BEGIN 
    INSERT INTO Wills (saylorId, willNum, documentName, dateOfProbate, notes, createdBy) 
        VALUES (sayId, wNum, docName, doP, note, creator); 
    IF(ROW_COUNT() = 0) THEN
       SIGNAL SQLSTATE '51601'
       SET MESSAGE_TEXT = 'Will not added.';
    END IF;
END//
DELIMITER ;

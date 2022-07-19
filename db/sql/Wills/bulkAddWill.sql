DROP PROCEDURE IF EXISTS bulkAddWill;
DELIMITER //
CREATE PROCEDURE bulkAddWill(
    sayId INT,
    wNum INT,
    docName VARCHAR(60),
    creator INT
) 
BEGIN 
    SELECT dateOfProbate
        INTO @dop
        FROM Saylors
        WHERE saylorId = sayId;
        
    CALL addWill(sayId, wNum, docName, @dop, NULL,creator);
    
    IF(ROW_COUNT() = 0) THEN
       SIGNAL SQLSTATE '51601'
       SET MESSAGE_TEXT = 'Will not added.';
    END IF;
END//
DELIMITER ;

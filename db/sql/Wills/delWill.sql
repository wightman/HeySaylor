DROP PROCEDURE IF EXISTS delWill;
DELIMITER //
CREATE PROCEDURE delWill(
    sayId INT,
    wNum INT
) 
BEGIN 
    DELETE 
        FROM Wills
        WHERE sayId = saylorId AND wNum = willNum;
        
    IF(ROW_COUNT() = 0) THEN
       SIGNAL SQLSTATE '54601'
       SET MESSAGE_TEXT = 'Will not deleted.';
    END IF;
END//
DELIMITER ;

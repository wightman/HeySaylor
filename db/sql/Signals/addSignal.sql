DROP PROCEDURE addSignal;
DELIMITER //
CREATE PROCEDURE addSignal(
    sigId INT, sigText TEXT
) 
BEGIN 
    INSERT INTO Signals VALUES (sigId, sigText); 
    IF(ROW_COUNT() = 0) THEN
        SIGNAL SQLSTATE '45001'
            SET MESSAGE_TEXT = 'Signal not added.';
    END IF;
    SELECT sigId;
END//
DELIMITER ;

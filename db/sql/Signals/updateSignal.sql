DROP PROCEDURE updateSignal;
DELIMITER //
CREATE PROCEDURE updateSignal(
    oldSigId INT,
    newSigId INT, 
    sigText TEXT
) 
BEGIN 
    UPDATE Signals 
        SET signalId = newSigId,
            description =  sigText
        WHERE signalId = oldSigId;
 
    IF(ROW_COUNT() = 0) THEN
        SIGNAL SQLSTATE '45001'
            SET MESSAGE_TEXT = 'Signal not updated.';
    END IF;

END//
DELIMITER ;

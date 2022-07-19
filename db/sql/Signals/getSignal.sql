DROP PROCEDURE getSignal;
DELIMITER //
CREATE PROCEDURE getSignal(
    sigId INT
) 
BEGIN 
    SELECT * 
        FROM Signals 
        WHERE signalId = sigId; 

    IF(FOUND_ROWS() = 0) THEN
        SIGNAL SQLSTATE '45001'
            SET MESSAGE_TEXT = 'No signal found.';
    END IF;
END//
DELIMITER ;

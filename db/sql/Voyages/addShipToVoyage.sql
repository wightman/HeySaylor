DROP PROCEDURE addShipToVoyage;
DELIMITER //
CREATE PROCEDURE addShipToVoyage(
    sId INT,
    vId INT
) 
BEGIN 
    INSERT INTO Fleets (shipId, VoyageId)
        VALUES (sId, vId); 
    IF(ROW_COUNT() = 0) THEN
    SIGNAL SQLSTATE '51201'
    SET MESSAGE_TEXT = 'Unable to add ship to voyage.';
  END IF;
END//
DELIMITER ;

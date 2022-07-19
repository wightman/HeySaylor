DROP PROCEDURE getShipByName;
DELIMITER //
CREATE PROCEDURE getShipByName
(
  IN sName VARCHAR(45)
)
/*  Collaborations identifies all lists that a particular user has access to.
 *  Each list identifies it's owner.
 */
BEGIN
SELECT shipId, shipName, startYear, endYear, notes, 
    Ships.dateCreated, username, Ships.dateModified 
    FROM Ships JOIN Users ON (userId = createdBy) 
    WHERE shipName = sName;

  IF(FOUND_ROWS() = 0) THEN
    SIGNAL SQLSTATE '45002'
    SET MESSAGE_TEXT = 'Ship not found.';
  END IF;

   
END //
DELIMITER ;

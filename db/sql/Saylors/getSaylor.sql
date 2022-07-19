DROP PROCEDURE getSaylor;
DELIMITER //
CREATE PROCEDURE getSaylor
(
  sId INT
)
/*  
 * Return all Saylor records, with createdBy name instead of userId
 */
BEGIN
  SELECT saylorId, reference, court, nameFirst, nameLast, testator, shipName, 
    dateOfWill, dateOfProbate, role, married, notes, creationDate, lastModified, userName As createdBy
    FROM Saylors JOIN Users ON createdBy = userId
    WHERE saylorId = sId;   

  IF(FOUND_ROWS() = 0) THEN
    SIGNAL SQLSTATE '52501'
    SET MESSAGE_TEXT = 'Saylor not found.';
  END IF;
END //
DELIMITER ;

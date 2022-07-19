DROP PROCEDURE getSaylors;
DELIMITER //
CREATE PROCEDURE getSaylors()
/*  
 * Return all Saylor records, with createdBy name instead of userId
 */
BEGIN
  SELECT saylorId, reference, court, nameFirst, nameLast, testator, shipName, 
    dateOfWill, dateOfProbate, role, married, notes, creationDate, lastModified, userName As createdBy
    FROM Saylors JOIN Users ON createdBy = userId;   
END //
DELIMITER ;

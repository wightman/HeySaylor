DROP PROCEDURE getSaylorsComponent;
DELIMITER //
CREATE PROCEDURE getSaylorsComponent()
/*  
 * Return all Saylor records, with createdBy name instead of userId, and with Will information
 */
BEGIN
  SELECT Saylors.saylorId, reference, court, nameFirst, nameLast, testator, shipName, 
      Saylors.dateOfWill, Saylors.dateOfProbate, role, married, Saylors.notes, Saylors.creationDate, 
      Saylors.lastModified, userName As 'createdBy', documentName
    FROM Saylors JOIN Users ON Saylors.createdBy = userId 
      LEFT JOIN Wills ON Saylors.saylorId = Wills.saylorId
    WHERE Wills.willNum = 1 OR willNum IS NULL
    ORDER BY saylorId;   
END //
DELIMITER ;

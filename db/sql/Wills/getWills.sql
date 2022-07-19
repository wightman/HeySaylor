DROP PROCEDURE getWills;
DELIMITER //
CREATE PROCEDURE getWills()
/*  
 * Return all Saylor records, with createdBy name instead of userId
 */
BEGIN
  SELECT *
     FROM Wills;   
END //
DELIMITER ;

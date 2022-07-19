DROP PROCEDURE getShip;
DELIMITER //
CREATE PROCEDURE getShip
(
  IN sId INT
)
/*  Collaborations identifies all lists that a particular user has access to.
 *  Each list identifies it's owner.
 */
BEGIN
   SELECT *
    FROM Ships 
    WHERE shipId = sId;

  IF(FOUND_ROWS() = 0) THEN
    SIGNAL SQLSTATE '51201'
    SET MESSAGE_TEXT = 'Ship not found.';
  END IF;

   
END //
DELIMITER ;

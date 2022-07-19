DROP PROCEDURE getWill;
DELIMITER //
CREATE PROCEDURE getWill
(
  sId INT,
  wNum INT
)
/*  
 * Return all Will record by saylorId and willNum (Remember that willNum is not unique)
 */
BEGIN
  SELECT *
    FROM Wills
    WHERE saylorId = sId AND willNum = wNum;   
  IF(FOUND_ROWS() = 0) THEN
    SIGNAL SQLSTATE '52601'
    SET MESSAGE_TEXT = 'Will not found.';
  END IF;
END //
DELIMITER ;

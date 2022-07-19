DROP PROCEDURE getShipsByVoyage;
DELIMITER //
CREATE PROCEDURE getShipsByVoyage
(
  IN vId INT
)
/*  Collaborations identifies all lists that a particular user has access to.
 *  Each list identifies it's owner.
 */
BEGIN
  SELECT *
    FROM Ships NATURAL JOIN Fleets
    WHERE voyageId = vId;

  IF(FOUND_ROWS() = 0) THEN
    SIGNAL SQLSTATE '51202'
    SET MESSAGE_TEXT = 'No ships found.';
  END IF;

   
END //
DELIMITER ;

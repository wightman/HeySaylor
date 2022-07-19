DELIMITER //

DROP PROCEDURE IF EXISTS checkCredentials//

CREATE PROCEDURE checkCredentials
(
    user VARCHAR(45),
    pw VARCHAR(100)
)
BEGIN
    SELECT userId, userName, userEmail
        FROM Users
        WHERE userEmail = user AND pass = pw;

    IF FOUND_ROWS() = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Incorrect credentials';
    END IF;
END//

DELIMITER ;


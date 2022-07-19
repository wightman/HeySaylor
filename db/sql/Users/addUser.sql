DROP PROCEDURE addUser;
DELIMITER //
CREATE PROCEDURE addUser(
    uName VARCHAR(45),
    uEmail VARCHAR(255),
    uPass varchar(100)
) 
BEGIN 
    INSERT INTO Users (userName, userEmail, pass) 
        VALUES (uName, uEmail, uPass); 
    IF(ROW_COUNT() = 0) THEN
    SIGNAL SQLSTATE '55555'
    SET MESSAGE_TEXT = 'User not added.';
  END IF;
END//
DELIMITER ;

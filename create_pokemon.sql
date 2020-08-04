
-- CREATE DATABASE pokemon_data;

USE pokemon_data;
DROP TABLE Owned_by;
DROP TABLE Of_type;
DROP TABLE Pokemon;
DROP TABLE Trainer;
DROP TABLE Types;

CREATE TABLE Pokemon
(
    id INT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    height INT NOT NULL,
    weight INT NOT NULL
);


CREATE TABLE Trainer
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    town VARCHAR(20),
);


CREATE TABLE Owned_by
(
    pokemon_id INT,
    trainer_id INT,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY (trainer_id) REFERENCES trainer(id),
    PRIMARY KEY(pokemon_id,trainer_id)
);


CREATE TABLE Types
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL
);


CREATE TABLE Of_type
(
    pokemon_id INT,
    type_id INT,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY (type_id) REFERENCES types(id),
    PRIMARY KEY(pokemon_id,type_id)
);
USE pokemon_data;
DELETE FROM Owned_by O
WHERE O.pokemon_id = 1 AND O.trainer_id = 1

DELETE FROM Owned_by
WHERE pokemon_id = 1 AND trainer_id = 1;

-- SELECT COUNT(*) FROM pokemon;
-- SELECT COUNT(*) FROM trainer;
-- SELECT COUNT(*) FROM owned_by;
-- SELECT COUNT(*) FROM types;
-- SELECT COUNT(*) FROM of_type;

-- VIEW Pok_with_type AS
-- SELECT *
-- FROM Pokemon P JOIN Of_type O on P.id = O.pokemon_id

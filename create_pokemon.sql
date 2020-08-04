
-- CREATE DATABASE pokemon_data;

USE pokemon_data;


DROP TABLE owned_by;
DROP TABLE of_type;
DROP TABLE pokemon;
DROP TABLE trainer;
DROP TABLE types;


CREATE TABLE pokemon
(
    id INT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    height INT NOT NULL,
    weight INT NOT NULL
);


CREATE TABLE trainer
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    town VARCHAR(20),
    UNIQUE(name, town)
);


CREATE TABLE owned_by
(
    pokemon_id INT,
    pokemon_name INT,
    trainer_id INT,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY (trainer_id) REFERENCES trainer(id),
    UNIQUE( pokemon_name, trainer_id)
);


CREATE TABLE types
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL
);


CREATE TABLE of_type
(
    pokemon_id INT,
    type_id INT,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY (type_id) REFERENCES types(id)
);



-- SELECT COUNT(*) FROM pokemon;
-- SELECT COUNT(*) FROM trainer;
-- SELECT COUNT(*) FROM owned_by;
-- SELECT COUNT(*) FROM types;
-- SELECT COUNT(*) FROM of_type;


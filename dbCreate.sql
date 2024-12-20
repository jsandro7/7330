CREATE SCHEMA IF NOT EXISTS degrees;

USE degrees;

-- CREATE USER IF NOT EXISTS '7330Team'@'localhost' IDENTIFIED BY 'Smu-Team2024!';

-- GRANT ALL PRIVILEGES ON degrees.* TO '7330Team'@'localhost';
DROP TABLE IF EXISTS `evaluation`;
DROP TABLE IF EXISTS `goal`;
DROP TABLE IF EXISTS `degree_course`;
DROP TABLE IF EXISTS `degree`;
DROP TABLE IF EXISTS `section`;
DROP TABLE IF EXISTS `instructor`;
DROP TABLE IF EXISTS `course`;

-- Creating degree table
CREATE TABLE IF NOT EXISTS degree (
    name VARCHAR(255),
    level VARCHAR(255),
    PRIMARY KEY (name, level)
);

-- Creating course table
CREATE TABLE IF NOT EXISTS course (
    course_id CHAR(9) PRIMARY KEY,
    name VARCHAR(255)
);

-- Creating degree_course table
CREATE TABLE IF NOT EXISTS degree_course (
    name VARCHAR(255),
    level VARCHAR(255),
    course_id CHAR(9),
    is_core BIT DEFAULT 0,
    PRIMARY KEY (name, level, course_id),
    CONSTRAINT FK_degree_course_name FOREIGN KEY (name, level) REFERENCES degree(name, level),   
    CONSTRAINT FK_degree_course_course_id FOREIGN KEY (course_id) REFERENCES course(course_id)
);


-- Creating degree table
CREATE TABLE IF NOT EXISTS instructor (
	ID CHAR(8) PRIMARY KEY,
    name VARCHAR(255)
);

-- Creating section table
CREATE TABLE IF NOT EXISTS section (
    section_id CHAR(3) PRIMARY KEY,
    course_id CHAR(9),
    ID CHAR(8),
    semester CHAR(2),
	year CHAR(4),
    student_enrolled INT,
    CONSTRAINT FK_section_course_id FOREIGN KEY (course_id) REFERENCES course(course_id),
    CONSTRAINT FK_section_ID FOREIGN KEY (ID) REFERENCES instructor(ID)
);

-- Creating goal table
CREATE TABLE IF NOT EXISTS goal (
    code CHAR(4) PRIMARY KEY,    
    name VARCHAR(255),
    level VARCHAR(255),
    course_id CHAR(9),
    description TEXT,
    PRIMARY KEY (code, name, level),
    CONSTRAINT FK_goal_name FOREIGN KEY (name, level) REFERENCES degree(name, level),
    CONSTRAINT FK_goal_course FOREIGN KEY (course_id) REFERENCES course(course_id)
);

-- Creating goal table
CREATE TABLE IF NOT EXISTS evaluation (
    section_id CHAR(3),
    code CHAR(4),
    name VARCHAR(255),
    level VARCHAR(255),    
    evaluation_method VARCHAR(255),
    comment TEXT,
    A_count INT,
	B_count INT,
    C_count INT,
    F_count INT,
    PRIMARY KEY (section_id, code, name, level),
    CONSTRAINT FK_evaluation_section_id FOREIGN KEY (section_id) REFERENCES section(section_id),
    CONSTRAINT FK_evaluation_goal FOREIGN KEY (code, name, level) REFERENCES goal(code, name, level)
);


CREATE TABLE IF NOT EXISTS eval_methods(
	name VARCHAR(50),
	PRIMARY KEY(name)
)


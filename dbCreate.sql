CREATE SCHEMA IF NOT EXISTS degrees;

USE degrees;

DROP TABLE IF EXISTS `degree_course`;
DROP TABLE IF EXISTS `teaches`;
DROP TABLE IF EXISTS `section`;
DROP TABLE IF EXISTS `course`;
DROP TABLE IF EXISTS `semester`;
DROP TABLE IF EXISTS `evaluation`;
DROP TABLE IF EXISTS `goal`;
DROP TABLE IF EXISTS `degree`;
DROP TABLE IF EXISTS `instructor`;

-- Creating degree table
CREATE TABLE IF NOT EXISTS degree (
    name VARCHAR(255) PRIMARY KEY,
    level VARCHAR(255)
);

-- Creating course table
CREATE TABLE IF NOT EXISTS course (
    course_id INT PRIMARY KEY,
    name VARCHAR(255)
);

-- Creating degree_course table
CREATE TABLE IF NOT EXISTS degree_course (
    name VARCHAR(255),
    course_id INT,
    PRIMARY KEY (name, course_id),
    CONSTRAINT FK_degree_course_name FOREIGN KEY (name) REFERENCES degree(name),
    CONSTRAINT FK_degree_course_course_id FOREIGN KEY (course_id) REFERENCES course(course_id)
);


-- Creating degree table
CREATE TABLE IF NOT EXISTS semester (
	semester_code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255),
    level VARCHAR(255)
);

-- Creating degree table
CREATE TABLE IF NOT EXISTS instructor (
	ID INT PRIMARY KEY,
    name VARCHAR(255)
);

-- Creating section table
CREATE TABLE IF NOT EXISTS section (
    section_id VARCHAR(50) PRIMARY KEY,
    course_id INT,
    semester_code VARCHAR(10),
    student_enrolled INT,
    CONSTRAINT FK_section_semester FOREIGN KEY (semester_code) REFERENCES semester(semester_code),
    CONSTRAINT FK_section_course_id FOREIGN KEY (course_id) REFERENCES course(course_id)
);


-- Creating teaches table
CREATE TABLE IF NOT EXISTS teaches (
    section_id VARCHAR(50),
    course_id INT,
    semester_code VARCHAR(10),
    ID INT,
    PRIMARY KEY (section_id, course_id, semester_code, ID),
    CONSTRAINT FK_teaches_semester FOREIGN KEY (semester_code) REFERENCES semester(semester_code),
    CONSTRAINT FK_teaches_course_id FOREIGN KEY (course_id) REFERENCES course(course_id),
	CONSTRAINT FK_teaches_section_id FOREIGN KEY (section_id) REFERENCES section(section_id),
    CONSTRAINT FK_teaches_ID FOREIGN KEY (ID) REFERENCES instructor(ID)
);


-- Creating goal table
CREATE TABLE IF NOT EXISTS goal (
    code VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    level VARCHAR(255),
    description TEXT,
    CONSTRAINT FK_goal_name FOREIGN KEY (name) REFERENCES degree(name)
);

-- Creating goal table
CREATE TABLE IF NOT EXISTS evaluation (
    ID INT,
    code VARCHAR(50),
    comment TEXT,
    number_A_students INT,
	number_B_students INT,
    number_C_students INT,
    number_F_students INT,
    PRIMARY KEY (ID, code),
    CONSTRAINT FK_evaluation_ID FOREIGN KEY (ID) REFERENCES instructor(ID),
    CONSTRAINT FK_evaluation_code FOREIGN KEY (code) REFERENCES goal(code)
);

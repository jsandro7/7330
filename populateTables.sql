INSERT INTO degree (
    name,
    level
)
VALUES
	('Computer Science','BA'),
    ('Computer Science','BS'), 
    ('Computer Science','MS'),
    ('Computer Science','Ph.D'),
    ('Electrical & Computer Engineering','BS'), 
    ('Electrical Engineering','MS'),
    ('Computer Engineering','Ph.D');
    

INSERT INTO goal(
	code,
	name,
    level,
    description
)
VALUES
('112A', 'Computer Science','BS', 'Goal for BS CS'),
('235B', 'Computer Science','MS', 'Goal for MS CS'),
('3569','Computer Science','Ph.D', 'Goal for Ph.D CS');

INSERT INTO course 
(
    course_id,
    name
)
VALUES 
	('CS7330','File Organ Data Base Man'), 
	('CS5330', 'File Organ Data Base Man'), 
    ('CS3330', 'File Organ Data Base Man'), 
    ('CS7343', 'Operating Systems'), 
    ('CS5343','Operating Systems');

INSERT INTO degree_course 
(
   level,
   name,
   course_id
)
VALUES 
	('BS','Computer Science','CS5330'), 
	('BA','Computer Science','CS3330'),
    ('MS','Computer Science','CS7330'), 
    ('MS','Computer Science','CS7343'), 
    ('BS','Computer Science','CS5343'),
    ('BS','Electrical & Computer Engineering','CS7343');
    
    
    
INSERT INTO instructor (
	ID,
    name
)
VALUES
	(2156,'Shaibal Chakrabarty'),
    (5355,'King Ip Lin');


INSERT INTO section (
    section_id,
    course_id,
    ID,
    semester,
	year,
    student_enrolled
)
VALUES
	('405','CS7330',5355,'SP', 2024,31),
    ('415','CS7343',2156,'FA',2024,27),
    ('425','CS5343',5355,'SM',2024,21);
    



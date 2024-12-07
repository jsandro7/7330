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
	(21561234,'Shaibal Chakrabarty'),
    (53551234,'King Ip Lin');


INSERT INTO section (
    section_id,
    course_id,
    ID,
    semester,
	year,
    student_enrolled
)
VALUES
	('405','CS7330',53551234,'SP', 2024,31),
    ('415','CS7343',21561234,'FA',2024,27),
    ('425','CS5343',53551234,'SM',2024,21);
    

INSERT INTO evaluation(
	section_id,
    code,
    evaluation_method,
    comment,
    A_count,
    B_count,
    C_count,
    F_count
)
VALUES
('405', '112A','Report', 'Testing comments', 11, 12, 5, 7),
('415', '235B','Homework', 'Testing comments 2', 21, 2, 3, 1);
    



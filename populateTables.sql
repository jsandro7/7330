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
	goal,
	name,
    level,
    description
)
VALUES
('112A', 'Computer Science','BS', 'Goal for BS CS'),
('235B', 'Computer Science','MS', 'Goal for MS CS'),
('3569','Computer Science','Ph.D', 'Goal for Ph.D CS');

INSERT INTO course (
    course_id,
    name)
VALUES 
	('001C-7330','File Organ Data Base Man'), 
	('001C-5330', 'File Organ Data Base Man'), 
    ('001C-3330', 'File Organ Data Base Man'), 
    ('401-7343', 'Operating Systems'), 
    ('401-5343','Operating Systems');

INSERT INTO degree_course (
   level,
   name,
   course_id
)
VALUES 
	('BS','Computer Science','001C-5330'), 
	('BA','Computer Science','001C-3330'),
    ('MS','Computer Science','001C-7330'), 
    ('MS','Computer Science','401-7343'), 
    ('BS','Computer Science','401-5343'),
    ('BS','Electrical & Computer Engineering','401-7343');
    

INSERT INTO semester (
	semester_code,    
    name
)
VALUES
	('2024-SPG','Spring'),
    ('2024-SUM', 'Summer'),
    ('2024-FAL','Fall');
    
    
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
    semester_code,
    student_enrolled
)
VALUES
	('405','001C-7330','2024-SPG',31),
    ('415','401-7343', '2024-SPG',27),
    ('425','401-5343', '2024-SPG',21);
    
INSERT INTO teaches (
    section_id,
    course_id,
    semester_code,
    ID
)
VALUES
	('405','001C-7330','2024-SPG',5355),
    ('415','401-7343','2024-SPG',2156);



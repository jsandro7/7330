INSERT INTO degree (
    name,
    level
)
VALUES
	('B.A. Computer Science','BA'),
    ('B.S. Computer Science','BS'), 
    ('M.S. Computer Science','MS'),
    ('Ph.D. Computer Science','Ph.D'),
    ('B.S. Electrical & Computer Engineering','BS'), 
    ('M.S Electrical Engineering','MS'),
    ('Ph.D. Computer Engineering','Ph.D');

INSERT INTO course (
    course_id,
    name)
VALUES 
	(7330,'File Organ Data Base Man'), 
	(5330, 'File Organ Data Base Man'), 
    (3330, 'File Organ Data Base Man'), 
    (7343, 'Operating Systems'), 
    (5343,'Operating Systems');

INSERT INTO degree_course (
    name,
    course_id
)
VALUES 
	('B.S. Computer Science',5330), 
	('B.A. Computer Science',3330),
    ('M.S. Computer Science',7330), 
    ('M.S. Computer Science',7343), 
    ('B.S. Computer Science',5343),
    ('B.S. Electrical & Computer Engineering',7343);
    

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
	('405',7330,'2024-SPG',31),
    ('415',7343, '2024-SPG',27),
    ('425',5330, '2024-SPG',21);
    
INSERT INTO teaches (
    section_id,
    course_id,
    semester_code,
    ID
)
VALUES
	('405',7330,'2024-SPG',5355),
    ('415',7343,'2024-SPG',2156);

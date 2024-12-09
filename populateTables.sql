-- Degrees
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
    ('Computer Engineering','Ph.D'),
    ('Software Engineering','BS'),
    ('Software Engineering','MS'),
    ('Mechanical Engineering','BS'),
    ('Mechanical Engineering','MS'),
    ('Data Science','BS'),
    ('Data Science','MS');



-- Courses
INSERT INTO course 
(
    course_id,
    name
)
VALUES 
    ('CS7330', 'File Organization Database Management'), 
    ('CS5330', 'Introduction to Databases'), 
    ('CS3330', 'Foundations of Computing'), 
    ('CS7343', 'Operating Systems'), 
    ('CS5343', 'Advanced Operating Systems'),
    ('CS1234', 'Artificial Intelligence'),
    ('CS2235', 'Machine Learning'),
    ('EE2345', 'Signal Processing'),
    ('ME3456', 'Thermodynamics'),
    ('DS4567', 'Data Visualization'),
    ('SE5678', 'Agile Development'),
    ('SE6789', 'Software Testing');

-- Degree-Course Relationships
INSERT INTO degree_course 
(
   level,
   name,
   course_id,
   is_core
)
VALUES 
    ('BS','Computer Science','CS5330', 1), 
    ('BA','Computer Science','CS3330', 0),
    ('MS','Computer Science','CS7330', 1), 
    ('MS','Computer Science','CS7343', 0), 
    ('BS','Computer Science','CS5343', 0),
    ('BS','Electrical & Computer Engineering','CS7343', 0),
    ('MS','Software Engineering','SE5678', 0),
    ('BS','Data Science','DS4567', 1),
    ('MS','Data Science','CS2235', 1),
    ('BS','Mechanical Engineering','ME3456', 0),
    ('Ph.D','Computer Science','CS1234', 1);
    
-- Goals
INSERT INTO goal(
    code,
    name,
    level,
    description,
    course_id
)
VALUES
    ('112A', 'Computer Science','BS', 'Goal for BS CS', 'CS5330'),
	('235B', 'Computer Science','MS', 'Goal for MS CS', 'CS7330'),
    ('3569', 'Computer Science','Ph.D', 'Goal for Ph.D CS', 'CS1234'),
    ('457A', 'Electrical & Computer Engineering','BS', 'Goal for BS EE', 'CS7343'),
    ('878C', 'Computer Science','Ph.D', 'Goal for Ph.D CS', 'CS1234'),
    ('678D', 'Software Engineering','MS', 'Goal for MS SE', 'SE5678'),
    ('234B', 'Data Science','MS', 'Goal for MS Data Science', 'CS2235'),
    ('789E', 'Mechanical Engineering','BS', 'Goal for BS ME', 'ME3456');

-- Instructors
INSERT INTO instructor (
    ID,
    name
)
VALUES
    (21561234,'Shaibal Chakrabarty'),
    (53551234,'King Ip Lin'),
    (11223344,'John Doe'),
    (33445566,'Jane Smith'),
    (55667788,'Emily Davis'),
    (66778899,'Michael Brown');

-- Sections
INSERT INTO section (
    section_id,
    course_id,
    ID,
    semester,
    year,
    student_enrolled
)
VALUES
    ('405','CS7330',53551234,'SP',2024,31),
    ('406','CS7330',11223344,'FA',2023,40),
    ('407','CS7330',33445566,'SM',2023,25),
    ('415','CS7343',21561234,'FA',2024,27),
    ('416','CS7343',53551234,'SM',2024,22),
    ('417','CS7343',55667788,'SP',2023,20),
    ('425','CS5343',53551234,'SM',2024,21),
    ('426','CS5343',66778899,'FA',2023,30),
    ('427','CS5343',21561234,'SP',2023,28),
    ('505','CS1234',11223344,'FA',2023,35),
    ('506','CS1234',53551234,'SP',2024,32),
    ('515','CS2235',33445566,'SP',2024,25),
    ('516','CS2235',55667788,'FA',2023,40),
    ('525','EE2345',55667788,'SM',2023,40),
    ('526','EE2345',21561234,'SP',2023,38),
    ('535','ME3456',66778899,'FA',2023,45),
    ('545','DS4567',33445566,'SP',2023,20),
    ('555','SE5678',11223344,'FA',2023,32),
    ('556','SE5678',55667788,'SM',2024,28),
    ('557','SE5678',66778899,'SP',2024,24);

-- Evaluations
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
    -- Complete Evaluations
    ('405', '112A', 'Report', 'Testing comments', 11, 12, 5, 7),
    ('406', '112A', 'Exam', 'Mid-term evaluation', 15, 10, 3, 2),
    ('407', '112A', 'Project', 'Final project', 20, 5, 5, 0),
    ('505', '3569','Exam', 'Ph.D level exam', 15, 5, 1, 2),
    ('506', '112A','Report', 'AI course report', 18, 7, 3, 2),
    ('515', '678D','Project', 'Machine learning project', 18, 6, 1, 0),
    ('516', '678D','Exam', 'ML final exam', 20, 5, 3, 2),
    ('525', '457A','Quiz', 'Signal processing quiz', 10, 15, 5, 1),
    ('526', '457A','Lab', 'Signal processing lab', 14, 12, 4, 0),
    ('535', '789E','Lab', 'Thermodynamics lab', 20, 10, 8, 3),
    ('545', '234B','Presentation', 'Data visualization presentation', 12, 8, 5, 2),
    ('555', '678D','Project', 'Agile development project', 25, 3, 2, 0),
    ('556', '678D','Exam', 'Final exam on agile concepts', 22, 7, 1, 1),
    ('557', '678D','Lab', 'Agile lab sessions', 24, 5, 0, 0),

    -- Partially Entered Evaluations
    ('415', '235B', NULL, 'Testing comments 2', 21, 2, 3, NULL), 
    ('416', '235B', 'Exam', NULL, 12, NULL, 7, 5),               
    ('417', '235B', NULL, NULL, 14, 8, NULL, NULL),              

    -- Not Entered Evaluations
    ('425', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('426', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('427', NULL, NULL, NULL, NULL, NULL, NULL, NULL);

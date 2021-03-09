PRAGMA foreign_keys = ON;

INSERT INTO eposts(epostid, filename, institution, major, start_time, end_time)
VALUES
	(1, 'ndalmia_casual_icon.jpg', 'U-M', 'CS', '2017', '2021');

INSERT INTO wposts(wpostid, filename, company, title, description, location, start_time, end_time)
VALUES
	(1, 'ndalmia_casual_icon_copy.jpg', 'Synapse India', 'Intern', 'Hello from the other side', 'Delhi India', '2021', '2021');

INSERT INTO pposts(ppostid, title, description, location, link)
VALUES
  (1, 'Maze Solver', 'Solving a 3D maze', 'EECS 281', 'https://www.google.com/');

PRAGMA foreign_keys = ON;

CREATE TABLE wposts(
    wpostid INTEGER,
    filename VARCHAR(20) NOT NULL,
    company VARCHAR(40) NOT NULL,
    title VARCHAR(40) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    location VARCHAR(40) NOT NULL,
    start_time VARCHAR(20) NOT NULL,
    end_time VARCHAR(20) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(wpostid)
);

CREATE TABLE pposts(
    ppostid INTEGER,
    title VARCHAR(40) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    location VARCHAR(40) NOT NULL,
    link VARCHAR(200) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(ppostid)
);

CREATE TABLE eposts(
    epostid INTEGER,
    filename VARCHAR(20) NOT NULL,
    institution VARCHAR(40) NOT NULL,
    major VARCHAR(40) NOT NULL,
    start_time VARCHAR(20) NOT NULL,
    end_time VARCHAR(20) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(epostid)
);

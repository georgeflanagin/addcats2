CREATE TABLE faculty_master (
    faculty varchar(20)
    );
CREATE UNIQUE INDEX faculty_idx on faculty_master(faculty);

CREATE TABLE faculty_partitions (
    faculty varchar(20),
    partition varchar(20),
    foreign key(faculty) references faculty_master(faculty)
    );

CREATE TABLE aliases (
    netid varchar(20) primary key, 
    alias_name varchar(20)
    );

CREATE TABLE "faculty_student" (
    faculty varchar(20), 
    student varchar(20), 
    when_added datetime default current_timestamp, 
    foreign key(faculty) references faculty_master(faculty)
    );

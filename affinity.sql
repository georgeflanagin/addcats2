create table faculty_master (
    faculty varchar(20)
    );

create table faculty_partitions (
    faculty varchar(20),
    partition varchar(20),
    foreign key(faculty) references faculty_master(faculty)
    );

create table faculty_student (
    faculty varchar(20),
    student varchar(20),
    foreign key(faculty) references faculty_master(faculty)
    );


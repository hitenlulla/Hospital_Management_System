insert into department values(100, 'ICU', 'First Floor', 'Oxygen Supply, Pulse rate detector, Defibrillator');
insert into department values(101, 'Operation Theatre', 'Fround Floor', 'Surgical Instruments, Anaestetics');
insert into department values(102, 'Pathology', 'Second Floor', 'Centrifuge, Colection vessels');
insert into department values(103, 'Covid Ward', 'Third Floor', 'Oxymeter, Thermal Scanner, Oxygen Supply');
insert into department values(104, 'General Ward', 'First Floor', 'All');

insert into doctor values(1000, 'Hiten Lulla', 'Neuro-Surgeon', 222000, 101);
insert into doctor values(1001, 'Meet Lulla', 'MBBS', 222200, 104);
insert into doctor values(1002, 'Hitesh Wadhwa', 'MBBS', 222220, 103);
insert into doctor values(1003, 'Dakshil Kanakia', 'Orthopedic', 222222, 101);
insert into doctor values(1004, 'Shlok Jethmalani', 'Pathologist', 222223, 102);

insert into on_call_doc values(1001, 1000);
insert into on_call_doc values(1002, 1500);

insert into reg_doc values(1000, 100000);
insert into reg_doc values(1003, 20000);
insert into reg_doc values(1004, 10000);

insert into patient values(10001,'Ashish Bablani','Male',121212,'Ulhasnagar, 421004', '2000-01-10', 20);
insert into patient values(10002,'Ajay Chhabria','Male',122212,'Ulhasnagar, 421004', '2001-02-20', 19);
insert into patient values(10003,'Jivitesh Sachdev','Male',122222,'Ulhasnagar, 421004', '2002-03-30', 18);
insert into patient values(10004,'Dhairya Panjwani','Male',121211,'Ulhasnagar, 421004', '2003-04-15', 17);
insert into patient values(10005,'Hiren Rajwani','Male',121112,'Ulhasnagar, 421004', '2004-05-25', 16);

insert into checkup values(1001,10001,'Penicilin','Mild','Fever');
insert into checkup values(1004,10005,'Blood Test','Mild','Weakness');
insert into checkup values(1002,10002,'Cetrazine','Severe','Cough');
insert into checkup values(1003,10003,'DicloPara','Undefined','Body Pain');
insert into checkup values(1000,10004,'O2','Severe','Stomach Ache');
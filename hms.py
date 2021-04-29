from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import mysql.connector

#Declaring the user-defined exception class
class MyEx(Exception):
	def __init__(self,msg):
		self.msg = msg

# Global Username and Password variables
USERNAME = ''
PASSWORD = ''

#Declaring the Root-Page GUI
login = Tk()
login.title("Login: Using your MySql Credentials")
login.geometry("640x320+350+275")
login.configure(background='#038ed1')

def setCredentials():
	global USERNAME
	USERNAME = ent0.get()

	global PASSWORD
	PASSWORD = ent1.get()

	login.withdraw()
	root.deiconify()

	con = None
	cursor = None
	try:
		con = mysql.connector.connect(user = USERNAME,password = PASSWORD,host = 'localhost')
		print("Connected to MySql")
		cursor = con.cursor()
		
		sql = "create database if not exists hospital;"
		cursor.execute(sql)

		sql = "use hospital;"
		cursor.execute(sql)

		sql = """CREATE TABLE if not exists department(
		d_id int PRIMARY KEY,
		d_name VARCHAR(30),
		d_location VARCHAR(50),
		d_facilities VARCHAR(100)
		);"""
		cursor.execute(sql)

		sql = """CREATE TABLE if not exists doctor(
		dr_id int PRIMARY KEY,
		dr_name VARCHAR(40),
		dr_qualification VARCHAR(20),
		dr_pno int,
		d_id int NOT NULL,
		FOREIGN KEY (d_id) REFERENCES department(d_id) ON DELETE CASCADE
		);"""
		cursor.execute(sql)

		sql = """CREATE TABLE if not exists on_call_doc(
		dr_id int PRIMARY KEY,
		fees_per_visit int NOT NULL,
		FOREIGN KEY (dr_id) REFERENCES doctor(dr_id) ON DELETE CASCADE
		);"""
		cursor.execute(sql)

		sql = """CREATE TABLE if not exists reg_doc(
		dr_id int PRIMARY KEY,
		dr_salary int NOT NULL,
		FOREIGN KEY (dr_id) REFERENCES doctor(dr_id) ON DELETE CASCADE
		);"""
		cursor.execute(sql)

		sql = """CREATE TABLE if not exists patient(
		p_id int PRIMARY KEY,
		p_name VARCHAR(40),
		p_sex enum('Male', 'Female'),
		p_pno int,
		p_address VARCHAR(100),
		p_dob date,
		p_age int
		);"""
		cursor.execute(sql)

		sql = """CREATE TABLE if not exists checkup(
		dr_id int NOT NULL,
		p_id int NOT NULL,
		treatment VARCHAR(30),
		status enum('Severe', 'Mild', 'Undefined'),
		diagnosis VARCHAR(30),
		FOREIGN KEY (p_id) REFERENCES patient(p_id) ON DELETE CASCADE,
		FOREIGN KEY (dr_id) REFERENCES doctor(dr_id) ON DELETE CASCADE
		);"""
		cursor.execute(sql)

		sql = """CREATE TABLE if not exists payment(
		p_id int NOT NULL,
		doc_fees int NOT NULL,
		nur_fees int NOT NULL,
		treat_fees int NOT NULL,
		FOREIGN KEY (p_id) REFERENCES patient(p_id) ON DELETE CASCADE
		);"""
		cursor.execute(sql)

	except Exception as e:
		messagebox.showerror("Error", str(e))
		con.rollback()
	finally:
		cursor.close()
		if con is not None:
			con.close()

lbl0 = Label(login, text = "Username", font= ("arial",30,"bold"))
lbl0.pack(pady=10)
lbl0.configure(bg = '#038ed1')
ent0 = Entry(login, bd = 5, font= ("arial",18))
ent0.pack(pady=10)

lbl1 = Label(login, text = "Password", font= ("arial",30,"bold"))
lbl1.pack(pady=10)
lbl1.configure(bg = '#038ed1')
ent1 = Entry(login, bd = 5, font= ("arial",18))
ent1.pack(pady=10)
ent1.config(show="*")

btnSubmit = Button(login, text = "Submit", width = 10, font = ('roman',30,'bold'), command = setCredentials)
btnSubmit.pack(pady = 10)

root = Toplevel(login)
root.title("Hospital Management")
root.geometry("640x320+350+275")
root.configure(background='light blue')

canvas = Canvas(root,width = 700, height = 550)
canvas.pack()

canvas.create_text(320,30,fill="black",font="Times 40 bold",text="Health-Care Hospital")
canvas.create_line(15, 50, 620, 50)
canvas.configure(bg = '#5bcdf0')

def openAddEntity():
	root.withdraw()
	addEnt.deiconify()

def openViewEntity():
	root.withdraw()
	viewEnt.deiconify()

def openUpdateEntity():
	root.withdraw()
	updEnt.deiconify()

def openDeleteEntity():
	root.withdraw()
	delEnt.deiconify()

def exitRoot():
	root.quit()

btnAdd = Button(root,text = 'Add Entity',width = 15, font = ('roman',25,'bold'), command = openAddEntity)
btnAddWindow =canvas.create_window(320,90, window = btnAdd)

btnView = Button(root,text = 'View Entity',width = 15, font = ('roman',25,'bold'), command = openViewEntity)
btnViewWindow =canvas.create_window(320,150, window = btnView)

btnUpdate = Button(root,text = 'Update Entity',width = 15, font = ('roman',25,'bold'), command = openUpdateEntity)
btnUpdateWindow =canvas.create_window(320,210, window = btnUpdate)

btnDelete = Button(root,text = 'Delete Entity',width = 15, font = ('roman',25,'bold'), command = openDeleteEntity)
btnDeleteWindow =canvas.create_window(320,270, window = btnDelete)

btnExit = Button(root,text = 'Exit', font = ('roman',15,'bold'), command = exitRoot)
btnExitWindow =canvas.create_window(600,290, window = btnExit)

root.withdraw()
# Inititalising database and creating tables
# Opening and closing sub directories
def openDept(toplvl, title, commandOnSubmit):
	toplvl.withdraw()
	dept = Toplevel(toplvl)
	dept.title(title)
	dept.geometry("640x320+350+275")
	dept.configure(bg = '#038ed1')

	def closeDept():
		dept.withdraw()
		toplvl.deiconify()

	btnBack = Button(dept, text = "Go Back", font = ('roman',15,'bold'), command = closeDept)
	btnBack.place(x = 550, y = 280)
	
	lbl0 = Label(dept, text = "ID:", font= ("arial",25,"bold"))
	lbl0.place(x = 130,y = 20)
	lbl0.configure(bg = '#038ed1')
	ent0 = Entry(dept, bd = 5,font= ("arial",18))
	ent0.place(x = 260, y = 20)

	lbl1 = Label(dept, text = "Name:", font= ("arial",25,"bold"))
	lbl1.place(x = 130,y = 80)
	lbl1.configure(bg = '#038ed1')
	ent1 = Entry(dept, bd = 5,font= ("arial",18))
	ent1.place(x = 260, y = 80)

	lbl2 = Label(dept, text = "Facilities:", font= ("arial",25,"bold"))
	lbl2.place(x = 130,y = 140)
	lbl2.configure(bg = '#038ed1')
	ent2 = Entry(dept, bd = 5,font= ("arial",18))
	ent2.place(x = 260, y = 140)

	lbl3 = Label(dept, text = "Location:", font= ("arial",25,"bold"))
	lbl3.place(x = 130,y = 200)
	lbl3.configure(bg = '#038ed1')
	ent3 = Entry(dept, bd = 5,font= ("arial",18))
	ent3.place(x = 260, y = 200)
	
	btnSubmit = Button(dept, text = "Submit", width = 10, font = ('roman',30,'bold'), command = commandOnSubmit)
	btnSubmit.place(x = 230, y = 260)

	return ent0, ent1, ent2, ent3

def openDoctor(toplvl, title, commandOnSubmit):
	toplvl.withdraw()
	doct = Toplevel(toplvl)
	doct.title(title)
	doct.geometry("640x480+350+275")
	doct.configure(bg = '#038ed1')

	def closeDoctor():
		doct.withdraw()
		toplvl.deiconify()

	btnBack = Button(doct, text = "Go Back", font = ('roman',15,'bold'), command = closeDoctor)
	btnBack.place(x = 550, y = 440)
	
	lbl0 = Label(doct, text = "ID:", font= ("arial",25,"bold"))
	lbl0.place(x = 100,y = 20)
	lbl0.configure(bg = '#038ed1')
	ent0 = Entry(doct, bd = 5,font= ("arial",18))
	ent0.place(x = 300, y = 20)
	
	lbl1 = Label(doct, text = "Name:", font= ("arial",25,"bold"))
	lbl1.place(x = 100,y = 80)
	lbl1.configure(bg = '#038ed1')
	ent1 = Entry(doct, bd = 5,font= ("arial",18))
	ent1.place(x = 300, y = 80)

	lbl2 = Label(doct, text = "Qualification:", font= ("arial",25,"bold"))
	lbl2.place(x = 100,y = 140)
	lbl2.configure(bg = '#038ed1')
	ent2 = Entry(doct, bd = 5,font= ("arial",18))
	ent2.place(x = 300, y = 140)

	lbl3 = Label(doct, text = "Phone Number:", font= ("arial",25,"bold"))
	lbl3.place(x = 100,y = 200)
	lbl3.configure(bg = '#038ed1')
	ent3 = Entry(doct, bd = 5,font= ("arial",18))
	ent3.place(x = 300, y = 200)
	
	lbl6 = Label(doct, text = "Department:", font= ("arial",25,"bold"))
	lbl6.place(x = 100,y = 260)
	lbl6.configure(bg = '#038ed1')
	ent6 = Entry(doct, bd = 5,font= ("arial",18))
	ent6.place(x = 300, y = 260)

	lbl4 = Label(doct, text = "Type:", font= ("arial",25,"bold"))
	lbl4.place(x = 100,y = 320)
	lbl4.configure(bg = '#038ed1')
	
	rb = IntVar()
	rb.set(1)
	rb1 = Radiobutton(doct, text = "On Call",font= ("arial",20,"bold"),variable = rb, value = 1)
	rb1.place(x = 300, y = 320)
	rb1.configure(bg = '#038ed1')
	rb2 = Radiobutton(doct, text = "Regular",font= ("arial",20,"bold"),variable = rb, value = 2)
	rb2.place(x = 400, y = 320)
	rb2.configure(bg = '#038ed1')

	lbl5 = Label(doct, text = "Fees:", font= ("arial",25,"bold"))
	lbl5.place(x = 100,y = 360)
	lbl5.configure(bg = '#038ed1')
	ent5 = Entry(doct, bd = 5, font= ("arial",18))
	ent5.place(x = 300, y = 360)

	btnSubmit = Button(doct, text = "Submit", width = 10, font = ('roman',30,'bold'), command = commandOnSubmit)
	btnSubmit.place(x = 250,y = 420)

	return ent0, ent1, ent2, ent3, rb, ent5, ent6

def openPatient(toplvl, title, commandOnSubmit):
	toplvl.withdraw()
	pat = Toplevel(toplvl)
	pat.title(title)
	pat.geometry("640x500+350+275")
	pat.configure(bg = '#038ed1')

	def closePatient():
		pat.withdraw()
		toplvl.deiconify()

	btnBack = Button(pat, text = "Go Back", font = ('roman',15,'bold'), command = closePatient)
	btnBack.place(x = 550, y = 460)
	
	lbl0 = Label(pat, text = "ID:", font= ("arial",25,"bold"))
	lbl0.place(x = 100,y = 20)
	lbl0.configure(bg = '#038ed1')
	ent0 = Entry(pat, bd = 5,font= ("arial",18))
	ent0.place(x = 300, y = 20)

	lbl1 = Label(pat, text = "Name:", font= ("arial",25,"bold"))
	lbl1.place(x = 100,y = 80)
	lbl1.configure(bg = '#038ed1')
	ent1 = Entry(pat, bd = 5,font= ("arial",18))
	ent1.place(x = 300, y = 80)

	lbl2 = Label(pat, text = "Sex:", font= ("arial",25,"bold"))
	lbl2.place(x = 100,y = 140)
	lbl2.configure(bg = '#038ed1')
	ent2 = Entry(pat, bd = 5,font= ("arial",18))
	ent2.place(x = 300, y = 140)

	lbl3 = Label(pat, text = "Phone Number:", font= ("arial",25,"bold"))
	lbl3.place(x = 100,y = 200)
	lbl3.configure(bg = '#038ed1')
	ent3 = Entry(pat, bd = 5,font= ("arial",18))
	ent3.place(x = 300, y = 200)

	lbl4 = Label(pat, text = "Address:", font= ("arial",25,"bold"))
	lbl4.place(x = 100,y = 260)
	lbl4.configure(bg = '#038ed1')
	ent4 = Entry(pat, bd = 5,font= ("arial",18))
	ent4.place(x = 300, y = 260)
	
	lbl5 = Label(pat, text = "Date of Birth:", font= ("arial",25,"bold"))
	lbl5.place(x = 100,y = 320)
	lbl5.configure(bg = '#038ed1')
	ent5 = Entry(pat, bd = 5,font= ("arial",18))
	ent5.place(x = 300, y = 320)

	lbl6 = Label(pat, text = "Age:", font= ("arial",25,"bold"))
	lbl6.place(x = 100,y = 380)
	lbl6.configure(bg = '#038ed1')
	ent6 = Entry(pat, bd = 5,font= ("arial",18))
	ent6.place(x = 300, y = 380)

	btnSubmit = Button(pat, text = "Submit", width = 10, font = ('roman',30,'bold'), command = commandOnSubmit)
	btnSubmit.place(x = 230, y = 440)

	return ent0, ent1, ent2, ent3, ent4, ent5, ent6

def openCheckup(toplvl, title, commandOnSubmit):
	toplvl.withdraw()
	chkup = Toplevel(toplvl)
	chkup.title(title)
	chkup.geometry("640x380+350+275")
	chkup.configure(bg = '#038ed1')

	def closeCheckup():
		chkup.withdraw()
		toplvl.deiconify()

	btnBack = Button(chkup, text = "Go Back", font = ('roman',15,'bold'), command = closeCheckup)
	btnBack.place(x = 550, y = 340)
	
	lbl0 = Label(chkup, text = "Patient ID:", font= ("arial",25,"bold"))
	lbl0.place(x = 120,y = 20)
	lbl0.configure(bg = '#038ed1')
	ent0 = Entry(chkup, bd = 5,font= ("arial",18))
	ent0.place(x = 280, y = 20)

	lbl4 = Label(chkup, text = "Doctor ID:", font= ("arial",25,"bold"))
	lbl4.place(x = 120,y = 80)
	lbl4.configure(bg = '#038ed1')
	ent4 = Entry(chkup, bd = 5,font= ("arial",18))
	ent4.place(x = 280, y = 80)

	lbl1 = Label(chkup, text = "Diagnosis:", font= ("arial",25,"bold"))
	lbl1.place(x = 120,y = 140)
	lbl1.configure(bg = '#038ed1')
	ent1 = Entry(chkup, bd = 5,font= ("arial",18))
	ent1.place(x = 280, y = 140)

	lbl2 = Label(chkup, text = "Treatment:", font= ("arial",25,"bold"))
	lbl2.place(x = 120,y = 200)
	lbl2.configure(bg = '#038ed1')
	ent2 = Entry(chkup, bd = 5,font= ("arial",18))
	ent2.place(x = 280, y = 200)

	lbl3 = Label(chkup, text = "Status:", font= ("arial",25,"bold"))
	lbl3.place(x = 120,y = 260)
	lbl3.configure(bg = '#038ed1')
	ent3 = Entry(chkup, bd = 5,font= ("arial",18))
	ent3.place(x = 280, y = 260)
	
	btnSubmit = Button(chkup, text = "Submit", width = 10, font = ('roman',30,'bold'), command = commandOnSubmit)
	btnSubmit.place(x = 230, y = 320)

	return ent0, ent4, ent1, ent2, ent3

def openPayment(toplvl, title, commandOnSubmit):
	toplvl.withdraw()
	payment = Toplevel(toplvl)
	payment.title(title)
	payment.geometry("640x320+350+275")
	payment.configure(bg = '#038ed1')

	def closePayment():
		payment.withdraw()
		toplvl.deiconify()

	btnBack = Button(payment, text = "Go Back", font = ('roman',15,'bold'), command = closePayment)
	btnBack.place(x = 550, y = 280)
	
	lbl0 = Label(payment, text = "Patient ID:", font= ("arial",25,"bold"))
	lbl0.pack(pady = 5)
	lbl0.configure(bg = '#038ed1')
	ent0 = Entry(payment, bd = 5,font= ("arial",18))
	ent0.pack(pady = 10)

	lbl1 = Label(payment, text = "Treatment Charges:", font= ("arial",25,"bold"))
	lbl1.pack(pady = 5)
	lbl1.configure(bg = '#038ed1')
	ent1 = Entry(payment, bd = 5,font= ("arial",18))
	ent1.pack(pady = 10)
	
	btnSubmit = Button(payment, text = "Submit", width = 10, font = ('roman',30,'bold'), command = commandOnSubmit)
	btnSubmit.pack(pady = 15)

	return ent0, ent1

def openView(toplvl,title):
	toplvl.withdraw()
	view = Toplevel(toplvl)
	view.title(title)
	view.geometry("850x320+350+275")
	view.configure(bg = '#038ed1')

	def closeView():
		view.withdraw()
		toplvl.deiconify()

	lblText = title.split(' ')[1].upper()
	lbl1 = Label(view, text = lblText, font= ("arial",30,"bold"))
	lbl1.pack(pady = 5)
	lbl1.configure(bg = '#038ed1')

	stData = scrolledtext.ScrolledText(view, width = 120, height = 15)
	stData.pack(pady = 5)

	btnBack = Button(view, text = "Go Back", font = ('roman',15,'bold'), command = closeView)
	btnBack.place(x = 760, y = 280)
	return stData

def openDelete(toplvl,title,commandOnSubmit):
	toplvl.withdraw()
	delete = Toplevel(toplvl)
	delete.title(title)
	delete.geometry("400x250+350+275")
	delete.configure(bg = '#038ed1')

	def closeDelete():
		delete.withdraw()
		toplvl.deiconify()

	lblText = title.split(' ')[1].upper() + " ID:-"
	lbl0 = Label(delete, text = lblText, font= ("arial",30,"bold"))
	lbl0.pack(pady=10)
	lbl0.configure(bg = '#038ed1')

	ent0 = Entry(delete, bd = 5, font= ("arial",18))
	ent0.pack(pady=10)

	btnSubmit = Button(delete, text = "Delete", width = 10, font = ('roman',30,'bold'), command = commandOnSubmit)
	btnSubmit.pack(pady = 10)

	btnBack = Button(delete, text = "Go Back", font = ('roman',15,'bold'), command = closeDelete)
	btnBack.place(x = 310, y = 210)

	return ent0;

# Add Entity Window
addEnt = Toplevel(root)
addEnt.title("Add an Entity")
addEnt.geometry("640x320+350+275")
addEnt.configure(bg = '#5bcdf0')

def openAddDept():
	def addDeptToDB():		
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			d_id = int(entId.get())
			d_name = entName.get()
			d_location = entLocation.get()
			d_facilities = entFacilities.get()

			if (d_id is None or d_name is None or d_location is None or d_facilities is None):
				raise MyEx("Entry fields can't be empty")
			if (int(d_id)<=0):
				raise MyEx("ID Should be a positive non zero integer")
			sql = "insert into department values('%d','%s','%s','%s');"
			args = (d_id,d_name,d_location,d_facilities)
			cursor.execute(sql % args)
			con.commit()
			msg = d_name + " Added to department table"
			messagebox.showinfo("Information", msg)
			entId.delete(0,END)
			entName.delete(0,END)
			entLocation.delete(0,END)
			entLocation.delete(0,END)
			entFacilities.delete(0,END)
			entId.focus()

		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))

		finally:
			if con is not None:
				con.rollback()
				con.close()

	entId, entName, entFacilities, entLocation = openDept(addEnt, "Add Department", addDeptToDB)

def openAddDoctor():
	def addDocToDB():
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			dr_id = int(entId.get())
			dr_name = entName.get()
			dr_qualification = entQualification.get()
			dr_pno = int(entPhoneNo.get())
			f_d_name = entDepName.get()
			dr_type = int(docType.get())
			dr_fees = int(entFees.get())

			if (dr_id is None or dr_name is None or dr_qualification is None or dr_pno is None or f_d_name is None or dr_fees is None):
				raise MyEx("Entry fields can't be empty")
			if (dr_id <= 0):
				raise MyEx("ID Should be a positive non zero integer")

			sqlFormat = "select d_id,d_name from department WHERE d_name LIKE" +" '%" + f_d_name +"%';"
			sql = sqlFormat
			cursor.execute(sql)
			departmentList = cursor.fetchall()
			flag = False
			for d in departmentList:
				if f_d_name not in d[1]:
					flag = True;
				else:
					flag = False;
					f_d_id = int(d[0])
					break

			if flag:		
				raise MyEx("Department doesn't exist")

			sql = "insert into doctor values('%d','%s','%s','%d','%d');"
			args = (dr_id,dr_name,dr_qualification,dr_pno,f_d_id)
			cursor.execute(sql % args)

			if dr_type == 1:
				sql = "insert into on_call_doc values('%d','%d');"
				args = (dr_id,dr_fees)
				cursor.execute(sql % args)
			elif dr_type == 2:
				sql = "insert into reg_doc values('%d','%d');"
				args = (dr_id,dr_fees)
				cursor.execute(sql % args)

			con.commit()
			msg = dr_name + " Added to doctors table"
			messagebox.showinfo("Information", msg)
			entId.delete(0,END)
			entName.delete(0,END)
			entQualification.delete(0,END)
			entPhoneNo.delete(0,END)
			entDepName.delete(0,END)
			entFees.delete(0,END)
			entId.focus()

		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))

		finally:
			if con is not None:
				con.rollback()
				con.close()

	entId, entName, entQualification, entPhoneNo, docType, entFees, entDepName = openDoctor(addEnt, "Add Doctor", addDocToDB)

def openAddPatient():
	def addPatientToDB():				
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			p_id = int(entId.get())
			p_name = entName.get()
			p_sex = entSex.get()
			p_address = entAddress.get()	
			p_pno = int(entPhoneNo.get())
			dob = entDOB.get()
			p_age = int(entAge.get())

			if (p_id is None or p_name is None or p_sex is None or p_age is None or dob is None or p_pno is None or p_address is None):
				raise MyEx("Entry fields can't be empty")
			if p_id <= 0:
				raise MyEx("ID Should be a positive non zero integer")

			dobSplit = dob.split("-")
			p_dob = dobSplit[2] +"-" + dobSplit[1] + "-" + dobSplit[0]

			sql = "insert into patient values('%d','%s','%s','%d','%s','%s','%d');"
			args = (p_id, p_name, p_sex, p_pno, p_address, p_dob, p_age)
			cursor.execute(sql % args)
			con.commit()
			msg = p_name + " Added to Patient table"
			messagebox.showinfo("Information", msg)
			entId.delete(0,END)
			entName.delete(0,END)
			entSex.delete(0,END)
			entAge.delete(0,END)
			entDOB.delete(0,END)
			entPhoneNo.delete(0,END)
			entAddress.delete(0,END)
			entId.focus()

		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))

		finally:
			if con is not None:
				con.rollback()
				con.close()

	entId, entName, entSex, entPhoneNo, entAddress, entDOB, entAge = openPatient(addEnt, "Add Patient", addPatientToDB)

def openAddCheckup():
	def addCheckupToDB():
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			dr_id = int(entDocId.get())
			p_id = int(entPatId.get())
			diagnosis = entDiagnosis.get()
			treatment = entTreatment.get()
			status = entStatus.get()


			if (p_id is None or dr_id is None or diagnosis is None or treatment is None or status is None):
				raise MyEx("Entry fields can't be empty")
			if p_id <= 0:
				raise MyEx("ID Should be a positive non zero integer")

			sql = "select dr_id from doctor;"
			cursor.execute(sql)
			docData = cursor.fetchall()
			docArr = []
			for d in docData:
				docArr.append(d[0])

			sql = "select p_id from patient;"
			cursor.execute(sql)
			patData = cursor.fetchall()
			patArr = []
			for d in patData:
				patArr.append(d[0])

			if p_id not in patArr:
				raise MyEx("Patient with this id doesn't exist")
			if dr_id not in docArr:
				raise MyEx("Doctor with this id doesn't exist")

			sql = "insert into checkup values('%d','%d','%s','%s','%s');"
			args = (dr_id, p_id, treatment, status, diagnosis)
			cursor.execute(sql % args)
			con.commit()
			msg ="Scheduled for checkup succesfully"
			messagebox.showinfo("Information", msg)
			entPatId.delete(0,END)
			entDocId.delete(0,END)
			entDiagnosis.delete(0,END)
			entTreatment.delete(0,END)
			entStatus.delete(0,END)
			entPatId.focus()

		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))

		finally:
			if con is not None:
				con.rollback()
				con.close()

	entPatId, entDocId, entDiagnosis, entTreatment, entStatus= openCheckup(addEnt, "Add Checkup", addCheckupToDB)

def openAddPayment():
	def addPaymentToDB():
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			p_id = int(entId.get())
			treat_fees = int(entTreatFee.get())

			if (p_id is None or treat_fees is None):
				raise MyEx("Entry fields can't be empty")
			if p_id <= 0:
				raise MyEx("ID Should be a positive non zero integer")

			sql = "select p_id from patient;"
			cursor.execute(sql)
			patData = cursor.fetchall()
			patArr = []
			for d in patData:
				patArr.append(d[0])

			if p_id not in patArr:
				raise MyEx("Patient with this id doesn't exist")

			sql = "select dr_id from checkup where p_id = " + str(p_id) + ";"
			cursor.execute(sql)
			dr_id = cursor.fetchone()[0]

			sql = "select * from on_call_doc"
			cursor.execute(sql)
			docOnCall = cursor.fetchall()

			dr_fees = 0

			for d in docOnCall:
				if dr_id == d[0]:
					dr_fees = d[1]

			sql = "select * from reg_doc"
			cursor.execute(sql)
			docReg = cursor.fetchall()

			for d in docReg:
				if dr_id == d[0]:
					dr_fees = d[1]
			
			nur_fees = dr_fees * 0.35

			sql = "insert into payment values('%d','%d','%d','%d');"
			args = (p_id,dr_fees,nur_fees,treat_fees)
			cursor.execute(sql % args)
			con.commit()
			msg = " Addition to Payment table succesful"
			messagebox.showinfo("Information", msg)
			entId.delete(0,END)
			entTreatFee.delete(0,END)			
			entId.focus()

		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))

		finally:
			if con is not None:
				con.rollback()
				con.close()

	entId, entTreatFee = openPayment(addEnt, "Add Payment", addPaymentToDB)

def closeAddOpenHome():
	addEnt.withdraw()
	root.deiconify()

lbl1 = Label(addEnt, text = "Select an Entity to add", font= ("arial",35,"bold"))
lbl1.place(x = 120,y = 10)
lbl1.configure(bg = '#5bcdf0')

btnAddDept = Button(addEnt, text = "Department", width = 15,font = ('roman',25,'bold'), command = openAddDept)
btnAddDept.place(x = 190, y=60)

btnAddDoctor = Button(addEnt, text = "Doctor", width = 15,font = ('roman',25,'bold'), command = openAddDoctor)
btnAddDoctor.place(x = 190, y=110)

btnAddPatient = Button(addEnt, text = "Patient", width = 15,font = ('roman',25,'bold'), command = openAddPatient)
btnAddPatient.place(x = 190, y=160)

btnAddCheckup = Button(addEnt, text = "Checkup", width = 15,font = ('roman',25,'bold'), command = openAddCheckup)
btnAddCheckup.place(x = 190, y=210)

btnAddPayment = Button(addEnt, text = "Payment", width = 15,font = ('roman',25,'bold'), command = openAddPayment)
btnAddPayment.place(x = 190, y=260)

btnBack = Button(addEnt, text = "Go Back", font = ('roman',15,'bold'), command = closeAddOpenHome)
btnBack.place(x = 550, y = 280)

addEnt.withdraw()

# View Entity Window
viewEnt = Toplevel(root)
viewEnt.title("View an Entity")
viewEnt.geometry("640x320+350+275")
viewEnt.configure(bg = '#5bcdf0')

def openViewDept():
	display = openView(viewEnt, "view Departments")
	con = None
	cursor = None
	try:
		display.delete('1.0',END)
		con = mysql.connector.connect(user=USERNAME, password = PASSWORD, host = 'localhost', database = 'hospital')
		cursor = con.cursor()
		sql = "select * from department;"
		cursor.execute(sql)
		data = cursor.fetchall()
		msg= ""
		display.insert(INSERT, " ID 		    Name 			 Location 			         Facilities\n")
		display.insert(INSERT, "-"*120 + "\n")
		for d in data:
			msg +=  str(d[0]) +" \t\t"+ str(d[1]) +" \t\t\t"+ str(d[2])+ " \t\t\t" + str(d[3]) + "\n"
		display.insert(INSERT, msg)
	except Exception as e:
		messagebox.showerror("Error", str(e))
	finally:
		if con is not None:
			con.close()	

def openViewDoctor():
	display = openView(viewEnt, "view Doctors")
	con = None
	cursor = None
	try:
		display.delete('1.0',END)
		con = mysql.connector.connect(user=USERNAME, password = PASSWORD, host = 'localhost', database = 'hospital')
		cursor = con.cursor()
		sql = "select * from doctor;"
		cursor.execute(sql)
		docData = cursor.fetchall()
		sql = "select * from on_call_doc;"
		cursor.execute(sql)
		onCallData = cursor.fetchall()
		sql = "select * from reg_doc;"
		cursor.execute(sql)
		regData = cursor.fetchall()
		sql = "select * from department;"
		cursor.execute(sql)
		departments = cursor.fetchall()

		docList = []
		for d in docData:
			docList.append(list(d))
		
		for  d in docList:
			for x in departments:
				if d[4] == x[0]:
					d.pop()
					d.append(x[1])

			for x in onCallData:
				if d[0] == x[0]:
					d.append('On Call')
					d.append(x[1])

			for x in regData:
				if d[0] == x[0]:
					d.append('Regular')
					d.append(x[1])

		display.insert(INSERT, " ID 	    Name 			Qualification 			Phone-No 		  Department 			 Type		 Fees\n")
		display.insert(INSERT, "-"*121 + "\n")
		msg= ""
		
		for d in docList:
			msg += str(d[0])+" \t"+str(d[1])+" \t\t\t"+str(d[2])+" \t\t\t"+str(d[3])+" \t\t"+str(d[4])+" \t\t\t"+str(d[5])+"\t\t"+str(d[6])+"\n"
		display.insert(INSERT, msg)
	except Exception as e:
		messagebox.showerror("Error", str(e))
	finally:
		if con is not None:
			con.close()	

def openViewPatient():
	display = openView(viewEnt, "view Patients")
	con = None
	cursor = None
	try:
		display.delete('1.0',END)
		con = mysql.connector.connect(user=USERNAME, password = PASSWORD, host = 'localhost', database = 'hospital')
		cursor = con.cursor()
		sql = "select * from patient;"
		cursor.execute(sql)
		data = cursor.fetchall()
		msg= ""
		display.insert(INSERT, " ID 		     Name 			Sex 	Phone No 		    Address 			   DOB 		Age\n")
		display.insert(INSERT, "-"*120 + "\n")
		for d in data:
			msg +=  str(d[0]) +" \t\t"+ str(d[1]) +" \t\t\t"+ str(d[2])+ "\t " + str(d[3]) +" \t\t" + str(d[4]) +" \t\t\t" + str(d[5]) + " \t\t" + str(d[6]) + "\n"
		display.insert(INSERT, msg)
	except Exception as e:
		messagebox.showerror("Error", str(e))
	finally:
		if con is not None:
			con.close()	

def openViewCheckup():
	display = openView(viewEnt, "view Checkup")
	con = None
	cursor = None
	try:
		display.delete('1.0',END)
		con = mysql.connector.connect(user=USERNAME, password = PASSWORD, host = 'localhost', database = 'hospital')
		cursor = con.cursor()
		sql = "select dr_id, dr_name, d_id from doctor;"
		cursor.execute(sql)
		docData = cursor.fetchall()
		sql = "select p_id, p_name from patient;"
		cursor.execute(sql)
		patData = cursor.fetchall()		
		sql = "select d_id, d_name from department;"
		cursor.execute(sql)
		departments = cursor.fetchall()
		sql = "select * from checkup;"
		cursor.execute(sql)
		checkData = cursor.fetchall()

		checkupList = []
		for c in checkData:
			checkupList.append(list(c))
		
		for c in checkupList:
			for x in docData:
				if c[0] == x[0]:
					c.remove(c[0])
					c.insert(1,x[1])

			for x in patData:
				if c[0] == x[0]:
					c.insert(1,x[1])		
		
		display.insert(INSERT, " ID 	 Patient Name 			Doctor Name 			Diagnosis 		Treatment 				Status\n")
		display.insert(INSERT, "-"*121 + "\n")
		msg= ""
		
		for d in checkupList:
			msg += str(d[0])+" \t"+str(d[1])+" \t\t\t"+str(d[2])+" \t\t\t"+str(d[5])+" \t\t"+str(d[3])+" \t\t\t\t"+str(d[4])+"\n"
		display.insert(INSERT, msg)
	except Exception as e:
		messagebox.showerror("Error", str(e))
	finally:
		if con is not None:
			con.close()

def openViewPayment():
	display = openView(viewEnt, "view Payment")
	con = None
	cursor = None
	try:
		display.delete('1.0',END)
		con = mysql.connector.connect(user=USERNAME, password = PASSWORD, host = 'localhost', database = 'hospital')
		cursor = con.cursor()
		sql = "select p_id, p_name from patient;"
		cursor.execute(sql)
		patData = cursor.fetchall()
		sql = "select * from payment;"
		cursor.execute(sql)
		payData = cursor.fetchall()

		payList = []
		for p in payData:
			payList.append(list(p))
			
		for p in payList:
			total = p[1] + p[2] + p[3]
			p.append(total)
			for d in patData:
				if p[0] == d[0]:
					p.insert(1, d[1])

		msg= ""
		display.insert(INSERT, " Patient ID 		 Patient Name 			Doctor Fees 		Nurse Fees 		Treatment Fees 			Total Amount\n")
		display.insert(INSERT, "-"*120 + "\n")
		for d in payList:
			msg +="   " + str(d[0]) +" \t\t"+ str(d[1]) +" \t\t\t   "+ str(d[2])+ " \t\t   " + str(d[3])+ " \t\t     " + str(d[4])+ " \t\t\t    "+ str(d[5]) + "\n"
		display.insert(INSERT, msg)
	except Exception as e:
		messagebox.showerror("Error", str(e))
	finally:
		if con is not None:
			con.close()
	
def closeViewOpenHome():
	viewEnt.withdraw()
	root.deiconify()

lbl2 = Label(viewEnt, text = "Select an Entity to View", font= ("arial",35,"bold"))
lbl2.place(x = 120,y = 10)
lbl2.configure(bg = '#5bcdf0')

btnViewDept = Button(viewEnt, text = "Department", width = 15,font = ('roman',25,'bold'), command = openViewDept)
btnViewDept.place(x = 190, y=60)

btnViewDoctor = Button(viewEnt, text = "Doctor", width = 15,font = ('roman',25,'bold'), command = openViewDoctor)
btnViewDoctor.place(x = 190, y=110)

btnViewPatient = Button(viewEnt, text = "Patient", width = 15,font = ('roman',25,'bold'), command = openViewPatient)
btnViewPatient.place(x = 190, y=160)

btnViewCheckup = Button(viewEnt, text = "Checkup", width = 15,font = ('roman',25,'bold'), command = openViewCheckup)
btnViewCheckup.place(x = 190, y=210)

btnViewPayment = Button(viewEnt, text = "Payment", width = 15,font = ('roman',25,'bold'), command = openViewPayment)
btnViewPayment.place(x = 190, y=260)

btnBack = Button(viewEnt, text = "Go Back", font = ('roman',15,'bold'), command = closeViewOpenHome)
btnBack.place(x = 550, y = 280)

viewEnt.withdraw()

# Update Entity Window
updEnt = Toplevel(root)
updEnt.title("Update an Entity")
updEnt.geometry("640x320+350+275")
updEnt.configure(bg = '#5bcdf0')

def openUpdateDept():
	def updDeptToDB():
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			d_id = int(entId.get())
			d_name = entName.get()
			d_location = entLocation.get()
			d_facilities = entFacilities.get()

			if (d_id is None or d_name is None or d_location is None or d_facilities is None):
				raise MyEx("Entry fields can't be empty")
			if (int(d_id)<=0):
				raise MyEx("ID Should be a positive non zero integer")

			sql = "select d_id from department;"
			cursor.execute(sql)
			depIdData = cursor.fetchall()
			depIdList = []

			for d in depIdData:
				depIdList.append(d[0])
			print(d_id)
			print(depIdList)

			if d_id in depIdList:
				sql = "update department set d_name = '%s', d_location = '%s', d_facilities = '%s' where d_id = '%d' ;"
				args = (d_name,d_location,d_facilities,d_id)
				cursor.execute(sql % args)
				con.commit()
				msg = d_name + " Updated in department table"
				messagebox.showinfo("Information", msg)
				entId.delete(0,END)
				entName.delete(0,END)
				entLocation.delete(0,END)
				entLocation.delete(0,END)
				entFacilities.delete(0,END)
				entId.focus()
			else:
				raise MyEx("This department id does not exists")
		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))
		finally:
			if con is not None:
				con.rollback()
				con.close()

	entId, entName, entFacilities, entLocation = openDept(updEnt, "Update Department", updDeptToDB)

def openUpdateDoctor():
	def updDocToDB():
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			dr_id = int(entId.get())
			dr_name = entName.get()
			dr_qualification = entQualification.get()
			dr_pno = int(entPhoneNo.get())
			f_d_name = entDepName.get()
			dr_type = int(docType.get())
			dr_fees = int(entFees.get())

			if (dr_id is None or dr_name is None or dr_qualification is None or dr_pno is None or f_d_name is None or dr_fees is None):
				raise MyEx("Entry fields can't be empty")
			if (dr_id <= 0):
				raise MyEx("ID Should be a positive non zero integer")

			sql = "select dr_id from doctor;"
			cursor.execute(sql)
			drIdData = cursor.fetchall()
			drIdList = []
			for d in drIdData:
				drIdList.append(d[0])

			if dr_id in drIdList:
				sqlFormat = "select d_id,d_name from department WHERE d_name LIKE" +" '%" + f_d_name +"%';"
				sql = sqlFormat
				cursor.execute(sql)
				departmentList = cursor.fetchall()
				flag = False
				for d in departmentList:
					if f_d_name not in d[1]:
						flag = True;
					else:
						flag = False;
						f_d_id = int(d[0])
						break

				if flag:		
					raise MyEx("Department doesn't exist")

				sql = "update doctor set dr_name = '%s', dr_qualification = '%s', dr_pno = '%d', d_id = '%d' where dr_id = '%d';"
				args = (dr_name,dr_qualification,dr_pno,f_d_id,dr_id)
				cursor.execute(sql % args)

				if dr_type == 1:
					sql = "select dr_id from on_call_doc;"
					cursor.execute(sql)
					onCallId = cursor.fetchall()
					onCallList = []
					for d in onCallId:
						onCallList.append(d[0])
					
					if dr_id in onCallList:
						sql = "update on_call_doc set fees_per_visit = '%d' where dr_id = '%d';"
						args = (dr_fees,dr_id)
						cursor.execute(sql % args)
					else:
						sql = "insert into on_call_doc values('%d','%d')"
						args = (dr_id, dr_fees)
						cursor.execute(sql % args)
						sql = "delete from reg_doc where dr_id = '%d'"
						args = (dr_id)
						cursor.execute(sql % args)
				elif dr_type == 2:
					sql = "select dr_id from reg_doc;"
					cursor.execute(sql)
					regDocId = cursor.fetchall()
					regDocList = []
					for d in regDocId:
						regDocList.append(d[0])
					
					if dr_id in regDocList:
						sql = "update reg_doc set dr_salary = '%d' where dr_id = '%d';"
						args = (dr_fees,dr_id)
						cursor.execute(sql % args)
					else:
						sql = "insert into reg_doc values('%d','%d')"
						args = (dr_id, dr_fees)
						cursor.execute(sql % args)
						sql = "delete from on_call_doc where dr_id = '%d'"
						args = (dr_id)
						cursor.execute(sql % args)

				con.commit()
				msg = dr_name + " Updated in doctors table"
				messagebox.showinfo("Information", msg)
				entId.delete(0,END)
				entName.delete(0,END)
				entQualification.delete(0,END)
				entPhoneNo.delete(0,END)
				entDepName.delete(0,END)
				entFees.delete(0,END)
				entId.focus()
			else:
				raise MyEx("Doctor with this id does not exist")
		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))

		finally:
			if con is not None:
				con.rollback()
				con.close()

	entId, entName, entQualification, entPhoneNo, docType, entFees, entDepName= openDoctor(updEnt, "Update Doctor", updDocToDB)

def openUpdatePatient():
	def updPatientToDB():
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			p_id = int(entId.get())
			p_name = entName.get()
			p_sex = entSex.get()
			p_address = entAddress.get()	
			p_pno = int(entPhoneNo.get())
			dob = entDOB.get()
			p_age = int(entAge.get())

			if (p_id is None or p_name is None or p_sex is None or p_age is None or dob is None or p_pno is None or p_address is None):
				raise MyEx("Entry fields can't be empty")
			if p_id <= 0:
				raise MyEx("ID Should be a positive non zero integer")

			sql = "select p_id from patient;"
			cursor.execute(sql)
			patIdData = cursor.fetchall()
			patIdList = []
			for d in patIdData:
				patIdList.append(d[0])

			if p_id in patIdList:
				dobSplit = dob.split("-")
				p_dob = dobSplit[2] +"-" + dobSplit[1] + "-" + dobSplit[0]

				sql = "update patient set p_name = '%s', p_sex = '%s', p_pno = '%d', p_address = '%s', p_dob = '%s', p_age = '%d' where p_id = '%d';"
				args = (p_name, p_sex, p_pno, p_address, p_dob, p_age,p_id)
				cursor.execute(sql % args)
				con.commit()
				msg = p_name + " Updated in Patient table"
				messagebox.showinfo("Information", msg)
				entId.delete(0,END)
				entName.delete(0,END)
				entSex.delete(0,END)
				entAge.delete(0,END)
				entDOB.delete(0,END)
				entPhoneNo.delete(0,END)
				entAddress.delete(0,END)
				entId.focus()
			else:
				raise MyEx("Patient with this id doesn't exist")
		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))

		finally:
			if con is not None:
				con.rollback()
				con.close()

	entId, entName, entSex, entPhoneNo, entAddress, entDOB, entAge = openPatient(updEnt, "Update Patient", updPatientToDB)

def openUpdateCheckup():
	def updCheckupToDB():
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			dr_id = int(entDocId.get())
			p_id = int(entPatId.get())
			diagnosis = entDiagnosis.get()
			treatment = entTreatment.get()
			status = entStatus.get()

			if (p_id is None or dr_id is None or diagnosis is None or treatment is None or status is None):
				raise MyEx("Entry fields can't be empty")
			if p_id <= 0:
				raise MyEx("ID Should be a positive non zero integer")

			sql = "select dr_id from doctor;"
			cursor.execute(sql)
			docData = cursor.fetchall()
			docArr = []
			for d in docData:
				docArr.append(d[0])

			sql = "select p_id from patient;"
			cursor.execute(sql)
			patData = cursor.fetchall()
			patArr = []
			for d in patData:
				patArr.append(d[0])

			if p_id not in patArr:
				raise MyEx("Patient with this id doesn't exist")
			if dr_id not in docArr:
				raise MyEx("Doctor with this id doesn't exist")

			sql = "update checkup set dr_id = '%d', diagnosis = '%s', treatment = '%s', status = '%s' where p_id = '%d';"
			args = (dr_id, diagnosis, treatment, status, p_id)
			cursor.execute(sql % args)

			con.commit()
			msg ="Scheduled for checkup updated succesfully"
			messagebox.showinfo("Information", msg)
			entPatId.delete(0,END)
			entDocId.delete(0,END)
			entDiagnosis.delete(0,END)
			entTreatment.delete(0,END)
			entStatus.delete(0,END)
			entPatId.focus()

		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))

		finally:
			if con is not None:
				con.rollback()
				con.close()

	entPatId, entDocId, entDiagnosis, entTreatment, entStatus = openCheckup(updEnt, "Update Checkup", updCheckupToDB)

def openUpdatePayment():
	def updPaymentToDB():
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			p_id = int(entId.get())
			treat_fees = int(entTreatFee.get())

			if (p_id is None or treat_fees is None):
				raise MyEx("Entry fields can't be empty")
			if p_id <= 0:
				raise MyEx("ID Should be a positive non zero integer")

			sql = "select p_id from patient;"
			cursor.execute(sql)
			patData = cursor.fetchall()
			patArr = []
			for d in patData:
				patArr.append(d[0])

			if p_id not in patArr:
				raise MyEx("Patient with this id doesn't exist")

			sql = "select dr_id from checkup where p_id = " + str(p_id) + ";"
			cursor.execute(sql)
			dr_id = cursor.fetchone()[0]

			sql = "select * from on_call_doc"
			cursor.execute(sql)
			docOnCall = cursor.fetchall()

			dr_fees = 0

			for d in docOnCall:
				if dr_id == d[0]:
					dr_fees = d[1]

			sql = "select * from reg_doc"
			cursor.execute(sql)
			docReg = cursor.fetchall()

			for d in docReg:
				if dr_id == d[0]:
					dr_fees = d[1]
			
			nur_fees = dr_fees * 0.35

			sql = "update payment set treat_fees = '%d' where p_id = '%d';"
			args = (treat_fees,p_id)
			cursor.execute(sql % args)
			con.commit()
			msg = " Payment table updated succesful"
			messagebox.showinfo("Information", msg)
			entId.delete(0,END)
			entTreatFee.delete(0,END)			
			entId.focus()

		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))

		finally:
			if con is not None:
				con.rollback()
				con.close()

	entId, entTreatFee= openPayment(updEnt, "Update Payment", updPaymentToDB)

def closeUpdateOpenHome():
	updEnt.withdraw()
	root.deiconify()

lbl2 = Label(updEnt, text = "Select an Entity to update", font= ("arial",35,"bold"))
lbl2.place(x = 120,y = 10)
lbl2.configure(bg = '#5bcdf0')

btnUpdateDept = Button(updEnt, text = "Department", width = 15,font = ('roman',25,'bold'), command = openUpdateDept)
btnUpdateDept.place(x = 190, y=60)

btnUpdateDoctor = Button(updEnt, text = "Doctor", width = 15,font = ('roman',25,'bold'), command = openUpdateDoctor)
btnUpdateDoctor.place(x = 190, y=110)

btnUpdatePatient = Button(updEnt, text = "Patient", width = 15,font = ('roman',25,'bold'), command = openUpdatePatient)
btnUpdatePatient.place(x = 190, y=160)

btnUpdateCheckup = Button(updEnt, text = "Checkup", width = 15,font = ('roman',25,'bold'), command = openUpdateCheckup)
btnUpdateCheckup.place(x = 190, y=210)

btnAddPayment = Button(updEnt, text = "Payment", width = 15,font = ('roman',25,'bold'), command = openUpdatePayment)
btnAddPayment.place(x = 190, y=260)

btnBack = Button(updEnt, text = "Go Back", font = ('roman',15,'bold'), command = closeUpdateOpenHome)
btnBack.place(x = 550, y = 280)

updEnt.withdraw()

# Delete Entity Window
delEnt = Toplevel(root)
delEnt.title("Delete an Entity")
delEnt.geometry("640x320+350+275")
delEnt.configure(bg = '#5bcdf0')

def openDeleteDept():
	def delDeptfromDB():		
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			d_id = int(entId.get())

			if (d_id is None):
				raise MyEx("Entry fields can't be empty")
			if (int(d_id)<=0):
				raise MyEx("ID Should be a positive non zero integer")

			sql = "select d_id from department;"
			cursor.execute(sql)
			idData = cursor.fetchall()
			idList = []
			for d in idData:
				idList.append(d[0])

			if d_id in idList:
				arg = (d_id)
				sql = "select d_name from department where d_id = '%d';"
				cursor.execute(sql % arg)
				name = cursor.fetchone()[0]
				sql = "delete from department where d_id = '%d';"
				cursor.execute(sql % arg)
				con.commit()
				msg = name + " Deleted from department table"
				messagebox.showinfo("Information", msg)
				entId.delete(0,END)
				entId.focus()
			else:
				raise MyEx("Department with this ID doesn't exist")
		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))

		finally:
			if con is not None:
				con.rollback()
				con.close()

	entId = openDelete(delEnt, "delete Department", delDeptfromDB)


def openDeleteDoctor():
	def delDoctorfromDB():
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			dr_id = int(entId.get())

			if (dr_id is None):
				raise MyEx("Entry fields can't be empty")
			if (int(dr_id)<=0):
				raise MyEx("ID Should be a positive non zero integer")

			sql = "select dr_id from doctor;"
			cursor.execute(sql)
			idData = cursor.fetchall()
			idList = []
			for d in idData:
				idList.append(d[0])

			if dr_id in idList:
				arg = (dr_id)
				sql = "select dr_name from doctor where dr_id = '%d';"
				cursor.execute(sql % arg)
				name = cursor.fetchone()[0]
				sql = "delete from doctor where dr_id = '%d';"
				cursor.execute(sql % arg)
				con.commit()
				msg = name + " Deleted from Doctor table"
				messagebox.showinfo("Information", msg)
				entId.delete(0,END)
				entId.focus()
			else:
				raise MyEx("Department with this ID doesn't exist")
		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))

		finally:
			if con is not None:
				con.rollback()
				con.close()

	entId = openDelete(delEnt, "delete Doctor", delDoctorfromDB)

def openDeletePatient():
	def delPatientfromDB():
		con = None
		cursor = None
		try:
			con = mysql.connector.connect(user = USERNAME, password = PASSWORD, host = 'localhost',database = 'hospital')
			cursor = con.cursor()
			p_id = int(entId.get())

			if (p_id is None):
				raise MyEx("Entry fields can't be empty")
			if (int(p_id)<=0):
				raise MyEx("ID Should be a positive non zero integer")

			sql = "select p_id from patient;"
			cursor.execute(sql)
			idData = cursor.fetchall()
			idList = []
			for d in idData:
				idList.append(d[0])

			if p_id in idList:
				arg = (p_id)
				sql = "select p_name from patient where p_id = '%d';"
				cursor.execute(sql % arg)
				name = cursor.fetchone()[0]
				sql = "delete from patient where p_id = '%d';"
				cursor.execute(sql % arg)
				con.commit()
				msg = name + " Deleted from Patient table"
				messagebox.showinfo("Information", msg)
				entId.delete(0,END)
				entId.focus()
			else:
				raise MyEx("Department with this ID doesn't exist")
		except MyEx as me:
			messagebox.showerror("Error",me)
		except ValueError as v:
			messagebox.showerror("Error","Enter valid Data")
		except Exception as e:
			messagebox.showerror("Error",str(e))

		finally:
			if con is not None:
				con.rollback()
				con.close()

	entId = openDelete(delEnt, "delete Patient", delPatientfromDB)

def closeDeleteOpenHome():
	delEnt.withdraw()
	root.deiconify()

lbl2 = Label(delEnt, text = "Select an Entity to Delete", font= ("arial",35,"bold"))
lbl2.place(x = 120,y = 10)
lbl2.configure(bg = '#5bcdf0')

btnDeleteDept = Button(delEnt, text = "Department", width = 15,font = ('roman',25,'bold'), command = openDeleteDept)
btnDeleteDept.place(x = 190, y=80)

btnDeleteDoctor = Button(delEnt, text = "Doctor", width = 15,font = ('roman',25,'bold'), command = openDeleteDoctor)
btnDeleteDoctor.place(x = 190, y=140)

btnDeletePatient = Button(delEnt, text = "Patient", width = 15,font = ('roman',25,'bold'), command = openDeletePatient)
btnDeletePatient.place(x = 190, y=200)

btnBack = Button(delEnt, text = "Go Back", font = ('roman',15,'bold'), command = closeDeleteOpenHome)
btnBack.place(x = 550, y = 280)

delEnt.withdraw()

root.mainloop()
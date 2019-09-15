
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import time
import sys
import MySQLdb
import datetime
from xlrd import *
from xlsxwriter import *
from PyQt5.uic import loadUiType
ui, _ = loadUiType('lib.ui')
Login,__ = loadUiType('Login.ui')
class Login(QWidget , Login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        self.Dark_Blue_Theme()
        #self.Handle_login()
        self.pushButton.clicked.connect(self.Handle_login)
        self.pushButton_12.clicked.connect(self.Handle_register)

    def Open_reg_tab(self):
        self.tabWidget.setCurrentIndex(0)
    def Open_login_tab(self):
        self.tabWidget.setCurrentIndex(1)
    def Dark_Blue_Theme(self):
        style =open('Themes/darkblue.css','r')
        style=style.read()
        self.setStyleSheet(style)

    def Handle_login(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        user_name=self.lineEdit.text()
        password=self.lineEdit_2.text()
        sql='''SELECT * FROM users'''
        self.cur.execute(sql)
        data=self.cur.fetchall()
        for row in data:
            if user_name == row[1] and password == row[3]:
                self.window2 = MainApp()
                self.close()
                self.window2.show()

            else:
                self.label_26.setText('Make sure you entered right username and password .')
    def Handle_register(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        username=self.lineEdit_16.text()
        email=self.lineEdit_13.text()
        password=self.lineEdit_15.text()
        password2=self.lineEdit_14.text()

        sql='''SELECT user_name FROM users'''
        self.cur.execute(sql)
        data=self.cur.fetchall()

        if username=='' or email =='' or password =='' or password2=='':
            self.label_25.setText('All details need to be filled.')


        else:
            for row in data:
                if username != row:
                    self.label_25.setText('Enter Different user name.')
                else:

                    if password==password2:
                        self.cur.execute('''
                            InsERT INTO users(user_name , user_email,user_password)
                            VALUES(%s, %s, %s)
                        ''',(username, email, password))
                        self.db.commit()
                        self.label_25.setText('New user added.')
                        self.lineEdit_16.setText('')
                        self.lineEdit_13.setText('')
                        self.lineEdit_15.setText('')
                        self.lineEdit_14.setText('')

                    else:
                        self.label_25.setText('password mismatch enter both passwords correctly.')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Buttons()

        self.show_Category()
        self.show_Author()
        self.show_Publisher()

        self.show_Category_Combobox()
        self.show_Author_Combobox()
        self.show_Publisher_Combobox()

        self.Show_All_Books()
        self.Show_All_Students()
        #self.search_Books()
        self.show_all_Opn()


    def Handle_UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)
        # pass

    def Handle_Buttons(self):
        self.pushButton_2.clicked.connect(self.Open_Day_To_Day_Tab)
        self.pushButton_3.clicked.connect(self.Open_Book_Tab)
        self.pushButton.clicked.connect(self.Open_User_Tab)
        self.pushButton_14.clicked.connect(self.Student)
        self.pushButton_4.clicked.connect(self.Open_Settings_Tab)

        self.pushButton_7.clicked.connect(self.Add_New_Book)
        self.pushButton_18.clicked.connect(self.Add_Category)
        self.pushButton_19.clicked.connect(self.Delete_Category)

        self.pushButton_20.clicked.connect(self.Add_Author)
        self.pushButton_22.clicked.connect(self.Delete_Author)
        self.pushButton_21.clicked.connect(self.Add_Publisher)
        self.pushButton_23.clicked.connect(self.Delete_Publisher)

        self.pushButton_9.clicked.connect(self.search_Books)
        self.pushButton_8.clicked.connect(self.Edit_Books)
        self.pushButton_10.clicked.connect(self.Delete_Books)

        self.pushButton_11.clicked.connect(self.Add_New_User)
        self.pushButton_12.clicked.connect(self.Login)
        self.pushButton_13.clicked.connect(self.Edit_User)
        self.pushButton_29.clicked.connect(self.Delete_User)
        self.pushButton_30.clicked.connect(self.search_user)

        self.pushButton_15.clicked.connect(self.Add_new_Student)
        self.pushButton_16.clicked.connect(self.Search_Students)
        self.pushButton_25.clicked.connect(self.Edit_Students_Data)
        self.pushButton_24.clicked.connect(self.Delete_Student)

        self.pushButton_5.clicked.connect(self.Open_Theme_Tab)
        self.pushButton_31.clicked.connect(self.Dark_Orange_Theme)
        self.pushButton_32.clicked.connect(self.Dark_Gray_Theme)
        self.pushButton_33.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_34.clicked.connect(self.QDark_Theme)

        self.pushButton_27.clicked.connect(self.Export_daytoday_Opn)
        self.pushButton_17.clicked.connect(self.Export_Books)
        self.pushButton_26.clicked.connect(self.Export_Students)
        self.pushButton_6.clicked.connect(self.Handle_day_opn)
#########################################
############Opening Tabs#################

    def Open_Day_To_Day_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Book_Tab(self):
        self.tabWidget.setCurrentIndex(1)
    def Student(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_User_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(4)
    def Open_Theme_Tab(self):
        self.tabWidget.setCurrentIndex(5)
#########################################
########Handle dattoday operation#######
    def Handle_day_opn(self):
        book_title =self.lineEdit.text()
        student_name=self.lineEdit_23.text()
        type=self.comboBox.currentText()
        days_num=self.comboBox_2.currentIndex()+1
        today_date = datetime.date.today()
        to_date=today_date+datetime.timedelta(days=days_num)

        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        sql='''SELECT student_name FROM students'''
        self.cur.execute(sql)
        data=self.cur.fetchall()
        book= '''SELECT book_name FROM books'''
        self.cur.execute(book)
        allbooks=self.cur.fetchall()
        if book_title ==''  or student_name=='' or type=='' or days_num=='' or today_date=='' or to_date=='':
            self.statusBar().showMessage('All details need tobe filled.')

        else:


            self.cur.execute('''
                INSERT INTO daytodayopn(book_name, student, type, days, date,to_date )
                VALUES( %s, %s,%s,%s,%s,%s )
                ''', ( book_title, student_name, type, days_num, today_date, to_date ))
            self.db.commit()
            self.lineEdit.setText('')
            self.lineEdit_23.setText('')
            self.comboBox.setCurrentIndex(0)
            self.comboBox_2.setCurrentIndex(0)

            self.statusBar().showMessage('Book is issued.',3000)
            self.show_all_Opn()




    def show_all_Opn(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''
            SELECT book_name,student,type,date,to_date FROM daytodayopn
        ''')
        data=self.cur.fetchall()
        print(data)
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, form in enumerate(data):
            for column , item in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column+=1
            row_position=self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)


    def fine(self):
        pass
#########################################
############Books########################

    def Show_All_Books(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()

        self.cur.execute('''SELECT book_code , book_name,book_desc,book_category,book_author,book_publisher,book_price,book_count FROM books''')
        data = self.cur.fetchall()

        print(data)
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)
        for row, form in enumerate(data):
            for column,item in enumerate(form):
                self.tableWidget_3.setItem(row, column,QTableWidgetItem(str(item)) )
                column+=1
            row_position =self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_position)

        self.db.close()

    def Add_New_Book(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()

        book_title=self.lineEdit_2.text()
        book_description=self.textEdit.toPlainText()
        book_code=self.lineEdit_3.text()

        book_category=self.comboBox_3.currentText()
        book_author=self.comboBox_4.currentText()
        book_publisher=self.comboBox_5.currentText()
        book_price=self.lineEdit_4.text()
        book_count=self.lineEdit_25.text()
        if book_title ==''  or book_description=='' or book_code=='' or book_category=='' or book_author=='' or book_publisher =='' or book_price=='' or book_count =='':
            self.statusBar().showMessage('All details need tobe filled.',3000)

        else:
            self.cur.execute('''
                INSERT INTO books(book_name,book_desc,book_code,book_category,book_author,book_publisher,book_price, book_count ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            
            ''',(book_title, book_description, book_code,book_category,book_author,book_publisher,book_price,book_count))
            self.db.commit()
            self.db.close()
            self.statusBar().showMessage('New Book Added.',3000)
            self.lineEdit_2.setText('')
            self.textEdit.setPlainText('')
            self.lineEdit_3.setText('')
            self.comboBox_3.setCurrentIndex(0)
            self.comboBox_4.setCurrentIndex(0)
            self.comboBox_5.setCurrentIndex(0)
            self.lineEdit_4.setText('')
            self.lineEdit_25.setText('')
            self.Show_All_Books()

    def search_Books(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        book_title=self.lineEdit_5.text()
        sql='''SELECT * FROM books WHERE book_name= %s'''
        self.cur.execute(sql,[(book_title)])

        data=self.cur.fetchone()
        if book_title=='':
            self.statusBar().showMessage('Enter Book title')
        elif data:

            print(data)
            self.lineEdit_8.setText(data[1])
            self.lineEdit_7.setText(data[3])
            self.textEdit_2.setPlainText(data[2])
            self.comboBox_6.setCurrentText(data[4])
            self.comboBox_8.setCurrentText(data[5])
            self.comboBox_7.setCurrentText(data[6])
            self.lineEdit_6.setText(str(data[7]))
        else:
            self.statusBar().showMessage('Book title you entered not found.')


    def Edit_Books(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        search_book_title=self.lineEdit_5.text()
        if search_book_title != '':
            book_title=self.lineEdit_8.text()
            book_description=self.textEdit_2.toPlainText()
            book_code=self.lineEdit_7.text()

            book_category=self.comboBox_6.currentText()
            book_author=self.comboBox_8.currentText()
            book_publisher=self.comboBox_7.currentText()
            book_price=self.lineEdit_6.text()
            if book_title=='' or book_description=='' or book_code== '' or  book_category=='' or book_author=='' or book_publisher=='' or  book_price=='' :
                self.statusBar().showMessage('All details need to be filled.')
            else:

                self.cur.execute(''' 
                UPDATE books SET book_name=%s ,book_desc=%s,book_code=%s,book_category=%s,book_author=%s,book_publisher=%s,book_price=%s WHERE book_name=%s
            
                ''',(book_title,book_description,book_code,book_category,book_author,book_publisher, book_price,search_book_title))
                self.db.commit()
                self.statusBar().showMessage('book updated')
                self.Show_All_Books()
        else:
            self.statusBar().showMessage('book name not found')
    def Delete_Books(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        book_title=self.lineEdit_5.text()
        warning = QMessageBox.warning(self, 'Delete Book','are you sure you want to delete this book ', QMessageBox.Yes | QMessageBox.No)
        if book_title =='':
            self.statusBar().showMessage('Enter book title/name.')
        elif warning == QMessageBox.Yes:
            sql='''DELETE FROM books WHERE book_name =%s'''
            self.cur.execute(sql, [(book_title)])
            self.db.commit()
            self.statusBar().showMessage('Book Deleted')
            self.Show_All_Books()
        else:
            self.statusBar().showMessage('book name not found.')
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Oh no!')

########################################
###########Students#####################

    def Add_new_Student(self):
        student_name= self.lineEdit_19.text()
        student_email= self.lineEdit_20.text()
        library_ID=self.lineEdit_21.text()
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        if student_name =='' or student_email =='' or library_ID=='':
            self.statusBar().showMessage('All Detail needs to be feel.')
        else:
            self.cur.execute('''
                INSERT INTO students (student_name, student_email,library_ID)
                VALUES(%s, %s, %s )
            ''',(student_name,student_email, library_ID ))
            self.db.commit()
            self.db.close()
            self.lineEdit_19.setText('')
            self.lineEdit_20.setText('')
            self.lineEdit_21.setText('')
            self.Show_All_Students()
            self.statusBar().showMessage('New Student Added.')
    def Show_All_Students(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT student_name, student_email, library_ID FROM students''')
        data=self.cur.fetchall()
        print(data)

        self.tableWidget_6.insertRow(0)
        for row, form in enumerate(data):
            for column,item in enumerate(form):
                self.tableWidget_6.setItem(row, column,QTableWidgetItem(str(item)) )
                column+=1
            row_position =self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_position)
        #self.db.commit
        self.db.close()


    def Search_Students(self):
        library_ID=self.lineEdit_22.text()
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        sql='''SELECT * FROM students WHERE library_ID=%s'''
        self.cur.execute(sql, [(library_ID)])
        data=self.cur.fetchone()
        if library_ID =='':
            self.statusBar().showMessage('Enter library Id')
        elif data:

            self.lineEdit_35.setText(data[1])
            self.lineEdit_32.setText(data[2])
            self.lineEdit_36.setText(data[3])
        else:
            self.statusBar().showMessage('library Id not found')
    def Edit_Students_Data(self):

        library_ord_ID=self.lineEdit_22.text()
        if library_ord_ID != '':
            student_name=self.lineEdit_35.text()
            student_email=self.lineEdit_32.text()
            library_ID=self.lineEdit_36.text()

            self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
            self.cur=self.db.cursor()
            if student_name =='' or student_email =='' or library_ID=='':
                self.statusBar().showMessage('All details need to be filled.')

            else:
                self.cur.execute('''
                    UPDATE students SET student_name=%s, student_email=%s, library_ID=%s WHERE library_ID=%s
                ''',(student_name, student_email, library_ID,library_ord_ID))
                self.db.commit()
                self.db.close()
                self.Show_All_Students()
                self.statusBar().showMessage('student info updated ')
        else:
            self.statusBar().showMessage('library ID not found.')

    def Delete_Student(self):
        library_ord_ID=self.lineEdit_22.text()
        warnin_msg=QMessageBox.warning(self, 'Delete student','are you want to delete this student',QMessageBox.Yes|QMessageBox.No)
        if library_ord_ID=='':
            self.statusBar().showMessage('Enter Student library ID to delete ')
        elif warnin_msg== QMessageBox.Yes:
            self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
            self.cur=self.db.cursor()
            sql ='''DELETE FROM students WHERE library_ID=%s'''
            self.cur.execute(sql, [(library_ord_ID)])
            self.db.commit()
            self.db.close()
            self.Show_All_Students()
            self.statusBar().showMessage('Student Deleted.')
        else:
            self.statusBar().showMessage('Student ID not found.')

########################################
###########User########################
    def search_user(self):
        username=self.lineEdit_24.text()
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        sql='''SELECT user_name FROM users WHERE user_name=%s'''
        self.cur.execute(sql, [(username)])
        data=self.cur.fetchone()
        if username =='':
            self.statusBar().showMessage('Enter user name',3000)
        elif username != data:
            self.statusBar().showMessage('user found',3000)
        else:
            self.statusBar().showMessage('user not found',3000)

    def Add_New_User(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        username=self.lineEdit_9.text()
        email=self.lineEdit_10.text()
        password=self.lineEdit_11.text()
        password2=self.lineEdit_12.text()

        sql='''SELECT user_name FROM users'''
        self.cur.execute(sql)
        data=self.cur.fetchall()

        if username=='' or email =='' or password =='' or password2=='':
            self.statusBar().showMessage('All details need tobe fill.',3000)

        else:
            for row in data:
                if username != row:
                    self.statusBar().showMessage('Enter Different user name.',3000)
                else:



                    if password==password2:
                        self.cur.execute('''
                            InsERT INTO users(user_name , user_email,user_password)
                            VALUES(%s, %s, %s)
                        ''',(username, email, password))
                        self.db.commit()
                        self.statusBar().showMessage('New user added.',3000)
                        self.lineEdit_9.setText('')
                        self.lineEdit_10.setText('')
                        self.lineEdit_11.setText('')
                        self.lineEdit_12.setText('')

                    else:
                        self.label_20.setText('password mismatch enter both passwords correctly.')
                #time.sleep(2)
                    #self.label_20.setText('')

    def Login(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        username=self.lineEdit_13.text()
        password=self.lineEdit_14.text()
        sql='''SELECt * FROM users'''
        self.cur.execute(sql)
        data=self.cur.fetchall()
        for row in data:
            if username=='' or password== '':
               self.statusBar().showMessage('login invalid.')
            elif username==row[1] and password== row[3]:
                print('user match')
                self.statusBar().showMessage('Valid username and password')
                self.groupBox_3.setEnabled(True)

                self.lineEdit_17.setText(row[1])
                self.lineEdit_18.setText(row[2])
                self.lineEdit_15.setText(row[3])
            else:
                self.label_29.setText('Enter correct UserName and Password.')
                self.lineEdit_13.setText('')
                self.lineEdit_14.setText('')


        #self.label_29.setText(' ')
               # self.lineEdit_16.setText(row[3])
    def Edit_User(self):

        username= self.lineEdit_17.text()
        email= self.lineEdit_18.text()
        password= self.lineEdit_15.text()
        password2= self.lineEdit_16.text()
        original_name= self.lineEdit_13.text()
        if username=='' or email =='' or password =='' or password2=='':
                self.statusBar().showMessage('All details need tobe fill.')
        else:
            if password == password2:
                self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
                self.cur=self.db.cursor()
                self.cur.execute('''
                    UPDATE users SET user_name= %s,user_email=%s, user_password = %s WHERE user_name=%s
                ''', (username, email, password,original_name))
                self.db.commit()
                self.statusBar().showMessage('user data updated successfully')

            else:
                self.statusBar().showMessage('make sure you entered password correctly')

    def Delete_User(self):
        user_name= self.lineEdit_17.text()
        email=self.lineEdit_18.text()
        warnin_msg=QMessageBox.warning(self, 'Delete user','are you want to delete this user',QMessageBox.Yes|QMessageBox.No)
        if user_name=='' or email =='':
            self.statusBar().showMessage('User name and email must be specfied.',3000)
        elif warnin_msg== QMessageBox.Yes:
            self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
            self.cur=self.db.cursor()
            sql ='''DELETE FROM users WHERE user_email=%s'''
            self.cur.execute(sql, [(email)])
            self.db.commit()
            self.db.close()

            self.statusBar().showMessage('user Deleted.',3000)
        else:
            self.statusBar().showMessage('user not found.',3000)

##########################################
###########Settings#######################
    def Add_Category(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        category_name =self.lineEdit_31.text()
        if category_name=='':
            self.statusBar().showMessage('Enter some name to the category.')
        else:

            self.cur.execute('''
                INSERT INTO category (category_name) VALUES (%s)
            ''',( category_name, ))
            self.db.commit()
            self.statusBar().showMessage(' New Category Added ')
            self.lineEdit_31.setText('')
            self.show_Category_Combobox()
            self.show_Category()
    def Delete_Category(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        category_name =self.lineEdit_37.text()

        if category_name=='':
            self.statusBar().showMessage('Give some category name to delete.')
        else:
            warning_msg=QMessageBox.warning(self, 'Delete category','are you want to delete this category.',QMessageBox.Yes|QMessageBox.No)
            if warning_msg== QMessageBox.Yes:
                self.cur.execute('''
                     DELETE FROM category WHERE category_name=%s
                ''',( category_name, ))
                self.db.commit()
                self.db.close()
                self.statusBar().showMessage(' Category deleted. ')
                self.lineEdit_37.setText('')
                self.show_Category_Combobox()
                self.show_Category()


    def show_Category(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        self.cur.execute(''' SELECT category_name FROM category''')
        data=self.cur.fetchall()
        print(data)
        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column +=1
                row_position=self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)


    def Add_Author(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        author_name =self.lineEdit_33.text()
        if author_name== '':
            self.statusBar().showMessage('Enter some name to the author field.')
        else:
            self.cur.execute('''
                INSERT INTO authors (author_name) VALUES (%s)
            ''',( author_name, ))
            self.db.commit()
            self.lineEdit_33.setText('')
            self.show_Author()
            self.show_Author_Combobox()

            self.statusBar().showMessage(' New Author Added ')
    def show_Author(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        self.cur.execute(''' SELECT author_name FROM authors''')
        data=self.cur.fetchall()
        print(data)
        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column +=1
                row_position=self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)
    def Delete_Author(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        author_name =self.lineEdit_38.text()

        if author_name=='':
            self.statusBar().showMessage('Give some author name to delete.')
        else:
            warning_msg=QMessageBox.warning(self, 'Delete author','are you want to delete this author.',QMessageBox.Yes|QMessageBox.No)
            if warning_msg== QMessageBox.Yes:
                self.cur.execute('''
                     DELETE FROM authors WHERE author_name=%s
                ''',( author_name, ))
                self.db.commit()
                self.db.close()
                self.statusBar().showMessage(' Author deleted. ')
                self.lineEdit_38.setText('')
                self.show_Author_Combobox()
                self.show_Author()

    def Add_Publisher(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        publisher_name =self.lineEdit_34.text()
        if publisher_name== '':
            self.statusBar().showMessage('Enter some name to the publisher field.')
        else:
            self.cur.execute('''
                INSERT INTO publisher (publisher_name) VALUES (%s)
            ''',( publisher_name, ))
            self.db.commit()
            self.lineEdit_34.setText('')
            self.show_Publisher()
            self.show_Publisher_Combobox()
            self.statusBar().showMessage(' New Publisher Added ')

    def show_Publisher(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        self.cur.execute(''' SELECT publisher_name FROM publisher''')
        data=self.cur.fetchall()
        print(data)
        if data:
            self.tableWidget_5.setRowCount(0)
            self.tableWidget_5.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                    column +=1
                row_position=self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(row_position)

    def Delete_Publisher(self):
            self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
            self.cur=self.db.cursor()
            publisher_name =self.lineEdit_39.text()

            if publisher_name=='':
                self.statusBar().showMessage('Give some Publisher name to delete.')
            else:
                warning_msg=QMessageBox.warning(self, 'Delete Publisher','are you want to delete this Publisher.',QMessageBox.Yes|QMessageBox.No)
                if warning_msg== QMessageBox.Yes:
                    self.cur.execute('''
                         DELETE FROM publisher WHERE publisher_name=%s
                    ''',( publisher_name, ))
                    self.db.commit()
                    self.db.close()
                    self.statusBar().showMessage(' Publisher deleted. ')
                    self.lineEdit_39.setText('')
                    self.show_Publisher_Combobox()
                    self.show_Publisher()


############################################
#########show settings data in UI ##########
    def show_Category_Combobox(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()

        self.cur.execute('''SELECT category_name FROM category''')
        data =self.cur.fetchall()
        self.comboBox_3.clear()
        for category in data:
            self.comboBox_3.addItem(category[0])
            self.comboBox_6.addItem(category[0])

    def show_Author_Combobox(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()

        self.cur.execute('''SELECT author_name FROM authors''')
        data =self.cur.fetchall()
        self.comboBox_4.clear()
        for author in data:
            self.comboBox_4.addItem(author[0])
            self.comboBox_8.addItem(author[0])

    def show_Publisher_Combobox(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()

        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data =self.cur.fetchall()
        self.comboBox_5.clear()
        for publisher in data:
            self.comboBox_5.addItem(publisher[0])
            self.comboBox_7.addItem(publisher[0])


 ##########################################
###########Export data #######################
    def Export_daytoday_Opn(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''
            SELECT book_name,student,type,date,to_date,fine FROM daytodayopn
        ''')
        data=self.cur.fetchall()
        wb = Workbook('day_opns.xlsx')

        sheet1=wb.add_worksheet()
        sheet1.write(0,0,'book_title')
        sheet1.write(0,1,'student name')
        sheet1.write(0,2,'type')
        sheet1.write(0,3,'from -date')
        sheet1.write(0,4,'to-date')
        sheet1.write(0,5,'fine')

        row_number=1
        for row in data:
            column_number=0
            for item in row:
                sheet1.write(row_number, column_number,str(time) )
                row_number+=1
        wb.close()
        self.statusBar().showMessage('Report created succesffully',3000    )
    def Export_Books(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()

        self.cur.execute('''SELECT book_code , book_name,book_desc,book_category,book_author,book_publisher,book_price FROM books''')
        data = self.cur.fetchall()

        wb = Workbook('BooksReport.xlsx')
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'Book Title')
        sheet1.write(0, 1, 'Book Code')
        sheet1.write(0, 2, 'Book Publisher')
        sheet1.write(0, 3, 'Book Category')
        sheet1.write(0, 4, 'Book Author')
        sheet1.write(0, 5, 'Book Price')
        sheet1.write(0, 6, 'Book Count')

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        wb.close()
        self.statusBar().showMessage('Book Exported',3000)

    def Export_Students(self):
        self.db= MySQLdb.connect(host='localhost',user='root',password='',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT student_name, student_email, library_ID FROM students''')
        data=self.cur.fetchall()

        wb=Workbook('all_books.xlsx')
        sheet1 =wb.add_worksheet()

        sheet1.write(0,0 ,'student name')
        sheet1.write(0,1, 'student email')
        sheet1.write(0,2,'student library Id')

        row_number =1
        for row in data:
            column_number =0
            for  item in row :
                sheet1.write(row_number ,column_number ,str(item))
                column_number +=1
            row_number +=1

        wb.close()
        self.statusBar().showMessage('Student Report Created Successfully.',3000)

    ##########################################
###########Settings#######################





    def Dark_Blue_Theme(self):
        style =open('Themes/darkblue.css','r')
        style=style.read()
        self.setStyleSheet(style)


    def Dark_Gray_Theme(self):
        style =open('Themes/greydark.css','r')
        style=style.read()
        self.setStyleSheet(style)
    def Dark_Orange_Theme(self):
        style =open('Themes/darkorange.css','r')
        style=style.read()
        self.setStyleSheet(style)

    def QDark_Theme(self):
        style =open('Themes/qdark.css','r')
        style=style.read()
        self.setStyleSheet(style)


def main():
    #app = QApplication(xlrd.sys.argv)
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

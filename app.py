from flask import Flask, render_template,request
import os

from database import Db

app=Flask(__name__)
db = Db(app)

@app.route('/register',methods=['GET','POST'])
def register():
	#this is to make a connection between flask and mysqlDB 
	if request.method=="POST":
		#getting data from the user (its mean from html to flask to store in mysqlDB)
		getdata=request.form
		name=getdata["name"]
		age=getdata["age"]
		city=getdata["city"]
		coupon=getdata["coupon"]
		#this if condition to check weather user entered all the required fields || I can check this in frontend itself using required function in form
		if name!="" and age!="" and city!="":
			if db.name_exists(name):
				return"Name is already taken"
				#i can also use alret method to display these errors
			else:
				'''
				if name not taken will be genrating the coupon for new user
				coupon genrator
			    i made auto increment ID so selection of last coupon will be use full to genrate next cupon for new user
				'''
				cur.execute("select coupon from eg1 order by id desc limit 1")
				val1=cur.fetchall()
				#i used some simple tech to genrate different coupons to new users 
				last_cupon=str(val1[0][0])
				intval=int(last_cupon[2::])
				intval=intval+1
				genrated_coupon=name[0:2]+str(intval)
				print(genrated_coupon)
				#done with coupon genration

			#this one to check weather user entered coupon is vaild or not
			if coupon!='':
				cur.execute("select coupon from eg1")
				val2=cur.fetchall()
				if len(val2)!=0:
					try: 
						#this condition is to insert the referal and refree in table seprate table
						#########################
						#here i can also use cur.execute("insert into refernce (referral)select name from eg1 where coupon=(%s))",[coupon]) this is subquery 
						#  
						cur.execute("select name from eg1 where coupon=(%s)",[coupon])
						val3=cur.fetchall()
						#i did normal method to insert here
						cur.execute("insert into refernce(referral, referee) values(%s,%s)",[val3[0][0],name])
						conn.commit()
					except:
						return"invaild coupon"
				else:
					return"invaild coupon"
			#registing the data into table if alll the condition is ok with it
			cur.execute("insert into eg1(name,age,city,coupon) values(%s,%s,%s,%s)",(name,age,city,genrated_coupon))
			conn.commit()
			conn.close()
			#after done with register i displaying thank you page to display the new coupon of the new  user
			return render_template("thankyou.html",name=name,genrated_coupon=genrated_coupon)

		else:
			#when user not enter the required field
			return "plz enter the required field"
	#to display the form 
	return render_template("register.html")
	#I tested with some testcases its working good 
	#if you found any bugs kindly report me i try to resolve it

if __name__ == '__main__':
	app.run(debug=True)

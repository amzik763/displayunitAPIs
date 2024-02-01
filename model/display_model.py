import mysql.connector
import json
from flask import make_response,jsonify
from datetime import datetime
import pytz
# class user_model():
#     def _init_(self):
#         try:
#             self.con=mysql.connector.connect(host="localhost",user="root",password="Ga2001pillu14##",database="dunit")
#             self.cur=self.con.cursor(dictionary=True)
#             self.con.autocommit=True
#             print("connected successfully")
#         except:
#             print("some error")
            
#     def user_getall_model(self):
#         self.cur.execute("SELECT * FROM stations")
#         result=self.cur.fetchall()
#         if len(result)>0:
#             res = make_response({'payload':result},200)
#             res.headers['Access-Control-Allow-Origin']="*"
#             return res
#         else:
#             return make_response({"message":"No Data found"},204)
        
        
#     def user_addone_model(self,data):
#         self.cur.execute(f"INSERT INTO users(id,name,email,phone,password,role) VALUES({data['id']},'{data['name']}','{data['email']}','{data['phone']}','{data['password']}','{data['role']}')")
        
        
#         return make_response({"message":"user created successfully"},201)
            

class display_unit_model():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host="localhost",user="root",password="Ga2001pillu14##",database="dunit")
            self.cur=self.con.cursor(dictionary=True)
            self.con.autocommit=True
            self.con2=mysql.connector.connect(host="localhost",user="root",password="Ga2001pillu14##",database="dunit")
            self.cur2=self.con2.cursor(dictionary=True)
            self.con2.autocommit=True
            print("connected successfully")
        except:
            print("some error")
            
    def Station_model(self, data):
        try:
            qry = "INSERT INTO stations(station_id, e_one, e_one_name, e_one_skill, e_two, e_two_name, e_two_skill, process_id, process_name, process_skill) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = [(stationdata.get('station_id'),
                stationdata.get('e_one'),
                stationdata.get('e_one_name'),
                stationdata.get('e_one_skill'),
                stationdata.get('e_two_skill'),
                stationdata.get('e_two_name'),
                stationdata.get('e_two_skill'),
                stationdata.get('process_id'),
                stationdata.get('process_name'),
                stationdata.get('process_skill')
                ) for stationdata in data]
            self.cur.executemany(qry, values)
            if self.cur.rowcount > 0 :
                res= make_response({"message": "Stations(s) added successfully"}, 201)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
            else:
                res= make_response({"message": "Stations(s) not successfully"}, 202)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res

        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
            
        
        # print(data)
        # qry="INSERT INTO stations(station_id, e_one, e_two, process_id) VALUES "
        # for stationdata in data:
        #     qry +=f"('{stationdata['station_id']}','{stationdata['e_one']}','{stationdata['e_two']}','{stationdata['process_id']}')"
        # finalqry = qry.rstrip(",")
        # self.cur.execute(finalqry)
        
        # # res.headers['Access-Control-Allow-Origin']="*"
        # # res.headers['Content-Type']="application/json"
        # return make_response({"message":"Station added successfully"},201)
    def get_process(self,data):
        try:
            qry = "SELECT process_id,process_name,prrocess_skill FROM processes WHERE part_id = %s"  
            values = [data.get('part_id')]
            self.cur.execute(qry,values)
            result = self.cur.fetchall()
            if len(result)>0:
                res = make_response({'payload':result},200)
                res.headers['Access-Control-Allow-Origin']="*"
                return res
            else:
             return make_response({"message":"No Data found"},204)
        
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
        

    def get_process_and_login_data(self,data):
        try:
            qry = "SELECT process_id,process_name,prrocess_skill FROM processes WHERE part_id = %s"  
            values = [data.get('part_id')]
            self.cur.execute(qry,values)
            process_result = self.cur.fetchall()

            qry_login_operators= "SELECT CONCAT(first_name, ' ', last_name) AS full_name, employee_code, skill FROM login_operator"
            self.cur.execute(qry_login_operators)
            employees_result=self.cur.fetchall()

            response_data={
                'process_data':process_result,
                'employess_data':employees_result
            }

            if len(process_result) > 0 or len(employees_result) > 0:
                res = make_response({'payload':response_data},200)
                res.headers['Access-Control-Allow-Origin']="*"
                return res
            else:
             return make_response({"message":"No Data found"},204)
        
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
    
    def task_assigned_model(self, data):
        try:
            now_utc = datetime.now(pytz.utc)
            ist = pytz.timezone('Asia/Kolkata')
            now_ist = now_utc.astimezone(ist)
            assigned_for_date = now_ist.strftime('%Y-%m-%d')
            assigned_timing = now_ist.strftime('%Y-%m-%d')

            qry = "INSERT INTO task_assigned(floor_id, line_id, part_id, part_name, prev_quantity, quantity, assigned_timing, assigned_for_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = [(taskassigned.get('floor_id'),
                taskassigned.get('line_id'),
                taskassigned.get('part_id'),
                taskassigned.get('part_name'),
                taskassigned.get('prev_quantity'),
                taskassigned.get('quantity'),
                assigned_timing,
                assigned_for_date) for taskassigned in data]
           
            self.cur.executemany(qry, values)
            return make_response({"message": "task_assigned successfully"}, 201)
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
    
    # def get_task_assigend_model(self):
    #     try:
    #         self.cur.execute("SELECT * FROM task_assigned WHERE floor_id = 1")
    #         result=self.cur.fetchall()
    #         if len(result)>0:
    #           res = make_response({'payload':result},200)
    #           res.headers['Access-Control-Allow-Origin']="*"
    #           return res
    #         else:
    #             return make_response({"message":"No Data found"},204)
    #     except mysql.connector.Error as err:
    #         print(f"MySQL Error: {err}")
    #         return make_response({"error": "Internal Server Error"}, 500)
    
    def get_asssigned_parts_model(self):
        try:
            self.cur.execute("SELECT * FROM assigned_parts")
            result=self.cur.fetchall()
            if len(result)>0:
              res = make_response({'payload':result},200)
              res.headers['Access-Control-Allow-Origin']="*"
              return res
            else:
                return make_response({"message":"No Data found"},204)
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
    
    def get_task_assigend_model(self,data):
        try:
            qry = "SELECT * FROM task_assigned WHERE assigned_for_date = %s"  
            values = [data.get('assigned_for_date')]
            self.cur.execute(qry,values)
            process_result = self.cur.fetchone()

            # qry_login_operators= "SELECT CONCAT(first_name, ' ', last_name) AS full_name, employee_code, skill FROM login_operator"
            # self.cur.execute(qry_login_operators)
            # employees_result=self.cur.fetchall()

            # response_data={
            #     'process_data':process_result,
            #     'employess_data':employees_result
            # }

            if len(process_result) > 0 :
                res = make_response({'payload':process_result},200)
                res.headers['Access-Control-Allow-Origin']="*"
                return res
            else:
             return make_response({"message":"No Data found"},204)
        
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
        
    def update_assigned_parts_model(self,data):
        try:
            self.con.start_transaction()
            line_id = data.get('line_id')
            part_id = data.get('part_id')
            part_name = data.get('part_name')

        # Update assigned_parts table
            qry1 = """UPDATE assigned_parts SET part_id = %s, part_name = %s WHERE line_id = %s"""
            values1 = [part_id, part_name, line_id]
            self.cur.execute(qry1, values1)

        # Update stations table
            qry2 = """UPDATE stations SET process_id = NULL, process_name = NULL, process_skill = NULL WHERE station_id LIKE %s"""
            pattern = f'% L{line_id} S%'

            values2 = [pattern]
            # qry2="SELECT * FROM stations"
            # self.cur.execute(qry2)
            # result= self.cur.fetchall()
            # print(result)
            self.cur.execute(qry2,values2)

            self.con.commit()

            if self.cur.rowcount > 0:
                return make_response({"status": "Data updated successfully"}, 200)
            else:
                return make_response({"status": "No matching records found for update"}, 401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status": "Rolled Back"}, 400)
        # try:
        #     self.con.start_transaction()
        #     line_id = data.get('line_id')
        #     part_id = data.get('part_id')
        #     part_name = data.get('part_name')

        # # Update assigned_parts table
        #     qry1 = """UPDATE assigned_parts SET part_id = %s, part_name = %s WHERE line_id = %s"""
        #     values1 = [part_id, part_name, line_id]
        #     self.cur.execute(qry1, values1)

        # # Update stations table
        #     # qry2 = """UPDATE stations SET process_id = NULL, process_name = NULL, process_skill = NULL WHERE station_id LIKE %s"""
        #     # pattern = f'% F1 L{line_id} S%'
        #     # values2 = [pattern]
        #     # self.cur.execute(qry2, values2)
        #     qry2 = "SELECT * FROM stations"
        #     self.cur2.execute(qry2)
        #     result = self.cur2.fetchall()
        #     if result is not None:
        #         for row in result:
        #             floor_num, line_num, station_num = row['station_id'].split(' ')
        #             transformed_row = {
        #                 'station_id': row['station_id'],
        #                 'floor_num': int(floor_num[1:]),
        #                 'line_num': int(line_num[1:]),
        #                 'station_num': int(station_num[1:]),
        #                 'e_one': row['e_one'],
        #                 'e_one_name': row['e_one_name'],
        #                 'e_one_skill': row['e_one_skill'],
        #                 'e_two': row['e_two'],
        #                 'e_two_name': row['e_two_name'],
        #                 'e_two_skill': row['e_two_skill'],
        #                 'process_id': row['process_id'],
        #                 'process_name': row['process_name'],
        #                 'process_skill': row['process_skill']
        #             }
        #             if str(int(line_num[1:])) == str(line_id):
        #                 row['process_id'] = None
        #                 row['process_name'] = None
        #                 row['process_skill'] = None



        #     self.con.commit()

        #     if self.cur.rowcount > 0:
        #         return make_response({"status": "Data updated successfully"}, 200)
        #     else:
        #         return make_response({"status": "No matching records found for update"}, 401)
        # except Exception as e:
        #     print(e)
        #     self.con.rollback()
        #     return make_response({"status": "Rolled Back"}, 400)
    
    def get_task_model(self):
        try:
            now_utc = datetime.now(pytz.utc)
            ist = pytz.timezone('Asia/Kolkata')
            now_ist = now_utc.astimezone(ist)
            assigned_for_date = now_ist.strftime('%Y-%m-%d')
            values = [assigned_for_date]
            qry = "SELECT * FROM task_assigned WHERE assigned_for_date = %s"
            self.cur.execute(qry,values)
            result=self.cur.fetchall()
            if len(result)>0:
              res = make_response({'payload':result},200)
              res.headers['Access-Control-Allow-Origin']="*"
              return res
            else:
                return make_response({"message":"No Data found"},204)
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)

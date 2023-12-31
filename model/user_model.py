from io import BytesIO
from tkinter import Image
import mysql.connector
import base64
import json
import os
from flask import jsonify, make_response
class user_model():
    def __init__(self):
        try:
            self.con =  mysql.connector.connect(host="localhost",user="root",password="amzad",database="vft_app")
            self.con.autocommit = True
            self.con._connection_timeout = 25
            self.cur = self.con.cursor(dictionary=True)
            self.con2 =  mysql.connector.connect(host="localhost",user="root",password="amzad",database="dunit")
            self.con2.autocommit = True
            self.con2._connection_timeout = 25
            self.cur2 = self.con2.cursor(dictionary=True)
            print("success")
        except mysql.connector.Error as err:
            print(f"Error: {err}")


###############check API
    def operator_check_model(self):
        self.cur2.execute("SELECT * from login_operator")
        result = self.cur2.fetchall()

        if len(result)>0:
            # return json.dumps(result)
            # return{"payload": result}
            res = make_response({"payload": result},200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        else:
            # return {"message":"No Data Found"}
            return make_response({"message":"No Data Found"},204)
             # message is not shown for 204    

###########################   LOGIN API   ##########3################
    def operator_login_model(self,data):
        try:
            employee_code = data.get('employee_code')
            password = data.get('password')

            # Construct and execute the query
            query = f"SELECT * FROM login_operator WHERE employee_code = '{employee_code}' AND password = '{password}'"
            self.cur2.execute(query)
            result = self.cur2.fetchone()

            if result is not None:
                # return json.dumps(result)
                # return{"payload": result}
                res = make_response({"logindata": result},200)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
            else:
                # return {"message":"No Data Found"}
                print("good")
                res = make_response({"logindata":"No Data Found"},401)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
                # message is not shown for 204    
        except:
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return make_response({"logindata":"Got error"},202)


###########################   GET TASK API   ##########################
    def operator_gettask_model(self,data):
        try:
            station_id = data.get('station_id')
            split_items = station_id.split()
            print(split_items)
            if len(split_items) == 3:
                F1, L1, S1 = split_items

                # Further split each part
                F1_part1, F1_part2 = F1[0], F1[1:]
                L1_part1, L1_part2 = L1[0], L1[1:]
                S1_part1, S1_part2 = S1[0], S1[1:]

                print("F1:", F1_part1, F1_part2)
                print("L1:", L1_part1, L1_part2)
                print("S1:", S1_part1, S1_part2)

                query = f"SELECT * FROM task_assigned WHERE line_id = '{L1_part2}' AND floor_id = '{F1_part2}'"
                self.cur2.execute(query)
                result = self.cur2.fetchone()
                if result is not None:
                    res = make_response({"taskdata": result},200)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                else:
                    print("good")
                    res = make_response({"taskdata":"No task assigned"},201)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                     
            else:
                res = make_response({"taskdata": "Invalid Station ID"},202)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res 
        except:
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return make_response({"taskdata":"Got error"},203)



###########################   LOGIN ADMIN API   ##########################
    def operator_loginadmin_model(self,data):
        try:
            employee_code = data.get('employee_code')
            password = data.get('password')

            # Construct and execute the query
            query = f"SELECT * FROM login_admin WHERE employee_code = '{employee_code}' AND password = '{password}'"
            self.cur2.execute(query)
            result = self.cur2.fetchone()

            if result is not None:
                # return json.dumps(result)
                # return{"payload": result}
                res = make_response({"logindata": result},200)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
            else:
                # return {"message":"No Data Found"}
                print("good")
                res = make_response({"logindata":"No Data Found"},401)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
                # message is not shown for 204    
        except Exception as e:
            print(e)
            res = make_response({"logindata":"Got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return res


###########################   GET FLOOR DETAILS API   ##########################
    def floor_model(self,data):
        try:
            floor_id = data.get('floor_id')
        
            # Construct and execute the query
            query = f"SELECT * FROM floors WHERE floor_id = '{floor_id}'"
            self.cur2.execute(query)
            result = self.cur2.fetchone()

            if result is not None:
                # return json.dumps(result)
                # return{"payload": result}
                res = make_response({"floordata": result},200)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
            else:
                # return {"message":"No Data Found"}
                print("good")
                res = make_response({"floordata":"No Data Found"},401)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
                # message is not shown for 204    
        except:
            res = make_response({"floordata":"Got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return res


###########################   GET STATIONS DETAILS API   ##########################
    def station_model(self):
        try:
            # Construct and execute the query
            query = f"SELECT * FROM stations"
            self.cur2.execute(query)
            result = self.cur2.fetchall()

            if result is not None:
            
                transformed_data = []
                for row in result:
                    floor_num, line_num, station_num = row['station_id'].split(' ')
                    transformed_row = {
                        'floor_num': int(floor_num[1:]),  # Extract numeric part and convert to int
                        'line_num': int(line_num[1:]),
                        'station_num': int(station_num[1:]),
                        'e_one': row['e_one'],
                        'e_two': row['e_two'],
                        'process_id': row['process_id']
                    }
                    transformed_data.append(transformed_row)
                    # Return the transformed data in JSON format
                print(transformed_data)
                response = make_response(jsonify({'stationdata': transformed_data}), 200)
                response.headers['Access-Control-Allow-Origin'] = "*"
                response.headers['Content-Type'] = 'application/json'
                return response
            else:
                # return {"message":"No Data Found"}
                print("good")
                res = make_response({"stationdata":"No Data Found"},401)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
                # message is not shown for 204    
        except:
            res = make_response({"stationdata":"got error"},401)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'



###########################   ADD LINE API   ##########################
    def add_line_model(self,data):
        try:
            floor_id = data.get('floor_id')
            # Construct and execute the query
            query = f"SELECT number_of_lines FROM floors WHERE floor_id = '{floor_id}'"
            self.cur2.execute(query)
            result = self.cur2.fetchone()
           
            if result is not None:
                number_of_lines = int(result.get('number_of_lines', 0))
                print(result)
                print(number_of_lines)
                query_update = f"UPDATE floors SET number_of_lines = '{number_of_lines}' + 1 WHERE floor_id = '{floor_id}'"
                self.cur2.execute(query_update)
                res = make_response({"floordata":"Added"},200)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
            else:
                # return {"message":"No Data Found"}
                print("good")
                res = make_response({"floordata":"No Data Found"},201)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
                # message is not shown for 204    
        except:
            res = make_response({"floordata":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'

###########################   GET FLOOR PARTS API   ##########################
    def get_floor_parts_model(self,data):
        try:
            floor_id = data.get('floor_id')
            # Construct and execute the query
            query = f"SELECT * FROM parts WHERE floor_id = '{floor_id}'"
            self.cur2.execute(query)
            result = self.cur2.fetchall()
            
            if result is not None:
                
                res = make_response({"floorpartsdata": result},200)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
            else:
                # return {"message":"No Data Found"}
                print("good")
                res = make_response({"floorpartsdata":"No Data Found"},201)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
                # message is not shown for 204    
        except:
            res = make_response({"floorpartsdata":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'


###########################   GET CHECKSHEET API   ##########################
    def get_checksheet_model(self):
        try:
            # Construct and execute the query
            query = f"SELECT * FROM checksheet"
            self.cur2.execute(query)
            result = self.cur2.fetchall()
           
            if result is not None:
                res = make_response({"checksheet": result},200)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
            else:
                # return {"message":"No Data Found"}
                print("good")
                res = make_response({"checksheet":"No Data Found"},201)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
                # message is not shown for 204    
        except:
            res = make_response({"checksheet":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'            

 
###########################   GET INSTRUCTION API   ##########################
    def get_instructionimage_model(self,data):
        try:
            station_id = data.get('station_id')
            query = f"SELECT process_id FROM stations WHERE station_id = '{station_id}'"
            self.cur2.execute(query)
            result = self.cur2.fetchone()
           
            if result is not None:
                process_id = int(result.get('process_id', 0))
                query = f"SELECT * FROM processes WHERE process_id = '{process_id}'"
                self.cur2.execute(query)
                result = self.cur2.fetchone()

                if result is not None:
                    res = make_response({"instructionImage": result},200)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                else:
                    print("not good")
                    res = make_response({"instructionImage":"No Data Found"},201)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res

            else:
                # return {"message":"No Data Found"}
                print("good")
                res = make_response({"instructionImage":"No Data Found"},201)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
                # message is not shown for 204    
        except:
            res = make_response({"instructionImage":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'            

#VFT

    def getAllUsers_model(self):
        self.cur.execute("SELECT * FROM centers")
        result =  self.cur.fetchall()

        if len(result)>0:
            # return json.dumps(result)
            # return{"payload": result}
            res = make_response({"payload": result},200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        else:
            # return {"message":"No Data Found"}
            return make_response({"message":"No Data Found"},204)
             # message is not shown for 204
        

    def addOneUser_model(self, data):
        self.cur.execute(f"INSERT INTO users(name, roll, password) VALUES('{data['name']}','{data['roll']}','{data['password']}')")
        # print(data['name'])
        return make_response({"message":"User Created Successfully"},201)
        
    

    def updateOneUser_model(self, data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', roll='{data['roll']}' WHERE id={data['id']}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Updated Successfully"},201)
        else:
            return make_response({"message":"No Data Found"},202)
   
        # print(data['name'])
        # return "updating data"    


    def deleteOneUser_model(self, id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Deleted Successfully"},201)
        else:
        # print(data['name'])
            return make_response({"message":"No Data Found"},202)
    
             
        # return result


        # USER VERIFY
    def verifyUser_model(self, username, tabpassword,center):
        self.cur.execute(f"SELECT * FROM users WHERE username='{username}' AND tabpassword='{tabpassword}' AND center = '{center}'")
        result = self.cur.fetchone()

        if result:
            return make_response({"message": "Login Successful"}, 200)
        else:
            return make_response({"message": "Authentication Error"}, 401)

        #USER VERIFY DESKTOP
    def verifyUser_modelpc(self, username, password,center):
        self.cur.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}' AND center = '{center}'")
        result = self.cur.fetchone()

        if result:
            return make_response({"message": "Login Successful"}, 200)
        else:
            return make_response({"message": "Authentication Error"}, 401)


            #CENTER VERIFY
    def verifyCenter_model(self, id, lat, lon):
        # self.cur.execute(f"SELECT * FROM centers WHERE id='{id}' AND (lat - {lat} < 2.5 OR lat - {lat} < 2.5) AND (lon - {lon} < 2.5 OR lon - {lon} < 2.5)")
        # self.cur.execute(f"SELECT * FROM centers WHERE (lat > {lat} - 0.5 OR lat < {lat} + 0.5) AND (lon > {lon} - 0.5 OR lon < {lon} + 0.5)")
        self.cur.execute(f"SELECT * FROM centers WHERE id='{id}' AND (lat >= {lat} - 1 AND lat <= {lat} + 1) AND (lon >= {lon} - 1 AND lon <= {lon} + 1)")

        result =  self.cur.fetchall()

        print(result)
        if len(result)>0:
            # return json.dumps(result)
            # return{"payload": result}
            return make_response({"status": "Found"},200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            # return res
        else:
            # return {"message":"No Data Found"}
            return make_response({"status":"No Data Found"},204)
            # return "failed"
             # message is not shown for 204


     #Check Pending Test
    def checkPendingTest_model(self, center):
        # self.cur.execute(f"SELECT * FROM centers WHERE id='{id}' AND (lat - {lat} < 2.5 OR lat - {lat} < 2.5) AND (lon - {lon} < 2.5 OR lon - {lon} < 2.5)")
        # self.cur.execute(f"SELECT * FROM centers WHERE (lat > {lat} - 0.5 OR lat < {lat} + 0.5) AND (lon > {lon} - 0.5 OR lon < {lon} + 0.5)")
        try:
            print(center)
            self.cur.execute(f"SELECT * FROM tests WHERE center='{center}' AND stage = 1")
            result =  self.cur.fetchone()
            print(result)
            if  result:
                test_id = result['id']
                mStage = result['stage']
                print(f"Test ID: {test_id}")

                self.cur.execute(f"SELECT * FROM appointments WHERE id = '{test_id}' AND testcenter='{center}'")
                result =  self.cur.fetchone()

            # return json.dumps(result)
                return{"payload": result,"id":test_id, "stage": mStage}
            # return make_response({"status": "Found"},200)
                res.headers['Access-Control-Allow-Origin'] = "*"
            # return res
            else:
            # return {"message":"No Data Found"}
                return make_response({"status":"No Data Found"},400)
            # return "failed"
             # message is not shown for 204
        except Exception as e: 
                print(e)
        
    #GETVEHICLEDATA
    def checkTest_model(self, id):
        # self.cur.execute(f"SELECT * FROM centers WHERE id='{id}' AND (lat - {lat} < 2.5 OR lat - {lat} < 2.5) AND (lon - {lon} < 2.5 OR lon - {lon} < 2.5)")
        # self.cur.execute(f"SELECT * FROM centers WHERE (lat > {lat} - 0.5 OR lat < {lat} + 0.5) AND (lon > {lon} - 0.5 OR lon < {lon} + 0.5)")
        self.cur.execute(f"SELECT * FROM tests WHERE id='{id}'")

        result =  self.cur.fetchone()

        print(result)
   
        return{"payload2": result}
        
        

    #TEST STATUS
    def checkVehicle_model(self, id):
        self.cur.execute(f"SELECT * FROM appointments WHERE vehicalnumber='{id}'")

        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

        
        

        #HEADLAMP STATUS
        


       #ADD HEADLMAP TEST ONE
      


    #ADD HEADLMAP TEST ONE
    def addHeadlampTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testheadlamp(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testheadlamp = '{status}' WHERE id='{id}'")
            self.con.commit()
            # print(len(img))
            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},402)

    #ADD TOPLIGHT TEST ONE
    def addTopLightTest_one_model(self, id,p1,p2,p3,p4,p5,p6,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testtoplight(id,p1,p2,p3,p4,p5,p6,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{p6}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testtoplight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD STOPLIGHT TEST ONE
    def addStopLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO teststoplight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET teststoplight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD PARKINGLIGHT TEST ONE
    def addParkingLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testparkinglight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testparkinglight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD FOGLIGHT TEST ONE
    def addFogLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testfoglight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testfoglight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD WARNINGLIGHT TEST ONE
    def addWarningLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testwarninglight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testwarninglight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD NUMBEPLATELIGHT TEST ONE
    def addPlateLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testnumberplatelight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testnumberplatelight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD MARKERLIGHT TEST ONE
    def addMarkerLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testoutlinemarkerlight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testoutlinemarkerlight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD MARKERLIGHT TEST ONE
    def addDirectionLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testdirectionlight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testdirectionlight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD HAZARDLIGHT TEST ONE
    def addHazardLightTest_one_model(self, id,p1,p2,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testhazardlight(id,p1,p2,remark,status,img) VALUES('{id}','{p1}','{p2}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testhazardlight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)


    #ADD SUPRESSOR TEST ONE
    def addSupressorTest_one_model(self, id,p1,p2,p3,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testsupressor(id,p1,p2,p3,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testsupressor = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD SAFETY GLASS TEST ONE
    def addSafetyGlassTest_one_model(self, id,p1,p2,p3,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testsafetyglass(id,p1,p2,p3,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testsafetyglass = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD HORN TEST ONE
    def addHornTest_one_model(self, id,p1,p2,p3,p4,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testhorn(id,p1,p2,p3,p4,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testhorn = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            print(e)
            return make_response({"status":"Rolled Back"},400)

    #ADD EXHAUST TEST ONE
    def addexhaustTest_one_model(self, id,p1,p2,p3,p4,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testexhaust(id,p1,p2,p3,p4,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testexhaust = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD WIPER SYSTEM TEST ONE
    def addwsystemTest_one_model(self, id,p1,p2,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testwipersystem(id,p1,p2,remark,status,img) VALUES('{id}','{p1}','{p2}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testwipersystem = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD WIPER BLADE TEST ONE
    def addwbladeTest_one_model(self, id,p1,p2,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testwiperblade(id,p1,p2,remark,status,img) VALUES('{id}','{p1}','{p2}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testwiperblade = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD DASH TEST ONE
    def addDashTest_one_model(self, id,p1,p2,p3,p4,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testdashboard(id,p1,p2,p3,p4,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testdashboard = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD BRAKE TEST ONE
    def addBrakeTest_one_model(self, id, status):
        try:
            self.con.start_transaction()
            # self.cur.execute(f"INSERT INTO testdashboard(id,p1,p2,p3,p4,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testbrake = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)
                  
 
    #ADD DASH TEST ONE
    def addCompleteTest_one_model(self, id,mstatus):
        try:

            self.cur.execute(f"UPDATE tests SET stage = 2,mtest = '{mstatus}' WHERE id='{id}'")

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Submitted"},200)
            else:
                return make_response({"status":"Cannot submit"},401)
        except Exception as e:
            print(e)
            return make_response({"status":"Error"},400)  
             
     #CHECK TEST
    def checkTest_one_model(self, id, center):
        try:
            # self.cur.execute(f"INSERT INTO testdashboard(id,p1,p2,p3,p4,remark,status) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}')")
            self.cur.execute(f"SELECT * FROM tests WHERE stage = 1")
            result = self.cur.fetchone()

            if result:
                print(result)
                return make_response({"status":"Test Already Running"},401)
            else:
                self.cur.execute(f"INSERT INTO tests(id,center,stage) VALUES('{id}','{center}',1)")
                result =  self.cur.fetchone()
                if self.cur.rowcount>0:
                    return make_response({"status":"Test Added"},200)
                else:
                    return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            return make_response({"status":"Error"},400)

    #CHECK TEST DATA
    def checkTestData_one_model(self, id, center):
        try:
            
            # self.cur.execute(f"INSERT INTO testdashboard(id,p1,p2,p3,p4,remark,status) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}')")

            self.cur.execute(f"SELECT * FROM tests WHERE id = '{id}'")
            result = self.cur.fetchone()

            if result:
                return make_response({"payload":result},200)
            else:
                return make_response({"payload":"Not found"},401)
        except Exception as e:
            print(e)
            return make_response({"status":"Error"},400)

    #HEADLAMP TEST STATUS
    def checkTest_headlamp_model(self, id): 
        
        try:
            self.cur.execute(f"SELECT * FROM testheadlamp WHERE id='{id}'")
            result =  self.cur.fetchone()

            if result:
                print(result)
                return{"payload": result}

            else: 
                return make_response({"status":"No Data Found"},204)
        except Exception as e: 
                print(e)
                  
    #TOP LIGHT STATUS
    def checkTest_toplight_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testtoplight WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

    #HEADLAMP TEST STATUS
    def checkTest_supressor_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testsupressor WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

    #HEADLAMP TEST STATUS
    def checkTest_safetyglasses_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testsafetyglass WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

    #HEADLAMP TEST STATUS
    def checkTest_horn_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testhorn WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)
        
      #HEADLAMP TEST STATUS
    def checkTest_exhaust_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testexhaust WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)    

    #HEADLAMP TEST STATUS
    def checkTest_wiperblade_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testwiperblade WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

    #HEADLAMP TEST STATUS
    def checkTest_wipersystem_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testwipersystem WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

    #HEADLAMP TEST STATUS
    def checkTest_dashboard_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testdashboard WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                                                                                                                                                
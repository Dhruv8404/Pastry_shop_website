
#users = []
def userExists(userData,cursor):
    #Execute sql query
    
    sql_query=f'''
        select * from users;
    
    '''
    try:  
     cursor.execute(sql_query)
     users=cursor.fetchall()
    except Exception as e:
     print("Error:",e)
    print('users:')
    print(users)
    
    email = userData['email']
    
    for user in users:
        if user[7] == email:
            # email found
            return {'response': True, 'user': user}
    
    # email not found
    return {'response': False, 'user': {}}

def registerUser(userData,cursor):
   
    # check email id is register or not
   
    checkUser =  userExists(userData,cursor)
    
    if (checkUser['response']):
       return{'statusCode':503,'message':"already registered"}  
    else:
      #  users.append(userData) 
        sql_query=f'''
                   insert into users(name,contact, address, landmark, city, pincode,email,password) values ('{userData['name']}','{userData['contact']}','{userData['address']}','{userData['landmark']}','{userData['city']}','{userData['pincode']}','{userData['email']}','{userData['password']}')
        
        '''
        try:
         cursor.execute(sql_query)
        except Exception as e:
         print("Error:",e)
        return{'statusCode':200,'message':"registered"}  
    
def loginUser(userData,cursor):
    # check email id is register or not
    checkUser =  userExists(userData,cursor)
    if (checkUser['response']):
        
        if userData['password']==checkUser['user'][8]:
             return{'statusCode':200,'message':"loggdin"}
        else:
              return{'statusCode':503,'message':" password error"} 
    else:
      # users.append(userData) 
        return{'statusCode':503,'message':" already registered"} 
 
def getUserDataByEmail(email, cursor):
    try:
        sql_query = f'''
            SELECT * FROM users
            WHERE email = %s;
        '''
        cursor.execute(sql_query, (email,))
        user_data = cursor.fetchone()
        return user_data
    except Exception as e:
        print("Error:", e)
        return None  


def updateUserData(userData, cursor):
    # Check if the email exists in the 'users' table
    checkUser = userExists(userData, cursor)

    if not checkUser['response']:
        return {'statusCode': 404, 'message': "User not found"}

    # Update user information
    sql_query = f'''
        UPDATE users
        SET address='{userData['address']}',
            landmark='{userData['landmark']}',
            city='{userData['city']}',
            pincode='{userData['pincode']}',
            contact='{userData['contact']}'
        WHERE email='{userData['email']}';
    '''

    try:
        cursor.execute(sql_query)
        return {'statusCode': 200, 'message': "Profile updated successfully"}
    except Exception as e:
        print("Error:", e)
        return {'statusCode': 500, 'message': "Update failed"}


# Assuming you have the required imports and functions defined...

def store_atm_card_data(userData, cursor):
    checkUser = userExists(userData, cursor)

    if not checkUser['response']:
        return {'statusCode': 404, 'message': "User not found"}  
    
    sql_query = f'''
        UPDATE users
        SET card_number = '{userData['card_number']}', card_holder_name = '{userData['card_holder_name']}', 
            expiration_date = '{userData['expiration_date']}', cvv = '{userData['cvv']}'
        WHERE email = '{userData['email']}';
    '''
    try:
        cursor.execute(sql_query)
        return {'statusCode': 200, 'message': "Profile updated successfully"}
    except Exception as e:
        print("Error:", e)
        return {'statusCode': 500, 'message': "Update failed"}


        
     

    
 
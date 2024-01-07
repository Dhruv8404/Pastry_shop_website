from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .utils import registerUser, loginUser,getUserDataByEmail, updateUserData,store_atm_card_data
import json
import psycopg2
from django.contrib.sessions.backends.db import SessionStore
import requests
from django.urls import reverse
import socket


# Create your views here.

s=SessionStore()

try:
    connection = psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        database="memestore",
        user="postgres",
        password="pgadmin"
    )
 
    print("Database connected")
except Exception as e:
    print("Error:",e)
    print("Database connection failed")

connection.autocommit = True
cursor = connection.cursor()


#Middlewere

def checkSession():
  try:
      email = s['email']
      return True
  except Exception as e:
      print('Error:',e)
      return False

def home(request):
    return HttpResponse('This is the home page')


def register(request):
    sessionExists= checkSession()
  
          
    if request.method == 'POST':
        # Collect data from the client
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']
        landmark = request.POST['landmark']
        city = request.POST['city']
        pincode = request.POST['pincode']
        email = request.POST['email']
        password = request.POST['password']

    

        # Print data
        print(f'Name: {name}')
        print(f'Contact: {contact}')
        print(f'Address: {address}')
        print(f'Landmark: {landmark}')
        print(f'City: {city}')
        print(f'Pincode: {pincode}')
        print(f'Email: {email}')
        print(f'Password: {password}')
        

        # Create user dictionary
        userData = {
            'name': name,
            'contact': contact,
            'address': address,
            'landmark': landmark,
            'city': city,
            'pincode': pincode,
            'email': email,
            'password': password,
           
        }

        # Save user data to the 'users' table in the database
        response = registerUser(userData, cursor)  # Assuming this function saves data to the 'users' table
        
        print('Response::')
        print(response)

        if response['statusCode'] == 200:
            # Session Store
            s['email'] = userData['email']
            s['password'] = userData['password']
            print('Session:::', s)

            return render(request, 'placeorder.html',{ 'name': name,
            'contact': contact,
            'address': address,
            'landmark': landmark,
            'city': city,
            'pincode': pincode,
            'email': email })
        else:
            return render(request, 'register.html', {'message': 'Already registered'})

    else:
        return render(request, 'register.html')

def update_profile(request):
    if request.method == 'POST':
        # Collect data from the client
        email = request.POST['email']
        address = request.POST['address']
        landmark = request.POST['landmark']
        city = request.POST['city']
        pincode = request.POST['pincode']
        contact = request.POST['contact']

      

        # Rest of your code to update the user data
        # ...


        # Print data
        print(f'Email: {email}')
        print(f'Address: {address}')
        print(f'Landmark: {landmark}')
        print(f'City: {city}')
        print(f'Pincode: {pincode}')
        print(f'Contact: {contact}')
       

        # Create user dictionary with updated data
        userData = {
            'email': email,
            'address': address,
            'landmark': landmark,
            'city': city,
            'pincode': pincode,
            'contact': contact,
           
        }

        # Update user data in the 'users' table
        response = updateUserData(userData, cursor)  # Assuming this function updates data in the 'users' table

        print('Response:')
        print(response)

        if response['statusCode'] == 200:
            return render(request, 'placeorder.html')
        else:
            return render(request, 'update_profile.html', {'message': 'Update failed'})

    else:
        return render(request, 'update_profile.html')

def login(request):
    
      sessionExists= checkSession()
   
  
   
    
      if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Print data
        print('Email:')
        print(email)
        print('Password:')
        print(password)

        userData = {
            'email': email,
            'password': password
        }

        # Register user
        response = loginUser(userData,cursor)

        if response['statusCode'] == 200:
            
              #Session Store
            s['email']=userData['email']
            s['password']=userData['password']
            print('Session:::',s)
            
            
            #return render(request, 'login.html', {'message': 'Successfully logged in'})
            return redirect('/main/pastry/')
        elif response['statusCode'] == 503 and response['message'] ==" password error":
            return render(request, 'login.html', {'message': 'Password does not match'})
        
        else:
            return render(request, 'login.html', {'message': 'Not registered'})

      else:
        return render(request, 'login.html')
 
  
def profile(request):
    sessionExists = checkSession()

    if sessionExists:
        try:
            email = s['email']
            # Fetch user registration data from the database using the email
            user_data = getUserDataByEmail(email, cursor)

            if user_data:
                return render(request, 'profile.html', {'user_data': user_data})
            else:
                return HttpResponse('User data not found.')
        except Exception as e:
            print('Error:', e)
            return HttpResponse('An error occurred while fetching user data.')
    else:
        return HttpResponse('You need to log in to view your profile.')


def logout (request):
    try:
        s.clear()
        return redirect('/main/login/')
    except:
        return redirect('/main/pastry/')     
 
def about(request):
    
    
  return render(request, 'about.html') 
  
def pastry(request):
    sessionExists =checkSession()
   
    products = [
        {'image': 'https://www.foodelicacy.com/wp-content/uploads/2020/11/fruit-cake-4C.jpg', 'description': 'pastry 1','price':800},
        {'image': 'https://images.pexels.com/photos/1854652/pexels-photo-1854652.jpeg?cs=srgb&dl=pexels-elli-1854652.jpg&fm=jpg', 'description': 'This is Product 2','price':200},
        {'image': 'https://images.unsplash.com/photo-1620980776848-84ac10194945?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fHBhc3RyeXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60', 'description': 'This is Product 3','price':200},
    ]
    return render(request, 'pastry.html',{'products': products})


def shop(request):
    sessionExists =checkSession()
    products = [
        {'image': 'https://www.foodelicacy.com/wp-content/uploads/2020/11/fruit-cake-4C.jpg', 'description': 'pastry 1','price':800},
        {'image': 'https://images.pexels.com/photos/1854652/pexels-photo-1854652.jpeg?cs=srgb&dl=pexels-elli-1854652.jpg&fm=jpg', 'description': 'This is Product 2','price':200},
        {'image': 'https://images.unsplash.com/photo-1620980776848-84ac10194945?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fHBhc3RyeXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60', 'description': 'This is Product 3','price':200},
        {'image':'https://j6e2i8c9.rocketcdn.me/wp-content/uploads/2021/05/Eggless-Black-forest-Pastry-recipe-1.jpg','description':'product 4','price':200},
        {'image':'https://images.unsplash.com/photo-1603532648955-039310d9ed75?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cGFzdHJ5fGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60','description':'product 4','price':200},
        {'image':'https://images.unsplash.com/photo-1605090930904-22cdf6dc608b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fHBhc3RyeXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60','description':'product 4','price':200},
        {'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRPtyHwaVOdLH__DQpcai00LHObAo_C-RqGRA&usqp=CAU','description':'product 4','price':200},
        {'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAsfEtaudqeb5O2WSCOtmi4kb1QaJ525ohsA&usqp=CAU','description':'product 4','price':200}
    ]
    return render(request, 'shop.html', {'products': products})

cart = []

def addtocart(request):
    sessionExists = checkSession()
    if request.method == 'POST':
        # Retrieve the product data from the form
        image = request.POST.get('image')
        description = request.POST.get('description')
        price = request.POST.get('price')

        # Check if the product already exists in the cart
        for item in cart:
            if item['image'] == image:
                # Product already exists, update quantity and return
                item['quantity'] += 1
                return HttpResponseRedirect(reverse('showcart'))

        # Check if the price value is None
        if price is None:
            # Handle the case when the price is not provided
            price = 0
        else:
            # Convert the price to an integer
            price = int(price)

        # Add the product to the cart with a quantity of 1
        cart.append({'image': image, 'description': description, 'price': price, 'quantity': 1})

    # Render the addtocart.html template with the updated cart data
    return render(request, 'addtocart.html', {'cart': cart})

def showcart(request):
    sessionExists = checkSession()
    return render(request, 'addtocart.html', {'cart': cart})
    
def removefromcart(request):
    sessionExists = checkSession()
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'remove':
            image = request.POST.get('image')

            # Find and remove the product from the cart
            for item in cart:
                if item['image'] == image:
                    cart.remove(item)
                    break
        elif action == 'clear':
            cart.clear()

    return HttpResponseRedirect(reverse('showcart'))


    


# Assuming you have the required imports and functions defined...

def payment(request):
    sessionExists = checkSession()

    if request.method == 'POST':
        # Collect data from the client
        card_number = request.POST['card_number']
        card_holder_name = request.POST['card_holder_name']
        expiration_date = request.POST['expiration_date']
        cvv = request.POST['cvv']
        email = request.POST['email']
        
        userData = {
            'card_number': card_number,
            'card_holder_name': card_holder_name,
            'expiration_date': expiration_date,
            'cvv': cvv,
            'email': email
        }
        
        response = store_atm_card_data(userData, cursor)  # Assuming this function updates data in the 'users' table

        print('Response:')
        print(response)

        if response['statusCode'] == 200:
            return render(request, 'card.html',{'message':'register'})  # Replace 'success.html' with the appropriate template for payment success
        else:
            return render(request, 'card.html',{'message':' not register'})  # Replace 'error.html' with the appropriate template for update failure

    else:
        return render(request, 'card.html')

       
def place_order(request):
    sessionExists = checkSession()

    if sessionExists:
        try:
            email = s['email']
            # Fetch user registration data from the database using the email
            user_data = getUserDataByEmail(email, cursor)

            if user_data:
                
                # Pass the cart data to the template
                return render(request, 'placeorder.html', {'user_data': user_data, 'cart': cart})
            else:
                return HttpResponse('User data not found.')
        except Exception as e:
            print('Error:', e)
            return HttpResponse('An error occurred while fetching user data.')
    else:
        return render(request, 'login.html')

      
 


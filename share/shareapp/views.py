from django.shortcuts import render
from django.http import JsonResponse
from ipware import get_client_ip
import ipaddress
from .models import *
from django.contrib.auth.hashers import check_password
from Crypto.PublicKey import RSA 
import os
from django.http import HttpResponse, Http404





def ipCheck(request):
    #set ip
    request.META['REMOTE_ADDR'] = '172.16.1.1'
    client_ip, is_routable = get_client_ip(request)
    #ip not set by proxy or vpn
    # if client_ip is not None and is_routable is True:
    if client_ip is not None:
        if ipaddress.IPv4Address(client_ip) in ipaddress.IPv4Network('172.16.0.0/12'):
            # return render(request, 'sign_in.html', {'client_ip': client_ip})
            return render(request, 'login.html', {'client_ip': client_ip})
        else:
            return render(request, 'not_found.html')
    else:
        return render(request, 'not_found.html')

# def loginError(request):
#     return render(request, 'index.html')


def auth(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    userData = Users.objects.get(username=email)
    is_password_correct = check_password(password, userData.password)
    
    if is_password_correct:
        request.session['username'] = email
        keygen(email)
        return JsonResponse({'status': 'Success'})
    else:
        return JsonResponse({'status': 'Error'})
    
def keygen(email):
    print('Generating..........')
    # Create the directory if it doesn't exist
    if not os.path.exists('keys'):
        os.makedirs('keys')

    # Define the filename and path
    # Find the index of the @ symbol in the email address
    at_index = email.index('@')
    # Extract the text before the @ symbol
    fn = email[:at_index]+'.key'
    #path to private key
    filepath = os.path.join('keys/', fn)    
    #generate keys
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    # Save the private key to a file
    with open(filepath, 'wb') as f:
        f.write(private_key)

    # Create a file path for the public key
    filepath = os.path.join('keys/', 'authorized_keys') 
    # # Save the public key to a file
    with open(filepath, 'wb') as f:
        f.write(public_key)

# def download():
def home(request):
    folder_path = 'public'  # Path to the "public" folder
    # Get the list of folders and files in the "public" folder
    folders = []
    files = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            folders.append(item)
        else:
            files.append(item)

    context = {
        'folders': folders,
        'files': files
    }

    return render(request, 'home.html', context)   

def folder(request): 
    is_allowed=check_keys(request)
    admin=is_admin(request)
    if is_allowed and admin:  
        name = request.POST.get('name')
        folder_path = os.path.join('public', name)  # Construct the folder path
        try:
            os.makedirs(folder_path)  # Create the folder
            return JsonResponse({'status': 'Success'})
        except OSError:
            return JsonResponse({'status': 'Error'})
    else:
        return JsonResponse({'status': 'Error'})
    
def upload_folder(request):
    print('Uploading..........')
    is_allowed=check_keys(request)
    admin=is_admin(request)
    if is_allowed and admin:
        print('Uploading..........')
        if request.method == 'POST':
            files = request.FILES.getlist('folder')
            folderName = request.POST.get('folder_name')

            # Check if the folder exists in the "public" directory
            folderPath = os.path.join('public', folderName)
            if not os.path.exists(folderPath):
                os.makedirs(folderPath)

            # Process and save the files
            for f in files:
                # Save the file to the desired location using os.path.join
                destination = os.path.join(folderPath, f.name)
                with open(destination, 'wb+') as destination_file:
                    for chunk in f.chunks():
                        destination_file.write(chunk)

            return JsonResponse({'status': 'Success'})
    else:
        return JsonResponse({'status': 'Error'})

def get_files(request):
    folder = request.GET.get('folder')
    if folder:
        folder_path = os.path.join('public', folder)  # Assuming the folder is located inside the 'public' directory
        files = os.listdir(folder_path)
    else:
        files = []

    context = {
        'folder': folder,
        'files': files,
    }
    return render(request, 'files.html', context)

def download_file(request):
    print('Uploading..........')
    is_allowed=check_keys(request)
    if is_allowed:
        file_name = request.GET.get('file')
        folder_name = request.GET.get('folder')
        if folder_name is not None:
            # Construct the file path
            file_path = os.path.join('public', folder_name, file_name)

            # Check if the file exists
            if os.path.exists(file_path):
                # Open the file in binary mode
                with open(file_path, 'rb') as file:
                    # Set the appropriate content type and headers
                    response = HttpResponse(file, content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                    return response
        else:
            # File does not exist, raise Http404
            raise Http404("File n")
    else:
        # Construct the file path
        file_path = os.path.join('public', file_name)

        # Check if the file exists
        if os.path.exists(file_path):
            # Open the file in binary mode
            with open(file_path, 'rb') as file:
                # Set the appropriate content type and headers
                response = HttpResponse(file, content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response
        else:
            # File does not exist, raise Http404
            return JsonResponse({'status': 'Error'})
        
def upload_file(request):
   print('Uploading..........')
   is_allowed=check_keys(request)
   admin=is_admin(request)
   if is_allowed and admin:
    if request.method == 'POST':
         fileName = request.FILES.get('file')
         folder = request.POST.get('folder')
         # Save the file to the specified folder
         file_path = os.path.join('public',folder, fileName.name)
         with open(file_path, 'wb') as destination:
             for chunk in fileName.chunks():
                 destination.write(chunk)

         return JsonResponse({'status': 'Success'})
   else:
    return JsonResponse({'status': 'Error'})

def check_keys(request):
    print("Verifying.........")
    email=request.session.get('username')
    print(email)
    # Define the filename and path for the private key
    at_index = email.index('@')
    private_key_filename = email[:at_index] + '.key'
    private_key_filepath = os.path.join('keys/', private_key_filename)

    # Define the filepath for the public key
    public_key_filepath = os.path.join('keys/', 'authorized_keys')

    # Load the private key from the file
    with open(private_key_filepath, 'rb') as f:
        private_key = RSA.import_key(f.read())

    # Load the public key from the file
    with open(public_key_filepath, 'rb') as f:
        public_key = RSA.import_key(f.read())

    # Check if the public key and private key match
    return private_key.publickey().export_key() == public_key.export_key()

def is_admin(request):
    email=request.session.get('username')
    userData = Users.objects.get(username=email)
    if  userData.is_admin==1:
        return True
    else:
        return False

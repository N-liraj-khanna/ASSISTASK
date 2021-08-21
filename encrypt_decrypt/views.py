from cryptography.fernet import Fernet, InvalidToken
from django.shortcuts import render
from .forms import UploadForm
from django.templatetags.static import static

def handle_uploaded_file(f):  
  ext=f.name.split('.')[-1]
  with open('encrypt_decrypt/static/upload/input.'+ext, 'wb+') as destination:  
      for chunk in f.chunks():  
          destination.write(chunk) 
  return 'encrypt_decrypt/static/upload/input.'+ext

def encrypt(request):
  key=None
  error=None
  if request.method == 'POST':
    form = UploadForm(request.POST, request.FILES) 
    
    if form.is_valid():  
      key = Fernet.generate_key()
      input_file = handle_uploaded_file(request.FILES['file'])        
      output_file = 'lock.lock'

      with open(input_file, 'rb') as f:
          data = f.read()  
          ext=f.name.split('.')[-1]

      fernet = Fernet(key)
      encrypted = fernet.encrypt(data)

      print(key.decode()+'.'+ext)
      key=key.decode()+'.'+ext

      with open('encrypt_decrypt/static/upload/'+output_file, 'wb+') as f:
          f.write(encrypted)
    else:
      error="Something went wrong while encrypting. Please try again later."
      key=None
  else:  
    form = UploadForm()      
  
  return render(request, 'encrypt_decrypt/encrypt.html', context={"key":key, "form": form,"error":error})

def decrypt(request):
  key=None
  error=None
  ext=None
  loc=None
  if request.method == 'POST':
    form = UploadForm(request.POST, request.FILES) 
    key=request.POST.get('key')
    if(len(key)==0):
      key=None
      error="Key can't be empty!"
    elif form.is_valid():  
      ext=key.split('.')[-1]
      key=key[:-len(ext)-1].encode()
      input_file=handle_uploaded_file(request.FILES['file']) 
      output_file='encrypt_decrypt/static/upload/output.'+ext
      print(output_file)
      
      with open(input_file, 'rb') as f:
        data = f.read()
      
      try:
        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)
        with open(output_file, 'wb') as f:
            f.write(decrypted) 
        loc=static('upload/output.'+ext)
      except :
          error="Invalid Key - Unsuccessfully decrypted"
          key=None
    else:
      error="Something went wrong while decrypting. Please try again later."
      key=None
      loc=None
      ext=None
  else:  
    form = UploadForm()      
  
  return render(request, 'encrypt_decrypt/decrypt.html', 
                context={"key":key, "form": form, 'error':error,'ext':ext, 'loc':loc})


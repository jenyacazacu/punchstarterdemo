import os
import cloudinary

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + BASE_DIR + '/app.db'
DEBUG = True

cloudinary.config( 
  cloud_name = "jenyacazacu", 
  api_key = "998443682692361", 
  api_secret = "MK01meyHgZJCAIBGX-vV2bdBS9c" 
)
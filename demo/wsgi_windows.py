# activate_this = 'C:/Users/Yasser/Documents/PythonApp/Notes_Mangement/env/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
# exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/wamp64/www/OceanWind-Ecommerce/venv/Lib/site-packages')




# Add the app's directory to the PYTHONPATH
sys.path.append('C:/wamp64/www/OceanWind-Ecommerce')
sys.path.append('C:/wamp64/www/OceanWind-Ecommerce/demo')

os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
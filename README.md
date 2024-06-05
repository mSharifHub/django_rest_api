# Django Registration Endpoint Testing

## Contributor
#### Mohamed Sharif (repository owner)

## License
#### MIT license Template
##### Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#### The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## About
#### This application is to be run without a User interface and the goal is to test end points using django python application. The application includes postman collections and tests that it can be run locally or using github actions. 

 ## Prerequisites

- Python installed
- Django installed
- Django REST Framework installed
- Recommended PostMan to test collections
## Setting Up the Project

1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-repo/django_back_end.git
   cd django_back_end
   
2. **Create and activate env**:
   ```sh
   python -m venv venv
   source venv/bin/activate 
   
3. **Install dependencies**:
   ```sh
    pip install -r requirements.txt



 ## Testing User Registrations

1. **Register User All Cases**:
   ```sh
   python manage.py test user_app
   


 ## Testing Watch List

1. **Test Base Case**:  
   ```shell
   python manage.py test api.tests.WatchListBaseTestCase

2. **Test Create Watch List Content**:  
   ```shell
   python manage.py test api.tests.CreateWatchListTestCase


3** Retrieve Watch List Content**:  
   ```shell
   python manage.py test api.tests.RetrieveWatchListTestCase







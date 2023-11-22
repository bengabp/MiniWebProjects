## FastAPI Contacts API

All api responses and requests must be written in pydantic models and all request and response fields in the client side must be in `snakeCase`

```python
# Example model
class Contact(BaseModel):
  first_name: str = Field(description = "First name of contact", alias="firstName")
  last_name: str = Field(description = "Last name of contact", alias="lastName")
  company_name: str = Field(description = "Company name of contact", alias="companyName")
  email: str = Field(description = "Email of contact", alias="email")
```
Notice how there is a description and the `alias` argument we have set. This ensures that it is shown as `firstName` and not `first_name` on the client side

Best practices must be followed. Make sure to include proper response status codes for each response in each endpoint
you can use the responses parameter in api.post, api.get api.put and api.delete

```python
@api.get(
  "/{contact_uid}",
  tags=["Contacts"],
  summary="Get Contact",
  description="Very long description about what this endpoint does",
  responses={
    status.HTTP_200_OK:{"model":Contact}
  }
)
async def get_single_contact(request: Request, response: Response, user=Depends(get_current_user)):
  """ Gets a single contact """
  response.status_code = status.HTTP_200_OK
  return Contact()
```
Notice that:
- There is a tags argument
- There is a summary argument
- There is a description for this endpoint
- There is a responses dict for all status codes and their response models
- function accepts request and response as first parameters.
- we are returning a Contact model and not a dictionary with the fields

Your endpoint structure must follow this convention
```python
"""
  |__contacts
  |       |_router.py # All endpoints
  |       |_schemas.py # Model schemas
  |       |_request_schemas.py # Request models
  |       |_response_schemas.py # Response schemas
  |       |___init__.py # Utility functions
  |__app.py
  |_config.py # logging functions and constants
  |_.env
"""
```

You must also include your .env file in your repo when pushing. You could create a dummy mongodb account using a dummy gmail account for this purpose because i will also be checking your collection and documents
## Make sure to create an issue containing information about how to run your project and the link to the pull request you made
- [x] First you have to create a fork of this repository
- [x] Push your changes to your own fork
- [x] Create a pull request against this repo

## Task1:
Create an api using fastapi, ideally, users must be able to upload csv files of specific formats, and your api endpoint must be able to parse the csv, return appropriate responses if its not a valid text/csv content_type, parse the csv and     extract the fields. fields must be validated and must match predefined fields
Objective: The objective of the api is to have an endpoint which accepts a csv form upload . The csv file contains contacts of people and their email (FirstName, Email, Lastname, Company_name)
This information should be saved in a database. so that when a user uploads another csv the records are extracted and added to the fields that the user already has in the database.

Any uploaded csv must have atleast these headers
```json
{
  "firstName":"Ben",
  "lastName":"Gab",
  "email":"bengab@gmail.com",
  "companyName":"samsung"
}
```
others can be ignored as we are only concerned about these fields.

## Task2: 
Create another endpoint GET /contacts?date="2023/8/20"
This endpoint would return all the contacts that the user has ever uploaded.
There is also option to specify query parameters like date ranges . lets say user specifies date to be "2023/4/5" it sould get
all contact files that have their upload date equal to that date . lets say user specifies date to be "2023/4/5 - 2023/4/10" it should get
all contact files that have their upload date within that date range.

The return format is 
```json
{
	"contacts":[
		{
			"uid":"98989adfadf",
			"uploadDate":"2023/4/5",
			"totalContacts":3000
		},
		{
			"uid":"98989adfadf",
			"uploadDate":"2023/4/5",
			"totalContacts":3000
		},
		{
			"uid":"98989adfadf",
			"uploadDate":"2023/4/5",
			"totalContacts":3000
		},
	],
	"totalContacts":20
}
```

## Task3: 
Create a similar endpoint to task2 but for getting the info of one speficif contact file using their contact_file_uid
/contacts/{uid}


## Task4 :
create an endpoint for downloading the a contact file (csv of contacts). It should return a 
fastapi Response object that returns a file, the file must have its content_type set to text/csv
you can defined Test Bearer token in your app to a static value. the aim is to deny any user 
trying to download a contactfile which does not belong to them. Remember that contacts are uploaded in 
csv so we also want to download them in csv. when the user specifies the contact uid, 
all contacts under that uid must be returned as a csv file

For example, In Task 1 user has uploaded a file called excluded_contacts.csv the schema for the contact object would be
```json
{
	"uid":"334343saedfadf",
	"filename":"adfadfadfadf.csv",
	"uploadedDate":"2023/4/5",
	"totalContacts":3000
}
```

This shows that the contact file uploaded has 3000 contacts in it. a contact is represented in this format

```json
{
	"firstName":"Ben",
	"lastName":"Gab",
	"email":"bengab@gmail.com",
	"companyName":"samsung"
}
```

a typical request would be GET /contacts/{contact_file_uid}
Your api endpoint for download should then return a file response of the csv file. 
If this contact_file_uid does not exist for the current user (remember we are 
	using the bearer token to keep track of user), the we should return a 404
Note that a contact_file_uid may be valid but its not for that user, either way we want to return 404

## Task5 :
Create a delete endpoint to delete a single contact file:
when a contact file is deleted. your api endpoint should remove all the contacts 
in that file from the contacts list of the current user


In summary for all tasks
Lets say a user uploads a csv file of 3000 contacts, task 1 is for upload endpoint, it will parse all rows and extract these fields
```json
{
	"firstName":"Ben",
	"lastName":"Gab",
	"email":"bengab@gmail.com",
	"companyName":"samsung"
}
```

This should be appended to the contacts attribute for each user in the collection (mongodb database)
If the contact already exist, is must be ignored.

# Looking forward to have you in our team

## Submission by [keenborder786](https://github.com/keenborder786)

### Additional Notes:
- Please run the `docker-compose` file before testing out the API. The `docker-compose` runs a testing MongoDB container, which is acting as a testing DB. You can go to the Mongo Express URL at `localhost:8081` to see how the documents and collections are being uploaded.

	- To run the Docker Compose, please run the following command:
		```console
		docker-compose up -d
		```
- Please note that I followed the same file structure that you asked for, except for the fact that I created a dedicated package called `api` to better handle the imports.

- In order to replicate a real-life situation, I have added an additional `/token` endpoint which authenticates the user. You can test run the API by logging in yourself as one of the users in `FAKE_USERS_DB`, given in the `config.py` file.

  - Make sure to log in before you test the API in Swagger UI by clicking the `Authorize` button. For example, to act as Mohammad, put in the username: `mohammad` and password: `secret` in the form-data.

- To run the API:
	- First create the conda environment by running the following command:

	```console
	conda env create -f environment.yml
	```

	- Activate the newly created conda environment

	```console
	conda activate fastapi
	```
	- Run the server
	
	```console
	uvicorn app:app --reload
	```

- I used test.py script to generate random CSV files that I used to test my API.

# Single record accounting
The app can be used for single record accounting for small businesses in Finland. In Finland, single record accounting is allowed for businesses that meet at most one of the following conditions: The balance sheet total is over 200 000 euros, the revenue is over 200 000 euros or it employs at least 3 persons. The app is for recording sales and costs, creating pdf invoices and having a record view that includes all required information for the income statement.

The features are:
* The user can create an account.
* The user can sign in and out.
* The user can edit account data, i.e. business name and business id
* The user can maintain favorite settings including IBAN, Business ID, contact information, payment term and VAT-%.
* The user can input incomes or expenses.
* The app has a list of income and expense types that are required to use in accounting in Finland.
* The user can view incomes and expenses in a list view that has all the required fieds for the income statement.
* The user can edit or remove added incomes or expenses.
* The user can open the invoice in a new tab from the corresponding income row in a format that can be printed to pdf.

Several elements of the invoice design were inspired by the styling found at https://github.com/codingmarket07/Simple-Invoice-UI-Design-Template

### Testing instructions

To register successfully on the app and maintain favorites, as well as add or edit income, ensure that you use a valid business ID and IBAN number in the correct format. You can generate valid business IDs and IBAN numbers using the following generator tool:  https://telepartikkeli.azurewebsites.net/tunnusgeneraattori

### Production address

You can access the app: https://single-record-accounting.fly.dev/

### Running the app locally

Clone this repository to your computer and navigate to its root folder. Create file ".env" in the directory and define its content as follows:
```
DATABASE_URL = <database-local-address>
SECRET_KEY = <secret-key>
```
Then, activate the virtual environment and install the app's dependencies using the following commands:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```

Next, create the database tables and insert seed data by running the following commands in the application folder: 
```
$ chmod u+x initialize.sh
$ ./initialize.sh
```
Now you can start the app with command:
```
$ flask run
```

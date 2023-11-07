# Single record accounting
The app can be used for single record accounting for small businesses in Finland. In Finland, single record accounting is allowed for businesses that meet at most one of the following conditions: The balance sheet total is over 200 000 euros, the revenue is over 200 000 euros or it employs at least 3 persons. The app is for recording sales and costs, creating pdf invoices and having a record view that includes all required information for the income statement.

The features are:
* The user can create an account.
* The user can sign in and out.
* The user can maintain favorite settings including IBAN, Business ID, contact information, payment term and VAT-%.
* The user can input sales or costs.
* The app has a list of sales and cost types that are required to use in accounting in Finland.
* The user can view sales and costs in a list view that has all the required fieds for the income statement.
* The user can open the invoice in pdf format from the corresponding sales row.

You can create the database tables by running the following command in the application folder: 
```
psql < schema.sql
```
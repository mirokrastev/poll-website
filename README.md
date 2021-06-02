# Poll System

## Requirements
This project requires Python >= 3.8 to work.<br>
You need to install the dependencies from ```requirements.txt``` and configure ```.env``` file
<br><br>

## Features
Registered users can create polls with multiple answers to vote on.<br>
Other registered users can view and vote on particular answer.<br>
View statistics for this Poll.<br><br>

## API
```api/accounts/``` only supports ```POST``` method.<br>

#### Obtain Auth Token
  * URL
    api/accounts/auth-token
  * Data Params
    Send body with ```username``` and ```password```
  * Success Response:
    * Code: 200
    * Content: { auth_token: {token} }<br><br>

 #### Register
  * URL
    api/accounts/register
  * Data Params
    Send body with ```username```, ```password``` and ```repeat_password```.
  * Success Response:
    * Code: 200
    * Content: { auth_token: {token} }
  * Notes:
    It registers the user and returns Auth Token<br><br>
 
 #### Authorized Requests<br>
 Include the following in Headers:<br>
 ```
 Authorization: Token {token}
 ```

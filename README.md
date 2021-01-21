# #jumga
World Greatest Marketplace as seen on Forbes




## Description
The **fJungas-app** is an application that allows the users to becamoes online sellers by creating stores. The Frontend build on **VueJs - Javascript** and the Backend built on **Django(DRF) - Python**.




- Key Application features

2. Sellers
    - Users can Sign up
    - Beecome sellers
    - Add accounts and products


2. Sales
    - Users can buy product from stores(no need to login)
    - stores can be accessed from https://awesome-brahmagupta-4bc69b.netlify.app/store/{{store url}}
    - Orders are fulfilled and amount sent to sellers/jumga and riders
    - Default shipping is 100usd

Things to Note
Due to want of timee heere are some assumptions I made
- Sellers can create only one store
- Each store will be assigned a rider
- Riders have been preepoulated form a riders.json filee in app/apps/deliver/fixtures/riders.json
- Already created subaccounts for riders
- Used USD as currency all through
- $100 as default delivery charge
- Only sellers can access the dashboard
- As sellers enter the dashboard the present button indicates the next line of action
- I have used the access test banks from "0690000030" to "0690000045" 
- Flutterwave API key is set to Test

Disclaimer - The frontend was super rushed hopefully I get chanced to rebuild after this challenge


- BackEnd


Here is the [ API DOCS ](https://jumga-tony.herokuapp.com/api/docs/) of the application

- FrontEnd

The FrontEnd is a VueJs application located in the client folder deployed on netlify.

Here is the [ LIVE FRONTEND URL](https://awesome-brahmagupta-4bc69b.netlify.app/) of the application


Features not completely present on the frontend


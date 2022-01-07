## Fit Apka do liczenia kalorii

Documentation (In Polish):
https://www.overleaf.com/read/pwfzsskkhvht

![alt text](fitapka_erd.png "ERD Diagram")

## TODO
Main:
- [x] Make latex docs.
- [x] Make ERD diagram.
- [x] Configure docker for postgres and Python/FastAPI.
- [x] Create db in Postgres.
- [x] Make CRUD in FastAPI (11/11)
    - [x] CRUD for User model
    - [x] CRUD for Post model
    - [x] CRUD for Comment model
    - [x] CRUD for Unit model
    - [x] CRUD for Allergen model
    - [x] CRUD for Product model
    - [x] CRUD for ProductCategory model
    - [x] CRUD for Entry model
    - [x] CRUD for Diary model
    - [x] CRUD for SetCategory model
    - [x] CRUD for Set model
- [x] Create package with function and procedure in SQL
  - [x] Create update diary procedure
  - [x] Create calculate proportions function
- [x] Pin SQL procedures and functions to backend
- [x] Create Indexes for tables in SQL
- [ ] Create UI in Vue.js
  - [x] Create Login Page
  - [x] Configure VUEX for storing authentication Token
  - [ ] Create UI for CRUD
    - [ ] Pagination for list elements
    - [ ] Filtering queries
    - [ ] Sorting queries
    - [x] UI for Post
      - [x] UI for Comment
    - [x] UI for User
      - [x] Login
      - [x] Register
      - [x] Account
        - [x] Modify/Update Account
      - [x] List - Admin
    - [x] UI for product
      - [x] UI for categories - product
      - [x] UI for allergens
      - [x] UI for units
    - [x] UI for diaries
      - [x] UI for entries
    - [x] UI for sets
      - [x] UI for categories - set

Optional:
- [x] Make REST API.
- [x] JWT Authentication.

---
# To run the app
- Build and start app
    
  ```docker-compose up --build```
- Run postgresql shell
  
  ```docker-compose exec db psql --username=fitapka --dbname=fitapka```
- Stop app

  ```docker-compose stop```
- Remove app and volumes

  ```docker-compose down -v```
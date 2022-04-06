## Fit Apka do liczenia kalorii

![alt text](fitapka_erd.png "ERD Diagram")


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

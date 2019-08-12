# market_backend
Market Application API

## Setup Instructions
__Steps__

1.  Install Required Packages for Server  
   
        sudo 	apt-get install python3  
        
        sudo 	apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
        
        sudo 	pip3 install virtualenv
    
2. Setup Postgres on Server  

    Create Postgresql database  
   
        sudo su – postgres
          
        createdb <dbname>  
        
    Create PostgreSQL Roles  
    
        createuser <username> --pwprompt  
        
    Connect to psql Mode  
    
        psql  
        
    Connect to the Database  
    
        \c <dbname> 
        
    Grant all privileges on the table <dbname> to the user <username>
      
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <dbname>;

3. Django Environment Setup
    
        virtualenv -p python3 env_name 
        
        source env_name/bin/activate
        
        pip install -r requirements.txt

4. Run Server
    
        python manage.py migrate            # to migrate all the migrations
         
        python manage.py setup_backend      # to create super user ( and other default data in future )
                
        python manage.py runserver          # to run the server
     
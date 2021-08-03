# Automação da busca de preço de máscaras PFF2
Program for Aura 3M mask pricing and availability verification.

# About The Project

The purpose of this project was to become familiar with Apache Airflow. My motivation was by the fact that, during the pandemic, the 3m brand PFF2 masks quickly sold out, so I developed this script, which searches the website of the store. As a result of the script, the date, the name, the price, the status, and the link to the product are returned. A SQLite database is used to store the information. Finally, if the product is available, a Telegram bot will send the user an alert with a link to purchase.

## Built With
-------------

- Language

    ![Badge](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen)

- Frameworks

    ![Badge](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
    ![Badge](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white)

- Database system

    ![Badge](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white	)


- Workflow managment

    ![Badge](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)

- IDEs

    ![Badge](https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)
    ![Badge](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)

<br>


# Getting Started

The following steps demonstrate how to run this locally.

## Prerequisites    
- Python 3.7+

- Virtual Enviroment ***(Optinal)***

    `python -m venv venv`

## Installation

1. Clone the repository

        git clone https://github.com/vrcunha/pff2_price_automation.git

2. Install the requirements.txt

       pip install -r requirements.txt
 
3. Start the airflow db

        airflow db init

4. Create a user (Replace bracket with your name) 

        airflow users create --username admin --password 123admin --firstname [fname] --lastname [lname] --role Admin --email [email]

## Usage

1. Start the webserver

        airflow webserver

2. Start the scheduler

        airflow scheduler

3. Then, you need to put the dag in the airflow dags folder
    > PS: For the first time, you will need to create a folder inside airflow called dags.

4. The token and chat ID must be included in the DAG in order for the telegram bot to work.

# Contribuições

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

# Autor
[![Badge](https://img.shields.io/badge/Autor-Victor_Cunha-07405E?style=for-the-badge)](https://github.com/vrcunha/)

#### Contatos

[![Badge](https://img.shields.io/badge/Github-black?style=for-the-badge&logo=github)](https://github.com/vrcunha)
[![Badge](https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/victor-de-rezende-cunha)
[![Badge](https://img.shields.io/badge/Telegram-blue?style=for-the-badge&logo=telegram)](https://t.me/VictorRCunha)
[![Badge](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:cunhavictorr@gmail.com)

# Licença

This project is licensed under the MIT License - see the LICENSE.md file for details

# Acknowledgements
- othneildrew
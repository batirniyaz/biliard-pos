# Billiard Club - Mini POS System

## Description
This project is a Python-based application that utilizes pip for package management. The primary goal of this project is to manage and control employee and fully digitalize the club. The application is designed to handle CRUD operations for products, manage product images, and ensure smooth database interactions.

## Features
- **CRUD Operations**: Create, read, update, and delete products.
- **Image Upload**: Upload and save product images.
- **Database Management**: Efficiently handle database operations using SQLAlchemy.
- **Periodic Tasks**: Perform periodic status checks.
- **Integration**: Integrated with telegram bot, light and check printer.

## Installation
To install the necessary dependencies, follow these steps:

### Prepare the Environment
1. Clone the repository:
    ```bash
    git clone https://github.com/batirniyaz/biliard-pos.git
    ```
2. Set up a virtual environment:
    ```bash
    python3 -m venv venv
    ```
3. Activate the virtual environment:
   - Linux:
    ```bash
    source venv/bin/activate
    ```
   - Windows:
    ```bash
    venv\Scripts\activate
    ```
4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Refactor the `.env-example` file to `.env` and set the necessary environment variables.

### Run the Application
To run the application, use the following command:
1. Run the application:
    ```bash
    uvicorn app.main:app --host 1.1.1.1 --port 1111 --reload
    ```
2. Open the browser and navigate to `http://1.1.1.1:1111`.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [Batirniyaz Muratbaev](https://www.github.com/batirniyaz): Python Developer

# Thank you for using my application!
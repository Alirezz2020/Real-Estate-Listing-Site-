# Real Estate Listing Site

A Django-powered real estate listing site where users can create, view, and search for property listings.

## Features
- User authentication (login, register)
- Create, update, and delete listings
- Search and filter listings by city, price, bedrooms, and bathrooms
- Display agent contact information directly on listing detail pages
- Pagination for listings and search results

## Technologies Used
- Django 4.x
- PostgreSQL (or SQLite for development)
- Bootstrap 5 for styling
- HTML, CSS, JavaScript

## Getting Started

### Prerequisites
- Python 3.8+
- pip
- virtualenv (optional but recommended)



## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Alirezz2020/Real-Estate-Listing-Site-.git
   cd RealEstateListingSite
2. **Set Up a Virtual Environment:**
    ```sh
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
3. **Install Dependencies:**
   ```sh
    pip install -r requirements.txt

4. **Apply Migrations:**
    ```sh
    python manage.py migrate
5. **Create a Superuser:**
    ```sh
   python manage.py createsuperuser
6. **Run the Development Server:**
    ```sh
   python manage.py runserver
7. **Access the Application:**

    Visit http://127.0.0.1:8000/ in your browser to start exploring the platform.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Make sure to include tests and follow the project’s coding standards.

## License
This project is licensed under the MIT License.


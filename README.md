# FastAPI Product Management System

A RESTful API service built with FastAPI for managing products, categories, and product images. The application uses MySQL as the database and Docker for containerization.

## Project Structure 

project/
├── app/
│ ├── init.py
│ ├── main.py # FastAPI application entry point
│ ├── database.py # Database connection configuration
│ ├── models/ # SQLAlchemy models
│ │ ├── category.py
│ │ ├── product.py
│ │ └── product_image.py
│ ├── routes/ # API endpoints
│ │ ├── category_routes.py
│ │ ├── product_routes.py
│ │ └── product_image_routes.py
│ └── schemas/ # Pydantic models for request/response
│ ├── category.py
│ ├── product.py
│ └── product_image.py
├── requirements.txt # Python dependencies
├── Dockerfile # Docker configuration
└── docker-compose.yml # Docker Compose configuration


## Prerequisites

- Docker
- Docker Compose

## Setup and Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/fastapi-product-management.git
cd fastapi-product-management
```
2. Start the application using Docker Compose:

```bash
docker-compose up --build
```

3. Access the API documentation at http://localhost:8000/docs.


The API will be available at `http://localhost:8000`

## API Documentation

After starting the application, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

### Available Endpoints

#### Categories
- `POST /categories/` - Create a new category
- `GET /categories/` - List all categories
- `GET /categories/{category_id}` - Get a specific category
- `PUT /categories/{category_id}` - Update a category
- `PUT /categories/bulk` - Bulk update categories

#### Products
- `POST /products/` - Create a new product
- `POST /products/bulk` - Create multiple products
- `GET /products/` - List all products
- `GET /products/{product_id}` - Get a specific product
- `PUT /products/{product_id}` - Update a product
- `PUT /products/bulk` - Bulk update products
- `DELETE /products/{product_id}` - Delete a product

#### Product Images
- `POST /products/{product_id}/images/` - Add an image to a product
- `GET /products/{product_id}/images/` - List all images for a product
- `DELETE /products/images/{image_id}` - Delete a product image
- `PUT /products/images/{image_id}/set-primary` - Set an image as primary

## Data Models

### Category
- `id`: int, primary key
- `name`: str
- `description`: str
- `created_at`: datetime
- `updated_at`: datetime

### Product
- `id`: int, primary key
- `name`: str
- `description`: str
- `category_id`: int, foreign key to Category
- `created_at`: datetime
- `updated_at`: datetime

### Product Image
- `id`: int, primary key
- `product_id`: int, foreign key to Product
- `image_url`: str
- `is_primary`: bool
- `created_at`: datetime
- `updated_at`: datetime

## Environment Variables

The application uses the following environment variables (defined in docker-compose.yml):

- `MYSQL_ROOT_PASSWORD`: Root password for MySQL
- `MYSQL_DATABASE`: Name of the database
- `MYSQL_USER`: Username for MySQL
- `MYSQL_PASSWORD`: Password for MySQL user
- `MYSQL_HOST`: Hostname for MySQL
- `MYSQL_PORT`: Port for MySQL

## Development

To add new features or modify existing ones:

1. Create or modify models in `app/models/`
2. Create corresponding schemas in `app/schemas/`
3. Add routes in `app/routes/`
4. Update the database migrations if needed

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Database Schema

The application uses three main tables:
- categories
- products
- product_images

Each table includes:
- Primary keys
- Foreign key relationships
- Timestamps (created_at, updated_at)
- Appropriate indexes for performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

# Project Introduction

CS Skin Analytics is a service designed to identify and capitalize on arbitrage opportunities within the Steam marketplace by comparing prices from various third-party vendors. The application enables users to track price differentials, purchase items from one vendor, and sell them to another, potentially generating profits. Future enhancements will include tracking historical data, building mathematical models to predict price trends, and providing users with informed profit-making predictions.

# Technology Stack

- **Backend**: Django
- **Frontend**: React
- **Database**: PostgreSQL
- **Caching**: Redis
- **Task Queue**: Celery and RabbitMQ
- **Containerization**: Docker

# How to Compile

The project is fully dockerized. To set up the development environment, you need Docker and Docker Compose installed.

### Steps to Set Up

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/YourLocalDuck/CS-Skin-Analytics.git
   cd CS-Skin-Analytics
   git checkout dev
   ```

2. **Build and Start the Containers**:
   ```sh
   docker-compose up --build
   ```

3. **Apply Migrations**:
   ```sh
   docker-compose exec web python manage.py migrate
   ```

4. **Create a Superuser** (For debugging/administration):
   ```sh
   docker-compose exec web python manage.py createsuperuser
   ```

# How to Run

With the containers up and running, the application will be accessible at `http://localhost:8000`. You can log in using the superuser credentials created during setup, however this port will be used for the API Gateway, rather than frontend.

As of 6/20/2024, the only working endpoint is POST /api/collection/init_update/. This endpoint expects a body of the names of all the markets that are to be updated, and will start a daemon that queries the API's of the relevant vendors and stores that data in the configured database.

Sample POST /api/collection/init_update/ body:
```json
{
  "markets": 
  [
    {"name": "steam"},
    {"name": "skinport"}
  ]
}
```

### Running Tasks

To handle background tasks with Celery and RabbitMQ, ensure the Celery worker is running:

```sh
docker-compose exec web celery -A cs_skin_analytics worker --loglevel=info
```

# Input/Output

### Input

- **User Actions**: Users can input buy and sell orders, view price differentials, and interact with the marketplace through the React frontend.
- **API Endpoints**: Interact with the application using various API endpoints for managing transactions and user data.

### Output

- **Price Differentials**: The application displays current price differences between vendors.
- **Transaction Results**: Users receive feedback on their buy and sell orders.
- **Future Predictions**: (Planned) Users will receive predictions based on historical data analysis.

# Features

### Current/In Progress Features

- **Price Tracking**: Track price differentials between multiple vendors.
- **Buy/Sell Functionality**: Execute buy and sell orders directly from the application.
- **Full-Stack Integration**: Django backend, React frontend, PostgreSQL database.

### Future Enhancements

- **Historical Data Analysis**: Track and analyze historical price data.
- **Predictive Modeling**: Build and integrate mathematical models to predict price trends.
- **User Notifications**: Inform users of profitable opportunities based on predictions.

# Database Schema

The database schema is designed to handle current needs and is expected to evolve with future requirements. Key tables include:

- **Users**: Stores user information and authentication details.
- **Items**: Details of items available in the marketplace.
- **Vendors**: Information about third-party vendors.
- **Transactions**: Records of buy and sell transactions.

# API Endpoints

Current API endpoints cover essential functionalities, with more endpoints planned for future needs. Some key planned endpoints include:

- **/api/prices/**: Get current price differentials.
- **/api/buy/**: Execute a buy order.
- **/api/sell/**: Execute a sell order.
- **/api/users/**: Manage user data.

# Development Roadmap

1. **Complete Backend Endpoints**: Develop remaining API endpoints.
2. **Frontend Development**: Build the React frontend to provide a seamless user experience.
3. **Deploy to AWS**: Deploy the fully dockerized application on AWS.
4. **Historical Data Tracking**: Implement tracking and storage of historical price data.
5. **Predictive Modeling**: Develop and integrate predictive models for price trend analysis.

# Team

This project is a work-in-progress and reflects ongoing efforts to build a comprehensive arbitrage platform for Steam marketplace items. Further contributions and developments are planned to enhance its capabilities and user experience. This project is currently being actively worked on by a single developer.

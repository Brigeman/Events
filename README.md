# Event Management API

## Technology Stack

- **Framework**: Django & Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Documentation**: Swagger (with drf-yasg)
- **Testing**: Django's built-in test framework
- **Code Coverage**: Coverage.py

## API Endpoints

This API includes endpoints for creating, listing, updating, and deleting events, registering users, and managing event registrations.

### Event Endpoints

- `POST /api/events/`: Create a new event (requires authentication).
- `GET /api/events/`: Retrieve a list of events.
- `GET /api/events/{id}/`: Retrieve details of a specific event.
- `PUT /api/events/{id}/`: Update an event (requires authentication).
- `DELETE /api/events/{id}/`: Delete an event (requires authentication).

### User Endpoints

- `POST /api/register/`: Register a new user.
- `POST /api/token/`: Obtain a new JWT for authenticated access.
- `POST /api/token/refresh/`: Refresh an existing JWT.

### Registration Endpoints

- `POST /api/events/register/{event_id}/`: Register the authenticated user for an event.
- `DELETE /api/events/cancel/{registration_id}/`: Cancel an event registration for the authenticated user.

## Running the Project

Before running the project, you need to have Python and pip installed on your system.

1. Clone the repository:

   ```bash
   git clone https://github.com/Brigeman/Events
     ```

2. Create and activate the virtual environment:

    ```bash
    cd path/to/project
    virtualenv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your .env file with the necessary secrets for the database:
# Example .env content
DATABASE_NAME=yourdbname
DATABASE_USER=yourdbuser
DATABASE_PASSWORD=yourdbpassword
DATABASE_HOST=yourdbhost
DATABASE_PORT=yourdbport
SECRET_KEY=yoursecretkey


5. Apply migrations to the database:

    ```bash
    python manage.py migrate
    ```

6. Start the development server:

    ```bash
    python manage.py runserver
    ```

## Testing

To run the tests, use the command:

   ```bash
   python manage.py test
   ```

For testing the API endpoints interactively, you can use the Swagger documentation available at:
http://127.0.0.1:8000/swagger/


# Code Coverage
For measuring test coverage and creating a report:

```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates a detailed HTML report
```

The test coverage report will be available in the `htmlcov/` directory.

# .gitignore

htmlcov/

This way, the coverage report remains accessible locally for developers, but it won't clutter your Git repository. The summary of the coverage can be committed separately as part of the documentation or as a badge in the README.md.


## Test Results

After running the tests using coverage, the results show approximately 93% coverage. Detailed results can be found in the generated HTML report.




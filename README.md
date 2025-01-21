# Journal

A Django app to keep track of attendance, absences, holidays with Discord bot and Superset integration.

## Run Locally using Docker

### Clone the repository
Clone the GitHub repository to your local machine:
```
git clone https://github.com/sandbox-pokhara/journal.git
cd journal
```

### Setup the .env file
Create a `.env` file inside the backend and discord_bot directories according to the provided `sample.env` file.

### Build and run the containers
Run the following command to build and start the containers:
```
docker-compose up --build -d
```

## License

This project is licensed under the terms of the MIT license.

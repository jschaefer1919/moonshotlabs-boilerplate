# MySQL + Flask Boilerplate Project - Moonshot Labs

This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 
1. To start and stop the containers, use `docker compose start` and `docker compose stop` respectively. 

# Overview of Moonshot Labs
1. At its core, Moonshot Labs is a data commerce platform focused on Major League Baseball. Moonshot
Labs is designed to provide an array of basic statistics and analytics to a wide variety of
customers with differing MLB data-driven needs. Subscribers of Moonshot Labs will have the opportunity to
access the online platform through three contributor packages: a basic, ante, and analyst package. As of late, Moonshot Labs decided to operate under an open-source managment style in order to aggregate a wider variety and amount of data on the MLB since its current team is too small.

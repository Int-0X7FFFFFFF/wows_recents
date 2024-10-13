# WOWS Recents Refractor

## Overview

The `intmax/wows_recents_refractor` is a Docker image designed to help you manage and analyze recent battle data from World of Warships (WOWS). This tool allows you to initialize the database and run the main application easily.

## Prerequisites

- Docker installed on your machine.
- A valid [Docker Hub](https://hub.docker.com/) account (if you wish to contribute or customize the image).
- Properly configured PostgreSQL database.

## Usage

### Pull the Docker Image

To get started, you need to pull the Docker image from Docker Hub:

```bash
docker pull intmax/wows_recents_refractor
```

## Running the Container
### You can run the container in two different modes:

### Initialize Database Tables
### To initialize the database tables, run the following command:

```bash
docker run --rm -v $(pwd)/config.py:/app/config.py -e COMMAND=init intmax/wows_recents_refractor
```
This will execute the init_db function in the application and set up the required tables in your PostgreSQL database.

Run the Main Application
To start the main application, use the following command:

```bash
docker run -d -v $(pwd)/config.py:/app/config.py intmax/wows_recents_refractor
```
This will run the main functionality of the application and process the recent battle data.

## Logging
### Logs will be output to the console. If you want to keep logs for further analysis, you can redirect the output to a file like this:

```bash
docker run -d -v $(pwd)/config.py:/app/config.py intmax/wows_recents_refractor > logs.txt
```

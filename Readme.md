# Elevator System Documentation

## Introduction 
This repository contains my submission for the Jumping Minds assignment, in which I was tasked with designing an elevator system. While the assignment provided comprehensive details, there was some ambiguity regarding how passengers would move between floors. Specifically, it was unclear whether the elevator system should operate instantaneously, handle one floor per request, or operate on a time-based system.


## Approach
To address this ambiguity, I opted for a real-life-inspired approach to simulate elevator operation. I implemented the elevator system using Celery, where the lift climbs one floor every 30 seconds, providing a more realistic elevator experience.

Ideally, the elevator system would have automatically opened and closed its doors as passengers entered and exited. However, the assignment requirements mandated the development of an API for this functionality. To comply with these requirements, I utilized an 'is_running' flag to halt the elevator at a floor until the 'open door' and 'close door' API endpoints were called. This allowed passengers to board and disembark from the elevator safely.

## Code Structure
he code for this project is written in Django and adheres to the PEP-8 coding standards, ensuring readability and maintainability.

For detailed information on how to run and use this elevator system, please read ahead

Please feel free to reach out if you have any questions or require further clarification regarding this submission.

Thank you for considering my work for the assignment.

## Postman Documentation

https://documenter.getpostman.com/view/17181619/2s9YJgU1d3

## Features
 - Moving elevators up and down
 - Opening and closing elevator doors
 - Starting and stopping elevator movement
 - Displaying the current status of elevators
 - Deciding elevator movement based on user requests
 - Associating elevators with floors
 - Marking elevators as available or busy
 - Marking elevators as operational or non-operational
 - Handling elevator requests from users



# Installation
Before you begin, ensure you have met the following requirements:
 - Python 3
 - Virtualenv module installed

## Clone
When you verify your Git account, any project you create will be automatically pushed to your GitHub account. From there, you can easily clone the project to your local machine by running the following command in your terminal: 

```bash
git clone https://github.com/ananya26-vishnoi/jumping_minds_project.git
```

If you haven't verified your Git account, don't worry! You can still download the project as a zip file and extract it to your local machine. This option is provided at the last step of project creation, so you can easily access and work with the files even without a Git account.

## Setup

### Virtual Environment
To ensure a clean and organized development environment, it is highly recommended to use a virtual environment when working with any project. You can create a virtual environment for your project by running the following command in your terminal:

```bash
python -m venv <name of virtual environment>
```

Once your virtual environment is created, you can activate it using the appropriate command for your operating system.

Windows:
```bash
.\<name of virtual environment>\Scripts\activate
```

Linux/Unix:
```bash
source <name of virtual environment>/bin/activate
```

By activating your virtual environment, you can ensure that any dependencies and packages you install will be isolated from your global environment, making it easier to manage and maintain your project.

### Installing Dependencies 
To install all the necessary dependencies for your project, simply run the following command in your terminal:

```bash
pip install -r requirements.txt
```
This command will read the requirements.txt file and automatically install all the listed dependencies for you. Make sure your virtual environment is activated before running this command to ensure that the packages are installed in the correct environment. Once the installation is complete, you'll be ready to start working on your project!

### .env

<b> Important Note: </b>
Demo.env have been provided please attach a postgres database of your own before proceeding further. Make sure to rename demo.env to .env

            
### Celery
1. Run celery worker in a new terminal
2. Make sure redis is installed and running. You can find documentation here: https://redis.io/docs/getting-started/

```bash
celery -A jumping_minds_project worker -l info -P eventlet
``` 



#!/bin/bash

sudo docker-compose run --rm app sh -c 'python manage.py test'
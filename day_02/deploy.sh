#!/bin/bash

export $(grep -v '^#' .env | xargs)

ansible-playbook -i ./deploy/inventory.yaml ./deploy/playbook.yaml
#!/bin/bash


cd .. && alembic revision -m "$1"

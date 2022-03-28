# WMS (Widget Management System)
> Widget Management System, a system that manages widgets through receive and creating files that contain widgets and stock numbers.

## General Info
* This app allows users to import csv documents of widgets to load into the inventory system of the app.
* The system will then allow the user to process and fulfill orders that will then change stock accordingly.
* I created this project as a way to get more familiar with python and some of the libraries that can be used in tandem with python.

## Technology
* Python

## Usage
### Commands:
- `load-stock <filename>`
- `check-stock <item>`
- `add-stock <item,qty>`
- `remove-stock <item,qty>`
- `pull-order <file>`
- `fill-order <order>`
- `restock-order <order>`
- `print-stock`

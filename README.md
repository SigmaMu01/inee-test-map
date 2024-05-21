# Python-developer trainee test project

This repository contains all files required for "Places Remember" test project.

PDF-file with [the task](https://drive.google.com/file/d/130BXj-3AXM8pQ06fscjxg2V5C7HIwriI/view?usp=drive_link):

Link to [the server](https://p01--web--4cqtxswnrj4s.code.run/) (contact me in case this link is down) 

## Supported features:

* Django framework
* PostGIS database
* VK authorization (using *allauth*)
* Google Maps integration
  * with multiple markers vizualization
  * and the ability to drag them
* Simple data protection from unauthorized users
* Several linters included (<ins>GitHub Actions implemented</ins>):
  * black
  * isort
  * flake
  * pylint
* Sufficient unit-test coverage (<ins>GitHub Actions implemented</ins>)
* Docker and docker compose files included
* The web-application is run on a VDS server

## Available repo branches:

| Branch  | Purpose |
| ------------- | ------------- |
| `master`  | Deployment branch  |
| `dev`  | New functions and testing  |
| `server`  | Stable active [server](https://p01--web--4cqtxswnrj4s.code.run/)  |

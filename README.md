# Test-Driven & Behavior-Driven Development – by Guy Landry Djolaud

[![Project Type](https://img.shields.io/badge/Project-Coursera%20Final%20Project-blue)]()
[![Testing Methodology](https://img.shields.io/badge/Testing-TDD%20%7C%20BDD-orange)]()
[![Built With](https://img.shields.io/badge/Language-Python-blue.svg)]()
[![Author](https://img.shields.io/badge/Author-Guy%20Landry%20Djolaud-brightgreen)]()
[![License](https://img.shields.io/badge/license-Apache--2.0-lightgrey)]()

This repository documents my final project for the Coursera course *Introduction to TDD/BDD*,  
where I applied **real-world software testing practices** using **Python**, **TDD** (*Test-Driven Development*),  
and **BDD** (*Behavior-Driven Development*) principles to build a resilient microservice API.

# Building Resilient Microservices with TDD & BDD – by Guy Landry Djolaud

This repository documents my final project for the Coursera course *Introduction to TDD/BDD*, where I applied real-world testing practices using **Python**, **TDD (Test-Driven Development)**, and **BDD (Behavior-Driven Development)** principles to build a robust microservice API.

---

## Project Purpose

This project demonstrates my ability to:

- Design features with user behavior in mind
- Write clean, testable, and maintainable Python code
- Apply TDD to ensure code stability before implementation
- Use BDD to define clear, business-readable acceptance criteria

---

## Key Features

- Python microservice architecture
- TDD with unit tests for routes and models
- BDD with Gherkin-based scenarios and steps
- Modular and scalable folder structure
- Dev environment setup with `setup.sh`
- Easily portable for integration in CI/CD pipelines

---

## Project Structure

- bin/ # Setup scripts (e.g., environment configuration)
- service/ # Business logic & API routes (core microservice logic)
  - routes.py # Main API route handlers
- tests/ # Unit tests for TDD (Test-Driven Development)
  - test_models.py # Model-level unit tests
  - test_routes.py # Route-level unit tests
- features/  # BDD Scenarios & Step Definitions
  - products.feature  # Gherkin-based feature scenarios
  - steps/ # Python step implementations
- load_steps.py
- flaskenv # Flask environment variables
- Makefile # Automation commands for setup/test/deploy
- README.md # Project documentation

---

## Project Setup

To initialize the environment:

```bash
bash bin/setup.sh
exit

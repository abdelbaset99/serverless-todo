# Serverless To-Do Application (AWS & Python)

![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![Python](https://img.shields.io/badge/Backend-Python%203.x-blue)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-green)

A cloud-native, serverless REST API and frontend application built on Amazon Web Services (AWS). This project demonstrates a full CRUD (Create, Read, Update, Delete) cycle without managing a single server, utilizing **AWS Lambda**, **API Gateway**, **DynamoDB**, and **S3**.

## 🏗 Architecture

The application relies on an Event-Driven Serverless architecture:

1.  **Frontend:** Hosted statically on **Amazon S3**.
2.  **API Layer:** **Amazon API Gateway** receives HTTP requests and manages CORS.
3.  **Compute:** **AWS Lambda** (Python 3.x) handles logic and routing. It utilizes the "Lambda Proxy Integration" pattern to handle all HTTP methods (`GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`) in a single function.
4.  **Database:** **Amazon DynamoDB** provides a NoSQL data store with On-Demand capacity.
5.  **Monitoring:** **Amazon CloudWatch** logs all API activity and runtime errors.
6.  **CI/CD:** **GitHub Actions** automatically deploys backend code and frontend assets upon commits to `main`.

## 🚀 Features

*   **Serverless CRUD:** Fully functional REST API for managing tasks.
*   **In-Place Editing:** Update task content dynamically or toggle completion status.
*   **Custom CORS Handling:** Python-based `OPTIONS` preflight handling for secure cross-origin resource sharing.
*   **Optimistic UI:** Fast, responsive frontend using vanilla JavaScript.
*   **Automated Deployment:** Continuous Delivery pipeline using AWS CLI and GitHub Actions.

## 🛠 Tech Stack

*   **Cloud Provider:** AWS
*   **Backend:** Python (Boto3 SDK)
*   **Database:** DynamoDB (NoSQL)
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+)
*   **DevOps:** GitHub Actions, AWS IAM (Least Privilege Policies)

## 🔌 API Reference

The API is exposed via a single resource endpoint: `/todos`

### 1. Get All Tasks
**GET** `/todos`
*   Returns a list of all items in the DynamoDB table.

### 2. Create Task
**POST** `/todos`
```json
{
  "task": "Buy groceries"
}

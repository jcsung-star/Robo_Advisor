![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&width=1000&height=200&section=header&text=Robo%20Advisor%20&fontSize=30&fontColor=black)

<!-- header is made with: https://github.com/kyechan99/capsule-render -->

[John Sung](https://linkedin.com/in/john-sung-3675569) [<img src="https://cdn2.auth0.com/docs/media/connections/linkedin.png" alt="LinkedIn -  John Sung" width=15/>](https://linkedin.com/in/john-sung-3675569/)

                                                             
<br>
Columbia FinTech Bootcamp Assignment - Module 15

---

### Table of Contents

* [Overview](#overview)
* [Requirements](#requirements)
* [Data](#data)
* [Evaluation Report](#evaluation-report)
* [License](#license)

---

## Overview


Using AWS Lex, RoboAdvisor was created and designed for clients searching for guidance towards their retirement. 

---

## Requirements

This project leverages **[python version 3.7](https://www.python.org/downloads/)** with the following packages and modules:

* [datetime](https://docs.python.org/3/library/datetime.html)

* [dateutil](https://dateutil.readthedocs.io/en/stable/index.html)

* [AWS Lex](https://aws.amazon.com/lex/) - A service for building conversational interfaces into any application using voice and text. This was used in combination with the functionality created on AWS Lambda.

* [AWS Lambda](https://aws.amazon.com/lambda/) - To build the functionality for the tool.

---

## Data

The data used in this neural network model was from derived from a CSV file called emerging_markets_ohlcv.csv:

---

## Installation Guide

---


---

## Usage

### To use the AWS Lambda function:

1. Go to AWS Lambda first. Create a new Lambda function from scratch, and name it recommendPortfolio. Choose Python 3.7 as the runtime programming language.

2. In the online code editor, delete the AWS-generated default lines of code, and then paste the new lambda_function.py that is provided with this file. 

---
### To use the AWS Lex Chatbot, our RoboAdvisor Investment Recommendation:

Steps with correct information from the beginning
1. User will input or speak an utterance "I want to invest for my retirement"*
2. User will then be asked for his first name.
2. User will then be asked for their age. 
3. User will then be asked for the amount to invest.
4. User will then be asked for their risk tolerance.
5. User will then be provided their recommended investment allocation.




---

## License

### **MIT License**

---

## How to unit test sending emails with Pytest

It is common to send emails to stakeholders to notify them your pipeline is complete and the data is ready (or notify if there has been an error with processing).

However, writing unit tests for the code that sends your emails can be tricky.

To run the code in your test or local environment would require access to your production email server. This might not be possible or feasible. For example managing credentials for the email server and also you want to avoid spamming an inbox with test messages. It is also difficult to emulate any exception handling you might have.

The way to avoid using a real email server for testing is to use 'mocking'.

You can use `pytest-mocker` to 'mock' calls to the email server. When using mocking, you don't actually send any emails, but your code will behave as though it did. This allows you to test aspects of your code related to sending emails without the dependency of a real email server.

Mocking is not fool proof as it is not a 100% accurate replacement to the real thing. But allows you to run through your code and see how it would behave when an email is successfully sent or how errors are handled if not.

### Getting Started

**Run the local email server**

For this example, to keep things simple and avoid dealing with credentials for connecting to a real email server, we will be using a local SMTP server.

This isn't a real email server but allows us to demonstrates the process of mocking. When we 'send' an email, the actual email is discarded and the output is printed to the console.

The scope of this tutorial is restricted to unit-testing emails sent using Python, rather than how to send emails using Python.

To start the local SMTP server, open a new terminal and run the following command:

```bash
python -m smtpd -c DebuggingServer -n localhost:1025
```

**Install dependencies**

Open a new terminal and run the following commands.

Install the required dependencies for `pytest` and `pytest-mocker`

```bash
pip install -r requirements.txt
```

**Run the actual code**

Run the fake 'pipeline' code which send an email after the pipeline has completed.

```bash
python send_email.py
```

Look at the terminal where your local SMTP server is running (from the previous step) and you will see the email output printed to the console. This indicates that the email has been sent.

Run the Python file a few times and you will see the ID in the console output changing. Each email will have a unique ID which shows a new email is being sent each time.


**Run the test case**

Use `pytest` to run the test case.

```bash
# run test case and print output to the console
pytest -rP
```

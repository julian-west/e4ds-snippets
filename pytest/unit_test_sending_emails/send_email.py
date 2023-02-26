"""Example code for sending an email"""

import smtplib
import sys
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def run_pipeline():
    """Some dummy code to run data pipeline"""
    # pipeline code ....

    # example statistics generarted from the run for email reporting purposes
    summary = {
        "total_files": 100,
        "success": 100,
        "failed": 0,
        "output_location": "gcs://my_data_lake/processed/example.csv",
    }
    return summary


def build_success_email_notification(
    config: ConfigParser, summary: dict[str, int]
) -> MIMEMultipart:
    """Build MIME message object"""
    sender_email = config.get("email", "sender_email")
    receiver_email = config.get("email", "receiver_email")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Completion Notification"

    email_body = f"""
    The pipeline has completed successfully.

    Total files processed: {summary.get('total_files')}
    Successful: {summary.get('success')}
    Failed: {summary.get('failed')}

    Output location: {summary.get('output_location')}
    """

    msg_body = MIMEText(email_body, "plain")

    msg.attach(msg_body)

    return msg


def send_pipeline_notification(config: ConfigParser, msg: MIMEMultipart) -> None:
    """Send an email, include some error handling"""
    host = config.get("email", "host")
    port = int(config.get("email", "port"))

    try:
        with smtplib.SMTP(host, port) as server:
            server.send_message(msg)
        print("Email notification sent successfully")

    except smtplib.SMTPException:
        print("SMTP Exception. Email failed to send")


def main():
    # read configuration file parameters
    config = ConfigParser()
    config.read("pipeline_config.ini")

    # print config to console for reference
    config.write(sys.stdout)

    # run pipeline code and return the summary info to report in the email
    summary = run_pipeline()

    msg = build_success_email_notification(config, summary)
    send_pipeline_notification(config, msg)


if __name__ == "__main__":
    main()

"""Example code for sending an email"""

import smtplib
import sys
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def run_pipeline():
    """Some dummy code to run data pipeline"""
    # pipeline code ....

    # example statistics from the run for reporting purposes
    summary = {
        "total_files": 100,
        "success": 100,
        "failed": 0,
        "output_location": "gcs://my_data_lake/processed/example.csv",
    }
    return summary


def send_pipeline_completion_notification(
    config: ConfigParser, summary: dict[str, int]
) -> None:
    sender_email = config.get("email", "sender_email")
    receiver_email = config.get("email", "receiver_email")
    host = config.get("email", "host")
    port = int(config.get("email", "port"))

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Completion Notification"

    email_body = f"""
    The pipeline has completed successfully.

    Total files processed {summary.get('total_files')}
    Successful: {summary.get('success')}
    Failed: {summary.get('failed')}

    Output location: {summary.get('output_location')}
    """

    msg_body = MIMEText(email_body, "plain")

    msg.attach(msg_body)

    try:
        with smtplib.SMTP(host, port) as server:
            server.send_message(
                msg,
                from_addr=sender_email,
                to_addrs=receiver_email,
                mail_options=[],
                rcpt_options=[],
            )
        print("Email notification sent successfully")

    except smtplib.SMTPException:
        print("SMTP Exception. Email failed to send")


if __name__ == "__main__":
    config = ConfigParser()
    config.read("pipeline_config.ini")

    # print config to console for reference
    config.write(sys.stdout)

    # run pipeline code
    summary = run_pipeline()

    send_pipeline_completion_notification(config, summary)

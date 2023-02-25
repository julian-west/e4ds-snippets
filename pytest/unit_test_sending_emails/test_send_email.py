"""Test your email code"""
import smtplib
from configparser import ConfigParser

from send_email import build_success_email_notification, send_pipeline_notification


def test_send_pipeline_notification(mocker):
    # setup
    config = ConfigParser()
    config.read("pipeline_config.ini")

    summary = {
        "total_files": 1_000,
        "success": 1_000,
        "failed": 0,
        "output_location": "gcs://my_data_lake/processed/",
    }

    # mock the smptlib.SMTP object
    mock_SMTP = mocker.MagicMock(name="smtplib.SMTP")
    mocker.patch("smtplib.SMTP", new=mock_SMTP)

    # run send email function
    msg = build_success_email_notification(config, summary)
    send_pipeline_notification(config, msg)


def test_send_pipeline_notification_smtpexception(mocker):
    config = ConfigParser()
    config.read("pipeline_config.ini")

    summary = {
        "total_files": 1_000,
        "success": 1_000,
        "failed": 0,
        "output_location": "gcs://my_data_lake/processed/",
    }

    mock_SMTP = mocker.MagicMock(name="smtplib.SMTP")
    mocker.patch("smtplib.SMTP", new=mock_SMTP)

    # mock STMPException error
    mock_SMTP.side_effect = smtplib.SMTPException

    msg = build_success_email_notification(config, summary)
    send_pipeline_notification(config, msg)

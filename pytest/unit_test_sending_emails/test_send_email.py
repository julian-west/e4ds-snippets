"""Test your email code"""
import smtplib
from configparser import ConfigParser

from send_email import send_pipeline_completion_notification


def test_send_pipeline_completion_notification(mocker):
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

    send_pipeline_completion_notification(config, summary)


def test_send_pipeline_completion_notification_smtpexception(mocker):
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

    send_pipeline_completion_notification(config, summary)

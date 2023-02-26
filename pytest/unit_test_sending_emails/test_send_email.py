"""Test your email code"""
import smtplib
from configparser import ConfigParser

from send_email import build_success_email_notification, send_pipeline_notification


def test_send_pipeline_notification(mocker, capsys):
    """Test the successful sending of the email"""
    # 1. SETUP

    # 1a. read config
    config = ConfigParser()
    config.read("pipeline_config.ini")

    # 1b. build an example message
    summary = {
        "total_files": 1_000,
        "success": 1_000,
        "failed": 0,
        "output_location": "gcs://my_data_lake/processed/",
    }
    msg = build_success_email_notification(config, summary)

    # 1c. mock the smptlib.SMTP object
    mock_SMTP = mocker.MagicMock(name="send_email.smtplib.SMTP")
    mocker.patch("send_email.smtplib.SMTP", new=mock_SMTP)

    # 2. ACT -- Run the function
    send_pipeline_notification(config, msg)

    # 3. ASSERT -- Test the outputs
    # 3a. Test 'send_message' method was actually called
    # Use the below if you are using a context manager
    assert mock_SMTP.return_value.__enter__.return_value.send_message.call_count == 1
    # Use the below if you are NOT using a context manager
    # assert mock_SMTP.return_value.send_message.call_count == 1

    # 3b. Test print statement after successfully running 'send_message'
    output = capsys.readouterr()
    assert "Email notification sent successfully" in output.out


def test_send_pipeline_notification_smtpexception(mocker, capsys):
    """Test SMTPException exception handling"""
    # 1. SETUP

    # 1a. read config
    config = ConfigParser()
    config.read("pipeline_config.ini")

    # 1b. build an example message
    summary = {
        "total_files": 1_000,
        "success": 1_000,
        "failed": 0,
        "output_location": "gcs://my_data_lake/processed/",
    }
    msg = build_success_email_notification(config, summary)

    # 1c. mock the smptlib.SMTP object
    mock_SMTP = mocker.MagicMock(name="send_email.smtplib.SMTP")
    mocker.patch("send_email.smtplib.SMTP", new=mock_SMTP)
    # mock STMPException error
    mock_SMTP.side_effect = smtplib.SMTPException

    # 2. ACT -- Run the function
    send_pipeline_notification(config, msg)

    # 3. ASSERT -- Test the outputs
    # 3a. Test 'send_message' method was NOT called
    # use if the below you are using a context manager
    assert mock_SMTP.return_value.__enter__.return_value.send_message.call_count == 0
    # use the below if you are NOT using a context manager
    # assert mock_SMTP.return_value.send_message.call_count == 0

    # 3b. Test print statement after triggering SMTPException
    output = capsys.readouterr()
    assert "SMTP Exception. Email failed to send" in output.out

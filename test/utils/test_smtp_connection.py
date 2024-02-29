import pytest

from utils.smtp_connection import SMTPConnection

setup = {
    'host': '172.22.88.6',
    'port': '25',
    'user': 'automatismo_GSGR@claro.com.co',
    'password': '',
    'subject': 'Example Subject',
    'recipients': 'martinezjha@globalhitss.com'
}

smtp_connection = SMTPConnection()


def test_object_created_successfully():
    """Initializes all necessary attributes with the provided setup dictionary."""
    smtp_connection.initialize(setup)
    assert isinstance(smtp_connection, SMTPConnection)


def test_object_not_created_if_setup_missing():
    """Database object is not created if setup is missing"""
    setup = {}
    with pytest.raises(Exception):
        smtp_connection.initialize(setup)


def test_send_email_with_valid_body_and_no_attachment():
    smtp_connection.initialize(setup)
    body = 'This is a test email'
    result, message = smtp_connection.send_email(body)
    assert result == True
    assert message == 'Mensaje enviado correctamente'

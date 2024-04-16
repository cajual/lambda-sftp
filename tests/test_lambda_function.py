from unittest.mock import patch

from common import conn, VFS
from lambda_function import lambda_handler


def test_lambda_handler(sftpserver):
    # Setup test environment: create some files
    with sftpserver.serve_content(VFS):
        event = {**conn(sftpserver)}
        with patch("lambda_function.send_file_to_s3") as mock_send_file_to_s3:
            response = lambda_handler(event, None)

    # Assert the mock was called
    mock_send_file_to_s3.assert_called()

    # Assert the response
    assert response["statusCode"] == 200
    assert "foo1" in response["body"]
    assert "foo2" in response["body"]
    assert "make.txt" in response["body"]

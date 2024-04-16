import boto3
import time
from sftpretty import Connection, CnOpts
import logging

# podman run -p 2222:22 -d atmoz/sftp foo:pass:::upload
event = {
    "default_path": "/upload",
    "host": "localhost",
    "port": 2222,
    "username": "foo",
    "password": "pass",
}

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("sftplogger")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """lambda to download files less than 24 hours old from an SFTP server and upload them to S3

    Args:
        event (dict): the event object containing the connection details
        context (dict): the context object containing the runtime details

    Returns:
        dict: status code and body
    """
    logger.info("Check for connection options")
    if "cnopts" not in event:
        event["cnopts"] = CnOpts(knownhosts=None)

    logger.info("Initialize the SFTP connection")
    with Connection(**event) as sftp:
        logger.info("List the directory contents of the SFTP server")
        files = sftp.listdir()
        logger.debug(f"Checking {files}")
        logger.info("Filter the files to download")
        files_to_download = [
            file
            for file in files
            # only download files created in the last 24 hours
            if sftp.stat(file).st_mtime > time.time() - 24 * 60 * 60
        ]
        logger.info("Send the files to S3")
        for file in files_to_download:
            # send the file to S3
            send_file_to_s3(f"/tmp/{file}", sftp)

    return {"statusCode": 200, "body": f"{files} sent to S3"}


def send_file_to_s3(file: str, sftp: Connection):
    """send a file to an S3 bucket

    Args:
        file (str): the file to send
        sftp (Connection): the sftp connection object
    """
    # assume all files are in range
    logger.debug(f"Uploading {file} to S3")
    s3 = boto3.client("s3")

    sftp.get(file, f"/tmp/{file}")
    s3.upload_file(f"/tmp/{file}", "hl7-receive", file)


if __name__ == "__main__":
    lambda_handler(event, None)

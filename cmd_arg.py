import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--host", type=str, default="127.0.0.1", help="Host to run the server on"
)
parser.add_argument("--port", type=int, default=7090, help="Port to run the server on")
parser.add_argument(
    "--log-level",
    type=str,
    choices=["debug", "info", "warning", "error"],
    default="info",
    help="Log level",
)

arg = parser.parse_args()

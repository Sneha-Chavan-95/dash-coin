"""Start the `Block chain api` using uvicorn"""

import uvicorn


def main(start_host: str = "0.0.0.0", start_port: int = 8000):
    """Method to start the `uvicorn` service on given host and port

    Args:
        host (str, optional): Host to start the app on. Defaults to "0.0.0.0".
        port (int, optional): Port to start the app on. Defaults to 8000.
    """
    uvicorn.run("app.main:app", host=start_host, port=start_port, reload=True, workers=1)


if __name__ == "__main__":
    main()
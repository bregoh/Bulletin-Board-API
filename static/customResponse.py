class CustomResponse:
    @classmethod
    def response(
        cls, data: list | dict = {}, message: str = "", error: list | dict = None
    ):
        return {
            "message": message,
            "data": data,
            "error": error,
        }

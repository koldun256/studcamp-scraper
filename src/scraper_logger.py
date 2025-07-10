from logger import Logger

class ScraperLogger:
    __id: int
    __url: str
    __parsed: int = 0
    __fails: int = 0
    __no_profile_url: int = 0

    __logger: Logger

    def __init__(self, logger: Logger) -> None:
        self.__id = id(self)
        self.__logger = logger

    def __log(self, message: str, level = Logger.Level.Info) -> None:
        self.__logger.log(f"(Scraper #{self.__id}): {message}", level)

    def get_begin(self, url: str) -> None:
        self.__url = url
        self.__log(f"GET {url}")
    
    def get_successful(self) -> None:
        self.__log(f"GET Successfull")

    def get_fail(self, error: Exception) -> None:
        self.__log(f"GET Fail with exception {error}", Logger.Level.Error)

    def progress(self, count: int) -> None:
        self.__parsed += count

    def review_parse_fail(self, error: Exception, review_id: str | None) -> None:
        self.__fails += 1
        self.__log(f"Failed to parse review {review_id}: {error}", Logger.Level.Error)

    def chunks_parse_fail(self, error: Exception) -> None:
        self.__log(f"Failed to get chunks: {error}", Logger.Level.Error)
    
    def report_no_url(self) -> None:
        self.__no_profile_url += 1

    def finish(self) -> None:
        self.__log(f"Finished parsing reviews. {({"parsed": self.__parsed, "fails": self.__fails, "no_profile": self.__no_profile_url})}")

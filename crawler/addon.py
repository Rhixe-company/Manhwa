from scrapy.core.downloader.handlers.http import HTTPDownloadHandler


FALLBACK_SETTING = "MY_FALLBACK_DOWNLOAD_HANDLER"


class MyAddon:
    def update_settings(self, settings):
        if not settings.get(FALLBACK_SETTING):
            settings.set(
                FALLBACK_SETTING,
                settings.getwithbase("DOWNLOAD_HANDLERS")["https"],
                "addon",
            )
        settings["DOWNLOAD_HANDLERS"]["https"] = HTTPDownloadHandler

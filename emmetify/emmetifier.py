from typing import Literal
from emmetify.config import EmmetifierConfig
from emmetify.converters.html_converter import HtmlConverter
from emmetify.parsers.html_parser import HtmlParser


SupportedFormats = Literal["html"]

class Emmetifier:
    def __init__(
        self,
        format: SupportedFormats = "html",
        config: EmmetifierConfig | dict | None = None
    ):
        # Handle config
        self.config = (
            EmmetifierConfig()
            if config is None
            else (
                EmmetifierConfig.model_validate(config)
                if isinstance(config, dict)
                else config
            )
        )

        self._parser = self._get_parser(format)
        self._converter = self._get_converter(format)

    def _get_parser(self, format: SupportedFormats):
        return {
            "html": HtmlParser(self.config),
        }.get(format, HtmlParser(self.config))

    def _get_converter(self, format: SupportedFormats):
        return {
            "html": HtmlConverter(self.config),
        }.get(format, HtmlConverter(self.config))

    def emmetify(self, content: str) -> str:
        nodes = self._parser.parse(content)
        return self._converter.convert(nodes)

    @classmethod
    def create(cls, format: SupportedFormats = "html", **config_kwargs) -> "Emmetifier":
        """Factory method with IDE support for config"""
        return cls(format=format, config=EmmetifierConfig(**config_kwargs))



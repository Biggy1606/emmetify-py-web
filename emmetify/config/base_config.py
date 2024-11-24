from pydantic import BaseModel, Field
from typing import Set

from emmetify.config.html_config import HtmlConfig

class EmmetifierConfig(BaseModel):
    
    # Optimization options
    simplify_classes: bool = False
    simplify_links: bool = False
    simplify_images: bool = False
    
    # Debug options
    debug: bool = False

    # Emmet Formatting options (run on debug=True only)
    indent: bool = False
    indent_size: int = Field(default=2, ge=1, le=8)

    html: HtmlConfig = Field(
        default_factory=HtmlConfig,
        description="HTML-specific configuration"
    )

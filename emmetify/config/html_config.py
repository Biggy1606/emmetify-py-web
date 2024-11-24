from pydantic import BaseModel, Field
from typing import Set

class HtmlAttributePriority(BaseModel):
    """HTML attribute priorities configuration"""
    primary_attrs: Set[str] = Field(
        default={
            'id',          # unique identifier, excellent for xpath
            'class',       # common for styling and semantic meaning
            'href',        # essential for links
            'role',        # semantic meaning for accessibility
            'aria-label',  # accessible label, often contains meaningful text
            'title'        # tooltip text, often descriptive
        },
        description="Highest priority attributes to keep"
    )
    
    secondary_attrs: Set[str] = Field(
        default={
            'name',        # form elements and anchors
            'type',        # input/button types
            'value',       # form element values
            'placeholder', # input placeholder text
            'alt',         # image alternative text
            'for'         # label associations
        },
        description="Secondary attributes to keep if no primary attributes present"
    )
    
    ignore_attrs: Set[str] = Field(
        default={
            'style',
            'target',
            'rel',
            'loading',
            'srcset',
            'sizes',
            'width',
            'height'
        },
        description="Attributes to always ignore"
    )

class HtmlConfig(BaseModel):
    """HTML-specific configuration"""
    skip_tags: Set[str] = Field(
        default={
            'script', 'style', 'noscript', 'head', 
            'meta', 'link', 'title', 'base', 'svg'
        },
        description="Tags to skip during conversion"
    )
    attribute_priority: HtmlAttributePriority = Field(
        default_factory=HtmlAttributePriority,
        description="Attribute priority configuration"
    )

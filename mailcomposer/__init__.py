#!/usr/bin/env python

"""API for composing emails through an external application.

mailcomposer aims to provide a simple, cross-platform interface for
composing emails through an external application like Microsoft Outlook.
"""

from .dummy import DummyMailComposer

try:
    from .outlook import OutlookComposer
except (ImportError):
    OutlookComposer = None

from .exceptions import MailComposerError


# Set MailComposer to a reasonable default for your system
if OutlookComposer:
    MailComposer = OutlookComposer
else:
    MailComposer = DummyMailComposer


# BaseMailComposer is an internal class that doesn't need to be exported
__all__ = [
    # Default interface
    "MailComposer",

    # All available interfaces
    "DummyMailComposer",
    "OutlookComposer",

    # Exception class
    "MailComposerError",
]

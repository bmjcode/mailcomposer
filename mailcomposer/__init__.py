#!/usr/bin/env python

"""API for composing emails through an external application.

mailcomposer aims to provide a simple, cross-platform interface for
composing emails through an external application like Microsoft Outlook.

mailcomposer provides several classes to support a variety of email
applications. Available classes are:

  MailComposer
    The default class, recommended for most applications. This is a
    special name that's automatically assigned to the most capable of
    the below classes available on your system.

  OutlookComposer
    MAPI-based interface for Microsoft Outlook. Requires the pywin32
    package. This interface is only available on Microsoft Windows.

  DummyMailComposer
    A dummy class provided for testing, and as a fallback in case no
    other interfaces are available. This class does not actually call an
    email application, but will display the message contents on stdout.

mailcomposer also provides its own exception class, MailComposerError,
for problems that occur during processing. It can, and probably will,
also raise any of the standard Python exceptions if you attempt something
you really shouldn't.
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

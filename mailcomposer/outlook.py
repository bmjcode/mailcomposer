#!/usr/bin/env python

"""MAPI-based interface for Microsoft Outlook."""

import os
import sys

import win32com.client

from .base import BaseMailComposer
from .exceptions import MailComposerError


class OutlookComposer(BaseMailComposer):
    """MAPI-based interface for Microsoft Outlook."""

    def display(self):
        """Display the message in Microsoft Outlook."""

        # TODO: Implement this!
        pass

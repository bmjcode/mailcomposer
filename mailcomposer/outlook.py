#!/usr/bin/env python

"""MAPI-based interface for Microsoft Outlook (requires pywin32)."""

import os
import sys

import win32com.client

from .base import BaseMailComposer
from .exceptions import MailComposerError


class OutlookComposer(BaseMailComposer):
    """MAPI-based interface for Microsoft Outlook."""

    def display(self, blocking=True):
        """Display the message in Microsoft Outlook."""

        # Connect to Outlook and create a new message
        outlook = win32com.client.Dispatch("Outlook.Application")
        message = outlook.CreateItem(0)

        # Process the message headers
        if self._to:
            message.To = "; ".join(self._to)
        if self._cc:
            message.CC = "; ".join(self._cc)
        if self._bcc:
            message.BCC = "; ".join(self._bcc)
        if self._subject:
            message.Subject = self._subject

        # Format the message body
        if self._body_format == "html":
            message.HTMLBody = self._body
        else:
            message.Body = self._body

        # Process message attachments
        for path in self._attachments:
            # Outlook requires an absolute path
            message.Attachments.Add(Source=os.path.abspath(path))

        # Display the message
        message.Display(blocking)

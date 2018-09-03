#!/usr/bin/env python

"""Base class for MailComposer objects."""

import os
import sys
import textwrap

from .exceptions import MailComposerError


class BaseMailComposer(object):
    """Base class for MailComposer objects.

    Your subclass should implement the display() method to open the
    message in its corresponding external application.
    """

    __slots__ = ["_to", "_cc", "_bcc", "_subject",
                 "_body", "_body_format", "_attachments"]

    def __init__(self, **kw):
        """Return a new MailComposer object."""

        if "to" in kw:
            self._to = self._parse_recipients(kw["to"])
        else:
            self._to = []

        if "cc" in kw:
            self._cc = self._parse_recipients(kw["cc"])
        else:
            self._cc = []

        if "bcc" in kw:
            self._bcc = self._parse_recipients(kw["bcc"])
        else:
            self._bcc = []

        if "subject" in kw:
            self._subject = str(kw["subject"])
        else:
            self._subject = ""

        if "body" in kw:
            self._body = str(kw["body"])
        else:
            self._body = ""

        if "body_format" in kw:
            self._body_format = self._parse_body_format(kw["body_format"])
        else:
            self._body_format = "text"

        # Attachments are not accepted as a keyword argument
        self._attachments = []

    def __str__(self):
        """Return the message as a string.

        The format approximates RFC 2822.
        """

        headers = []
        lines = []

        # Process the message headers
        if self._to:
            headers.append("To: {0}".format(", ".join(self._to)))
        if self._cc:
            headers.append("CC: {0}".format(", ".join(self._cc)))
        if self._bcc:
            headers.append("BCC: {0}".format(", ".join(self._bcc)))
        if self._subject:
            headers.append("Subject: {0}".format(self._subject))

        # Format the message headers
        for header in headers:
            for line in textwrap.wrap(header, width=78,
                                      subsequent_indent=" "):
                lines.append(line)

        # Add a blank line separating the headers from the body text
        lines.append("")

        # Format the body text
        for body_line in self._body.splitlines():
            if body_line:
                for line in textwrap.wrap(body_line, width=78):
                    lines.append(line)
            else:
                # This is necessary to keep empty lines in the body text
                lines.append("")

        return "\n".join(lines)

    # ------------------------------------------------------------------------

    def attach_file(self, path):
        """Attach the specified file to this message."""

        if os.path.exists(path):
            self._attachments.append(path)

        else:
            message = "No such file or directory: '{0}'".format(path)
            raise MailComposerError(message)

    def display(self):
        """Display this message in your email application."""

        raise NotImplementedError

    # ------------------------------------------------------------------------

    def _parse_body_format(self, body_format):
        """Parse the "body_format" property."""

        if body_format in ("text", "html"):
            return body_format

        else:
            raise ValueError("body_format must be one of 'text' or 'html'")

    def _parse_recipients(self, recipients):
        """Parse the "to", "cc", or "bcc" property."""

        if isinstance(recipients, str):
            return [recipients]

        else:
            return list(recipients)

    # ------------------------------------------------------------------------

    @property
    def to(self):
        """List of recipients in the "To:" field."""
        return self._to

    @to.setter
    def to(self, value):
        self._to = self._parse_recipients(value)

    @to.deleter
    def to(self):
        del self._to
        self._to = []

    # ------------------------------------------------------------------------

    @property
    def cc(self):
        """List of recipients in the "CC:" field."""
        return self._cc

    @cc.setter
    def cc(self, value):
        self._cc = self._parse_recipients(value)

    @cc.deleter
    def cc(self):
        del self._cc
        self._cc = []

    # ------------------------------------------------------------------------

    @property
    def bcc(self):
        """List of recipients in the "BCC:" field."""
        return self._bcc

    @bcc.setter
    def bcc(self, value):
        self._bcc = self._parse_recipients(value)

    @bcc.deleter
    def bcc(self):
        del self._bcc
        self._to = []

    # ------------------------------------------------------------------------

    @property
    def subject(self):
        """The subject line of the email."""
        return self._subject

    @subject.setter
    def subject(self, value):
        self._subject = str(value)

    @subject.deleter
    def subject(self):
        del self._subject
        self._subject = ""

    # ------------------------------------------------------------------------

    @property
    def body(self):
        """The body of the email."""
        return self._body

    @body.setter
    def body(self, value):
        self._body = str(value)

    @body.deleter
    def body(self):
        del self._body
        self._body = ""

    # ------------------------------------------------------------------------

    @property
    def body_format(self):
        """The body format of the email.

        Recognized values:

          "text"
            Use plain-text formatting (the default).

          "html"
            Use HTML formatting. The level of support depends on your
            email application's capabilities.
        """
        return self._body_format

    @body_format.setter
    def body_format(self, value):
        self._body_format = self._parse_body_format(value)

    # ------------------------------------------------------------------------

    @property
    def attachments(self):
        """List of files to attach to this email."""
        return self._attachments

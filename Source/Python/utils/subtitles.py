__author__    = 'Gilles Boccon-Gibod (bok@bok.net)'
__copyright__ = 'Copyright 2011-2020 Axiomatic Systems, LLC.'

import xml.etree.ElementTree as ET
import os.path as path
from mp4utils import LanguageCodeMap, LanguageNames, BooleanFromString

TTML_XML_NAMESPACE = 'http://www.w3.org/ns/ttml'
XML_NAMESPACE      = 'http://www.w3.org/XML/1998/namespace'

class SubtitlesFile:
    def __init__(self, options, media_source):
        self.media_source    = media_source
        self.format          = None

        filename = media_source.filename
        self.media_name = path.basename(filename)
        if options.debug:
            print('Processing Subtitles file', filename)

        self.size = path.getsize(filename)

        self.language = media_source.spec.get('+language')
        self.language_name = 'Unknown'
        if not self.language:
            self.language = 'unknown'

        if len(self.language) == 3:
            # convert to 2 char code
            self.language = LanguageCodeMap.get(self.language, self.language)
        language_name = LanguageNames.get(self.language, self.language_name)
        self.language_name = media_source.spec.get('+language_name', language_name)

        self.representation_id = media_source.spec.get('+representation_id', self.language)

        if media_source.format == 'ttml':
            self.parse_ttml(options)
        elif media_source.format == 'webvtt':
            self.parse_webvtt(options)

        if '+media' in media_source.spec:
            self.media_name = media_source.spec['+media']

        # HLS options
        self.hls_default = media_source.spec.get('+hls_default', None)  # None means: unspecified
        if self.hls_default is not None:
            self.hls_default = BooleanFromString(self.hls_default)
        self.hls_autoselect = BooleanFromString(media_source.spec.get('+hls_autoselect', 'YES'))
        self.hls_group = media_source.spec.get('+hls_group')
        self.hls_group_match = media_source.spec.get('+hls_group_match', '*').split('&')

    def parse_ttml(self, options):
        self.format    = 'ttml'
        self.mime_type = 'application/ttml+xml'

        xml_tree= ET.parse(self.media_source.filename)
        xml_root = xml_tree.getroot()

        if xml_root.tag != '{'+TTML_XML_NAMESPACE+'}tt':
            if options.debug:
                print('ERROR: no root level <tt> element found')

        # get the language
        language = xml_root.get('{'+XML_NAMESPACE+'}lang')
        if language:
            self.language = language

        if options.rename_media:
            self.media_name = 'subtitles-'+self.language+'.xml'

    def parse_webvtt(self, options):
        self.format    = 'webvtt'
        self.mime_type = 'text/vtt'

#############################################
# Module Exports
#############################################
__all__ = ['SubtitlesFile']

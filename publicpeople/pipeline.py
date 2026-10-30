import codecs
import os

import sass
from django.conf import settings
from pipeline.compilers import SubProcessCompiler
from pipeline.storage import PipelineMixin
from whitenoise.storage import CompressedManifestStaticFilesStorage


class GzipManifestPipelineStorage(PipelineMixin, CompressedManifestStaticFilesStorage):
    pass


class SassCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.scss')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not outdated and not force:
            return

        result = sass.compile(
            filename=infile,
            include_paths=settings.SASS_INCLUDE_PATHS,
        )

        output_dir = os.path.dirname(outfile)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with codecs.open(outfile, 'w', encoding='utf-8') as f:
            f.write(result)

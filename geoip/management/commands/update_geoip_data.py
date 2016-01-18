import os
import gzip
import urllib
import urlparse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


download_folder = settings.GEOIP_PATH


class Command(BaseCommand):
    help = 'Updates GeoIP data in {}'.format(download_folder)
    base_url = 'http://www.maxmind.com/download/geoip/database/'
    files = ['GeoLiteCity.dat.gz', 'GeoLiteCountry/GeoIP.dat.gz']

    def handle(self, *args, **options):
        for path in self.files:
            root, filepath = os.path.split(path)
            dowloadpath = os.path.join(download_folder, filepath)
            downloadurl = urlparse.urljoin(self.base_url, path)
            self.stdout.write('Downloading {} to {}\n'.format(downloadurl, dowloadpath))
            urllib.urlretrieve(downloadurl, dowloadpath)
            outfilepath, ext = os.path.splitext(dowloadpath)
            if ext != '.gz':
                raise CommandError('Something went wrong while decompressing {}'.format(dowloadpath))
            self.stdout.write('Extracting {} to {}\n'.format(dowloadpath, outfilepath))
            with gzip.open(dowloadpath, 'rb') as infile, open(outfilepath, 'wb') as outfile:
                outfile.writelines(infile)
            self.stdout.write('Deleting {}\n'.format(dowloadpath))
            os.remove(dowloadpath)
            self.stdout.write('Done with {}'.format(path))
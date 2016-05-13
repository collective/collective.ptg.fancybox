from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery.browser.views.display import \
    BatchingDisplayType
from collective.plonetruegallery.browser.views.display import BaseDisplayType
from collective.plonetruegallery.browser.views.display import jsbool
from collective.plonetruegallery.interfaces import IBaseSettings
from collective.plonetruegallery.utils import createSettingsFactory


_ = MessageFactory('collective.ptg.fancybox')

class IFancyBoxDisplaySettings(IBaseSettings):
    beta = schema.Bool(
        title=_(u"label_beta",
            default=u"Use version 3 beta instead of version 2 stable"),
        default=False)


class FancyBoxDisplayType(BatchingDisplayType):
    name = u"fancybox"
    schema = IFancyBoxDisplaySettings
    description = _(u"label_fancybox_display_type",
        default=u"Fancy Box")
    typeStaticFilesRelative = '++resource++ptg.fancybox'

    def fancybox_url(self):
        if self.settings.beta:
            return '++resource++ptg.fancybox/jquery.fancyboxb'
        return  '++resource++ptg.fancybox/jquery.fancybox'

    def javascript(self):
        return u"""
<script type="text/javascript"
    src="%(base_url)s/jquery.easing.js"></script>
<script type="text/javascript"
    src="%(base_url)s/jquery.mousewheel.js"></script>
 <script type="text/javascript" src="%(fancybox_url)s.js"></script>
  <script type="text/javascript">
    var auto_start = %(start_automatically)s;
    var start_image_index = %(start_index_index)i;
    (function($){
        $(document).ready(function() {
            $("a.fancyzoom-gallery").fancybox({
                'type': 'image',
                'transitionIn': 'elastic',
                'transitionOut': 'elastic'});
            var images = $('a.fancyzoom-gallery');
            if(images.length <= start_image_index){
                start_image_index = 0;
            }
            if(auto_start){
                $(images[start_image_index]).trigger('click');
            }
        });
    })(jQuery);
    </script>
    """ % {
            'start_automatically': jsbool(
                self.settings.start_automatically or self.settings.timed),
            'start_index_index': self.start_image_index,
            'staticFiles':  self.staticFiles,
            'base_url': self.typeStaticFiles,
            'fancybox_url' : self.fancybox_url(),
        }

    def css(self):
        return u"""
<link rel="stylesheet" type="text/css"
    href="%(fancybox_url)s.css" media="screen" />
    <style>
    #content  a.fancyzoom-gallery {
        border-bottom: 0 none;
    }
    </style>
""" % {
        'staticFiles': self.staticFiles,
        'fancybox_url' : self.fancybox_url(),
        }
FancyBoxSettings = createSettingsFactory(FancyBoxDisplayType.schema)
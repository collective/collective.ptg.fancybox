from zope.i18nmessageid import MessageFactory
from collective.plonetruegallery.utils import createSettingsFactory
from collective.plonetruegallery.browser.views.display import \
    BatchingDisplayType
from collective.plonetruegallery.browser.views.display import jsbool
from collective.plonetruegallery.interfaces import IBaseSettings

_ = MessageFactory('collective.ptg.fancybox')

class IFancyBoxDisplaySettings(IBaseSettings):
    pass


class FancyBoxDisplayType(BatchingDisplayType):

    name = u"fancybox"
    schema = IFancyBoxDisplaySettings
    description = _(u"label_fancybox_display_type",
        default=u"Fancy Box")
    typeStaticFilesRelative = '++resource++ptg.fancybox'

    def javascript(self):
        return u"""
<script type="text/javascript"
    src="%(base_url)s/jquery.easing.js"></script>
<script type="text/javascript"
    src="%(base_url)s/jquery.mousewheel.js"></script>
<script type="text/javascript"
    src="%(base_url)s/jquery.fancybox.js"></script>
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
            'base_url': self.typeStaticFiles
        }

    def css(self):
        return u"""
<link rel="stylesheet" type="text/css"
    href="%(staticFiles)s/jquery.fancybox.css" media="screen" />
    <style>
    #content  a.fancyzoom-gallery {
        border-bottom: 0 none;
    }
    </style>

""" % {'staticFiles': self.typeStaticFiles}
FancyBoxSettings = createSettingsFactory(FancyBoxDisplayType.schema)
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
    src="%(base_url)s/jquery.mousewheel-3.0.6.pack.js"></script>
<script type="text/javascript"
    src="%(base_url)s/jquery.fancybox.pack.js"></script>
<script type="text/javascript"
    src="%(base_url)s/helpers/jquery.fancybox-buttons.js"></script>
<script type="text/javascript"
    src="%(base_url)s/helpers/jquery.fancybox-media.js"></script>
<script type="text/javascript"
    src="%(base_url)s/helpers/jquery.fancybox-thumbs.js"></script>


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
    href="%(staticFiles)s/jquery.fancybox.css" />
<link rel="stylesheet" type="text/css"
    href="%(staticFiles)s/helpers/jquery.fancybox-buttons.css" />
<link rel="stylesheet" type="text/css"
    href="%(staticFiles)s/helpers/jquery.fancybox-thumbs.css" />

    <style>
    #content  a.fancyzoom-gallery {
        border-bottom: 0 none;
    }
    </style>

""" % {'staticFiles': self.typeStaticFiles}
FancyBoxSettings = createSettingsFactory(FancyBoxDisplayType.schema)

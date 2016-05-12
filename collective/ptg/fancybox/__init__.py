from zope.i18nmessageid import MessageFactory
from collective.plonetruegallery.utils import createSettingsFactory
from collective.plonetruegallery.browser.views.display import \
    BatchingDisplayType
from collective.plonetruegallery.browser.views.display import jsbool
from collective.plonetruegallery.interfaces import IBaseSettings

_ = MessageFactory('collective.ptg.fancybox')

class IFancyBoxDisplaySettings(IBaseSettings):
    beta = schema.Bool(
        title=_(u"label_beta",
            default=u"Use version 3 beta instead of version 2 stable"),
        default=False)
    caption = schema.Choice(
        title = _(u"label_caption"),
            default=u"Where to show caption"),
            vocabulary=SimpleVocabulary([
            SimpleTerm("float", "float",
                _(u"float", default=u"float")),
            SimpleTerm("outside", "outside",
                _(u"outside", default=u"outside")),
            SimpleTerm("inside", "inside",
                _(u"inside", default=u"inside")),
            SimpleTerm("outside", "outside",
                _(u"outside", default=u"outside")),
            SimpleTerm("over", "over",
                _(u"over", default=u"over"))
        ])

class FancyBoxDisplayType(BatchingDisplayType):

    name = u"fancybox"
    schema = IFancyBoxDisplaySettings
    description = _(u"label_fancybox_display_type",
        default=u"Fancy Box")
    typeStaticFilesRelative = '++resource++ptg.fancybox'
    fancybox_url = %(base_url) + '/jquery.fancybox'
    if self.beta:
        fancybox_url = %(staticFiles) + '/jquery.fancybox3'

    def javascript(self):
        return u"""
<script type="text/javascript"
    src="%(base_url)s/jquery.easing.js"></script>
<script type="text/javascript"
    src="%(base_url)s/jquery.mousewheel.js"></script>
 <script type="text/javascript" src="%(facebook_url)s.js"></script>
  <script type="text/javascript">
    var auto_start = %(start_automatically)s;
    var start_image_index = %(start_index_index)i;
    (function($){
        $(document).ready(function() {
            $("a.fancyzoom-gallery").fancybox({
                'type': 'image',
                'transitionIn': 'elastic',
                'caption': %(caption)s,
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
            'staticFiles': self.typeStaticFiles,
            'caption' : self.caption,
            'beta' : self.beta,
        }

    def css(self):
        return u"""
<link rel="stylesheet" type="text/css"
    href="%(facebook_url)s.css"> media="screen" />
    <style>
    #content  a.fancyzoom-gallery {
        border-bottom: 0 none;
    }
    </style>

""" % {'staticFiles': self.typeStaticFiles}
FancyBoxSettings = createSettingsFactory(FancyBoxDisplayType.schema)
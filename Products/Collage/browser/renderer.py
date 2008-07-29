from AccessControl import getSecurityManager, Unauthorized

from zope.interface import Interface
from zope.interface import directlyProvidedBy, directlyProvides
from zope.component import getMultiAdapter

from Products.Five.browser import BrowserView

from Products.Collage.interfaces import ICollageBrowserLayer, IDynamicViewManager
from Products.Collage.interfaces import ICollageAlias

try:
    from Products.LinguaPlone.interfaces import ITranslatable
except ImportError:
    HAS_LINGUAPLONE = False
else:
    HAS_LINGUAPLONE = True

class SimpleContainerRenderer(BrowserView):
    def getItems(self, contents=None):
        # needed to circumvent bug :-(
        self.request.debug = False

        # transmute request interfaces
        ifaces = directlyProvidedBy(self.request)
        directlyProvides(self.request, ICollageBrowserLayer)

        views = []

        if not contents:
            contents = self.context.folderlistingFolderContents()

        for context in contents:
            target = context
            manager = IDynamicViewManager(context)
            layout = manager.getLayout()

            if not layout:
                layout, title = manager.getDefaultLayout()

            if ICollageAlias.providedBy(context):
                target = context.get_target()

                # if not set, revert to context
                if target is None:
                    target = context

                # verify that target is accessible
                try:
                    getSecurityManager().validate(self, self, target.getId(), target)
                except Unauthorized:
                    continue

            # Filter out translation duplicates:
            # If a non-alias object is translatable, check if its language
            # is set to the currently selected language or to neutral,
            # or if it is the canonical version
            elif HAS_LINGUAPLONE and ITranslatable.providedBy(target):
                language = self.request.get('LANGUAGE','')
                if target.Language() not in (language, ''):
                    # Discard the object, if it is not the canonical version
                    # or a translation is available in the requested language.
                    if not target.isCanonical() or target.getTranslation(language) in contents:
                        continue

            # assume that a layout is always available
            view = getMultiAdapter((target, self.request), name=layout)

            # store reference to alias if applicable
            if ICollageAlias.providedBy(context):
                view.__alias__ = context

            views.append(view)

        # restore interfaces
        directlyProvides(self.request, ifaces)

        return views


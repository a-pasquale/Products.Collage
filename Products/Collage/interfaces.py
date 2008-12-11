# -*- coding: utf-8 -*-
# $Id$

from zope import interface
from zope.viewlet.interfaces import IViewletManager

from Products.Collage.browser.controlpanel import ICollageSiteOptions

class ICollage(interface.Interface):
    pass

class ICollageRow(interface.Interface):
    pass

class ICollageColumn(interface.Interface):
    pass

class ICollageAlias(interface.Interface):
    pass

class IDynamicViewManager(interface.Interface):
    pass

class ICollageBrowserLayer(interface.Interface):
    """Collage browser layer. Views registered with this layer
    are available to objects inside a collage."""
    pass
    
class ICollageBrowserLayerType(interface.interfaces.IInterface):
    """Marker interface for Collage theme-specific layers
    """
    pass

class ICollageEditLayer(interface.Interface):
    """Collage edit layer."""
    pass

class IContentMenu(IViewletManager):
    """Interface for the content-menu viewlet manager."""
    pass

class IPortletSkin(interface.Interface):
    """Interface for skinable portlets views."""
    pass

